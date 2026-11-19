"""
🛡️ Hak Secure - Web Edition v5.0
Per: B - Sito web
Protegge da DDoS, Bot, SQL Injection, XSS
"""

import time
import re
from collections import defaultdict

VERSIONE = "5.0.0"
richieste_ip = defaultdict(list)
ip_bannati = {}
statistiche_web = {"ddos": 0, "bot": 0, "sqli": 0, "xss": 0}
MAX_RICHIESTE = 40
TEMPO_BAN = 3600

def controlla_richiesta(ip, user_agent, url, metodo="GET"):
    ora = time.time()
    if ip in ip_bannati and ora < ip_bannati[ip]:
        return False, "IP bannato da Hak Secure"
    if not user_agent or len(user_agent) < 10 or user_agent.lower() in ["curl", "wget", "python-requests"]:
        statistiche_web["bot"] += 1
        return False, "Bot bloccato da Hak Secure"
    richieste_ip[ip] = [t for t in richieste_ip[ip] if ora - t < 60]
    richieste_ip[ip].append(ora)
    if len(richieste_ip[ip]) > MAX_RICHIESTE:
        ip_bannati[ip] = ora + TEMPO_BAN
        statistiche_web["ddos"] += 1
        return False, "DDoS bloccato - Ban 1 ora"
    url_low = url.lower()
    pattern_sql = ["' or ", '" or ', "union select", "drop table", "delete from", "1=1", "--", "/*"]
    if any(p in url_low for p in pattern_sql):
        statistiche_web["sqli"] += 1
        return False, "SQL Injection bloccata"
    if "<script" in url_low or "javascript:" in url_low or "onerror=" in url_low:
        statistiche_web["xss"] += 1
        return False, "XSS bloccato"
    if "../" in url or "..\\" in url or "/etc/passwd" in url_low:
        return False, "Path Traversal bloccato"
    if any(x in url_low for x in ["/wp-admin", "/.env", "/config.php", "/admin.php", "/phpmyadmin"]):
        return False, "Scan admin bloccato"
    return True, "OK - Hak Secure"

def sblocca_ip(ip):
    if ip in ip_bannati:
        del ip_bannati[ip]
        return True
    return False

def get_statistiche():
    return {
        "versione": VERSIONE,
        "ddos_bloccati": statistiche_web["ddos"],
        "bot_bloccati": statistiche_web["bot"],
        "sqli_bloccate": statistiche_web["sqli"],
        "xss_bloccati": statistiche_web["xss"],
        "ip_bannati": len(ip_bannati)
    }

if __name__ == "__main__":
    print("🛡️ Hak Secure Web - Test")
    test = [
        ("1.2.3.4", "Mozilla/5.0 Chrome", "/index.html"),
        ("1.2.3.4", "curl", "/index.html"),
        ("5.6.7.8", "Mozilla/5.0", "/login.php?id=1' OR '1'='1"),
        ("5.6.7.8", "Mozilla/5.0", "/page?<script>alert(1)</script>"),
        ("5.6.7.8", "Mozilla/5.0", "/.env"),
    ]
    for ip, ua, url in test:
        ok, msg = controlla_richiesta(ip, ua, url)
        print(f"{'✅' if ok else '⛔'} {url} -> {msg}")
    print("\nStatistiche:", get_statistiche())
    print("\nSimulo DDoS...")
    for i in range(50):
        ok, msg = controlla_richiesta("9.9.9.9", "Mozilla/5.0", "/")
        if not ok:
            print(f"✅ DDoS bloccato a richiesta {i+1}: {msg}")
            break