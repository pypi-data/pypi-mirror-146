from pymjdcal import pymjdcal
import sys, datetime

if __name__ == "__main__":
    if len(sys.argv) == 3:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
    else:
        t = datetime.datetime.now();
        year = t.year;
        month = t.month;
    pymjdcal.calmjdprint(year, month)

