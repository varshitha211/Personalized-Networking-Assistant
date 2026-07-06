import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.database import Base, get_db
from backend.main import create_app


@pytest.fixture(autouse=True)
def mock_pipelines():
    with patch("backend.services.event_analyzer._get_pipeline") as mock_event:
        with patch("backend.services.topic_generator._get_generator") as mock_topic:
            mock_instance = MagicMock()
            mock_instance.return_value = {
                "labels": ["technology", "climate change", "urban planning", "sustainability", "innovation"],
                "scores": [0.85, 0.72, 0.68, 0.55, 0.42],
            }
            mock_event.return_value = mock_instance

            mock_gen = MagicMock()
            mock_gen.return_value = [{"generated_text": "What trends in this field interest you most?"}]
            mock_topic.return_value = mock_gen
            yield


@pytest.fixture
def db_session():
    db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = db_file.name
    db_file.close()
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    engine.dispose()
    Base.metadata.drop_all(bind=engine)
    try:
        os.unlink(db_path)
    except PermissionError:
        pass


@pytest.fixture
def client(db_session):
    app = create_app()

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_event_description():
    return "AI for Sustainable Cities Conference focusing on climate tech and urban innovation"


@pytest.fixture
def sample_interests():
    return "climate change, urban planning, data science"
