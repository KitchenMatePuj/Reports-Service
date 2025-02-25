import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Aseguramos que estas variables de entorno estén definidas
os.environ["DATABASE_URL"] = "mysql+pymysql://root:1234@localhost:3306/reports_db"
os.environ["DATABASE_POOL_SIZE"] = "5"

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.models.Report import Base, Report
from src.main.python.Application import app

# Create an engine and a test session
engine = create_engine(os.environ["DATABASE_URL"])
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

# Override the FastAPI get_db dependency to use our test session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def clear_reports():
    """
    Clears the 'report' table before and after each test to ensure test isolation.
    """
    db = TestingSessionLocal()
    db.query(Report).delete()
    db.commit()
    db.close()
    yield
    db = TestingSessionLocal()
    db.query(Report).delete()
    db.commit()
    db.close()

def test_create_report():
    """
    Test creating a new report via POST /reports
    """
    payload = {
        "reporter_user_id": "tester_123",
        "resource_type": "comment",
        "resource_id": "42",
        "description": "Inappropriate language in this comment",
        "status": "pending"
    }
    response = client.post("/reports/", json=payload)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["reporter_user_id"] == "tester_123"
    assert data["resource_type"] == "comment"
    assert data["resource_id"] == "42"
    assert data["description"] == "Inappropriate language in this comment"
    assert data["status"] == "pending"
    assert "report_id" in data

def test_get_report_by_id():
    """
    Test retrieving a report by ID (GET /reports/{report_id})
    """
    # Insert a report directly into the DB
    db = TestingSessionLocal()
    new_report = Report(
        reporter_user_id="user_999",
        resource_type="recipe",
        resource_id="55",
        description="Recipe contains offensive content",
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    db.close()

    # Request it via the endpoint
    response = client.get(f"/reports/{new_report.report_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["report_id"] == new_report.report_id
    assert data["reporter_user_id"] == "user_999"
    assert data["resource_type"] == "recipe"

def test_list_reports():
    """
    Test listing all reports (GET /reports)
    """
    db = TestingSessionLocal()
    report1 = Report(
        reporter_user_id="user_a",
        resource_type="recipe",
        resource_id="11",
        description="Something is wrong",
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    report2 = Report(
        reporter_user_id="user_b",
        resource_type="comment",
        resource_id="22",
        description="Offensive content in comment",
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(report1)
    db.add(report2)
    db.commit()
    db.refresh(report1)
    db.refresh(report2)
    db.close()

    response = client.get("/reports/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    ids = [item["report_id"] for item in data]
    assert report1.report_id in ids
    assert report2.report_id in ids

def test_delete_report_by_id():
    """
    Test deleting a report by ID (DELETE /reports/{report_id})
    """
    db = TestingSessionLocal()
    test_report = Report(
        reporter_user_id="delete_user",
        resource_type="advertisement",
        resource_id="77",
        description="Spam advertisement",
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(test_report)
    db.commit()
    db.refresh(test_report)
    db.close()

    # Verify it exists
    response_get = client.get(f"/reports/{test_report.report_id}")
    assert response_get.status_code == 200

    # Perform DELETE
    response_del = client.delete(f"/reports/{test_report.report_id}")
    assert response_del.status_code == 204

    # Verify it's gone
    response_after_del = client.get(f"/reports/{test_report.report_id}")
    assert response_after_del.status_code == 404
