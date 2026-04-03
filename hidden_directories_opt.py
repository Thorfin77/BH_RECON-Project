import requests
from concurrent.futures import ThreadPoolExecutor
import time
import sys
from urllib.parse import urlparse
import hashlib
from requests.adapters import HTTPAdapter


# Handle The exceptions
# Test (I have to test the request and the CDN request to know if i can add low timeout for more optimization.)
# Fix Threads - Time Management in The Command Line.
# You can choose The Threads But not required.



def hidden_dirs(url, threads, max_time, file_path):

    if max_time <= 0 or threads <=0:
        if threads <=0:
            print("Threads Error Try again!")
        if max_time <=0 :
            print("Time Error Try again!")
        sys.exit(0)
        
    def body_hash(response):
        return hashlib.sha256(response.content).hexdigest()
    
    def find_hidden_directories(url):
        Success = [200, 201, 202, 203, 205, 206, 207, 208, 226]
        confidence = 0

        if time.monotonic() - start_time > max_time:
            sys.exit(0)

        try:
            response = session.get(url, timeout=(2, 5), allow_redirects=False)
            response_hash = body_hash(response)
            # Class B (To )
            if response_hash != main_hash:
                try:
                    responseHeader = {
                                    
                                        "content_length": round(len(response.content)),
                                        "status": response.status_code,
                                        "header": response.headers
                                    }                       
                except:
                    pass
                else:

                    if CDN != "":
                        if response_hash != wildcard_hash:
                            confidence += 20
                            if CDNheader["content_length"] != responseHeader["content_length"]:
                                confidence += 20
                                if CDNheader["header"] !=  responseHeader:
                                    confidence += 20
                                if responseHeader["status"] in Success:
                                    return f"[+]Crawl {url}  {confidence+20+5}%   Status:{response.status_code}"
                                elif responseHeader["status"] not in Success and responseHeader["status"] not in range(400, 409):
                                    return f"[-]Crawl {url}  {confidence+5}%   Status:{response.status_code}"

        except:
            pass
        else:
            if response.status_code in Success:
                return f"[+]Crawl {url}  {confidence+20+5}%   Status:{response.status_code}"

            

    # Manipulate the file before launching , how to manage the thread for more efficiency and speed.
    def Low_memory_usage(url, file_path):
        # Testing..
        base_url = str(url).rstrip("/")
        try:
            with open(file_path, "r") as dirs:
                for dir in dirs:
                    yield f"{base_url}/{str(dir.strip())}"

        except FileExistsError as file_exist:
            print(file_exist)

        except FileNotFoundError as file_error:
            print(file_error)
        
        except:
            print("File Error, Try Again Homie :)")


    start = time.time()

    session = requests.Session()
    adapter = HTTPAdapter(pool_connections=200, pool_maxsize=200)
    session.mount("http://", adapter)
    session.mount("https://", adapter)


    try:
        Urlcheck = session.get(url, timeout=(2, 5), allow_redirects=False)
        
    except:
        print("[-] URL Not Found!")
        sys.exit(0)
    else:
        main_hash = body_hash(Urlcheck)
        host = urlparse(url).hostname
        try:
            CDN = requests.get(f"{url}/abcdeffgghh", timeout=(3, 5)) 
        except:
            wildcard_hash = ""
            CDN = ""
        else:
            wildcard_hash = body_hash(CDN)
            CDNheader = {
                "content_length": len(CDN.content),
                "status": CDN.status_code,
                "header": CDN.headers
                }
        
        session = requests.Session()
        # File Path with the parametres.
        start_time = time.monotonic()
        #50 Thread required
        print("Starting hidden directory...")
        with ThreadPoolExecutor(max_workers=threads) as thread:
            for result in thread.map(find_hidden_directories, Low_memory_usage(url, file_path)):
                try:
                    if result:
                        print(result)
                        if time.monotonic() - start_time > max_time:
                            sys.exit(0)
                except Exception as e:
                    print("Problem Exist %s" %e) # The MOdified File ...

                except:
                    pass


        print((time.time()-start))

#url = "https://bluemail.me/"
#threads = 60
#max_time = 120
#file_path = "wordlists\common.txt"
#hidden_dirs(url, threads, max_time, file_path)


