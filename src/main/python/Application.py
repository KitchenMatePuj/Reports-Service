from fastapi import FastAPI
from src.main.python.config.DatabasesConfig import engine
from src.main.python.models.Report import Base
from src.main.python.controller.ReportController import router as report_router
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Reports Microservice")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://localhost:8080"],  # Cambia si usas otra URL en frontend
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(report_router)

    return app

app = create_app()
