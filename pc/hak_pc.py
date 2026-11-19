"""
🛡️ Hak Secure - PC Edition v5.0
Per: A - PC singolo | E - PC piccole aziende
Anti-Phishing | Anti-Ransomware | Anti-BruteForce | Anti-DDoS locale
"""

import os
import hashlib
import json
import time
import re
import socket
import threading
from datetime import datetime
from collections import defaultdict

VERSIONE = "5.0.0"
FILE_BASELINE = "baseline.json"
FILE_LOG = "hak_secure_log.txt"
FILE_BAN = "banned_ips.json"
FILE_CONFIG = "config.json"

CONFIG_DEFAULT = {
    "max_richieste_minuto": 40,
    "max_tentativi_login": 3,
    "tempo_blocco_secondi": 3600,
    "cartella_da_proteggere": "Documenti",
    "password_corretta": "CambiaQuestaPassword123!",
    "paesi_bloccati": ["RU", "KP", "BY"]
}

def carica_config():
    if os.path.exists(FILE_CONFIG):
        try:
            with open(FILE_CONFIG, "r") as f:
                c = json.load(f)
                for k, v in CONFIG_DEFAULT.items():
                    if k not in c:
                        c[k] = v
                return c
        except:
            pass
    with open(FILE_CONFIG, "w") as f:
        json.dump(CONFIG_DEFAULT, f, indent=2)
    return CONFIG_DEFAULT.copy()

CONFIG = carica_config()
richieste_ip = defaultdict(list)
ip_bloccati = {}
tentativi_falliti = defaultdict(int)
statistiche = {"phishing": 0, "ddos": 0, "bot": 0, "ransomware": 0, "attacchi_totali": 0}

if os.path.exists(FILE_BAN):
    try:
        with open(FILE_BAN) as f:
            ip_bloccati = {k: float(v) for k, v in json.load(f).items()}
    except:
        pass

def salva_ban():
    with open(FILE_BAN, "w") as f:
        json.dump(ip_bloccati, f)

def log(msg, livello="INFO"):
    ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    testo = f"[{ora}] [{livello}] {msg}"
    print(testo)
    try:
        with open(FILE_LOG, "a", encoding="utf-8") as f:
            f.write(testo + "\n")
    except:
        pass
    if livello in ["ATTACCO", "CRITICO"]:
        statistiche["attacchi_totali"] += 1

def banner():
    print("=" * 65)
    print("  🛡️  HAK SECURE v" + VERSIONE + " - PC EDITION")
    print("  Protezione PC Singolo + PC Piccole Aziende")
    print("  Anti-Phishing | Anti-Ransomware | Anti-DDoS | Anti-Bot")
    print("=" * 65)

# ============ 1. ANTI-PHISHING ============
def controlla_phishing(url):
    url_lower = url.lower()
    punti = 0
    motivi = []
    if re.search(r"http[s]?://\d+\.\d+\.\d+\.\d+", url):
        punti += 4; motivi.append("Usa IP invece di dominio")
    if any(p in url_lower for p in ["verifica-ora", "sblocca", "urgente", "banca", "premio", "crypto-gratis", "airdrop", "conferma-ora", "account-sospeso"]):
        punti += 3; motivi.append("Parole truffa")
    if url.count("-") > 3:
        punti += 2; motivi.append("Troppi trattini")
    if url.count(".") > 4:
        punti += 2; motivi.append("Troppi punti")
    if re.search(r"(xn--|bit\.ly|tinyurl|t\.co|cutt\.ly)", url_lower):
        punti += 3; motivi.append("Link accorciato / punycode")
    if any(d in url_lower for d in [".tk", ".xyz", ".top", ".buzz", ".su", ".ru"]):
        punti += 2; motivi.append("Dominio a rischio")
    if "paypal" in url_lower and "paypal.com" not in url_lower:
        punti += 5; motivi.append("Finto PayPal")
    if "amazon" in url_lower and "amazon." not in url_lower:
        punti += 5; motivi.append("Finto Amazon")
    if "google" in url_lower and "google.com" not in url_lower:
        punti += 5; motivi.append("Finto Google")
    if punti >= 5:
        statistiche["phishing"] += 1
        log(f"🎣 PHISHING BLOCCATO! {url} | {', '.join(motivi)}", "ATTACCO")
        return False
    elif punti >= 2:
        log(f"⚠️ URL SOSPETTO ({punti} punti): {url} | {', '.join(motivi)}", "WARNING")
        return True
    else:
        log(f"✅ URL sicuro: {url}")
        return True

