from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import EmployeeDetail
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl



def index(request):
    return render(request, 'index.html')

def registration(request):
    error = ""
    if request.method == "POST":
        try:
            fn = request.POST['firstname']
            ln = request.POST['lastname']
            ec = request.POST['empcode']
            em = request.POST['email']
            pwd = request.POST['pwd']

            user = User.objects.create_user(
                first_name=fn,
                last_name=ln,
                username=em,
                password=pwd
            )
            EmployeeDetail.objects.create(user=user, empcode=ec)
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"

    return render(request, 'registration.html', {'error': error})

def emp_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user:
            login(request,user)
            error ='no'
        else:
            error ='yes'

    return render(request, 'emp_login.html',locals())

@login_required
def emp_home(request):
    # if not request.user.is_authenticated:
    #     return redirect('emp_login')
    return render(request, 'emp_home.html')

def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    error = ""
    user = request.user

    try:
        employee = EmployeeDetail.objects.get(user=user)
    except EmployeeDetail.DoesNotExist:
        employee = None

    if request.method == "POST":
        try:
            fn = request.POST['firstname']
            ln = request.POST['lastname']
            ec = request.POST['empcode']
            department = request.POST['department']
            designation = request.POST['designation']
            contact = request.POST['contact']
            jdate = request.POST['jdate']
            gender = request.POST['gender']

            # Update user model
            user.first_name = fn
            user.last_name = ln
            user.save()

            # Update employee model
            if employee:
                employee.empcode = ec
                employee.empdepartment = department
                employee.designation = designation
                employee.contact = contact
                employee.gender = gender
                if jdate:
                    employee.joiningdate = jdate
                employee.save()

            error = "no"
        except Exception as e:
            print(e)
            error = "yes"

    return render(request, 'profile.html', {'error': error, 'employee': employee})


# def admin_login(request):
#     error = ""
#     if request.method == 'POST':
#         u = request.POST['email']
#         p = request.POST['password']
#         user = authenticate(username=u,password=p)
#         if user.is_staff:
#             login(request,user)
#             error ='no'
#         else:
#             error ='yes'

#     return render(request, 'admin_login.html',locals())




def admin_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            error = "no"
        else:
            error = "yes"

    return render(request, 'admin_login.html', {'error': error})

@login_required(login_url='admin_login')
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    error = ""
    user = request.user

    if request.method == 'POST':
        c = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')

        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request, 'change_password.html', {'error': error})

@login_required(login_url= admin_login)
def employee_list(request):
    return render(request, 'employee_list.html')



def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    error = ""
    user = request.user

    if request.method == 'POST':
        c = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')

        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request, 'change_passwordadmin.html', {'error': error})

def employee_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    employee = EmployeeDetail.objects.all()
    return render(request, 'employee_list.html', {'employee': employee})

def edit_employee(request, id):
    employee = get_object_or_404(EmployeeDetail, id=id)
    if request.method == 'POST':
        user = employee.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('email')
        user.save()

        employee.empcode = request.POST.get('empcode')
        employee.contact = request.POST.get('contact')
        employee.designation = request.POST.get('designation')
        employee.empdepartment = request.POST.get('department')
        employee.joiningdate = request.POST.get('joiningdate')
        employee.gender = request.POST.get('gender')
        employee.save()

        return redirect('employee_list')

    return render(request, 'edit_employee.html', {'employee': employee})


def delete_employee(request, id):
    employee = get_object_or_404(EmployeeDetail, id=id)
    user = employee.user
    user.delete()  # Also deletes employee due to on_delete=models.CASCADE
    return redirect('employee_list')



def salary_calculation(request):

    performance = 80
    attendance = 90
    experience = 5
    basic_salary = 50000
    deductions = 2000

    weighted_score = (performance * 0.50) + (attendance * 0.30) + (experience * 0.20)

    
    if weighted_score >= 70:
        bonus = basic_salary * 0.10
    else:
        bonus = basic_salary * 0.05

 
    net_salary = basic_salary + bonus - deductions

    context = {
        'performance': performance,
        'attendance': attendance,
        'experience': experience,
        'basic_salary': basic_salary,
        'deductions': deductions,
        'weighted_score': round(weighted_score, 2),
        'bonus': round(bonus, 2),
        'net_salary': round(net_salary, 2),
    }

    return render(request, 'salary_calculation.html', context)


def fuzzy_salary_prediction(performance, attendance, experience):
   
    perf = ctrl.Antecedent(np.arange(0, 101, 1), 'performance')
    attd = ctrl.Antecedent(np.arange(0, 101, 1), 'attendance')
    exp = ctrl.Antecedent(np.arange(0, 31, 1), 'experience')
   
    bonus = ctrl.Consequent(np.arange(0, 16, 1), 'bonus')

   
    perf['low'] = fuzz.trimf(perf.universe, [0, 0, 50])
    perf['medium'] = fuzz.trimf(perf.universe, [30, 50, 70])
    perf['high'] = fuzz.trimf(perf.universe, [60, 100, 100])

    attd['low'] = fuzz.trimf(attd.universe, [0, 0, 50])
    attd['medium'] = fuzz.trimf(attd.universe, [30, 60, 80])
    attd['high'] = fuzz.trimf(attd.universe, [70, 100, 100])

    exp['low'] = fuzz.trimf(exp.universe, [0, 0, 10])
    exp['medium'] = fuzz.trimf(exp.universe, [5, 10, 20])
    exp['high'] = fuzz.trimf(exp.universe, [15, 30, 30])

    bonus['low'] = fuzz.trimf(bonus.universe, [0, 2, 5])
    bonus['medium'] = fuzz.trimf(bonus.universe, [3, 7, 10])
    bonus['high'] = fuzz.trimf(bonus.universe, [8, 12, 15])

   
    rule1 = ctrl.Rule(perf['high'] & attd['high'] & exp['high'], bonus['high'])
    rule2 = ctrl.Rule(perf['medium'] & attd['medium'] & exp['medium'], bonus['medium'])
    rule3 = ctrl.Rule(perf['low'] | attd['low'] | exp['low'], bonus['low'])

    bonus_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    bonus_calc = ctrl.ControlSystemSimulation(bonus_ctrl)


    bonus_calc.input['performance'] = performance
    bonus_calc.input['attendance'] = attendance
    bonus_calc.input['experience'] = experience

    bonus_calc.compute()
    return round(bonus_calc.output['bonus'], 2)




def fuzzy_salary_view(request):
    context = {}

    if request.method == 'POST':
        try:
            performance = float(request.POST.get('performance'))
            attendance = float(request.POST.get('attendance'))
            experience = float(request.POST.get('experience'))

            basic_salary = 50000  # You can also take this from a model or form
            deductions = 1500     # Fixed or dynamic

            predicted_bonus_percent = fuzzy_salary_prediction(performance, attendance, experience)
            bonus_amount = basic_salary * predicted_bonus_percent / 100
            net_salary = basic_salary + bonus_amount - deductions

            context = {
                'performance': performance,
                'attendance': attendance,
                'experience': experience,
                'predicted_bonus_percent': predicted_bonus_percent,
                'basic_salary': basic_salary,
                'bonus_amount': round(bonus_amount, 2),
                'deductions': deductions,
                'net_salary': round(net_salary, 2),
            }
        except Exception as e:
            context['error'] = "Invalid input. Please enter correct values."

    return render(request, 'fuzzy_salary.html', context)




     

    
 
