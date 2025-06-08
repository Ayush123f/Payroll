class PayrollCalculation:
  def calculate_payroll(self, working_days, attd, postion, bonus):
    return {
      "GS": working_days,
      "NS" : working_days
    }
  

  def map_performace_score(self, score):
    BONUS_MAPPING = {
      "LOW": 30,
      "MID": 60,
      "HIGH": 100,
    }
    return BONUS_MAPPING.get(score)

if __name__ == "__main__":
  payroll_instance = PayrollCalculation()
  bonus_calc = payroll_instance.map_performace_score("LOW")
  print("BONUS Percentage", bonus_calc)

  payroll_calc = payroll_instance.calculate_payroll(40, 100, "Jr", bonus_calc)
  print(payroll_calc)


# working_hours = 40
# attendance = 100%
# experience(Jr)

# GS 30000
# NS 25000
# tax 1000
# ssf 2000