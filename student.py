from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import time
import json

from app.database import get_db
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentResponse
from app.utils.security import get_current_user, require_admin
from app.utils.logger import logger
from app.utils.redis_client import redis_client

router = APIRouter()


# CREATE
@router.post("/students", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} is creating student {student.name}")

    db_student = Student(
        name=student.name,
        department=student.department,
        gpa=student.gpa,
        user_id=current_user.id
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    try:
        redis_client.delete("students")
        redis_client.delete(f"student:{db_student.id}")
    except Exception as e:
        logger.error(f"Redis delete error: {e}")

    logger.info(f"User {current_user.username} created student {db_student.name}")

    return db_student


# GET ALL
@router.get("/students")
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    department: str = Query(None),
    min_gpa: float = Query(None),
    skip: int = 0,
    limit: int = 10
):
    start = time.time()

    logger.info(f"User {current_user.username} requested students list")

    cache_key = "students"

    try:
        cached_data = redis_client.get(cache_key)
    except Exception as e:
        logger.error(f"Redis get error: {e}")
        cached_data = None

    if cached_data:
        students = json.loads(cached_data)
        duration = time.time() - start
        logger.info(f"GET /students FROM CACHE in {duration:.4f}s")
    else:
        db_students = db.query(Student).all()

        students = [
            {
                "id": s.id,
                "name": s.name,
                "department": s.department,
                "gpa": s.gpa,
                "user_id": s.user_id
            }
            for s in db_students
        ]

        try:
            redis_client.set(cache_key, json.dumps(students), ex=60)
        except Exception as e:
            logger.error(f"Redis set error: {e}")

        duration = time.time() - start
        logger.info(f"GET /students FROM DB in {duration:.4f}s")

    if current_user.role != "admin":
        students = [s for s in students if s["user_id"] == current_user.id]

    if department:
        students = [s for s in students if s["department"].lower() == department.lower()]

    if min_gpa:
        students = [s for s in students if s["gpa"] >= min_gpa]

    return students[skip: skip + limit]


# GET BY ID
@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start = time.time()

    cache_key = f"student:{student_id}"

    try:
        cached_data = redis_client.get(cache_key)
    except Exception as e:
        logger.error(f"Redis get error: {e}")
        cached_data = None

    if cached_data:
        student_data = json.loads(cached_data)

        if current_user.role != "admin" and student_data["user_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")

        duration = time.time() - start
        logger.info(f"GET /students/{student_id} FROM CACHE in {duration:.4f}s")

        return student_data

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if current_user.role != "admin" and student.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    student_data = {
        "id": student.id,
        "name": student.name,
        "department": student.department,
        "gpa": student.gpa,
        "user_id": student.user_id
    }

    try:
        redis_client.set(cache_key, json.dumps(student_data), ex=60)
    except Exception as e:
        logger.error(f"Redis set error: {e}")

    duration = time.time() - start
    logger.info(f"GET /students/{student_id} FROM DB in {duration:.4f}s")

    return student_data


# UPDATE
@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated_student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if current_user.role != "admin" and student.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    student.name = updated_student.name
    student.department = updated_student.department
    student.gpa = updated_student.gpa

    db.commit()
    db.refresh(student)

    try:
        redis_client.delete("students")
        redis_client.delete(f"student:{student_id}")
    except Exception as e:
        logger.error(f"Redis delete error: {e}")

    logger.info(f"User {current_user.username} updated student {student_id}")

    return student


# DELETE
@router.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    try:
        redis_client.delete("students")
        redis_client.delete(f"student:{student_id}")
    except Exception as e:
        logger.error(f"Redis delete error: {e}")

    logger.warning(f"User {current_user.username} deleted student {student_id}")

    return {"message": "Student deleted successfully"}


