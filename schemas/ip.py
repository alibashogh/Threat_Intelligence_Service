from datetime import datetime

from pydantic import BaseModel
from fastapi import Path


regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


class ReqReportIp(BaseModel):
    ip_address: str = Path(regex=regex)


class ResReportIp(BaseModel):
    id: int

    class Config:
        from_attributes = True


class ResQueryIp(BaseModel):
    id: int
    ip_address: str
    report_count: int
    last_report_time: datetime

    class Config:
        from_attributes = True
