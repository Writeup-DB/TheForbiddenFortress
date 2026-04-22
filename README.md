# The Forbidden Fortress - Practice Lab

This intentionally vulnerable environment is designed to demonstrate and test the capabilities of the **403Override NG** Burp Suite extension. It simulates real-world architecture discrepancies between reverse proxies (Nginx) and back-end application servers.

Brought to you by [Writeup-DB.com](https://writeup-db.com) & WriteupDB_Academy.

<img width="1297" height="941" alt="image" src="https://github.com/user-attachments/assets/9f9c79c3-5098-4f20-8d83-ae0f7432b030" />


## Quick Start

1. **Prerequisites:** You must have Docker and Docker Compose installed.
2. **Launch the Lab:**
   Navigate to the lab directory and run:
   ```bash
   docker-compose up -d --build
   ```

3. Verify:
Open your browser and navigate to `http://localhost`. You should see the Welcome JSON message.

4. Configure Burp Suite:
Ensure Burp Suite is intercepting traffic, load the `403Override_*.py` extension, and route your browser traffic through Burp.


|Challenge|Target Endpoint|Attack Phase| Needed,Hint |
|-|-|-|-|
1|  http://localhost/api/v1/admin|    Phase 1 (Headers)|  The backend trusts local IPs.
2|  http://localhost/metrics| Phase 2 (Trailings)| The proxy is too strict with exact matches.
3|  http://localhost/api/internal/users|  Phase 3 (Normalization)|  Exploit Matrix Variable behavior (;) to confuse the proxy.
4|  http://localhost/secret-vault|    Phase 4 (Mutations)|    The WAF regex forgot about case sensitivity.
5|  http://localhost/debug/logs|  Extension Default|    Try alternative HTTP verbs.
6|  http://localhost/forbidden|   UI Config (Regex)| Configure the Ignore Regex to stop the timestamp from triggering false positives.
7|  http://localhost/api/v2/admin|    Phase 1 + Regex|    A dynamic hash changes on every 403. You need IP spoofing AND a regex filter to find the real bypass.
8|  http://localhost/system/config|   Phase 1 (Headers)| Target an open page (like /) and use X-Original-URL to rewrite the internal route.
9|  http://localhost/vault|   Phase 4 (Mutations)|   "The proxy decodes once|    but the backend decodes twice. Try double URL encoding."
|||||

## Teardown
To stop and remove the containers, run:

```bash
docker-compose down
```

## Structure
```plaintext
lab/
├── docker-compose.yml
├── README.md
├── proxy/
│   └── nginx.conf
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py
```
