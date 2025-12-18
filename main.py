#importing necessary modules
import requests
import logging
import csv
from concurrent.futures import ThreadPoolExecutor
import os

#Building absolute file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR,"URL.txt")
RESULT_FILE = os.path.join(BASE_DIR,"result.csv")
LOG_FILE = os.path.join(BASE_DIR,"api_calls.log")

#logging setup
logger = logging.getLogger("url_checker")
logger.setLevel(logging.DEBUG)
frmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(frmt)
logger.addHandler(ch)

fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
fh.setFormatter(frmt)
logger.addHandler(fh)

def check_url(url:str) -> tuple :
    '''make api calls and logs the result to the file'''
    try:
        resp = requests.get(url,timeout=7)
        logger.info(f"api calling successful to {url} ,status code: {resp.status_code}")
        return url, resp.status_code, "UP"
    except Exception as e:
        logger.error(f"Some error occured while calling {url} {e}")
        return url, str(e), "DOWN"

def load_urls(path:str =PATH) ->list[str]:
    '''reads urls from the file and returns them as a list'''
    with open(path,"r") as f:
        url_lst = []
        for line in f:
            url = line.strip()
            if url:
                url_lst.append(url)
    return url_lst

def save_result(result:list[tuple]) -> None:
    '''saves the result in a csv file'''
    with open(RESULT_FILE,"a",newline="") as f:
        w = csv.writer(f)
        w.writerow(["URL","STATUS_CODE","STATE"])
        w.writerows(result)

def main():
    url_lst = load_urls(path=PATH) 
    print("urls loaded:",url_lst)
    result=[]
    with ThreadPoolExecutor(max_workers=8) as workers:
        for res in workers.map(check_url,url_lst):
            result.append(res)
    save_result(result=result)

if __name__ == "__main__":
    main()


    