import argparse
import time
from colorama import Fore, Style, init

from subdomains_opt import subdomain_enumeration
from hidden_directories_opt import hidden_dirs
from Links_extraction_opt import all_links

init(autoreset=True)


# -----------------------------
# TERMINAL THEME
# -----------------------------

PRIMARY = Fore.LIGHTMAGENTA_EX
SECONDARY = Fore.WHITE
ACCENT = Fore.LIGHTBLUE_EX
SUCCESS = Fore.LIGHTBLUE_EX
WARN = Fore.LIGHTMAGENTA_EX
ERROR = Fore.LIGHTMAGENTA_EX


def _rule(char="-", width=58, color=PRIMARY):
    return color + (char * width) + Style.RESET_ALL


def _kv(label, value):
    return f"{ACCENT}{label:<10}{Style.RESET_ALL}: {SECONDARY}{value}{Style.RESET_ALL}"

# -----------------------------
# LOGO
# -----------------------------

def logo():
    print(
        PRIMARY
        + r"""
   ██████╗ ██╗  ██╗        ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
   ██╔══██╗██║  ██║        ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
   ██████╔╝███████║        ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
   ██╔══██╗██╔══██║        ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
   ██████╔╝██║  ██║        ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
   ╚═════╝ ╚═╝  ╚═╝        ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
        """
        + Style.RESET_ALL
    )
    print(_rule("═"))
    print(_kv("Tool", "BH_Recon Framework"))
    print(_kv("Profile", "Offensive Web Recon Tool"))
    print(_kv("Author", "BH_Unknown"))
    print(_kv("Version", "1.0"))
    print(_rule("═"))


# -----------------------------
# STATUS FUNCTIONS
# -----------------------------

def info(msg):
    print(PRIMARY + "[*] " + Style.RESET_ALL + msg)

def success(msg):
    print(SUCCESS + "[+] " + Style.RESET_ALL + msg)

def error(msg):
    print(ERROR + "[-] " + Style.RESET_ALL + msg)


# -----------------------------
# SPEED METER
# -----------------------------

def speed_meter(start_time, count):
    elapsed = time.time() - start_time
    if elapsed == 0:
        return 0
    return round(count / elapsed, 2)


# -----------------------------
# PROGRESS COUNTER
# -----------------------------

def progress(current, total, start_time):

    percent = (current / total) * 100
    speed = speed_meter(start_time, current)

    print(
        f"\r{PRIMARY}[{current}/{total}] "
        f"{percent:.1f}% | Speed: {speed} req/s",
        end=""
    )


def print_runtime_profile(args, rows):
    print(_rule())
    print(WARN + "[BH_Recon] Runtime Profile" + Style.RESET_ALL)
    for label, value in rows:
        print(_kv(label, value))
    print(_rule())


# -----------------------------
# SUBDOMAIN ENUMERATION
# -----------------------------

def subdomain_enum(args):

    info("Running Subdomain Enumeration")
    print_runtime_profile(
        args,
        [
            ("Target", args.url),
            ("Threads", args.threads),
            ("Timeout", f"{args.time}s"),
            ("Wordlist", args.file),
        ],
    )

    subdomain_enumeration(args.url, args.threads, args.time, args.file)
    success("Subdomain enumeration completed")


# -----------------------------
# DIRECTORY SCAN
# -----------------------------

def vhidden_dirs(args):

    info("Running Hidden Directory Scan")
    print_runtime_profile(
        args,
        [
            ("Target", args.url),
            ("Threads", args.threads),
            ("Timeout", f"{args.time}s"),
            ("Wordlist", args.file),
        ],
    )

    hidden_dirs(args.url, args.threads, args.time, args.file)
    success("Hidden directory scan completed")


# -----------------------------
# LINKS EXTRACTION
# -----------------------------

def links_(args):

    info("Running Web Crawler")
    print_runtime_profile(
        args,
        [
            ("Target", args.url),
            ("Domain", args.domain),
            ("Timeout", f"{args.time}s"),
        ],
    )

    all_links(args.url, args.domain, args.time)
    success("Link extraction completed")


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return ivalue


# -----------------------------
# MAIN CLI
# -----------------------------

def main():

    logo()

    parser = argparse.ArgumentParser(
        prog="BH_Recon",
        description="Professional reconnaissance CLI for web surface mapping.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  BH_Recon sub   -u https://example.com -f subdomains.txt -th 40 -t 90\n"
            "  BH_Recon dirs  -u https://example.com -f dirs.txt -th 50 -t 120\n"
            "  BH_Recon links -u https://example.com -d example.com -t 120"
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    # ----------------
    # SUBDOMAIN ENUM
    # ----------------

    sub = subparsers.add_parser(
        "sub",
        help="subdomain enumeration",
        description="Enumerate subdomains for a target domain using a wordlist.",
    )

    sub.add_argument("-u", "--url", type=str, required=True)
    sub.add_argument("-th", "--threads", type=positive_int, default=25)
    sub.add_argument("-t", "--time", type=positive_int, default=80)
    sub.add_argument("-f", "--file", required=True, help="Wordlist path")

    sub.set_defaults(func=subdomain_enum)

    # ----------------
    # DIRECTORY SCAN
    # ----------------

    dirs = subparsers.add_parser(
        "dirs",
        help="hidden directory brute force",
        description="Bruteforce hidden paths and directories on target web servers.",
    )

    dirs.add_argument("-u", "--url", type=str, required=True)
    dirs.add_argument("-th", "--threads", type=positive_int, default=40)
    dirs.add_argument("-t", "--time", type=positive_int, default=120)
    dirs.add_argument("-f", "--file", required=True, help="Wordlist path")

    dirs.set_defaults(func=vhidden_dirs)

    # ----------------
    # LINKS EXTRACTION
    # ----------------

    links = subparsers.add_parser(
        "links",
        help="links extraction",
        description="Crawl and extract URLs constrained by a target domain.",
    )

    links.add_argument("-u", "--url", type=str, required=True)
    links.add_argument("-d", "--domain", type=str, required=True)
    links.add_argument("-t", "--time", type=positive_int, default=120)

    links.set_defaults(func=links_)

    # ----------------

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print(_rule())
        print(ERROR + "[!] No command selected." + Style.RESET_ALL)
        parser.print_help()


# -----------------------------

if __name__ == "__main__":
    main()