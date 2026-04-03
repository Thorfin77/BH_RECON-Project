from playwright.sync_api import sync_playwright
import time
from searching_file import search_file
import sys
import os

# Handle The exceptions
# Test
# Time Management in The Command Line


def Found_socials(social_media, link):
    for sc in social_media:
        if str(sc).lower() in str(link).lower():
            return True
    return False


def get_links(page, link, domain, start_time, MAX_TIME):
    
    all_links_found = []
    f = open("links.txt", "a")
    social_media = ["Facebook", "Twitter", "TikTok", "YouTube", "linkedin", "Reddit", "Pinterest", "play.google", "microsoft"]

    # ⏱ Time check
    if time.monotonic() - start_time > MAX_TIME:
        print(" Time limit reached. Exiting...")
        f.close()
        sys.exit(0)

    try:
        page.goto(link, timeout=10000)
    except:
        pass
    else:
        links = page.eval_on_selector_all("a", "element => element.map(el=>el.href)")
        for link in links:
            # ⏱ Time check inside loop
            if time.monotonic() - start_time > MAX_TIME:
                f.close()
                sys.exit(0)

            if domain in str(link):
                if not(Found_socials(social_media, link)):
                    if search_file("links.txt", link) == False:
                        if link not in all_links_found:
                            time.sleep(0.2)
                            print(f"[+] Found: {link}")
                            f.write(link+"\n")
                            all_links_found.append(link)

    f.close()
    return all_links_found


def all_links(Url, domain, MAX_TIME):
    if MAX_TIME <= 0:
        print("Time Error Try again!")
        sys.exit(0)

    print("Starting....")
    start_time = time.monotonic()  # ⏱ start timer

    try:
        First_links = []

        try:
            if "links.txt" in os.listdir():
                os.remove("links.txt")
        except FileExistsError as file:
            print(f"File Error {file}")

        with sync_playwright() as pr:
            browser = pr.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(Url)

            links = page.eval_on_selector_all("a", "element => element.map(el=>el.href)")
            First_links.extend(links)

            if len(First_links) != 0:
                for link in First_links:

                    # ⏱ Time check
                    if time.monotonic() - start_time > MAX_TIME:
                        print("⏳Time limit reached. Exiting...")
                        sys.exit(0)

                    try:
                        if (domain in str(link)):
                            new_list = get_links(page, link, domain, start_time, MAX_TIME)
                            if len(new_list) != 0:
                                for l in new_list:
                                    if l not in First_links:
                                        First_links.append(l)

                    except KeyboardInterrupt:
                        sys.exit(0)
                    except KeyError:
                        sys.exit(0)
                    except:
                        pass
            else:
                print("No Links Exists!")

        if "links.txt" in os.listdir():
            return True
        else:
            return False

    except Exception as e:
        return e