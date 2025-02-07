import datetime

print(datetime.datetime.today())
print(datetime.datetime.now())
print(datetime.datetime.utcnow())
print(datetime.datetime.fromtimestamp(time.time()))
print(datetime.datetime.utcfromtimestamp(time.time()))
print(datetime.datetime.combine(datetime.date(2019, 12, 1), datetime.time(10, 10, 10)))
print(datetime.datetime.min)
print(datetime.datetime.max)