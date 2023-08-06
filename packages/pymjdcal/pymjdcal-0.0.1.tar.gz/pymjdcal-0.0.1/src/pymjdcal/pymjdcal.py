import calendar, julian
from datetime import datetime as dt

def calprint(year, month):
    print(calendar.month(year, month))

def calmjdprint(year, month):
    MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")
    strout  = "                           %s %4d                           \n" % (MONTHS[month-1], year)
    strout += "    Mo       Tu       We       Th       Fr       Sa       Su    \n"
    cal = calendar.Calendar()
    today = dt.now()
    if today.year == year and today.month == month:
        today_thismonth = True
    else:
        today_thismonth = False
    for i, e in enumerate(cal.itermonthdays(year, month)):
        if e > 0:
            mjd = julian.to_jd(dt(year,month,e), fmt='mjd')
            strout += "|"
            if today_thismonth and today.day == e:
                strout += "\033[48;2;255;0;0m"
            strout += "%2d %5d" % (e, mjd)
            if today_thismonth and today.day == e:
                strout += "\033[0m"
        else:
            strout += "|        "
        if (i+1)%7 == 0:
            strout += "|\n"

    print(strout, end='')
