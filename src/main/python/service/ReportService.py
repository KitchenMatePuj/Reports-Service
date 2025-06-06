from typing import List
import traceback
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.main.python.models.Report import Report
from src.main.python.repository.ReportRepository import (
    create_report,
    get_report_by_id,
    list_all_reports,
    update_report,
    delete_report
)
from src.main.python.transformers.ReportTransformer import (
    ReportSearch,
    ReportTransformer,
    ReportResponse,
    ReportCreate
)

def create_new_report(db: Session, report_data: ReportCreate) -> ReportResponse:
    try:
        report_entity = Report(**report_data.dict())  
        created_report = create_report(db, report_entity)
        return ReportTransformer.to_response_model(created_report)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database integrity error", "details": str(e.__cause__)}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Unexpected error creating report", "details": str(e)}
        )

def get_report(db: Session, report_id: int) -> ReportResponse:
    report = get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportTransformer.to_response_model(report)


def list_reports(db: Session) -> List[ReportResponse]:
    try:
        reports = list_all_reports(db)
        return [ReportTransformer.to_response_model(r) for r in reports]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error listing reports", "details": str(e)}
        )

def modify_report(db: Session, report_id: int, data: dict) -> ReportResponse:
    try:
        report = get_report_by_id(db, report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Report not found"}
            )
        # Update only non-null fields
        for key, value in data.items():
            if value is not None:
                setattr(report, key, value)

        updated_report = update_report(db, report)
        return ReportTransformer.to_response_model(updated_report)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database integrity error", "details": str(e.__cause__)}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error updating report", "details": str(e)}
        )

def remove_report(db: Session, report_id: int) -> dict:
    try:
        report = get_report_by_id(db, report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Report not found"}
            )
        delete_report(db, report)
        return {"message": "Report successfully deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error deleting report", "details": str(e)}
        )

def search_reports(db: Session, filters: ReportSearch) -> List[ReportResponse]:
    query = db.query(Report)

    if filters.resource_type:
        query = query.filter(Report.resource_type == filters.resource_type)
    if filters.status:
        query = query.filter(Report.status == filters.status)
    if filters.date:
        query = query.filter(Report.created_at >= filters.date)

    results = query.all()
    return [ReportTransformer.to_response_model(r) for r in results]
