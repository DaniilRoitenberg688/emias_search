import base64
import os
from enum import Enum
from subprocess import run
import platform

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from requests import post


class ScannerType(str, Enum):
    twain = 'twain'
    wia = 'wia'
    sane = 'sane'


class Scanner(BaseModel):
    name: str
    scanner_type: ScannerType


load_dotenv()

base_command = os.environ.get('COMMAND', 'C:/Program Files/NAPS2/NAPS2.Console.exe')
url = os.environ.get('URL', 'http://localhost:5252')

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
    scanners = []
    os_name = platform.system()
    if os_name == 'Linux':
        sane_command = [base_command, 'console', '--listdevices', '--driver', 'sane']
        sane_command_result = run(sane_command, capture_output=True)
        for scanner in sane_command_result.stdout.decode().split('\n'):
            if scanner:
                scanners.append(Scanner(name=scanner, scanner_type=ScannerType.sane))

    else:
        wia_command = [base_command, '--listdevices', '--driver', 'wia']
        twain_command = [base_command, '--listdevices', '--driver', 'twain']


        wia_command_result = run(wia_command, capture_output=True)
        twain_command_result = run(twain_command, capture_output=True)

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
    if scanner.scanner_type == ScannerType.sane:
        command = [base_command, 'console', '-o', f'{mdoc_id}.pdf', '--noprofile', '--driver', scanner.scanner_type, '--device',
                   scanner.name]


    command_result = run(command, capture_output=True)
    code = command_result.returncode
    if code == 0:

        with open(f'{mdoc_id}.pdf', 'rb') as file:
            data = file.read()

        send_data = {
            'mdoc_id': mdoc_id,
            'data': base64.b64encode(data).decode('utf-8')
        }
        os.remove(f'{mdoc_id}.pdf')

        request = post(f'{url}/api/scan', headers={"Content-Type": "application/json"}, json=send_data)
        if request.status_code == 200:
            return {'result': 'ok'}
        else:
            raise HTTPException(status_code=400, detail=f'cannot send data on server. Status code: {request.status_code}')
    else:
        raise HTTPException(400, {'result': 'something went wrong', 'reason': command_result.stdout.decode()})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=3000)
