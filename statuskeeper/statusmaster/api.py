from datetime import date
import logging
from typing import List
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from .models import Scan, Progress
from .models import Employee, Department
# from .schemas import ScanSchema, ProgressSchema
from .schemas import AuthSchema, ScanInSchema, ScanOutSchema, ProgressInSchema, ScanUpdateSchema
from ninja_jwt.tokens import RefreshToken

from ninja.security import django_auth
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


# api = NinjaAPI(auth=JWTAuth())
api = NinjaAPI()

logger = logging.getLogger(__name__)

"""
API Master to manage the scan models.
"""

class UserSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access: str
    refresh: str

@api.post("/register/", response={201: UserSchema, 400: dict})
def register(request, payload: UserSchema):
    print("[register] Got New register request")
    if User.objects.filter(username=payload.username).exists():
        return 400, {"error": "User with this username already exists"}
    
    user = User.objects.create(
        username=payload.username,
        password=make_password(payload.password)
    )
    return 201, UserSchema(username=user.username, password="********")

@api.post("/token/", response={200: TokenSchema, 401: dict})
def login(request, payload: UserSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        return 401, {"error": "Invalid credentials"}
    
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


@api.get("/scanslatest/", auth=JWTAuth(), response=List[ScanOutSchema])
def get_scan(request):
    latest_scans = Scan.objects.all().order_by('-created_at')[:10]
    return latest_scans

@api.post("/scans/", auth=JWTAuth())
def create_scan(request, payload: ScanInSchema):
    scan = Scan.objects.create(**payload.dict())
    logger.debug(f"Created scan: {scan.id}")
    # return {"id": scan.id, "name": scan.name, "status": scan.status}
    return 200, ScanOutSchema(id=scan.id, name=scan.name, status=scan.status)

@api.put("/scans/{scan_id}/", response={200: dict, 404: dict})
def update_scan_name(request, scan_id: int, payload: ScanUpdateSchema):
    scan = get_object_or_404(Scan, id=scan_id)
    scan.name = payload.name
    scan.save()
    return {"status": "success", "message": f"Scan name updated to {scan.name}"}

@api.get("/scans/{scan_id}/", auth=JWTAuth())
def get_scan(request, scan_id: int):
    scan = get_object_or_404(Scan, id=scan_id)
    progress = scan.progress.all()
    logger.debug(f"Retrieved scan: {scan.id}")
    return {
        "id": scan.id,
        "name": scan.name,
        "status": scan.status,
        "progress": [{"percentage": p.progress_percentage, "timestamp": p.timestamp} for p in progress]
    }

@api.post("/scans/{scan_id}/progress/", auth=JWTAuth())
def update_progress(request, scan_id: int, payload: ProgressInSchema):
    scan = get_object_or_404(Scan, id=payload.scan_id)
    Progress.objects.create(scan=scan, progress_percentage=payload.progress_percentage)
    logger.debug(f"Updated progress for scan: {scan.id} to {payload.progress_percentage}%")
    if payload.progress_percentage >= 100:
        scan.status = "completed"
        scan.save()
    return {"status": "progress updated"}



"""
OLD Schemas. Delete later.
"""
class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

#------------------------------- DEPARTMENT -------------------------------#
@api.post("/departments")
def create_department(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return {"id": department.id}

@api.get("/departments/{department_id}", response=DepartmentOut)
def get_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    return department

@api.get("/departments", response=List[DepartmentOut])
def list_departments(request):
    qs = Department.objects.all()
    return qs

@api.put("/departments/{department_id}")
def update_department(request, department_id: int, payload: DepartmentIn):
    department = get_object_or_404(Department, id=department_id)
    for attr, value in payload.dict().items():
        setattr(department, attr, value)
    department.save()
    return {"success": True}


@api.delete("/departments/{department_id}")
def delete_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    return {"success": True}

#------------------------------- EMPLOYEE -------------------------------#

@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    print(payload.dict())
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs


@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}