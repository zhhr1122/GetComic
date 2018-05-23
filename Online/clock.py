import schedule
import time

import Online
import threading

def job1_task():
    threading.Thread(target=Online.getComicList,args=(80,)).start()


schedule.every().day.at("8:00").do(job1_task)
schedule.every().day.at("12:00").do(job1_task)
schedule.every().day.at("15:00").do(job1_task)
schedule.every().day.at("18:00").do(job1_task)
schedule.every().day.at("23:00").do(job1_task)

while True:
    schedule.run_pending()
    time.sleep(1)