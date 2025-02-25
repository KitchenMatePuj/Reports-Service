from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.main.python.models.Report import Report

class ReportResponse(BaseModel):
    report_id: int
    reporter_user_id: str
    resource_type: str
    resource_id: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

class ReportTransformer:
    @staticmethod
    def to_response_model(report: Report) -> ReportResponse:
        return ReportResponse(
            report_id=report.report_id,
            reporter_user_id=report.reporter_user_id,
            resource_type=report.resource_type,
            resource_id=report.resource_id,
            description=report.description,
            status=report.status,
            created_at=report.created_at,
            updated_at=report.updated_at
        )