# ============ 2. ANTI-RANSOMWARE ============
def calcola_hash(percorso):
    try:
        with open(percorso, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def crea_baseline(cartella=None):
    cartella = cartella or CONFIG["cartella_da_proteggere"]
    if not os.path.exists(cartella):
        os.makedirs(cartella, exist_ok=True)
        log(f"Cartella {cartella} creata")
    baseline = {}
    for nome in os.listdir(cartella):
        p = os.path.join(cartella, nome)
        if os.path.isfile(p):
            h = calcola_hash(p)
            if h:
                baseline[nome] = h
    with open(FILE_BASELINE, "w") as f:
        json.dump(baseline, f, indent=2)
    log(f"📸 Baseline creata: {len(baseline)} file in {cartella}")
    return baseline

def controlla_file(cartella=None):
    cartella = cartella or CONFIG["cartella_da_proteggere"]
    if not os.path.exists(FILE_BASELINE):
        return crea_baseline(cartella)
    try:
        with open(FILE_BASELINE) as f:
            baseline = json.load(f)
    except:
        return crea_baseline(cartella)
    modificati = 0
    for nome, vecchio in baseline.items():
        p = os.path.join(cartella, nome)
        nuovo = calcola_hash(p)
        if nuovo is None:
            statistiche["ransomware"] += 1
            log(f"🔴 File CANCELLATO: {nome} - POSSIBILE RANSOMWARE!", "CRITICO")
            modificati += 1
        elif nuovo != vecchio:
            statistiche["ransomware"] += 1
            log(f"🔴 File MODIFICATO: {nome} - CONTROLLA SUBITO!", "CRITICO")
            modificati += 1
    if modificati == 0:
        log("✅ Nessun file modificato - Tutto sicuro")
    return modificati

# ============ 3. ANTI-DDOS ============
def controlla_ddos(ip, user_agent=""):
    ora = time.time()
    if ip in ip_bloccati and ora < ip_bloccati[ip]:
        return False
    richieste_ip[ip] = [t for t in richieste_ip[ip] if ora - t < 60]
    richieste_ip[ip].append(ora)
    if len(richieste_ip[ip]) > CONFIG["max_richieste_minuto"]:
        ip_bloccati[ip] = ora + CONFIG["tempo_blocco_secondi"]
        statistiche["ddos"] += 1
        salva_ban()
        log(f"🚨 DDoS BLOCCATO! IP {ip} - {len(richieste_ip[ip])} richieste/min. Ban 1 ora!", "ATTACCO")
        return False
    return True

# ============ 4. ANTI-BOT + AI ============
def controlla_bot(user_agent, ip="0.0.0.0"):
    if not user_agent or user_agent.strip() in ["", "Mozilla", "curl", "wget", "python"]:
        statistiche["bot"] += 1
        log(f"🤖 BOT BLOCCATO da {ip} - User-Agent: {user_agent}", "WARNING")
        return False
    return True

def calcola_pericolo(ip, user_agent, url=""):
    punti = 0
    if ip in ip_bloccati:
        punti += 50
    if not user_agent or len(user_agent) < 10:
        punti += 30
    if any(x in url.lower() for x in ["admin", "wp-login", ".env", "config", "sql", "wp-admin"]):
        punti += 40
    if len(richieste_ip.get(ip, [])) > 30:
        punti += 30
    if punti >= 70:
        ip_bloccati[ip] = time.time() + CONFIG["tempo_blocco_secondi"]
        salva_ban()
        log(f"🧠 AI: IP {ip} PERICOLO ALTO ({punti}/100) - BLOCCO AUTOMATICO", "CRITICO")
        return False
    elif punti >= 40:
        log(f"🧠 AI: IP {ip} SOSPETTO ({punti}/100)", "WARNING")
    return True

# ============ 5. ANTI BRUTE-FORCE ============
def controlla_login(password, ip="127.0.0.1"):
    corretta = CONFIG["password_corretta"]
    if ip in ip_bloccati and time.time() < ip_bloccati[ip]:
        log(f"⛔ Login rifiutato, IP {ip} bannato", "WARNING")
        return False
    if password == corretta:
        tentativi_falliti[ip] = 0
        log(f"✅ Login OK da {ip}")
        return True
    tentativi_falliti[ip] += 1
    log(f"⚠️ Login fallito {ip} ({tentativi_falliti[ip]}/{CONFIG['max_tentativi_login']})", "WARNING")
    if tentativi_falliti[ip] >= CONFIG["max_tentativi_login"]:
        ip_bloccati[ip] = time.time() + CONFIG["tempo_blocco_secondi"]
        salva_ban()
        log(f"🚨 BRUTE-FORCE BLOCCATO! IP {ip} bannato 1 ora", "ATTACCO")
    return False

# ============ 6. SCANSIONE PORTE ============
def scansiona_porte(host="127.0.0.1"):
    porte_comuni = [21, 22, 23, 80, 443, 3306, 3389, 8080, 9000]
    aperte = []
    log(f"🔍 Scansione porte su {host}...")
    for porta in porte_comuni:
        s = socket.socket()
        s.settimeout(0.5)
        try:
            if s.connect_ex((host, porta)) == 0:
                aperte.append(porta)
                log(f"⚠️ Porta APERTA: {porta}")
        except:
            pass
        s.close()
    if not aperte:
        log("✅ Nessuna porta pericolosa aperta")
    else:
        log(f"📋 Porte aperte: {aperte} - Chiudi quelle che non usi")
    return aperte

# ============ 7. DASHBOARD ============
def avvia_dashboard():
    def server():
        s = socket.socket()
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", 8081))
            s.listen(5)
            log("🌐 Dashboard: http://127.0.0.1:8081")
            while True:
                conn, _ = s.accept()
                try:
                    conn.recv(1024)
                except:
                    pass
                html = f"""
                <html><head><meta charset='utf-8'><meta http-equiv='refresh' content='5'>
                <style>body{{font-family:Arial;background:#0a0a0a;color:#00ff00;padding:20px}}
                .box{{background:#111;border:1px solid #00ff00;padding:15px;border-radius:10px;margin:10px 0}}
                h1{{color:#00ff00}} b{{color:white}}</style></head><body>
                <h1>🛡️ Hak Secure v{VERSIONE} - LIVE</h1>
                <div class='box'><h2>📊 Statistiche</h2>
                <p>🚨 Attacchi totali: <b>{statistiche['attacchi_totali']}</b></p>
                <p>🎣 Phishing: <b>{statistiche['phishing']}</b></p>
                <p>💥 DDoS: <b>{statistiche['ddos']}</b></p>
                <p>🤖 Bot: <b>{statistiche['bot']}</b></p>
                <p>🔴 File modificati: <b>{statistiche['ransomware']}</b></p>
                <p>⛔ IP bannati: <b>{len(ip_bloccati)}</b></p>
                </div><p>Hak Secure ti protegge - Aggiornamento ogni 5 sec</p></body></html>
                """
                try:
                    conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(html.encode())}\r\n\r\n".encode() + html.encode())
                except:
                    pass
                conn.close()
        except Exception as e:
            log(f"Dashboard non avviata: {e}")
    threading.Thread(target=server, daemon=True).start()

