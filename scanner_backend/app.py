import base64
import os
from enum import Enum
from subprocess import run

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from requests import post


class ScannerType(str, Enum):
    twain = 'twain'
    wia = 'wia'


class Scanner(BaseModel):
    name: str
    scanner_type: ScannerType


load_dotenv()

base_command = os.environ.get('COMMAND', 'C:/Program Files/NAPS2/NAPS2.Console.exe')
url = os.environ.get('URL', 'http://localhost:8000/api/scan')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/ping')
async def ping():
    return {'result': 'pong'}


@app.get('/scanners')
async def get_scanners() -> list[Scanner]:
    wia_command = [base_command, '--listdevices', '--driver', 'wia']
    twain_command = [base_command, '--listdevices', '--driver', 'twain']

    wia_command_result = run(wia_command, capture_output=True)
    twain_command_result = run(twain_command, capture_output=True)

    scanners = []

    for scanner in twain_command_result.stdout.decode().split('\r\n'):
        if scanner:
            scanners.append(Scanner(name=scanner, scanner_type=ScannerType.twain))

    for scanner in wia_command_result.stdout.decode().split('\r\n'):
        if scanner:
            scanners.append(Scanner(name=scanner, scanner_type=ScannerType.wia))

    return scanners


@app.post('/scan')
async def make_scan(scanner: Scanner, mdoc_id: str):
    command = [base_command, '-o', f'{mdoc_id}.pdf', '--noprofile', '--driver', scanner.scanner_type, '--device',
               scanner.name]

    command_result = run(command, capture_output=True)
    code = command_result.returncode
    if code == 0:

        with open(f'{mdoc_id}.pdf', 'rb') as file:
            data = file.read()

        send_data = {
            'mdoc_id': mdoc_id,
            'data': base64.b64encode(data).decode("utf-8")
        }
        os.remove(f'{mdoc_id}.pdf')

        request = post(url, headers={"Content-Type": "application/json"}, json=send_data)
        print(request.status_code)
        if request.status_code == 200:
            return {'result': 'ok'}
        else:
            raise HTTPException(status_code=400, detail=request.json())
    else:
        raise HTTPException(400, {'result': 'something went wrong', 'reason': command_result.stdout.decode()})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=3000)
