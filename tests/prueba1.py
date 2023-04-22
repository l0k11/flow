import schedule, time


schedule.every(3).seconds.do(lambda: print("aa"))
print("aa")
while True:
    schedule.run_pending()
    time.sleep(1)