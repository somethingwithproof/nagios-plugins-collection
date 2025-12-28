from typing import Any, Dict, Optional

from fastapi import Body, FastAPI, Form, Query
from fastapi.responses import JSONResponse

app = FastAPI(title="NPC E2E Mocks")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/token")
def token(
    client_id: str = Form(...),
    client_secret: str = Form(...),
    grant_type: str = Form("client_credentials"),
    scope: Optional[str] = Form(None),
) -> JSONResponse:
    # Minimal OAuth2 token endpoint
    data = {
        "access_token": "mock-token",
        "token_type": "Bearer",
        "expires_in": 3600,
    }
    if scope:
        data["scope"] = scope
    return JSONResponse(content=data)


@app.get("/api/v1/query")
def prom_query(query: str = Query(...)) -> JSONResponse:  # pragma: no cover - e2e only
    # Return a scalar result that varies by query string
    value = "5" if "errors" in query.lower() else "0.42"
    payload = {
        "status": "success",
        "data": {
            "resultType": "vector",
            "result": [
                {
                    "metric": {},
                    "value": [0, value],
                }
            ],
        },
    }
    return JSONResponse(content=payload)


@app.post("/es/{index}/_search")
def es_search(
    index: str, body: Optional[Dict[str, Any]] = None
) -> JSONResponse:  # pragma: no cover
    # Very small subset of ES search for tests: returns hits.total.value
    if body is None:
        body = Body(...)
    try:
        q = (
            body.get("query", {})
            .get("bool", {})
            .get("filter", [])[1]
            .get("query_string", {})
            .get("query", "")
        )
    except Exception:
        q = ""
    hits = 25 if ("errors" in q.lower() and "many" in q.lower()) else 0
    return JSONResponse(content={"hits": {"total": {"value": hits}}})
