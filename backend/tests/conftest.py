import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture
def base_url():
    return os.getenv("BASE_URL", "http://localhost:8000")