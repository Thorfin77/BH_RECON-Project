import time
import requests
import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor
from dns.resolver import resolve
from urllib.parse import urlparse

# ------------------------------------------------------------
# Handle The exceptions
# Test
# Fix Threads - Time Management in The Command Line
# -----------------------------------------------------------


def subdomain_enumeration(URL, threads, max_time, file_path):

    if max_time <= 0 or threads <=0:
        if threads <=0:
            print("Threads Error Try again!")
        if max_time <=0 :
            print("Time Error Try again!")
        sys.exit(0)


    def body_hash(response):
        return hashlib.sha256(response.content).hexdigest()

    def subdomains(URL):
        Success = [200, 201, 202, 203, 205, 206, 207, 208, 226]
        confidence = 0
        host = urlparse(URL).hostname
        try:
            Dns_search = str(resolve(host, "A", raise_on_no_answer=False).rrset)
            Real_ip_addr = Dns_search[Dns_search.find(" A ")+3:]
        except:
            return None
        else:
            confidence+=20
            if false_ipAddr != "":
                if Real_ip_addr not in [false_ipAddr1, false_ipAddr2, false_ipAddr3]:
                    confidence+=20
                    try:
                        # To test after the dns resolver and then take the action.
                        response = session.get(URL, timeout=(2, 5), allow_redirects=False)
                        response_hash = body_hash(response)
                        if wildcard_hash != "":

                            if response_hash != wildcard_hash:
                                if response_hash != main_hash:
                                    try:
                                        responseHeader = {
                                                "content_length": round(len(response.content)),
                                                "status": response.status_code,
                                                "header": response.headers
                                            }
                                    
                                    except:
                                        print("Error Exist Here?")
                                        sys.exit(0)

                                    if CDN != "":
                                        # I Have to check the --round-- if it's working or no => 
                                        if responseHeader["content_length"] != CDNheader["content_length"]:
                                            confidence+=20
                                            if responseHeader["status"] == 200:
                                                if responseHeader["status"] != CDNheader["status"]:
                                                    confidence+=10
                                                else:
                                                    confidence+=20
                                        else:
                                            if responseHeader["status"] == 200:
                                                if responseHeader["status"] != CDNheader["status"]:
                                                    confidence+=10
                                                else:
                                                    confidence+=20
                                                #elif responseHeader["status"] in [300]
                                    else:
                                        confidence+=40

                    except requests.ConnectionError:
                        return None
                    except:
                        return None
                    else:
                        if  response.status_code in Success:
                            ############# => i have to test the code here???? (length, status_code, lengthOfContent=> and the hash=> For the random subdomain, when it's diffrent i put the confidence There?)
                            # I Have to know about the Header and how can i compare the fake header with the realOne?
                            return f"[+] {URL}  {confidence}%   Status:{response.status_code}"
                        else:
                            return f"[-] {URL}  {confidence-5}%  Status:{response.status_code}"
            # This else when the The ip is empty!
            else:
                try:
                    response = session.get(URL, timeout=(2, 5), allow_redirects=False)
                except:
                    pass
                else:
                    if response.status_code in Success:
                        return f"[+] {URL}  Confidence {confidence+65}%  Status:{response.status_code}"
                    # Just here we need to see the other status_code.


    def build_urls(base_url, file_path):
        prefix = base_url[:str(base_url).find("//") + 2]
        domain = base_url[str(base_url).find("//") + 2:]
        try:
            with open(file_path) as f:
                for line in f:
                    sub = line.strip()
                    yield f"{prefix}{sub}.{domain}"
        except FileNotFoundError as file_error:
            print("File Error {}".format(file_error))
        except FileExistsError as file_exist:
            print(file_exist)
        except:
            print("File Error")

    try:
        Urlcheck = requests.get(URL, timeout=(3, 5))
        
        
    except:
        print("[-] URL Not Found!")
        sys.exit(0)
    else:
        main_hash = body_hash(Urlcheck)
        host = urlparse(URL).hostname
        session = requests.Session()

        try:
            dns_wildcard1 = str(resolve(f"myrandomm333.{host}", "A", raise_on_no_answer=False).rrset)
            dns_wildcard2 = str(resolve(f"myrandomm222.{host}", "A", raise_on_no_answer=False).rrset)
            dns_wildcard3 = str(resolve(f"myrandomm111.{host}", "A", raise_on_no_answer=False).rrset)
            
        except:
            false_ipAddr = ""

        else:
            
            false_ipAddr1 = dns_wildcard1[dns_wildcard1.find(" A ")+3:]
            false_ipAddr2 = dns_wildcard2[dns_wildcard2.find(" A ")+3:]
            false_ipAddr3 = dns_wildcard3[dns_wildcard3.find(" A ")+3:]
            
            try:
                CDN = session.get(f"https://myrandomm123.{host}", timeout=(2, 5))
            except:
                CDN = ""
                wildcard_hash = ""
            else:
                # Real Hash for Wildcard Detection!
                wildcard_hash = body_hash(CDN)
                CDNheader = {
                    "content_length": len(CDN.content),
                    "status": CDN.status_code,
                    "header": CDN.headers
                }


        base_Url = URL.rstrip("/")
        # max 30 thread
        start = time.time()
        start_time = time.monotonic()
        # Time For Crawling
        with ThreadPoolExecutor(max_workers=threads) as threadP:
            print("Starting Subdomin Enumeration!")
            
            for res in threadP.map(subdomains, build_urls(base_Url, file_path)):
                if res:
                    print(res)
                    # ⏱ Time check
                    if time.monotonic() - start_time > max_time:
                        print("⏳ Time limit reached. Exiting...")
                        sys.exit(0)
                
        print(time.time()-start)
        






        
