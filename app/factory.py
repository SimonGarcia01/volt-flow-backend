from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Volt Flow Backend",
        version="0.1.0",
        description="Backend for managing OCPP charge points.",
    )

    return app