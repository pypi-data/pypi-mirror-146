def mortgagecalculator (amount,years,interest):
  interest=interest/100
  nper = years*12
  interest_monthly=interest/12
  numerator=interest_monthly*((1+interest_monthly)**nper)
  denominator=(1+interest_monthly)**nper-1
  payment=float("{0:.2f}".format(amount*numerator/denominator))
  return(payment)
print ('MORTGAGE CALCULATOR')
x = input('enter amount borrowed: ')
y = input('enter number of years for mortgage: ')
i = input('enter yearly interest rate in percent: ')
print("monthly payment",mortgagecalculator(float(x),float(y),float(i)))
input("Press Enter to continue...")
