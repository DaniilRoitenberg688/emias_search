import asyncio
import base64
from logging import raiseExceptions
import os
from enum import Enum
from asyncio.subprocess import create_subprocess_exec
import platform
import subprocess
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, Request, APIRouter
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from requests import post
from pypdf import PdfWriter


class ScannerType(str, Enum):
    twain = "twain"
    wia = "wia"
    sane = "sane"


class Scanner(BaseModel):
    name: str
    scanner_type: ScannerType


load_dotenv()

base_command = os.environ.get("COMMAND", "C:/Program Files/NAPS2/NAPS2.Console.exe")
url = os.environ.get("FRONT_URL", "http://scan-doc-ppak.vmeda.local")
base_path = os.environ.get("BASE_PATH", "docs")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if not os.path.isdir(base_path):
        os.mkdir(base_path)
    response = await call_next(request)
    return response


@app.get("/ping", tags=["Ping"])
async def ping():
    return {"result": "pong"}


@app.get("/scanners", tags=["Scanner"])
async def get_scanners() -> list[Scanner]:
    scanners = []
    os_name = platform.system()
    if os_name == "Linux":
        sane_command = [base_command, "console", "--listdevices", "--driver", "sane"]
        process = await create_subprocess_exec(*sane_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, _ = await process.communicate()
        for scanner in stdout.decode().split("\n"):
            if scanner:
                scanners.append(Scanner(name=scanner, scanner_type=ScannerType.sane))

    else:
        wia_command = [base_command, "--listdevices", "--driver", "wia"]
        twain_command = [base_command, "--listdevices", "--driver", "twain"]

        process = await create_subprocess_exec(*wia_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        wia_stdout, _ = await process.communicate()

        process = await create_subprocess_exec(*twain_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        twain_stdout, _ = await process.communicate()

        for scanner in twain_stdout.decode().split("\r\n"):
            if scanner:
                scanners.append(Scanner(name=scanner, scanner_type=ScannerType.twain))

        for scanner in wia_stdout.decode().split("\r\n"):
            if scanner:
                scanners.append(Scanner(name=scanner, scanner_type=ScannerType.wia))
    print(scanners)
    return scanners


@app.post("/scan", tags=["Scanner"])
async def make_scan(scanner: Scanner, mdoc_id: str, group_doc_id: int):
    docs_path = f"{base_path}/{mdoc_id}_{str(group_doc_id)}",
    command = [
        base_command,
        "-o",
        f"{docs_path}/{len(os.listdir(str(docs_path))) + 1}.pdf"
        "--noprofile",
        "--driver",
        scanner.scanner_type,
        "--device",
        scanner.name,
    ]
    if scanner.scanner_type == ScannerType.sane:
        command = [
            base_command,
            "console",
            "-o",
            f"{docs_path}/{len(os.listdir(str(docs_path))) + 1}.pdf"
            "--noprofile",
            "--driver",
            scanner.scanner_type,
            "--device",
            scanner.name,
        ]
    command_result = subprocess.run(command, capture_output=True)
    code = command_result.returncode
    if code == 0:
        return {"status": "ok"}
    else:
        raise HTTPException(
            400,
            {
                "result": "something went wrong",
                "reason": command_result.stdout.decode(),
            },
        )


docs_router = APIRouter(prefix="/documents", tags=["Documents"])


@docs_router.get("", status_code=200)
async def get_docs(mdoc_id: str, group_doc_id: int) -> list[str]:
    user_dir = f"{mdoc_id}_{str(group_doc_id)}"
    all_docs = os.listdir(base_path)
    if user_dir not in all_docs:
        raise HTTPException(
            404, "cannot find any docs, associated with this user and document group"
        )
    return os.listdir(f"{base_path}/{user_dir}")


@docs_router.delete("", status_code=204)
async def delete_doc(mdoc_id: str, group_doc_id: int, filename: str):
    user_doc = f"{base_path}/{mdoc_id}_{str(group_doc_id)}/{filename}"
    if not os.path.isfile(user_doc):
        raise HTTPException(
            404, "cannot find any docs, associated with this user and document group"
        )
    os.remove(user_doc)


@docs_router.post("/send", status_code=200)
async def send_docs(mdoc_id: str, group_doc_id: int):
    if not os.path.isdir(f"{base_path}/{mdoc_id}_{group_doc_id}"):
        raise HTTPException(404, "cannot find any docs for this patient")
    if not os.listdir(f"{base_path}/{mdoc_id}_{group_doc_id}"):
        raise HTTPException(400, "No files")
    writer = PdfWriter()         
    for f in os.listdir(f"{base_path}/{mdoc_id}_{group_doc_id}"):
        writer.append(f"{base_path}/{mdoc_id}_{group_doc_id}/{f}")
    with open(f"{base_path}/{mdoc_id}_{group_doc_id}/result.pdf", "wb") as file:
        writer.write(file)
    writer.close()

    with open(f"{base_path}/{mdoc_id}_{group_doc_id}/result.pdf", "rb") as file:
        data = file.read()

        send_data = {
            "mdoc_id": mdoc_id,
            "data": base64.b64encode(data).decode("utf-8"),
            "group_doc_id": group_doc_id,
        }
        shutil.rmtree(f"{base_path}/{mdoc_id}_{group_doc_id}")

        request = post(
            f"{url}/api/scan",
            headers={"Content-Type": "application/json"},
            json=send_data,
        )
        if request.status_code == 200:
            return {"result": "ok"}
        else:
            raise HTTPException(
                status_code=400,
                detail=f"cannot send data on server. Status code: {request.status_code}",
            )


app.include_router(docs_router)


if __name__ == "__main__":
    import uvicorn

    os.mkdir(base_path)
    uvicorn.run(app, port=3000)
