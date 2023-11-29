import logging
import threading
import time


def run_startables_in_parallel(startables: list, delay_between: float = 4.0):
    """
    Starts a Fork-Join of workers (classes with a start method)
    @param startables: list of classes having method start inside
    @param delay_between: sleep time (in seconds) between each start
    """
    logging.info("Starting threads in parallel")
    thread_list = []
    for worker in startables:
        th = threading.Thread(target=worker.start)
        th.start()
        thread_list.append(th)
        time.sleep(delay_between)
    logging.info("All threads had ended")
    for th in thread_list:
        th.join()
    return
