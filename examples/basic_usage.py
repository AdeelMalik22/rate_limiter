"""
Basic RateGuard usage example.

Run with:
    uvicorn examples.basic_usage:app --reload
"""

from fastapi import FastAPI, Request
from requestguard import limit

app = FastAPI()


@limit(requests=3, window=10)
def hello(request: Request):
    return {"message": "hello"}


@app.get("/hello")
def hello_route(request: Request):
    return hello(request)