#!/usr/bin/python3

# # # # # This is allows you to generate an amortization table
# /(_)\ # calculated from the principle, interest, loan duration
# \* */ # and writes it to the file name passed from the command
#  \_/  # line. This script produces one file and returns a message 
# # # # # containing the monthly payment.

import sys
import argparse as ap
import os.path as op
import math
from pandas import DataFrame as xl
from pandas import ExcelWriter as ew
import xlsxwriter

# this class is for formatting in future updates.
# class formatting:
#    f_underline = '\033[4m'
#    f_close = '\033[0m'
#    f_tab = '\t'

def i_amortize(p,r,n):
    # calculate the monthly interest and apply the
    # amortization formula
    r = r/12
    a = p*( (r*((1+r)**n))/((1+r)**n-1) )
    return(a)

def zero_interest(p,n):
    # this is for calculating the monthly payment
    # for no interest loans
    a = p/n
    return(a)

def i_schedule(p,r,n):
    # calculate the monthly interest rate and pass to
    # i_amortize to calculate the monthly payment and
    # calculate the total loan ammount.
    m_interest = r/12
    payment = i_amortize(p,r,n)
    balance = payment*n
    p_balance = p

    # create the list to hold the dictionary entries
    # to be used to output the data frame for output
    rows = []
    for a in range(n):
        i_paid = p_balance*m_interest
        p_paid = payment-i_paid
        t = {
                "balance": round(balance,2),
                "principle": round(p_paid,2),
                "interest": round(i_paid,2),
                "payment": round(payment,2)
                }
        rows.append(t)
        
        # reduce the total loan balance by the payment
        # and reduce the principle balance by the
        # principle paid in this payment
        balance = balance-payment
        p_balance = p_balance-p_paid
    return(rows)

def o_schedule(rows):
    # stuff the rows in a data frame and re-order the
    # columns for output. I may add some formatting
    # here to allow for usable output to screen
    df = xl(rows)
    a = df.reindex(columns=['balance','principle','interest','payment'])
    b = a.applymap("${0:,.2f}".format)
    return(b)

def xlwriter(rows,p,r,n,title):
    # convert the interest rate to monthly for output.
    # pass p,r,n to i_amortize to retrieve the monthly
    # payment. calculate the total loan after interest.
    mpr = (r/100)/12
    mp = i_amortize(p,r,n)
    amount = mp*n
    name = title+".xlsx"
    if op.isfile(name):
        ErrorBack = (1,f"{title}.xlsx already exists")
        return ErrorBack

    # stuff the rows from the passed dictionary into a
    # data frame, and create the writer.
    df1 = xl(rows)
    writer = ew(name, engine='xlsxwriter')

    # attempt to output the data frame to a spreadsheet
    try:
        df1.to_excel(writer, startrow=6, index=False)
        ErrorBack = (0,'success!')
    except ValueError:
        # more error handling will go here as testing
        # progresses. for now it returns a 1 value for
        # a ValueError
        ErrorBack = (2,"some other funky thing went wrong")
        return ErrorBack
    
    # open a workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # number formats for currency, percentage, and whole numbers
    format_per = workbook.add_format({'num_format': '%##.##'})
    format_mpr = workbook.add_format({'num_format': '%.######'})
    format_num = workbook.add_format({'num_format': '#,###'})
    format_cur = workbook.add_format({'num_format': '$#,##0.00'})
    
    # set the format for all columns to currency
    worksheet.set_column('A:E', 18, format_cur)
    
    # write the summary info at the top
    worksheet.write(0, 0, 'Loan Amount')
    worksheet.write(0, 1, p, format_cur)
    worksheet.write(1, 0, 'Interest Rate')
    worksheet.write(1, 1, r, format_per)
    worksheet.write(2, 0, 'Number of Payments')
    worksheet.write(2, 1, n, format_num)
    worksheet.write(3, 0, 'Monthly Interset Rate')
    worksheet.write(3, 1, mpr, format_mpr)
    worksheet.write(4, 0, 'Total Loan Amount')
    worksheet.write(4, 1, amount, format_cur)
   
    # save the spreadsheet
    writer.save()
    return ErrorBack

def launch(pri,rte,trm,title):
    # this is used to kick off the processing. the
    # arguments are passed into main and then launched
    # from here. this provides the facility to use
    # 'from amortization_grid import launch' to execute
    # from other scripts.
    if rte == 0:
        o_put = zero_interest(pri,trm)
        print('%s payments at %s = %s' % (trm, round(o_put,2), o_put*trm))
    else:
        pct = rte/100
        o_put = i_amortize(pri,pct,trm)
        o = i_schedule(pri,pct,trm)
        q = o_schedule(o)
        x = xlwriter(q,pri,pct,trm,title)
        if x[0] == 0:
            print('your monthly payment will be %s\n' % (round(o_put,2)))
        else:
            print('Error %s: %s\n' % (x[0],x[1]))

if __name__ == "__main__":
    try:
        # assign command line parameters
        args = ap.ArgumentParser()
        args.add_argument(
                "--principle",
                nargs = "*",
                type = float,
                default = 5000.00,
                )
        args.add_argument(
                "--apr",
                nargs = "*",
                type = float,
                default = 5.5,
                )
        args.add_argument(
                "--months",
                nargs = "*",
                type = int,
                default = 36,
                )
        args.add_argument(
                "--title",
                nargs = "*",
                type = str,
                default = "new_script",
                )
        a = args.parse_args()
        pri = a.principle[0]
        rte = a.apr[0]
        trm = a.months[0]
        title = a.title[0]
        # launch it!
        launch(pri,rte,trm,title)
    except IndexError:
        print('principle, rate, and term are required.')
