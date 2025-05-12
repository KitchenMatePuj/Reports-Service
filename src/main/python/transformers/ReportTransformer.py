from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.main.python.models.Report import Report

class ReportCreate(BaseModel):
    reporter_user_id: str
    resource_type: str
    description: Optional[str] = None
    status: Optional[str] = "pending"

class ReportUpdate(BaseModel):
    reporter_user_id: Optional[str] = None
    resource_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ReportResponse(BaseModel):
    report_id: int
    reporter_user_id: Optional[str] = None
    resource_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ReportSearch(BaseModel):
    resource_type: Optional[str] = None
    status: Optional[str] = None
    date: Optional[str] = None

class ReportTransformer:
    @staticmethod
    def to_response_model(report: Report) -> ReportResponse:
        return ReportResponse(
            report_id=report.report_id,
            reporter_user_id=report.reporter_user_id,
            resource_type=report.resource_type,
            description=report.description,
            status=report.status,
            created_at=report.created_at,
            updated_at=report.updated_at
        )
