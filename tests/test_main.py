from unittest.mock import patch, Mock
import requests
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_programming_joke():
    response = client.get("/joke")
    assert response.status_code == 200
    assert "setup" in response.json()
    assert "punchline" in response.json()


# Тест успешного получения шутки
def test_get_programming_joke_success():
    # Мокируем успешный ответ от API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        "setup": "Why do programmers prefer dark mode?",
        "punchline": "Because the light attracts bugs."
    }]

    with patch("requests.get", return_value=mock_response):
        response = client.get("/joke")
        assert response.status_code == 200
        data = response.json()
        assert "setup" in data
        assert "punchline" in data
        assert data["setup"] == "Why do programmers prefer dark mode?"
        assert data["punchline"] == "Because the light attracts bugs."
        assert "error" not in data


# Тест обработки ошибки при запросе к API
def test_get_programming_joke_failure():
    # Мокируем ошибку от API
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("API Error")

    with patch("requests.get", return_value=mock_response):
        response = client.get("/joke")
        assert response.status_code == 200  # FastAPI вернет 200 даже при ошибке(это часть логики)
        data = response.json()
        assert "error" in data
        assert data["error"].startswith("Failed to fetch joke:")
        assert "setup" not in data
        assert "punchline" not in data


# Тест эндпоинта /status
def test_get_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "Server is running"


# Тест успешного создания элемента через /items
def test_create_item_success():
    item_data = {"name": "test_item", "value": 42}
    response = client.post("/items", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["data"] == item_data


# Тест обработки некорректного JSON в /items
def test_create_item_invalid_json():
    response = client.post("/items", content="invalid json")
    assert response.status_code == 422  # FastAPI вернет 422 при некорректном JSON
    data = response.json()
    assert "detail" in data
    assert "msg" in data["detail"][0]
    assert "type" in data["detail"][0]


# Тест запуска main (проверяем, что uvicorn.run вызывается с правильными параметрами)
def test_main_function():
    with patch("uvicorn.run") as mock_run:
        from app.main import main # pylint: disable=import-outside-toplevel
        main()
        mock_run.assert_called_once_with(
            "main:app", host="0.0.0.0", port=8000, reload=True
        )
