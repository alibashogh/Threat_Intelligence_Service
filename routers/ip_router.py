from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPAuthorizationCredentials
from models.models import SuspiciousIp
import schemas.ip as ip_schema
from routers import security
from settings.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


async def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "admin"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return credentials.username


@router.post('/report-ip/', response_model=ip_schema.ResReportIp)
async def report_ip(report_ip: ip_schema.ReqReportIp,
                    db: Session = Depends(get_db),
                    current_username: str = Depends(authenticate_user)):
    try:
        suspicious_ip = db.query(SuspiciousIp).filter(SuspiciousIp.ip_address == report_ip.ip_address).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="server error: database")
    if suspicious_ip:
        suspicious_ip.report_count += 1
        suspicious_ip.last_report_time = datetime.now()
        db.commit()
        db.refresh(suspicious_ip)
    else:
        suspicious_ip = SuspiciousIp(
            ip_address=report_ip.ip_address
        )
        db.add(suspicious_ip)
        db.commit()
        db.refresh(suspicious_ip)
    return suspicious_ip


@router.get('/query-ip/', response_model=ip_schema.ResQueryIp)
async def query_ip(ip_address: str | None = Query(None, pattern=ip_schema.regex),
                   db: Session = Depends(get_db),
                   current_username: str = Depends(authenticate_user)):
    try:
        suspicious_ip = db.query(SuspiciousIp).filter(SuspiciousIp.ip_address == ip_address).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="server error: database")
    if not suspicious_ip:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ip does not exist")
    return suspicious_ip
