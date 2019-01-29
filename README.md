# SharesOutstanding
Get 'shares outstanding' info from '10-Q' report on www.sec.gov

Takes stock-symbol and goes to sec.gov,
finds the last 10-Q report for that company and
returns back 'shares outstanding' info, like:

- ex1:   "AMD'" the result is "999,407,216"
- ex2:   "KTOS" the result is " 103,297,525 "
- ex3    "INTC" the result is "4,564" etc
