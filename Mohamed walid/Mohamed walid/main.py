from fastapi import FastAPI
from app.database import engine, Base
import app.models.user
import app.models.student
from app.routes import student

app = FastAPI()

import time
import app.utils.metrics as metrics

# 🔥 Middleware Monitoring
@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    # 📊 Requests count
    metrics.request_count += 1

    # ⏱️ Response time
    metrics.total_response_time += process_time
    metrics.avg_response_time = (
        metrics.total_response_time / metrics.request_count
    )

    # 🚨 Errors
    if response.status_code >= 400:
        metrics.error_count += 1

        # آخر 5 أخطاء
        metrics.recent_errors.append(
            f"{request.method} {request.url.path} - {response.status_code}"
        )

        if len(metrics.recent_errors) > 5:
            metrics.recent_errors.pop(0)

    print(
        f"{request.method} {request.url.path} - "
        f"{response.status_code} - {process_time:.4f}s"
    )

    return response


# 🌍 CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🗄️ Create DB tables
Base.metadata.create_all(bind=engine)

# 📌 Routers
app.include_router(student.router)

@app.get("/")
def root():
    return {"message": "Hello, FastAPI is working 🚀"}

from app.routes import auth
app.include_router(auth.router)

from app.routes import monitor
app.include_router(monitor.router)
