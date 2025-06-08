from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import EmployeeDetail
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



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

# @login_required(login_url='admin_login')
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


     

    
 


# def attendance(request):
#     return render(request, 'attendance.html')
