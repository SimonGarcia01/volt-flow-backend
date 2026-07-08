from app.auth import models as auth_models


def import_all_models() -> None:
    """Import every module-owned SQLAlchemy model before metadata operations."""
    _ = auth_models
