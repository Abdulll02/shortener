import os

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_shorten_url():
    response = client.post("/shorten", json={"url": "https://google.com"})
    assert response.status_code == 200
    assert "short_url" in response.json()
    assert "code" in response.json()

def test_redirect():
    # Создаем ссылку
    res = client.post("/shorten", json={"url": "https://python.org"})
    code = res.json()["code"]
    
    # Проверяем редирект
    redirect_res = client.get(f"/{code}", follow_redirects=False)
    assert redirect_res.status_code == 307
    assert redirect_res.headers["location"] == "https://python.org/"

def test_not_found():
    response = client.get("/nonexistentcode")
    assert response.status_code == 404