# ============ MAIN ============
if __name__ == "__main__":
    banner()
    log("Hak Secure avviato")
    if not os.path.exists(FILE_BASELINE):
        crea_baseline()
    avvia_dashboard()
    print("\n--- MENU HAK SECURE ---")
    print("1 = Simula DDoS (200 richieste)")
    print("2 = Testa link phishing")
    print("3 = Test Bot + AI")
    print("4 = Simula Brute-Force")
    print("5 = Controlla file / Anti-Ransomware")
    print("6 = Scansiona porte aperte")
    print("7 = Statistiche")
    print("8 = Cambia cartella protetta")
    print("Dashboard: http://127.0.0.1:8081")
    print("esci = chiudi\n")
    while True:
        try:
            scelta = input("Hak Secure > ").strip().lower()
        except KeyboardInterrupt:
            print("\nChiusura Hak Secure...")
            break
        if scelta == "esci":
            break
        elif scelta == "1":
            print("💥 Simulo DDoS...")
            for i in range(200):
                if not controlla_ddos("45.155.204.1", "bot"):
                    print(f"✅ DIFESA HA VINTO! Bloccato a richiesta {i+1}")
                    break
        elif scelta == "2":
            url = input("URL > ")
            controlla_phishing(url)
        elif scelta == "3":
            controlla_bot("", "89.1.1.1")
            calcola_pericolo("89.1.1.1", "", "http://sito.com/wp-login")
        elif scelta == "4":
            for i in range(4):
                controlla_login("sbagliata", "1.2.3.4")
        elif scelta == "5":
            controlla_file()
        elif scelta == "6":
            scansiona_porte()
        elif scelta == "7":
            print(f"\n📊 {statistiche} | IP bannati: {list(ip_bloccati.keys())}\n")
        elif scelta == "8":
            nuova = input("Nuova cartella da proteggere > ").strip()
            if nuova:
                CONFIG["cartella_da_proteggere"] = nuova
                with open(FILE_CONFIG, "w") as f:
                    json.dump(CONFIG, f, indent=2)
                crea_baseline(nuova)
                print(f"✅ Ora proteggo: {nuova}")
        else:
            if scelta:
                print("Comando non riconosciuto")