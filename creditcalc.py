from math import ceil, floor, log, pow
import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description="Credit Calculator Project")

# Add the parameters positional/optional
parser.add_argument('--type', help="Type of Payment (Annuity or Differential")
parser.add_argument('--payment', help="Monthly payment", type=int)
parser.add_argument('--principal', help="Credit principal", type=int)
parser.add_argument('--periods', help="Count of months", type=int)
parser.add_argument('--interest', help="Credit interest (rate of interest)", type=float)

# Parse the arguments
args = parser.parse_args()

# Will check if type of payment is specified or invalid.
if args.type not in ['diff', 'annuity']:
    print('Incorrect parameters')
    exit(0)

# Payment is different for each therefore, payment is invalid arguments in --type=diff.
if args.type == 'diff' and args.payment is not None:
    print('Incorrect Parameters')
    exit(0)

# Collect the state of arguments. no value = None
args_list = [args.type, args.payment, args.principal, args.periods, args.interest]
# print(args_list)

# Checks if arguments has value. Less than four arguments is invalid.
count = 0
for arg in args_list:
    if arg is None:
        count += 1
# print(count)

if count > 1:
    print('Incorrect Parameters')
    exit(0)

# Checks if negative number is present in arguments.
if args_list[1] is not None and args_list[1] < 0 or args_list[2] is not None and args_list[2] < 0 or args_list[3] \
        is not None and args_list[3] < 0 or args_list[4] is not None and args_list[4] < 0.0:
    print('Incorrect Parameters')
    exit(0)

# Function for annuity computation.
if args.type == 'annuity' and args.payment is None:
    nominal_rate = args.interest / (12 * 100)

    annuity = ceil((args.principal * (nominal_rate * pow((1 + nominal_rate), args.periods))
                    / (pow((1 + nominal_rate), args.periods) - 1)))
    overpayment = annuity * args.periods - args.principal
    print(f'Your annuity payment = {annuity}!')
    print('Overpayment =', overpayment)

# Function for credit principal computation.
elif args.type == 'annuity' and args.principal is None:
    nominal_rate = args.interest / (12 * 100)

    principal = floor((args.payment / ((nominal_rate * pow((1 + nominal_rate), args.periods))
                                       / (pow((1 + nominal_rate), args.periods) - 1))))
    overpayment = args.payment * args.periods - principal

    print(f'Your credit principal = {principal}!')
    print('Overpayment =', overpayment)

# Function to calculate how much time a user needs to pay.
elif args.type == 'annuity' and args.periods is None:
    nominal_rate = args.interest / (12 * 100)

    args.periods = ceil(log((args.payment / (args.payment - nominal_rate * args.principal)), (1 + nominal_rate)))

    years = args.periods // 12
    months = args.periods % 12

    if years >= 1:
        if months >= 1:
            print(f'You need {years} years and {months} months to repay this credit!')
        else:
            print(f'You need {years} years to repay this credit!')
    else:
        print(f'You need {months} months to repay this credit!')

    overpayment = args.payment * args.periods - args.principal
    print('Overpayment =', overpayment)

# Function to calculate differentiated payments.
elif args.type == 'diff':
    nominal_rate = args.interest / (12 * 100)
    total_amount = 0

    for months in range(1, args.periods + 1):
        diff_monthly = ceil((args.principal / args.periods) + nominal_rate *
                            (args.principal - ((args.principal * (months - 1)) / args.periods)))
        total_amount += diff_monthly
        print(f'Month {months}: paid out {diff_monthly}')

    overpayment = total_amount - args.principal
    print('\nOverpayment =', overpayment)
