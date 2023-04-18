import schedule
import time

schedule.every(5).seconds.do(print, "hola")

while True:
    schedule.run_pending()
    time.sleep(1)