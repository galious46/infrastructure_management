from fastapi import FastAPI
import requests
from typing import List, Dict
import uvicorn

app = FastAPI()

@app.get("/joke")
async def get_programming_joke() -> Dict:
    url = "https://official-joke-api.appspot.com/jokes/programming/random"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        joke_data = response.json()[0]  # API возвращает список с одним объектом
        return {
            "setup": joke_data["setup"],
            "punchline": joke_data["punchline"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch joke: {str(e)}"}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()