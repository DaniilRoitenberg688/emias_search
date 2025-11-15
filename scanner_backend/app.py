import base64
import os
import shutil
from enum import Enum

import img2pdf
import win32com.client
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfWriter
from requests import post


class ScannerType(str, Enum):
    twain = "twain"
    wia = "wia"
    sane = "sane"


class Scanner(BaseModel):
    name: str
    scanner_type: ScannerType
    index: int


async def list_scanners(device_manager):
    scanners = []
    for i in range(1, device_manager.DeviceInfos.Count + 1):
        info = device_manager.DeviceInfos(i)
        if info.Type == 1:
            scanners.append(info.Properties("Name").Value)
    return scanners


async def scan_image(device_manager, index, path):
    dev = device_manager.DeviceInfos(index).Connect()
    item = dev.Items(1)
    image = item.Transfer()
    image.SaveFile("template.jpg")
    with open(path, "wb") as f:
        pdf = img2pdf.convert("template.jpg")
        f.write(pdf)
    os.remove("template.jpg")


load_dotenv()

base_command = os.environ.get("COMMAND", "C:/Program Files/NAPS2/NAPS2.Console.exe")
url = os.environ.get("FRONT_URL", "http://scan-doc-ppak.vmeda.local")
base_path = os.environ.get("BASE_PATH", "docs")

app = FastAPI()
device_manager = win32com.client.Dispatch("WIA.DeviceManager")

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
    # scanners = []
    # os_name = platform.system()
    # if os_name == "Linux":
    #     sane_command = [base_command, "console", "--listdevices", "--driver", "sane"]
    #     process = await create_subprocess_exec(*sane_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    #     stdout, _ = await process.communicate()
    #     for scanner in stdout.decode().split("\n"):
    #         if scanner:
    #             scanners.append(Scanner(name=scanner, scanner_type=ScannerType.sane))

    # else:
    #     wia_command = [base_command, "--listdevices", "--driver", "wia"]
    #     twain_command = [base_command, "--listdevices", "--driver", "twain"]

    #     process = await create_subprocess_exec(*wia_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    #     wia_stdout, _ = await process.communicate()

    #     process = await create_subprocess_exec(*twain_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    #     twain_stdout, _ = await process.communicate()

    #     for scanner in twain_stdout.decode().split("\r\n"):
    #         if scanner:
    #             scanners.append(Scanner(name=scanner, scanner_type=ScannerType.twain))

    #     for scanner in wia_stdout.decode().split("\r\n"):
    #         if scanner:
    #             scanners.append(Scanner(name=scanner, scanner_type=ScannerType.wia))
    try:
        scanners = await list_scanners(device_manager)
        scanners_schemas = []
        for i in range(len(scanners)):
            scanners_schemas.append(
                Scanner(name=scanners[i], scanner_type=ScannerType.wia, index=i + 1)
            )
        return scanners_schemas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan", tags=["Scanner"])
async def make_scan(scanner: Scanner, mdoc_id: str, group_doc_id: int):
    # docs_path = f"{base_path}/{mdoc_id}_{str(group_doc_id)}",
    # command = [
    #     base_command,
    #     "-o",
    #     f"{docs_path}/{len(os.listdir(str(docs_path))) + 1}.pdf"
    #     "--noprofile",
    #     "--driver",
    #     scanner.scanner_type,
    #     "--device",
    #     scanner.name,
    # ]
    # if scanner.scanner_type == ScannerType.sane:
    #     command = [
    #         base_command,
    #         "console",
    #         "-o",
    #         f"{docs_path}/{len(os.listdir(str(docs_path))) + 1}.pdf"
    #         "--noprofile",
    #         "--driver",
    #         scanner.scanner_type,
    #         "--device",
    #         scanner.name,
    #     ]
    # command_result = subprocess.run(command, capture_output=True)
    # code = command_result.returncode
    # if code == 0:
    #     return {"status": "ok"}
    # else:
    #     raise HTTPException(
    #         400,
    #         {
    #             "result": "something went wrong",
    #             "reason": command_result.stdout.decode(),
    #         },
    #     )

    docs_path = f"{base_path}/{mdoc_id}_{str(group_doc_id)}"
    try:
        await scan_image(
            device_manager,
            scanner.index,
            f"{docs_path}/{len(os.listdir(str(docs_path))) + 1}.pdf",
        )
        return {"status": "ok"}
    except Exception as e:
        os.remove("template.jpg")
        raise HTTPException(
            400,
            {
                "result": "something went wrong",
                "reason": str(e),
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
    if os.listdir(f"{base_path}/{mdoc_id}_{group_doc_id}") == []:
        os.rmdir(f"{base_path}/{mdoc_id}_{group_doc_id}")


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
