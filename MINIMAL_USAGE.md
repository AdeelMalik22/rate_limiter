# RateGuard Minimal Usage Guide

RateGuard is a **framework-agnostic** rate limiting library. While it includes a built-in decorator for FastAPI, its core `RateLimiter` class can be used in **any** Python framework (Flask, Django, Celery, or pure Python scripts).

---

## 1. Framework-Agnostic Usage (Any Python App)

You can use the core `RateLimiter` class directly anywhere in your code.

```python
from rateguard import RateLimiter

# Create a limiter: Allow 100 requests every 60 seconds
limiter = RateLimiter(
    max_retries=100,
    ttl=60 #-----> total time limit
)

def some_action(user_id: str):
    # Check the rate limit for this specific user
    result = limiter.check(user_id)
    
    if result["allowed"]:
        print(f"Action allowed! Remaining requests: {result['remaining']}")
        # Perform the action...
    else:
        print(f"Rate limited. Try again in {result['retry_after']} seconds")
        # Return an error to the user
```

---

## 2. FastAPI Usage (Built-in Decorator)

If you are using FastAPI, RateGuard provides a convenient `@limit` decorator that automatically handles key resolution (like IP addresses or authenticated users) and throws standard `429 Too Many Requests` HTTP errors.

```python
from fastapi import FastAPI, Request
from rateguard import limit

app = FastAPI()

# Limit this endpoint to 5 requests per 60 seconds
@limit(max_retries=5, ttl=60)
def my_endpoint(request: Request):
    return {"message": "Hello!"}

@app.get("/hello")
def hello_route(request: Request):
    return my_endpoint(request)
```
