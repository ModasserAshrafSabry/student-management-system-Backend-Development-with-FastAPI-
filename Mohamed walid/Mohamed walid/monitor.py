from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.utils.security import require_admin
import app.utils.metrics as metrics

router = APIRouter()


@router.get("/monitor")
def monitor(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    student_count = db.query(Student).count()

    from app.models.user import User
    user_count = db.query(User).count()

    return {
        "students": student_count,
        "users": user_count,
        "requests": metrics.request_count,
        "errors": metrics.error_count,

        # ⏱️ New
        "avg_response_time": round(metrics.avg_response_time, 4),

        # 🚨 New
        "recent_errors": metrics.recent_errors,

        # 🔐 New
        "recent_auth_logs": metrics.recent_auth_logs,

        "status": "Running",

        "alert": (
            "⚠️ High error rate!"
            if metrics.error_count > 0
            else "✅ System healthy"
        )
    }
