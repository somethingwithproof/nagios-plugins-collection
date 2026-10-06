# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
from typing import Any

from fastapi import Body, FastAPI, Form, Query
from fastapi.responses import JSONResponse

app = FastAPI(title="NPC E2E Mocks")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/token")
def token(
    client_id: str = Form(...),
    client_secret: str = Form(...),
    grant_type: str = Form("client_credentials"),
    scope: str | None = Form(None),
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
    q = query.lower()
    if "errors" in q:
        value = "5"  # critical path
    elif "warn" in q:
        value = "1.5"  # warning path (between default thresholds 1 and 2 in CI)
    else:
        value = "0.42"  # ok path
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
def es_search(index: str, body: dict[str, Any] | None = None) -> JSONResponse:  # pragma: no cover
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
    ql = q.lower()
    if "errors" in ql and "many" in ql:
        hits = 25  # CRITICAL
    elif "errors" in ql and "some" in ql:
        hits = 5  # WARNING
    else:
        hits = 0  # OK
    return JSONResponse(content={"hits": {"total": {"value": hits}}})
