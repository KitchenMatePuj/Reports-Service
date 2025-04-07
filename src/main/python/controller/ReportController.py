from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.ReportService import (
    create_new_report,
    get_report,
    modify_report,
    remove_report,
    list_reports,
    search_reports
)
from src.main.python.transformers.ReportTransformer import ReportResponse, ReportCreate, ReportSearch, ReportUpdate

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/", response_model=ReportResponse)
def create_report_endpoint(report_data: ReportCreate, db: Session = Depends(get_db)):
    return create_new_report(db, report_data)

@router.get("/", response_model=List[ReportResponse])
def list_all_reports_endpoint(db: Session = Depends(get_db)):
    return list_reports(db)

@router.get("/{report_id}", response_model=ReportResponse)
def get_report_endpoint(report_id: int, db: Session = Depends(get_db)):
    return get_report(db, report_id)

@router.put("/{report_id}", response_model=ReportResponse)
def update_report_endpoint(report_id: int, report_data: ReportUpdate, db: Session = Depends(get_db)):
    return modify_report(db, report_id, report_data.dict(exclude_unset=True))

@router.delete("/{report_id}", status_code=204)
def delete_report_endpoint(report_id: int, db: Session = Depends(get_db)):
    remove_report(db, report_id)
    return

@router.get("/search", response_model=List[ReportResponse])
def search_reports_endpoint(
    filters: ReportSearch = Depends(),
    db: Session = Depends(get_db)
):
    return search_reports(db, filters.user_type, filters.status, filters.date)
