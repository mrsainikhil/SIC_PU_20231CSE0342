name = input("Enter your Name: ")
emp_id = input("Enter your Employee ID: ")
basic_sal = int( input("Enter your Basic Salary: "))
speacial_allowance = int( input("Enter your Special Allowance: "))
bonus_percent = int( input("Enter your Bonus Percentage: "))
gross_sal = basic_sal + speacial_allowance
annual_gross_sal = gross_sal * 12
print(f"Name : {name}\nEmployee ID : {emp_id}\nMonthly Salary : {gross_sal}\nAnnual Salary : {annual_gross_sal}")
taxable_income=annual_gross_sal-50000
print(f"Taxable income after standard deduction {annual_gross_sal} - 50000 = {taxable_income}")
tax_rate = 0
tax_payable=0
print("Tax Breakdown")
if taxable_income <= 700000:
    print(f"Your taxable income is less 700000. You get 100% rebate\nTax Payable = 0")
else:
    while(taxable_income > 0 and tax_rate < 25):
        taxable_income -= 300000
        tax=tax_rate / 100 * 300000
        tax_payable += tax
        print(f"tax at rate of {tax_rate}% {tax}")
        tax_rate+=5
