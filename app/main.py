import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.database import init_db, get_db_cursor
from app.schemas import URLShortenRequest, URLShortenResponse
from app.services import generate_short_code

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # логика при старте приложения
    init_db()
    logger.info("Database initialized and app started")
    yield
    # здесь можно добавить логику при выключении (например, закрытие пулов БД)
    logger.info("Shutting down...")

app = FastAPI(
    title="URL Shortener",
    lifespan=lifespan
)

@app.post("/shorten", response_model=URLShortenResponse)
async def shorten_url(payload: URLShortenRequest, request: Request):
    code = payload.custom_code or generate_short_code()
    url_str = str(payload.url)

    with get_db_cursor() as cur:
        # проверка на конфликт кастомного кода
        cur.execute("SELECT 1 FROM links WHERE code = ?", (code,))
        if cur.fetchone():
            if payload.custom_code:
                logger.warning(f"Conflict: custom code '{code}' already exists")
                raise HTTPException(status_code=400, detail="Custom code already taken")
            # если сгенерированный код случайно совпал, пробуем еще раз
            code = generate_short_code(8)

        cur.execute(
            "INSERT INTO links (code, original_url) VALUES (?, ?)",
            (code, url_str)
        )
        logger.info(f"URL shortened: {url_str} -> {code}")

    base_url = str(request.base_url)
    return {"short_url": f"{base_url}{code}", "code": code}

@app.get("/{code}")
async def redirect_to_url(code: str):
    with get_db_cursor() as cur:
        cur.execute("SELECT original_url FROM links WHERE code = ?", (code,))
        row = cur.fetchone()
        
        if not row:
            logger.warning(f"Failed redirect: code '{code}' not found")
            raise HTTPException(status_code=404, detail="Short link not found")
        
        return RedirectResponse(url=row["original_url"], status_code=307)

@app.delete("/links/{code}")
async def delete_link(code: str):
    with get_db_cursor() as cur:
        cur.execute("DELETE FROM links WHERE code = ?", (code,))
        logger.info(f"Link deleted: {code}")
        return {"detail": f"Link {code} deleted"}