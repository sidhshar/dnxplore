from datetime import date
from typing import List
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from statusmaster.models import Employee, Department

api = NinjaAPI()

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