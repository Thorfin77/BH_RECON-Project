# BH_RECON-Project
Offensive Web Recon Tool
# 🕵️‍♂️ BH_RECON Project

> Offensive Web Reconnaissance Tool for Bug Bounty Hunters 🔥

---

## 🚀 Overview

**BH_RECON** is a Python-based reconnaissance tool designed for bug bounty hunters and security researchers.

It automates key recon tasks such as:

* 🔎 Crawling internal links
* 🌐 Subdomain enumeration
* 📂 Hidden directory discovery

Built with performance, threading, and time-controlled execution in mind.

---

## ⚙️ Features

### 🔗 Link Crawling

* Extracts internal links from a target website
* Filters out social media links
* Avoids duplicates
* Saves results to `links.txt`

---

### 🌍 Subdomain Enumeration

* DNS-based discovery
* Wildcard detection
* Response hashing (SHA-256)
* Confidence scoring system
* Multi-threaded scanning

---

### 📁 Hidden Directory Discovery

* Brute-force directories using wordlists
* CDN & wildcard detection
* Response comparison (hash + headers)
* Thread-optimized for speed

---

## 🧠 Tech Stack

* Python 3   version(3.11)
* Playwright (for browser automation)
* Requests (HTTP handling)
* DNS Resolver
* ThreadPoolExecutor (parallel execution)

---

## 📦 Installation

```bash
git clone https://github.com/your-username/BH_RECON-Project.git
cd BH_RECON-Project
pip install -r requirements.txt
```

### Install Playwright browsers:

```bash
playwright install
```

---

## 🛠 Usage

### 🔗 Crawl Links

```bash
python main.py
```

---

### 🌍 Subdomain Enumeration

```python
subdomain_enumeration(URL, threads, max_time, wordlist)
```

---

### 📂 Hidden Directories

```python
hidden_dirs(url, threads, max_time, wordlist)
```

---

## ⏱ Time Management

Each module supports a **MAX_TIME** parameter:

* Prevents long scans
* Automatically stops execution when time limit is reached

---

## 🧪 Example

```python
hidden_dirs(
    url="https://example.com",
    threads=50,
    max_time=120,
    file_path="wordlists/common.txt"
)
```

---

## ⚠️ Disclaimer

This tool is created for **educational and ethical purposes only**.

* Do NOT use against systems without permission
* The author is NOT responsible for misuse

---

## 📌 Roadmap

* [ ] Add CLI interface
* [ ] JSON output support
* [ ] Proxy support
* [ ] Rate limiting control
* [ ] Better error handling

---

## 👨‍💻 Author

* GitHub: BH_UNKNOWN

---

## ⭐ Support

If you like this project:

👉 Star the repo
👉 Share with other hunters
👉 Contribute improvements

---

## 🔥 Final Note

> Recon is where bugs are born. Master recon → master bug bounty.

---
