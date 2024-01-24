from starlette.testclient import TestClient
from settings.config import app

client = TestClient(app=app)
