from sqlalchemy.orm import Session
from src.main.python.models.Report import Report

def create_report(db: Session, report: Report) -> Report:
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_report_by_id(db: Session, report_id: int) -> Report:
    return db.query(Report).filter(Report.report_id == report_id).first()

def list_all_reports(db: Session):
    return db.query(Report).all()

def update_report(db: Session, report: Report) -> Report:
    db.commit()
    db.refresh(report)
    return report

def delete_report(db: Session, report: Report) -> None:
    db.delete(report)
    db.commit()
