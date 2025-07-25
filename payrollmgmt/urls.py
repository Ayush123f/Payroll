"""
URL configuration for payrollmgmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from payroll.views import *

urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('',index,name='index'),
    path('registration',registration,name='registration'),
    path('emp_login',emp_login,name='emp_login'),
    path('emp_home',emp_home,name='emp_home'),
    path('profile',profile,name='profile'),
    path('logout',Logout,name='logout'),
    path('admin_login',admin_login,name='admin_login'),
    path('admin_home',admin_home,name='admin_home'),
    path('change_password',change_password,name='change_password'),
    path('change_passwordadmin',change_passwordadmin,name='change_passwordadmin'),
    path('employee_list',employee_list,name='employee_list'),
    path('edit_employee/<int:id>/', edit_employee, name='edit_employee'),
    path('delete_employee/<int:id>/', delete_employee, name='delete_employee'),
    path('salary/',salary_calculation, name='salary_calculation'),
    path('fuzzy_salary', fuzzy_salary_view, name='fuzzy_salary'),
    
]


# admin.site.site_header= "Payroll"