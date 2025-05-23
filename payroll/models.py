from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    attendance_score = models.IntegerField(default=0)   # e.g., days present
    performance_score = models.IntegerField(default=0)  # e.g., rating out of 10
    bonus = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def calculate_salary(self):
        # Example weighted scoring algorithm:
        w_att = 0.2; w_perf = 0.4; w_bonus = 0.1; w_ot = 0.3
        score = (self.attendance_score * w_att +
                 self.performance_score * w_perf +
                 float(self.bonus) * w_bonus +
                 float(self.overtime_hours) * w_ot)
        return self.base_salary + score

    def __str__(self):
        return self.user.username
