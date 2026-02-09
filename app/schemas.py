from pydantic import BaseModel, HttpUrl

class URLShortenRequest(BaseModel):
    url: HttpUrl
    custom_code: str | None = None

class URLShortenResponse(BaseModel):
    short_url: str
    code: str