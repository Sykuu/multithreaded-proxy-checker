import threading
import queue
import requests
import os
from colorama import Fore

def checker(proxy1,proxy):
    try:
        r = requests.get('https://www.google.com', proxies=proxy1, timeout=3)
        gp.put(proxy)
        os.system(f'title Good Proxies [{gp.qsize()}/{num_proxies}]')
        print(f'{Fore.GREEN}Good Proxy  {proxy}{Fore.RESET}')
    except Exception:
        print(f'{Fore.RED}Bad Proxy   {proxy}{Fore.RESET}')

def worker():
    while True:
        proxy = q.get()
        if proxy is None:
            break
        proxy1 = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        checker(proxy1,proxy)
        q.task_done()

while True:
    q = queue.Queue()
    gp = queue.Queue()
    num_workers = 10
    num_proxies = 0
    num_threads = []
    
    try:
        with open('proxies.txt', 'r') as f:
            proxies = f.read().splitlines()
    except FileNotFoundError:
        print('ERROR! Make sure there is an existing file named "proxies.txt".')
        exit()

    for item in proxies:
        q.put(item)
    for i in range(num_workers):
        q.put(None)

    num_proxies = q.qsize() - num_workers
    os.system('cls')
    os.system(f'title Good Proxies [0/{num_proxies}]')
    print(f'''{Fore.YELLOW}======================={Fore.RESET}
Proxy Checker by Sykuu
Starting {num_workers}{Fore.RESET} Threads
{Fore.YELLOW}======================={Fore.RESET}''')

    for _ in range(num_workers):
        t = threading.Thread(target=worker)
        num_threads.append(t)
        t.start()

    for t in num_threads:
        t.join()

    print(f'''{Fore.YELLOW}==============================
{Fore.RESET}Good Proxies [{gp.qsize()}/{num_proxies}] | {round(gp.qsize() / num_proxies * 100, 2)}%
{Fore.YELLOW}=============================={Fore.RESET}''')

    with open('working_proxies.txt', 'w') as f1:
        for _ in range(gp.qsize()):
            f1.write(f'{gp.get()}\n')
    
    while True:
        recheck = input('Check good proxies again? (Y/N) >> ').lower()
        if recheck == 'y' or recheck == 'n':
            break
        else:
            print("ERROR Wrong input.")
            
    if recheck == 'y':    
        with open('working_proxies.txt', 'r') as f:
            recheck_proxies = f.read()
        with open('proxies.txt', 'w') as f:
            f.write(recheck_proxies)
        os.system('cls')   
    else:
        print("Goodbye")
        break