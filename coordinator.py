'''
    initializes scraper instances and everything they need eg shared memory

    notes: 
        - must install:
            - chrome (.deb works)
            - xvfb (apt works)
            - tkinter (instructions upon running)

'''
import sys
import random
import time
import json
from multiprocessing import Queue, Pool, Process, Manager, TimeoutError
from seleniumbase import SB


def main():
    # defaults (TODO: replace with cmdline args)
    NUM_INSTANCES = 1

    # initialization
    manager = Manager()
    results = manager.dict()  # scraper results (shared)
    urls = Queue()  # urls to scrape (shared)

    instances = []

    # spawn multiple scraper instances
    for instance_num in range(NUM_INSTANCES):
        instance = Process(
            target=scraper_instance,
            args=(urls, results, instance_num+1)
        )
        instance.start()
        instances.append(instance)
        print(f"Spawned instance {instance_num}")

    # wait for all processes to complete
    for instance in instances:
        instance.join()
        print(f"Instance completed")


def scraper_instance(urls, results, instance_num, doer=None):
    with SB(
        uc=True,
        xvfb=False,
        headed=True,
        ad_block=True,
        page_load_strategy="eager",
        skip_js_waits=True,
        # block_images=True,
        # disable_js=True,
    ) as sb:
        sb.activate_cdp_mode("https://datadome.co/")

        # wait for earlier instances to initialize list
        sb.sleep(instance_num * 5)


if __name__ == "__main__":
    main()
