from fastapi import FastAPI
from src.main.python.config.DatabasesConfig import engine
from src.main.python.models.Report import Base
from src.main.python.controller.ReportController import router as report_router

def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Reports Microservice")
    app.include_router(report_router)

    return app

app = create_app()
