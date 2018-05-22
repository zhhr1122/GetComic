import schedule
import time

import Online
import threading

def job1_task():
    threading.Thread(target=Online.getComicList,args=(80,)).start()


schedule.every(1).minutes.do(job1_task)

while True:
    schedule.run_pending()
    time.sleep(1)