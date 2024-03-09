import datetime
import ephem
from datetime import timedelta

def get_phase_on_day(year: int, month: int, day: int):
    date = ephem.Date(datetime.date(year,month,day))
    nnm = ephem.next_new_moon(date)
    pnm = ephem.previous_new_moon(date)
    lunation = (date-pnm)/(nnm-pnm)
    return lunation

def get_lunar_day(year: int, month: int, day: int):
    lunation = get_phase_on_day(year, month, day)
    lunar_month = 29.53
    lunar_day = lunation * lunar_month
    return round(lunar_day)

def moon_phase(month, day, year):
    ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    description = ["new (totally dark)",
      "waxing crescent (increasing to full)",
      "in its first quarter (increasing to full)",
      "waxing gibbous (increasing to full)",
      "full (full light)",
      "waning gibbous (decreasing from full)",
      "in its last quarter (decreasing from full)",
      "waning crescent (decreasing from full)"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if day == 31:
        day = 1
    days_into_phase = ((ages[(year + 1) % 19] +
                        ((day + offsets[month-1]) % 30) +
                        (year < 1900)) % 30)
    index = int((days_into_phase + 2) * 16/59.0)
    if index > 7:
        index = 7
    status = description[index]
    return status

def print_moon_phases(year, month):
    start_date = datetime.date(year, month, 1)
    end_date = start_date + timedelta(days=1)
    
    while start_date.month == month:
        print(f"Date: {start_date}, Day of Week: {start_date.strftime('%A')}, PyEphem: {get_phase_on_day(start_date.year, start_date.month, start_date.day)}, Custom: {moon_phase(start_date.month, start_date.day, start_date.year)}")
        start_date += timedelta(days=1)
        end_date += timedelta(days=1)
