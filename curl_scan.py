import requests
import threading
from numpy import array_split
from json import dumps
from time import time
from multiprocessing import cpu_count
from sys import argv
from os.path import exists

start_time = time()
cpu_count = cpu_count()

argv_len = len(argv)
input_val = 0
num_results = 0
target = ""
wordlist = ""
split_wordlist =[]
results = []

def input_val():
    
    global target
    global wordlist
    iv = False

    if argv_len == 3 and exists(argv[2]):
        iv = True
        print('Available processors: ', cpu_count)
        print('Number of arguments: ',argv_len)
        print('Argument List: ', str(argv))
        target = argv[1]
        wordlist = argv[2]
        print("Target: ",target)
        print("Wordlist Path: ",wordlist,"\n")
    else:
        print("Syntax: python curl_scan.py <target_box> <wordlist_path>")

    return iv


def prep_wordlist(w):
    global wordlist
    global split_wordlist
    with open(w) as f:
        wordlist = f.readlines()
    split_wordlist = array_split(wordlist,cpu_count)
    #print('Wordlist: ',wordlist)
    #print('Split wordlist: ',split_wordlist,"\n")


def curl_run(path):
    
    global num_results
    full_target = target+path.replace("\n","")

    try:
        res = requests.get(full_target).json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if (res.get('status') is None or res.get('status') != 404):
        res = dumps(res, indent=2)
        res = "JSON Response from "+full_target+":\n"+res+"\n"
        results.append(res)
        num_results += 1

def curl_list(wl,n):
    for x in wl:
        curl_run(x)
    print("List ",n," done!\n")

def main():

    iv = input_val()
    counter = 0
    threads = []

    if iv: 
    
        prep_wordlist(wordlist)
    
        for n in range(0,cpu_count):
            process = threading.Thread(target=curl_list, args=(split_wordlist[n],n))
            process.start()
            threads.append(process)

        for p in threads:
            p.join()

        for r in results:
            print(r)

if __name__ == "__main__":
    main()

print("Total results: ", num_results)
print("\nEnd of script.")
print("Execution time: ", round(time()-start_time, 3), " seconds")
