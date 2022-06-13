from multiprocessing import context
from django.http import HttpResponseGone
from django.shortcuts import redirect, render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q


def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'view_all_emp.html', context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = request.POST['salary']
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name=first_name,
                           last_name=last_name,
                           salary=salary,
                           bonus=bonus,
                           phone=phone,
                           dept_id=dept,
                           role_id=role,
                           hire_date=datetime.now())
        new_emp.save()
        return redirect('/')

    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse(
            "An Exception Occured! Employee Has not been added.")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Please enter a valid EMP ID")
    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method == 'POST':
        # import ipdb;ipdb.set_trace()
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        # emps = Employee.objects.all()
        if name :
            emps_name = Employee.objects.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name),
                Q(dept__name__icontains=dept) , Q(role__name__icontains=role))
        # if dept: filter on multiple fields 
        #     # dept = emps.filter(dept__name__icontains=dept)
        #     emps_dept_name = emps_name.filter(dept__name__icontains=dept)
        # if role:
        #     # role = emps.filter(role__name__icontains=role)
        #     emps_dept_name_role = emps_dept_name.filter(role__name__icontains=role)

        context = {'emps': emps_name}
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An exception occured')
