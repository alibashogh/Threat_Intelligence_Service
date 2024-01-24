import datetime
from sqlalchemy import Column, Integer, String, DateTime
from settings.database import Base


class SuspiciousIp(Base):
    __tablename__ = 'suspicious_ip'
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True, unique=True)
    report_count = Column(Integer, default=1)
    last_report_time = Column(DateTime, default=datetime.datetime.now())
