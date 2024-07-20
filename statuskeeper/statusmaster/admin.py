from django.contrib import admin

from .models import Department, Employee

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'department', 'birthdate', )

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
