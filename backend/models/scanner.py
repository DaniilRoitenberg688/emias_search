from enum import Enum

from pydantic import BaseModel


class ScannerType(str, Enum):
    twain = 'twain'
    wia = 'wia'


class Scanner(BaseModel):
    name: str
    scanner_type: ScannerType
