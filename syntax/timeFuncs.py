# https://www.tutorialspoint.com/python/python_date_time.htm

# From                        To	                        Use
# seconds since the epoch	    struct_time in UTC	        gmtime()
# seconds since the epoch	    struct_time in local time	localtime()
# struct_time in UTC	        seconds since the epoch	    calendar.timegm()
# struct_time in local time	    seconds since the epoch	    mktime()

import time

# localtime = time.asctime( time.localtime(time.time()) )
# print("Local current time : ", localtime)

print("time.time() : ", time.time())
# 1534430145.858704

# time struct를 읽을 수 있게 조립해주는 함수
print("time.asctime() : ", time.asctime())
# Local current time : Tue Jan 13 10:17:09 2009




# This is UTC
print("time.gmtime() : ", time.gmtime())
# time.gmtime() : time.struct_time(tm_year=2018, tm_mon=6, tm_mday=18, tm_hour=13, tm_min=55, tm_sec=16, tm_wday=0, tm_yday=169, tm_isdst=0)

print("time.localtime() : ", time.localtime())
# Local current time : time.struct_time(tm_year=2013, tm_mon=7, tm_mday=17, tm_hour=21, tm_min=26, tm_sec=3, tm_wday=2, tm_yday=198, tm_isdst=0)


# current gmtime
print("current gmtime : ", time.asctime(time.gmtime()))
# yesterday gmtime
oneDay = 60*60*24
print("yesterday gmtime : ", time.asctime(time.gmtime( time.time() - oneDay )))

# stringify
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime() ))
# %a - abbreviated weekday name
# %A - full weekday name
# %b - abbreviated month name
# %B - full month name
# %c - preferred date and time representation
# %C - century number (the year divided by 100, range 00 to 99)
# %d - day of the month (01 to 31)
# %D - same as %m/%d/%y
# %e - day of the month (1 to 31)
# %g - like %G, but without the century
# %G - 4-digit year corresponding to the ISO week number (see %V).
# %h - same as %b
# %H - hour, using a 24-hour clock (00 to 23)
# %I - hour, using a 12-hour clock (01 to 12)
# %j - day of the year (001 to 366)
# %m - month (01 to 12)
# %M - minute
# %n - newline character
# %p - either am or pm according to the given time value
# %r - time in a.m. and p.m. notation
# %R - time in 24 hour notation
# %S - second
# %t - tab character
# %T - current time, equal to %H:%M:%S
# %u - weekday as a number (1 to 7), Monday=1. Warning: In Sun Solaris Sunday=1
# %U - week number of the current year, starting with the first Sunday as the first day of the first week
# %V - The ISO 8601 week number of the current year (01 to 53), where week 1 is the first week that has at least 4 days in the current year, and with Monday as the first day of the week
# %W - week number of the current year, starting with the first Monday as the first day of the first week
# %w - day of the week as a decimal, Sunday=0
# %x - preferred date representation without the time
# %X - preferred time representation without the date
# %y - year without a century (range 00 to 99)
# %Y - year including the century
# %Z or %z - time zone or name or abbreviation
# %% - a literal % character


# building time struct
struct_time = time.strptime("03 Nov 00", "%d %b %y")
print ("returned tuple: ", struct_time)
# returned tuple:  time.struct_time(tm_year=2000, tm_mon=11, tm_mday=3, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=335, tm_isdst=-1)
