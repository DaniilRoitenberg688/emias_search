import base64
import os
import uuid

import paramiko
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from db.engine import get_session_pdf
from db.models import PdfMdoc
from models import Scanner, ScannerType

scan_router = APIRouter(prefix='/scan')


@scan_router.get('')
async def get_scanners(host: str):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=config.SSH_USER, password=config.SSH_PASSWORD)
        stdin, stdout, stderr = client.exec_command(
            ' '.join([f'"{config.BASE_COMMAND}"', '--listdevices', '--driver', 'twain']))
        scanners = stdout.read().decode().split('\r\n')
        print(scanners)
        client.close()
        return [Scanner(name=i, scanner_type=ScannerType.twain) for i in scanners if i]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='something went wrong')


@scan_router.post('')
async def create_scan(host: str, mdoc_id: str, scanner: Scanner,
                      session_pdf: AsyncSession = Depends(get_session_pdf)):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=config.SSH_USER, password=config.SSH_PASSWORD)

        stdin, stdout, stderr = client.exec_command(
            ' '.join([f'"{config.BASE_COMMAND}"', '-o', f'{mdoc_id}.pdf', '--noprofile', '--driver',
                      scanner.scanner_type, '--device',
                      scanner.name]))
        print(stdout.read())
        tr = paramiko.Transport((host, 22))
        tr.connect(username=config.SSH_USER, password=config.SSH_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(tr)

        sftp.get(f'{mdoc_id}.pdf', f'{mdoc_id}.pdf')

        with open(f'{mdoc_id}.pdf', 'rb') as file:
            data = file.read()

        new_doc = PdfMdoc(mdoc_id=mdoc_id, pdf_data=base64.b64encode(data))
        session_pdf.add(new_doc)
        await session_pdf.commit()

        os.remove(f'{mdoc_id}.pdf')
        stdin, stdout, stderr = client.exec_command(f'del {mdoc_id}.pdf')

        client.close()

        return {'status': 'ok'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={'reason': e})
