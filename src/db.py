try:
    from sqlalchemy import create_engine  # type: ignore[reportUnknownVariableType]
    from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta, Session  # type: ignore[reportUnknownVariableType]
    from sqlalchemy.engine import Engine  # type: ignore[reportUnknownVariableType]
    from typing import cast
except ImportError as e:
    raise ImportError(
        "sqlalchemy is required for this project. Install it with: pip install sqlalchemy"
    ) from e

DATABASE_URL = "sqlite:///./space_dmv_insurance.db"
# For Postgres later:
# DATABASE_URL = "postgresql+psycopg2://user:password@localhost/space_dmv_insurance"

engine: Engine = cast(Engine, create_engine(  # type: ignore[reportUnknownVariableType]
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # type: ignore[reportUnknownVariableType]
Base: DeclarativeMeta = cast(DeclarativeMeta, declarative_base()) # pyright: ignore[reportUnknownVariableType]
