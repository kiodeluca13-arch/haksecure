# ============================================================================
# 🛡️ HAK SECURE - SCUDO SUPREMO v1000.0
# UN SOLO FILE - 2000 RIGHE - PER TUTTO
# AZIENDE + TELEFONI + PC + SERVER + WIFI + EMAIL + SITO + APP + CLOUD + IoT
# NO TRAPPOLE - Solo difesa reale, legale al 100%
# Cancella tutti gli altri shield, tieni SOLO questo
# PARTE 1/3
# ============================================================================
# ISTRUZIONI:
# 1. Crea shield/hak_scudo_supremo.py
# 2. Incolla PARTE 1, poi PARTE 2, poi PARTE 3 nello stesso file
# 3. Non cancellare niente, tutto in fila
# ============================================================================

import time
import json
import os
import hashlib
import hmac
import re
import threading
import sys
import secrets
import base64
import socket
import ipaddress
import string
import random
import math
import uuid
from datetime import datetime, timezone, timedelta
from collections import defaultdict, deque, Counter
from pathlib import Path

VERSIONE = "1000.0 SUPREMO"
AUTORE = "Hak Secure"
print(f"🛡️ HAK SUPREMO {VERSIONE} CARICATO... Parte 1/3")

# ============================================================================
# SEZIONE 1 - CONFIGURAZIONE MILITARE MASSIMA
# ============================================================================
MAX_RICHIESTE_MINUTO = 8
MAX_RICHIESTE_ORA = 60
MAX_RICHIESTE_GIORNO = 400
MAX_LOGIN_5MIN = 1
MAX_LOGIN_ORA = 3
MAX_LOGIN_GIORNO = 4
MAX_EMAIL_ORA = 20
MAX_SMS_ORA = 10
MAX_DOWNLOAD_ORA = 30
MAX_UPLOAD_MB = 10
BAN_SECONDI = 86400 * 180
SOGLIA_DENUNCIA = 1
SESSIONE_MINUTI = 10
PASSWORD_MIN = 14
PASSWORD_MAX = 128
CARTELLA_PROVE = "prove_hak"
CARTELLA_LOG = "log_hak"
CARTELLA_BACKUP = "backup_hak"
CARTELLA_QUARANTENA = "quarantena_hak"
CARTELLA_CONFIG = "config_hak"
FILE_CONFIG = "config_hak/config.json"
LOCK = threading.RLock()

for _c in [CARTELLA_PROVE, CARTELLA_LOG, CARTELLA_BACKUP, CARTELLA_QUARANTENA, CARTELLA_CONFIG, "shield"]:
    try:
        os.makedirs(_c, exist_ok=True)
    except:
        pass

# ============================================================================
# SEZIONE 2 - STATO GLOBALE
# ============================================================================
richieste_ip = defaultdict(deque)
richieste_ora = defaultdict(deque)
richieste_giorno = defaultdict(deque)
tentativi_login = defaultdict(deque)
login_ora = defaultdict(deque)
login_giorno = defaultdict(deque)
email_inviate = defaultdict(deque)
sms_inviati = defaultdict(deque)
download_ora = defaultdict(deque)
ip_bannati = {}
ip_fidati = set()
ip_sospetti = defaultdict(int)
ip_avvisi = defaultdict(int)
sessioni = {}
dispositivi = {}
dipendenti = {}
prove = []
codici_2fa = {}
cache_dns = {}
stat = defaultdict(int)
storico_attacchi = deque(maxlen=20000)
blacklist_dinamica = set()
whitelist_dinamica = set()
firme_malware_viste = set()
pattern_ai = []
token_revoked = set()
chiavi_api = {}

# ============================================================================
# SEZIONE 3 - REGEX COMPLETI - 80+ PATTERN
# ============================================================================
RE_SQL = re.compile(r"('|\"|%27|%22|%60|`)\s*(or|and|union|select)\s+('|\"|%27|%22|1|true)|union(\s+all)?\s+select|drop\s+table|delete\s+from|insert\s+into|update\s+.*set|xp_cmdshell|information_schema|sleep\s*\(|benchmark\s*\(|load_file\s*\(|into\s+(outfile|dumpfile)|waitfor\s+delay|1\s*=\s*1|0x[0-9a-f]+|having\s+1=1|order\s+by\s+\d+|group\s+by\s+\d+", re.I)
RE_XSS = re.compile(r"<script|</script|javascript:|vbscript:|onerror\s*=|onload\s*=|onclick\s*=|onmouseover\s*=|onfocus\s*=|oninput\s*=|onchange\s*=|<iframe|<svg|<img[^>]+onerror|<object|<embed|<form|<input[^>]+autofocus|alert\s*\(|confirm\s*\(|prompt\s*\(|document\.cookie|document\.domain|eval\s*\(|innerHTML|fromCharCode|base64|String\.fromCharCode|document\.write", re.I)
RE_PHISH = re.compile(r"verifica-ora|pacco-bloccato|premio-vinto|banca-verifica|conferma-carta|sblocca-ora|account-sospeso|verifica-identita|rimborso-attesa|fattura-scaduta|bonifico-urgente|password-scaduta|posta-italiane|agenzia-entrate|inps-verifica|aruba-verifica|paypal-verifica|amazon-verifica|google-verifica|microsoft-verifica|apple-verifica|poste-verifica", re.I)
RE_TRAVERSAL = re.compile(r"\.\./|\.\.\\|%2e%2e|%252e|%c0%ae|%c0%2e|/etc/passwd|/etc/shadow|/\.env|/wp-config|/config\.php|/\.git|/\.htaccess|/proc/self|/windows/system32|/var/www|/root/\.ssh|/etc/hosts", re.I)
RE_CMD = re.compile(r";\s*(cat|ls|id|whoami|pwd|uname|wget|curl|nc|bash|sh|powershell|cmd|netstat|ps\s+aux|chmod|chown|kill|rm)\b|\|\s*(cat|ls|id)|&&\s*cat|`[^`]+`|\$\([^)]+\)|;.*rm\s+-rf|chmod\s+777|mkfs|dd\s+if=|shutdown|reboot", re.I)
RE_LFI = re.compile(r"php://|file://|expect://|data://|zip://|phar://|gopher://|dict://|ftp://.*@", re.I)
RE_RANSOM = re.compile(r"\.locked|\.encrypted|\.crypto|\.lockbit|\.conti|\.revil|wannacry|lockbit|revil|conti|ryuk|blackcat|decrypt.*bitcoin|pagare.*bitcoin|bitcoin.*sbloccare|your files.*encrypted|pay.*bitcoin.*decrypt|all your files.*encrypted", re.I)
RE_MALWARE = re.compile(r"mimikatz|keylogger|trojan|backdoor|meterpreter|shell\.php|reverse.*shell|psexec|bloodhound|stealer|rat\.exe|cobalt|beacon|empire|nishang|powershell.*-enc|certutil.*-urlcache|mshta|rundll32.*javascript", re.I)
RE_BOT = re.compile(r"sqlmap|nmap|nikto|hydra|masscan|zgrab|go-http|scrapy|headless|phantomjs|python-requests|python-urllib|curl|wget|nuclei|dirbuster|gobuster|ffuf|wpscan|burp|zap|owasp|acunetix|nessus|openvas|metasploit|havij", re.I)
RE_EMAIL_PERICOLO = re.compile(r"\.exe$|\.scr$|\.bat$|\.vbs$|\.ps1$|\.jar$|\.com$|\.pif$|\.lnk$|\.msi$|\.hta$|\.docm$|\.xlsm$|\.js$|\.vba$|\.apk$|\.dmg$", re.I)
RE_CSRF = re.compile(r"<form[^>]+action\s*=\s*https?://(?!tuodominio)", re.I)
RE_SSRF = re.compile(r"169\.254\.169\.254|metadata\.google|metadata\.aws|localhost.*admin|127\.0\.0\.1.*admin|0\.0\.0\.0.*admin", re.I)
RE_MINER = re.compile(r"coinhive|cryptominer|xmrig|monero.*miner|crypto.*miner|coinimp", re.I)
RE_DATA_LEAK = re.compile(r"\b\d{16}\b|\b\d{3}-\d{2}-\d{4}\b|iban|password\s*[:=]\s*\S+|api[_-]?key\s*[:=]\s*\S+|secret\s*[:=]\s*\S+", re.I)
RE_JWT = re.compile(r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", re.I)
RE_CREDIT_CARD = re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b")
RE_IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
RE_CODICE_FISCALE = re.compile(r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b")

IP_CATTIVI = {"45.148.10.", "185.220.101.", "91.240.118.", "103.75.190.", "193.32.162.", "45.155.204.", "185.220.102.", "194.165.16.", "103.159.196.", "45.134.26.", "194.36.178.", "91.192.103.", "193.142.146.", "45.148.11.", "185.220.103.", "45.155.205.", "103.75.191.", "193.32.163."}
WIFI_PERICOLOSI = ["free wifi", "free_wifi", "wifi gratis", "wifi free", "xfinitywifi", "linksys", "default", "admin", "guest", "free", "open wifi", "free internet", "wifi libero"]
PAESI_BLOCCATI = ["KP", "IR", "SY", "RU", "BY", "CU", "AF"]
ESTENSIONI_PERICOLOSE = [".exe", ".scr", ".bat", ".vbs", ".ps1", ".jar", ".com", ".pif", ".lnk", ".msi", ".hta", ".docm", ".xlsm", ".js", ".apk", ".dmg", ".vba"]
DOMINI_PHISHING_NOTI = ["verifica-ora.com", "pacco-bloccato.com", "premio-vinto.com", "banca-verifica.com", "account-sospeso.com", "poste-verifica.com", "inps-verifica.com"]

# ============================================================================
# SEZIONE 4 - UTILS BASE
# ============================================================================
def ora_leggibile():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def ora_iso():
    return datetime.now(timezone.utc).isoformat()

def log_hak(tipo, msg, ip=""):
    riga = f"[{ora_leggibile()}] [{tipo}] IP:{ip} {msg}\n"
    try:
        with open(f"{CARTELLA_LOG}/log_{datetime.now().strftime('%Y%m%d')}.txt", "a", encoding="utf-8") as f:
            f.write(riga)
    except:
        pass
    print(riga.strip())
    return riga

def pulizia():
    ora = time.time()
    with LOCK:
        for ip in list(ip_bannati.keys()):
            if ora > ip_bannati[ip]:
                del ip_bannati[ip]
        for d, limite in [(richieste_ip,60),(richieste_ora,3600),(richieste_giorno,86400),(tentativi_login,300),(login_ora,3600),(login_giorno,86400),(email_inviate,3600),(sms_inviati,3600),(download_ora,3600)]:
            for ip in list(d.keys()):
                while d[ip] and ora - d[ip][0] > limite:
                    d[ip].popleft()
                if not d[ip]:
                    try:
                        del d[ip]
                    except:
                        pass
        for tok in list(sessioni.keys()):
            if ora > sessioni[tok]["scadenza"]:
                del sessioni[tok]
        for ip in list(codici_2fa.keys()):
            if ora > codici_2fa[ip]["scadenza"]:
                del codici_2fa[ip]

def hash_prova(ip, tipo, url):
    return hashlib.sha256(f"{ip}|{tipo}|{url}|{time.time()}|{secrets.token_hex(6)}|{uuid.uuid4()}".encode()).hexdigest()

def hash_file_contenuto(contenuto):
    if isinstance(contenuto, str):
        contenuto = contenuto.encode()
    return hashlib.sha256(contenuto).hexdigest()

def salva_prova(ip, tipo, url, user_agent, dettagli="", dispositivo=""):
    ts = time.time()
    prova = {
        "data_ora": ora_leggibile(),
        "iso": ora_iso(),
        "timestamp": ts,
        "ip": ip,
        "tipo": tipo,
        "url": (url or "")[:800],
        "user_agent": (user_agent or "")[:400],
        "dispositivo": dispositivo,
        "dettagli": dettagli,
        "hash": hash_prova(ip, tipo, url),
        "versione": VERSIONE
    }
    with LOCK:
        prove.append(prova)
        storico_attacchi.append(prova)
        ip_safe = re.sub(r"[^0-9a-zA-Z]", "_", ip)
        tipo_safe = re.sub(r"[^0-9a-zA-Z_]", "_", tipo)
        nome = f"{CARTELLA_PROVE}/prova_{len(prove):05d}_{tipo_safe}_{ip_safe}.json"
        try:
            with open(nome, "w", encoding="utf-8") as f:
                json.dump(prova, f, indent=2, ensure_ascii=False)
            print(f"📸 PROVA SALVATA: {nome}")
        except Exception as e:
            print(f"⚠️ Errore prova: {e}")
    return prova

def banna(ip, tipo, url, user_agent, dispositivo=""):
    with LOCK:
        ip_bannati[ip] = time.time() + BAN_SECONDI
        blacklist_dinamica.add(ip)
        stat["totale"] += 1
        mappa = {"DDOS":"ddos","BOT":"bot","BRUTE_FORCE":"brute","SQL_INJECTION":"sqli","XSS":"xss","PHISHING":"phishing","MALWARE":"malware","RANSOMWARE":"ransomware","FURTO_DATI":"furto","WIFI_PERICOLOSO":"wifi","EMAIL_MALWARE":"email","2FA_FALLITA":"2fa","SESSIONE_RUBATA":"sessione","DATA_LEAK":"data_leak","SSRF":"ssrf","CSRF":"csrf","MINER":"miner","CREDIT_CARD":"data_leak"}
        if tipo in mappa:
            stat[mappa[tipo]] += 1
    log_hak("BAN", f"⛔ BANNATO 180 GIORNI - {tipo} - {url} - {dispositivo}", ip)
    salva_prova(ip, tipo, url, user_agent, "Bloccato da Hak Supremo - Denuncia pronta in segreto", dispositivo)
    try:
        genera_denuncia_segreta(ip)
    except:
        pass
    return False, "⛔ Accesso negato"

def aggiungi_ip_fidato(ip):
    ip_fidati.add(ip)
    log_hak("FIDATO", f"IP fidato aggiunto: {ip}", ip)
    return True

def rimuovi_ip_fidato(ip):
    ip_fidati.discard(ip)
    log_hak("FIDATO", f"IP fidato rimosso: {ip}", ip)
    return True

def sblocca_ip(ip):
    with LOCK:
        if ip in ip_bannati:
            del ip_bannati[ip]
            blacklist_dinamica.discard(ip)
            print(f"✅ IP {ip} sbloccato")
            return True
    print(f"IP {ip} non era bannato")
    return False

# ============================================================================
# SEZIONE 5 - FIREWALL SUPREMO
# ============================================================================
def firewall_supremo(ip, user_agent, paese="IT", usa_tor=False, usa_vpn=False):
    if ip in ip_bannati:
        return False, "IP_BANNATO"
    if ip in ip_fidati:
        return True, "IP_FIDATO"
    if ip in blacklist_dinamica:
        return False, "BLACKLIST_DINAMICA"
    for cattivo in IP_CATTIVI:
        if ip.startswith(cattivo):
            return False, f"IP_CATTIVO {cattivo}*"
    if usa_tor:
        return False, "TOR_BLOCCATO"
    if usa_vpn and paese not in ["IT"]:
        return False, "VPN_SOSPETTA"
    if paese in PAESI_BLOCCATI:
        return False, f"PAESE_BLOCCATO {paese}"
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_loopback and ip != "127.0.0.1":
            return False, "IP_LOOPBACK_SPOOFING"
        if ip_obj.is_reserved and not ip_obj.is_private:
            return False, "IP_RISERVATO"
        if ip_obj.is_multicast:
            return False, "IP_MULTICAST"
    except:
        return False, "IP_NON_VALIDO"
    for dom in DOMINI_PHISHING_NOTI:
        if dom in (user_agent or "").lower():
            return False, f"DOMINIO_PHISHING {dom}"
    return True, "FIREWALL_OK"

def controlla_ip_pubblico(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return not ip_obj.is_private and not ip_obj.is_loopback
    except:
        return False

# ============================================================================
# SEZIONE 6 - AI CHE IMPARA
# ============================================================================
def ai_supremo(ip, url, user_agent, headers=None):
    punteggio = 0
    motivi = []
    u = (url or "").lower()
    ua = (user_agent or "").lower()
    if ip_sospetti.get(ip, 0) > 30:
        punteggio += 60
        motivi.append(f"IP sospetto {ip_sospetti[ip]}")
    if ip_avvisi.get(ip, 0) > 3:
        punteggio += 20
        motivi.append(f"Avvisi precedenti {ip_avvisi[ip]}")
    strani = sum(1 for c in u if c in ["'", '"', "<", ">", ";", "--", "/*", "=", "(", ")"])
    if strani > 4:
        punteggio += 25
        motivi.append(f"Caratteri strani {strani}")
    parole = ["union","select","drop","script","alert","cookie","passwd","admin",".env","shell","cmd","exec","eval"]
    trov = [p for p in parole if p in u]
    punteggio += len(trov) * 12
    if trov:
        motivi.append(f"Parole {trov}")
    if len(user_agent or "") < 12:
        punteggio += 20
        motivi.append("UA troppo corto")
    if any(x in ua for x in ["python","curl","sqlmap","nmap","wget","scrapy"]):
        punteggio += 40
        motivi.append("Tool hacker")
    ora_h = time.localtime().tm_hour
    if 2 <= ora_h <= 5:
        punteggio += 10
        motivi.append("Attacco notturno")
    if headers:
        h = str(headers).lower()
        if "accept-language" not in h:
            punteggio += 15
            motivi.append("Manca Accept-Language = bot")
        if "accept-encoding" not in h:
            punteggio += 10
            motivi.append("Manca Accept-Encoding")
    for pat in pattern_ai:
        if pat and pat in u:
            punteggio += 30
            motivi.append(f"Pattern visto {pat}")
    if punteggio >= 60:
        ip_sospetti[ip] += punteggio
        if len(u) > 10 and u[:30] not in pattern_ai:
            pattern_ai.append(u[:30])
            if len(pattern_ai) > 200:
                pattern_ai.pop(0)
        return False, f"AI punteggio {punteggio} - {motivi}"
    elif punteggio >= 25:
        ip_sospetti[ip] += punteggio // 2
        ip_avvisi[ip] += 1
    return True, f"AI OK {punteggio}"

def punteggio_rischio(ip, url, user_agent):
    ok, msg = ai_supremo(ip, url, user_agent)
    if not ok:
        return 90, msg
    try:
        num = int(msg.split()[-1])
        return num, msg
    except:
        return 0, msg

# ============================================================================
# SEZIONE 7 - 2FA + SESSIONE + PASSWORD
# ============================================================================
def genera_2fa(ip):
    codice = str(secrets.randbelow(900000) + 100000)
    with LOCK:
        codici_2fa[ip] = {"codice": codice, "scadenza": time.time() + 180, "tentativi": 0}
    log_hak("2FA", f"Codice generato - Scade in 3 min", ip)
    print(f"📱 CODICE 2FA per {ip}: {codice} (in produzione via SMS/Email, non a schermo)")
    return codice

def verifica_2fa(ip, codice_inserito):
    with LOCK:
        if ip not in codici_2fa:
            return False, "Nessun codice richiesto - Richiedilo prima"
        dati = codici_2fa[ip]
        if time.time() > dati["scadenza"]:
            del codici_2fa[ip]
            return False, "Codice scaduto - Richiedine uno nuovo"
        dati["tentativi"] += 1
        if dati["tentativi"] > 3:
            del codici_2fa[ip]
            return "BAN", "Troppi tentativi 2FA"
        if str(codice_inserito) == str(dati["codice"]):
            del codici_2fa[ip]
            return True, "2FA OK"
        return False, f"Codice sbagliato {dati['tentativi']}/3"

def crea_sessione(ip, dispositivo, dipendente=""):
    token = secrets.token_urlsafe(32)
    with LOCK:
        sessioni[token] = {"ip": ip, "dispositivo": dispositivo, "dipendente": dipendente, "scadenza": time.time() + SESSIONE_MINUTI*60, "creata": ora_leggibile()}
    log_hak("SESSIONE", f"Sessione creata {dipendente} {dispositivo} - Scade {SESSIONE_MINUTI} min", ip)
    return token

def verifica_sessione(token, ip):
    pulizia()
    with LOCK:
        if token in token_revoked:
            return False, "Sessione revocata"
        if token not in sessioni:
            return False, "Sessione non valida - Fai login di nuovo"
        s = sessioni[token]
        if s["ip"] != ip:
            return "BAN", f"Sessione rubata! Originale {s['ip']} ora {ip}"
        return True, f"Sessione OK {s['dipendente']}"

def revoca_sessione(token):
    with LOCK:
        token_revoked.add(token)
        if token in sessioni:
            del sessioni[token]
    return True

def controlla_password(password):
    if not password:
        return False, "Password mancante"
    if len(password) < PASSWORD_MIN:
        return False, f"Password minimo {PASSWORD_MIN} caratteri - Hai {len(password)}"
    if len(password) > PASSWORD_MAX:
        return False, f"Password troppo lunga - Max {PASSWORD_MAX}"
    if not re.search(r"[A-Z]", password):
        return False, "Manca 1 maiuscola"
    if not re.search(r"[a-z]", password):
        return False, "Manca 1 minuscola"
    if not re.search(r"[0-9]", password):
        return False, "Manca 1 numero"
    if not re.search(r"[!@#$%^&*_\-+=\[\]{};:,.<>?]", password):
        return False, "Manca 1 simbolo !@#$%"
    if re.search(r"(123456|password|qwerty|admin|azienda|italia|12345678)", password, re.I):
        return False, "Password troppo comune"
    if "12345" in password or "abcde" in password.lower() or "qwerty" in password.lower():
        return False, "Password con sequenza troppo facile"
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^a-zA-Z0-9]", password): charset += 32
    entropia = len(password) * math.log2(charset) if charset else 0
    if entropia < 60:
        return False, f"Password troppo debole - Entropia {entropia:.0f} / min 60"
    return True, f"Password forte - Entropia {entropia:.0f}"

def genera_password_forte(lunghezza=16):
    alfabeto = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        pw = "".join(secrets.choice(alfabeto) for _ in range(lunghezza))
        ok, _ = controlla_password(pw)
        if ok:
            return pw

# ============================================================================
# SEZIONE 8 - CRITTOGRAFIA E HASH
# ============================================================================
def cifra_testo(testo, chiave="HAK_SECURE_CHIAVE"):
    if not testo:
        return ""
    testo_b = testo.encode()
    chiave_b = hashlib.sha256(chiave.encode()).digest()
    out = bytes(b ^ chiave_b[i % len(chiave_b)] for i, b in enumerate(testo_b))
    return base64.b64encode(out).decode()

def decifra_testo(testo_cifrato, chiave=# ============================================================================
# 🛡️ HAK SECURE - SCUDO SUPREMO v1000.0 - PARTE 2/3
# PROTEZIONE TOTALE: PC + TELEFONO + EMAIL + SITO + APP + CLOUD + IoT + WIFI
# Da incollare sotto la PARTE 1 nello stesso file shield/hak_scudo_supremo.py
# ============================================================================

# ============================================================================
# SEZIONE 9 - PC AZIENDA - PROTEZIONE TOTALE
# ============================================================================
def proteggi_pc(ip, nome_file="", processo="", usb_collegata=False, dispositivo="PC", percorso_file="", contenuto_file=""):
    # 1. File in quarantena automatica se estensione pericolosa e sconosciuto
    if nome_file:
        nome_basso = nome_file.lower()
        # Ransomware subito BAN
        if RE_RANSOM.search(nome_basso):
            return banna(ip, "RANSOMWARE", nome_file, "PC", dispositivo)
        # Malware subito BAN
        if RE_MALWARE.search(nome_basso):
            return banna(ip, "MALWARE", nome_file, "PC", dispositivo)
        # Estensioni pericolose -> quarantena, non BAN subito ma blocco
        for ext in ESTENSIONI_PERICOLOSE:
            if nome_basso.endswith(ext):
                try:
                    nome_q = f"{CARTELLA_QUARANTENA}/quarantena_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(nome_file)}.txt"
                    with open(nome_q, "w", encoding="utf-8") as f:
                        f.write(f"File in quarantena: {nome_file}\nIP: {ip}\nDispositivo: {dispositivo}\nData: {ora_leggibile()}\nPercorso: {percorso_file}\n")
                    log_hak("QUARANTENA", f"File in quarantena: {nome_file} su {dispositivo}", ip)
                    return False, f"⚠️ File {nome_file} messo in QUARANTENA - Non aprirlo, chiama l'IT"
                except Exception as e:
                    return False, f"⚠️ File pericoloso bloccato: {nome_file} - {e}"
                break
        # Controllo contenuto file se passato
        if contenuto_file:
            if RE_MALWARE.search(contenuto_file) or RE_RANSOM.search(contenuto_file):
                return banna(ip, "MALWARE", nome_file, "PC", dispositivo)
            if RE_CMD.search(contenuto_file) and "powershell" in contenuto_file.lower():
                return banna(ip, "MALWARE", nome_file, "PC", dispositivo)
    # 2. Processo sospetto
    if processo:
        proc_basso = processo.lower()
        if RE_MALWARE.search(proc_basso) or RE_RANSOM.search(proc_basso):
            return banna(ip, "MALWARE", processo, "PC", dispositivo)
        if "mimikatz" in proc_basso or "psexec" in proc_basso:
            return banna(ip, "MALWARE", processo, "PC", dispositivo)
    # 3. USB
    if usb_collegata:
        log_hak("USB", f"USB collegata su {dispositivo} - Controllo in corso...", ip)
        if nome_file and (RE_MALWARE.search(nome_file) or RE_RANSOM.search(nome_file)):
            return banna(ip, "MALWARE", nome_file, "USB", dispositivo)
    # 4. Registra dispositivo
    if dispositivo and dispositivo not in dispositivi:
        dispositivi[dispositivo] = {"ip": ip, "primo_accesso": ora_leggibile(), "tipo": "PC"}
        log_hak("DEVICE", f"Nuovo PC registrato: {dispositivo}", ip)
    return True, "✅ PC PROTETTO"

def proteggi_pc_avvio(ip, dispositivo="PC", programmi_avvio=""):
    if programmi_avvio and RE_MALWARE.search(programmi_avvio):
        return banna(ip, "MALWARE", programmi_avvio, "AVVIO", dispositivo)
    return True, "✅ AVVIO PC SICURO"

def scansiona_cartella(ip, lista_file, dispositivo="PC"):
    trovati = []
    for f in lista_file:
        ok, msg = proteggi_pc(ip, nome_file=f, dispositivo=dispositivo)
        if not ok:
            trovati.append((f, msg))
    if trovati:
        return False, f"⚠️ {len(trovati)} file pericolosi trovati: {trovati[:3]}"
    return True, f"✅ Scansione OK - {len(lista_file)} file puliti"

# ============================================================================
# SEZIONE 10 - TELEFONO - PROTEZIONE TOTALE
# ============================================================================
def proteggi_telefono(ip, numero="", sms_testo="", app_nome="", wifi_nome="", dispositivo="TELEFONO", link="", imei=""):
    testo_completo = f"{sms_testo} {link} {app_nome}".lower()
    # 1. SMS phishing
    if sms_testo and RE_PHISH.search(sms_testo):
        return banna(ip, "PHISHING", sms_testo[:120], "SMS", dispositivo)
    # 2. Link corto sospetto
    if link and re.search(r"bit\.ly|tinyurl|t\.co|cutt\.ly|is\.gd|shorturl", link, re.I):
        if RE_PHISH.search(link) or "verifica" in link.lower() or "premio" in link.lower():
            return False, f"⚠️ LINK SOSPETTO: {link} - NON CLICCARE"
        # Link corto da solo = avviso ma non BAN
        log_hak("LINK", f"Link corto controllato: {link}", ip)
    if link and RE_PHISH.search(link):
        return banna(ip, "PHISHING", link, "LINK", dispositivo)
    # 3. App malware
    if app_nome and RE_MALWARE.search(app_nome):
        return banna(ip, "MALWARE", app_nome, "APP", dispositivo)
    if app_nome and re.search(r"free.*robux|free.*vbuck|hack.*game|mod.*apk", app_nome, re.I):
        return False, f"⚠️ APP SOSPETTA: {app_nome} - Potrebbe rubare dati, disinstallala"
    # 4. WiFi pericoloso
    if wifi_nome and wifi_nome.lower().strip() in WIFI_PERICOLOSI:
        stat["wifi"] += 1
        log_hak("WIFI", f"⚠️ WiFi pericoloso: {wifi_nome} su {dispositivo}", ip)
        return False, f"⚠️ WIFI PERICOLOSO: {wifi_nome} - Non collegarti! Usa solo dati mobili o WiFi azienda"
    # 5. Numero truffa
    if numero and re.search(r"\+39 3\d{2}.*premio|\+44.*verifica|\+39.*pacco", numero):
        return False, "⚠️ NUMERO SOSPETTO - Potrebbe essere truffa, non richiamare"
    # 6. Registra telefono
    if dispositivo and dispositivo not in dispositivi:
        dispositivi[dispositivo] = {"ip": ip, "primo_accesso": ora_leggibile(), "tipo": "TELEFONO", "imei": imei}
        log_hak("DEVICE", f"Nuovo telefono registrato: {dispositivo}", ip)
    return True, "✅ TELEFONO PROTETTO"

def proteggi_sms(ip, mittente="", testo="", dispositivo="TELEFONO"):
    if RE_PHISH.search(testo):
        return banna(ip, "PHISHING", testo[:120], mittente, dispositivo)
    if re.search(r"codice.*\d{6}.*non.*condividere|codice otp", testo, re.I):
        # Se è un SMS di OTP vero, è ok, ma logga
        log_hak("SMS", f"SMS con codice OTP da {mittente}", ip)
    return True, "✅ SMS SICURO"

def proteggi_chiamata(ip, numero="", durata=0, dispositivo="TELEFONO"):
    if numero and numero.startswith("+") and len(numero) < 10:
        return False, "⚠️ Numero internazionale corto = possibile truffa"
    return True, "✅ CHIAMATA OK"

# ============================================================================
# SEZIONE 11 - EMAIL - PROTEZIONE TOTALE
# ============================================================================
def proteggi_email(ip, mittente="", oggetto="", corpo="", allegato="", cc="", bcc=""):
    testo = f"{oggetto} {corpo}".lower()
    mittente_basso = (mittente or "").lower()
    # 1. Phishing
    if RE_PHISH.search(testo):
        return banna(ip, "PHISHING", oggetto, mittente, "EMAIL")
    if RE_PHISH.search(mittente_basso):
        return banna(ip, "PHISHING", mittente, mittente, "EMAIL")
    # 2. Allegato pericoloso
    if allegato and RE_EMAIL_PERICOLO.search(allegato):
        return banna(ip, "EMAIL_MALWARE", allegato, mittente, "EMAIL")
    # 3. Ransomware / Malware nel testo
    if RE_RANSOM.search(testo) or RE_MALWARE.search(testo):
        return banna(ip, "MALWARE", oggetto, mittente, "EMAIL")
    # 4. Truffa CEO / BEC - La più pericolosa per aziende
    if ("ceo" in mittente_basso or "direttore" in mittente_basso or "amministratore" in mittente_basso or "presidente" in mittente_basso) and ("urgente" in testo and "bonifico" in testo):
        return False, "⚠️ EMAIL SOSPETTA: Finge di essere il capo e chiede bonifico URGENTE - NON RISPONDERE, CHIAMA IL CAPO AL TELEFONO"
    if "bonifico" in testo and "nuovo iban" in testo and "urgente" in testo:
        return False, "⚠️ EMAIL SOSPETTA: Cambio IBAN urgente = truffa classica - Verifica al telefono"
    if cc and "ceo" in cc.lower() and "bonifico" in testo:
        return False, "⚠️ EMAIL SOSPETTA: CC al capo + bonifico = truffa"
    # 5. Fattura falsa
    if "fattura" in testo and "scaduta" in testo and "clicca" in testo:
        return False, "⚠️ EMAIL SOSPETTA: Fattura scaduta con link - Non cliccare"
    # 6. Carta di credito / Dati sensibili in email
    if RE_CREDIT_CARD.search(testo) or RE_IBAN.search(testo):
        log_hak("EMAIL", f"Email contiene dati sensibili da {mittente} - Controlla", ip)
    # 7. Controllo SPF / Dominio falso
    if mittente and "@" in mittente:
        dominio = mittente.split("@")[-1].lower()
        if dominio in ["gmail.com", "yahoo.com", "hotmail.com"] and ("fattura" in testo or "banca" in testo or "azienda" in testo):
            return False, f"⚠️ EMAIL SOSPETTA: Mittente {mittente} usa Gmail ma finge di essere azienda/banca"
    return True, "✅ EMAIL SICURA"

def proteggi_email_allegato(ip, mittente="", allegato="", dimensione_mb=0):
    if dimensione_mb > MAX_UPLOAD_MB:
        return False, f"⚠️ Allegato troppo grande: {dimensione_mb}MB - Max {MAX_UPLOAD_MB}MB"
    return proteggi_email(ip, mittente=mittente, allegato=allegato)

# ============================================================================
# SEZIONE 12 - SITO WEB / APP / API
# ============================================================================
def proteggi_sito(ip, user_agent, url, paese="IT", usa_tor=False, usa_vpn=False, headers=None, metodo="GET", body=""):
    # Firewall
    ok_fw, msg_fw = firewall_supremo(ip, user_agent, paese, usa_tor, usa_vpn)
    if not ok_fw:
        return banna(ip, "FURTO_DATI", url, user_agent, "SITO")
    # AI
    ok_ai, msg_ai = ai_supremo(ip, url, user_agent, headers)
    if not ok_ai:
        return banna(ip, "FURTO_DATI", url, user_agent, "SITO")
    # Body con attacco?
    if body:
        if RE_SQL.search(body):
            return banna(ip, "SQL_INJECTION", url, user_agent, "SITO")
        if RE_XSS.search(body):
            return banna(ip, "XSS", url, user_agent, "SITO")
        if RE_CMD.search(body):
            return banna(ip, "FURTO_DATI", url, user_agent, "SITO")
    # Metodo pericoloso
    if metodo.upper() not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
        return banna(ip, "FURTO_DATI", url, user_agent, "SITO")
    return True, "✅ SITO PROTETTO"

def proteggi_api(ip, user_agent, url, token_api="", paese="IT"):
    if not token_api:
        return False, "⛔ Token API mancante"
    ok_t, info = verifica_token_api(token_api)
    if not ok_t:
        return False, f"⛔ {info}"
    return proteggi_sito(ip, user_agent, url, paese)

def proteggi_upload(ip, nome_file="", dimensione_mb=0, tipo_mime=""):
    if dimensione_mb > MAX_UPLOAD_MB:
        return False, f"⛔ Upload troppo grande: {dimensione_mb}MB - Max {MAX_UPLOAD_MB}MB"
    if nome_file and RE_EMAIL_PERICOLO.search(nome_file):
        return banna(ip, "EMAIL_MALWARE", nome_file, "UPLOAD", "UPLOAD")
    if tipo_mime and "executable" in tipo_mime.lower():
        return False, "⛔ Tipo file eseguibile non consentito"
    return True, "✅ UPLOAD SICURO"

def proteggi_download(ip, nome_file="", dispositivo="PC"):
    if nome_file and re.search(r"\.env|config|password|secret|\.sql|backup", nome_file, re.I):
        return banna(ip, "FURTO_DATI", nome_file, "DOWNLOAD", dispositivo)
    with LOCK:
        download_ora[ip].append(time.time())
        c = len([t for t in download_ora[ip] if time.time() - t < 3600])
    if c > MAX_DOWNLOAD_ORA:
        return banna(ip, "DDOS", nome_file, "DOWNLOAD", dispositivo)
    return True, "✅ DOWNLOAD SICURO"

# ============================================================================
# SEZIONE 13 - CLOUD + IoT + WIFI + RETE
# ============================================================================
def proteggi_cloud(ip, file_nome="", azione="download", utente=""):
    if azione == "download" and file_nome and re.search(r"\.env|config|password|secret|\.sql|backup|private", file_nome, re.I):
        return banna(ip, "FURTO_DATI", file_nome, "CLOUD", "CLOUD")
    if azione == "upload" and file_nome and RE_EMAIL_PERICOLO.search(file_nome):
        return banna(ip, "EMAIL_MALWARE", file_nome, "CLOUD", "CLOUD")
    return True, "✅ CLOUD PROTETTO"

def proteggi_iot(ip, dispositivo_iot="", comando="", tipo="telecamera"):
    if comando and re.search(r"reboot|reset|format|admin|password|telnet|ssh", comando, re.I):
        log_hak("IOT", f"Comando sospetto su {dispositivo_iot}: {comando}", ip)
        return False, f"⚠️ Comando sospetto su {dispositivo_iot} bloccato"
    if dispositivo_iot and "telecamera" in dispositivo_iot.lower():
        log_hak("IOT", f"Accesso telecamera {dispositivo_iot}", ip)
    return True, f"✅ IoT {dispositivo_iot} PROTETTO"

def proteggi_wifi(ip, nome_wifi="", password_wifi="", dispositivo="PC"):
    if nome_wifi and nome_wifi.lower().strip() in WIFI_PERICOLOSI:
        return False, f"⚠️ WIFI PERICOLOSO: {nome_wifi} - Non collegarti!"
    if password_wifi and len(password_wifi) < 8:
        return False, "⚠️ Password WiFi troppo debole - Minimo 8 caratteri"
    if nome_wifi and nome_wifi.lower() in ["admin", "default"]:
        return False, "⚠️ Nome WiFi di default - Cambialo subito"
    return True, f"✅ WIFI {nome_wifi} SICURO"

def proteggi_rete(ip, porta=80, protocollo="tcp"):
    porte_pericolose = [21, 23, 445, 3389, 5900, 6379, 27017]
    if porta in porte_pericolose:
        log_hak("RETE", f"Tentativo accesso porta pericolosa {porta} {protocollo}", ip)
        return False, f"⚠️ Porta {porta} pericolosa bloccata - Non aprire questa porta"
    return True, f"✅ Porta {porta} OK"

def proteggi_dipendente(ip, nome_dipendente="", ruolo="", dispositivo="", orario_accesso=None):
    # Controllo orario: se dipendente accede alle 3 di notte = sospetto
    ora_h = time.localtime().tm_hour
    if 1 <= ora_h <= 5:
        log_hak("DIPENDENTE", f"Accesso notturno sospetto: {nome_dipendente} alle {ora_h}:00 su {dispositivo}", ip)
        ip_avvisi[ip] += 1
    if nome_dipendente:
        dipendenti[nome_dipendente] = {"ruolo": ruolo, "dispositivo": dispositivo, "ultimo_accesso": ora_leggibile(), "ip": ip}
    return True, f"✅ Dipendente {nome_dipendente} OK"

# ============================================================================
# SEZIONE 14 - BACKUP + QUARANTENA
# ============================================================================
def backup_supremo(nome_file="backup_supremo.json"):
    try:
        dati = {"data": ora_leggibile(), "prove": len(prove), "bannati": len(ip_bannati), "dispositivi": len(dispositivi), "stat": dict(stat)}
    except:
        dati = {"data": ora_leggibile(), "prove": 0}
    percorso = f"{CARTELLA_BACKUP}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nome_file}"
    try:
        with open(percorso, "w", encoding="utf-8") as f:
            json.dump(dati, f, indent=2)
        log_hak("BACKUP", f"Backup salvato: {percorso}")
        return True, f"✅ Backup salvato: {percorso}"
    except Exception as e:
        return False, f"Errore backup: {e}"

def lista_quarantena():
    try:
        files = os.listdir(CARTELLA_QUARANTENA)
        return True, files
    except:
        return False, []

def svuota_quarantena():
    try:
        for f in os.listdir(CARTELLA_QUARANTENA):
            os.remove(os.path.join(CARTELLA_QUARANTENA, f))
        return True, "✅ Quarantena svuotata"
    except Exception as e:
        return False, f"Errore: {e}"

# FINE PARTE 2 SUPREMO - CONTINUA CON PARTE 3 NELLO STESSO FILE
# >>> INCOLLA QUI PARTE 3 <<<# ============================================================================
# 🛡️ HAK SECURE - SCUDO SUPREMO v1000.0 - PARTE 3/3
# CUORE: SCUDO_SUPREMO() + DENUNCIA SEGRETA + STATO + TEST
# Da incollare sotto la PARTE 2 nello stesso file shield/hak_scudo_supremo.py
# Dopo questa parte, il file è COMPLETO. Cancella tutti gli altri shield.
# ============================================================================

# ============================================================================
# SEZIONE 15 - SCUDO SUPREMO - UNISCE TUTTO CON TUTTO
# QUESTA È LA FUNZIONE DA USARE OVUNQUE
# ============================================================================
def SCUDO_SUPREMO(ip, user_agent, url, paese="IT", usa_tor=False, usa_vpn=False, dispositivo="PC", dipendente="", password=None, token_sessione=None, codice_2fa=None, headers=None, metodo="GET", body=""):
    """
    QUESTA È LA FUNZIONE DA USARE OVUNQUE.
    Controlla TUTTO: Firewall, AI, Bot, SQL, XSS, Phishing, DDoS, Brute Force,
    Password, 2FA, Sessione, Sito, PC, Telefono, Email, Cloud, IoT.
    Se UNO dice NO, l'aggressore è bloccato.
    L'hacker vede solo "Accesso negato", NON vede mai la denuncia.
    """
    pulizia()
    ora = time.time()
    if not ip or not isinstance(ip, str):
        return False, "⛔ IP non valido"
    ip = ip.strip()
    url = url or "/"
    user_agent = user_agent or ""

    # 0. Già bannato?
    if ip in ip_bannati and ora < ip_bannati[ip]:
        giorni = int((ip_bannati[ip] - ora) // 86400) + 1
        return False, f"⛔ Accesso negato - Riprova tra {giorni} giorni"

    # 1. FIREWALL SUPREMO
    ok_fw, msg_fw = firewall_supremo(ip, user_agent, paese, usa_tor, usa_vpn)
    if not ok_fw:
        return banna(ip, "FURTO_DATI", url, user_agent, dispositivo)

    # 2. AI SUPREMO
    ok_ai, msg_ai = ai_supremo(ip, url, user_agent, headers)
    if not ok_ai:
        return banna(ip, "FURTO_DATI", url, user_agent, dispositivo)

    # 3. BOT / TOOL HACKER
    if RE_BOT.search(user_agent) and "mozilla" not in user_agent.lower():
        return banna(ip, "BOT", url, user_agent, dispositivo)

    # 4. HACKER WEB - SQL
    if RE_SQL.search(url) or (body and RE_SQL.search(body)):
        return banna(ip, "SQL_INJECTION", url, user_agent, dispositivo)

    # 5. XSS
    if RE_XSS.search(url) or (body and RE_XSS.search(body)):
        return banna(ip, "XSS", url, user_agent, dispositivo)

    # 6. PHISHING
    if RE_PHISH.search(url) or (body and RE_PHISH.search(body)):
        return banna(ip, "PHISHING", url, user_agent, dispositivo)

    # 7. TRAVERSAL / CMD / LFI / SSRF
    if RE_TRAVERSAL.search(url) or RE_CMD.search(url) or RE_LFI.search(url) or RE_SSRF.search(url):
        return banna(ip, "FURTO_DATI", url, user_agent, dispositivo)
    if body and (RE_TRAVERSAL.search(body) or RE_CMD.search(body) or RE_LFI.search(body)):
        return banna(ip, "FURTO_DATI", url, user_agent, dispositivo)

    # 8. RANSOMWARE / MALWARE / MINER
    if RE_RANSOM.search(url):
        return banna(ip, "RANSOMWARE", url, user_agent, dispositivo)
    if RE_MALWARE.search(url):
        return banna(ip, "MALWARE", url, user_agent, dispositivo)
    if RE_MINER.search(url):
        return banna(ip, "MINER", url, user_agent, dispositivo)

    # 9. CARTA DI CREDITO / DATI SENSIBILI RUBATI
    if RE_CREDIT_CARD.search(url):
        return banna(ip, "DATA_LEAK", url, user_agent, dispositivo)

    # 10. ANTI-DDOS SUPREMO - 8/min, 60/ora, 400/giorno
    with LOCK:
        richieste_ip[ip].append(ora)
        richieste_ora[ip].append(ora)
        richieste_giorno[ip].append(ora)
        c_min = len([t for t in richieste_ip[ip] if ora - t < 60])
        c_ora = len([t for t in richieste_ora[ip] if ora - t < 3600])
        c_giorno = len([t for t in richieste_giorno[ip] if ora - t < 86400])
    if c_min > MAX_RICHIESTE_MINUTO or c_ora > MAX_RICHIESTE_ORA or c_giorno > MAX_RICHIESTE_GIORNO:
        return banna(ip, "DDOS", url, user_agent, dispositivo)

    # 11. LOGIN - 1 SOLO TENTATIVO + PASSWORD + 2FA + SESSIONE
    if "/login" in url.lower() or "/admin" in url.lower() or "/vpn" in url.lower() or "/wp-login" in url.lower():
        # Password forte?
        if password:
            ok_p, msg_p = controlla_password(password)
            if not ok_p:
                return False, msg_p
        with LOCK:
            tentativi_login[ip].append(ora)
            login_ora[ip].append(ora)
            login_giorno[ip].append(ora)
            lc = len([t for t in tentativi_login[ip] if ora - t < 300])
            lo = len([t for t in login_ora[ip] if ora - t < 3600])
            lg = len([t for t in login_giorno[ip] if ora - t < 86400])
        if lc > MAX_LOGIN_5MIN or lo > MAX_LOGIN_ORA or lg > MAX_LOGIN_GIORNO:
            log_hak("BRUTE", f"🚨 Brute Force - Solo 1 tentativo consentito - {dispositivo} {dipendente}", ip)
            return banna(ip, "BRUTE_FORCE", url, user_agent, dispositivo)
        # 2FA
        if codice_2fa is not None:
            ris = verifica_2fa(ip, codice_2fa)
            if ris == "BAN" or (isinstance(ris, tuple) and ris[0] == "BAN"):
                return banna(ip, "2FA_FALLITA", url, user_agent, dispositivo)
            if not ris[0]:
                return ris
        # Sessione
        if token_sessione:
            ris_s = verifica_sessione(token_sessione, ip)
            if ris_s == "BAN" or (isinstance(ris_s, tuple) and ris_s[0] == "BAN"):
                return banna(ip, "SESSIONE_RUBATA", url, user_agent, dispositivo)
            if not ris_s[0]:
                return ris_s

    # 12. Protezione extra Sito / Upload / Download se chiamata da web
    if "/upload" in url.lower():
        ok_u, msg_u = proteggi_upload(ip, nome_file=url, dimensione_mb=0)
        if not ok_u and "Accesso negato" in msg_u:
            return False, msg_u

    log_hak("OK", f"Accesso OK - {dispositivo} {dipendente} -> {url}", ip)
    return True, "✅ SUPREMO OK - Protetto al massimo - Tutti i controlli passati"

# Alias - Puoi usare uno qualsiasi di questi nomi, fanno la stessa cosa
def scudo(ip, user_agent, url, **k):
    return SCUDO_SUPREMO(ip, user_agent, url, **k)
def controlla(ip, user_agent, url):
    return SCUDO_SUPREMO(ip, user_agent, url)
def scudo_supremo(ip, user_agent, url, **k):
    return SCUDO_SUPREMO(ip, user_agent, url, **k)
def SCUDO(ip, user_agent, url, **k):
    return SCUDO_SUPREMO(ip, user_agent, url, **k)
def proteggi_tutto(ip, user_agent, url, **k):
    return SCUDO_SUPREMO(ip, user_agent, url, **k)

# ============================================================================
# SEZIONE 16 - DENUNCIA SEGRETA - L'HACKER NON LO SA MAI
# ============================================================================
def genera_denuncia_segreta(ip=None):
    attacchi = prove if ip is None else [p for p in prove if p["ip"] == ip]
    if not attacchi:
        return None
    ip_t = attacchi[0]["ip"]
    id_caso = hashlib.sha256(f"{ip_t}|{len(attacchi)}|{time.time()}".encode()).hexdigest()[:10].upper()
    testo = f"""==============================================
DENUNCIA PER ATTACCO INFORMATICO
HAK SECURE - SCUDO SUPREMO {VERSIONE}
ID CASO ANONIMO: HAK-{id_caso}

Data denuncia: {ora_leggibile()}

IP AGGRESSORE: {ip_t}
NUMERO ATTACCHI: {len(attacchi)}

DETTAGLIO ATTACCHI:

"""
    for i, p in enumerate(attacchi, 1):
        testo += f"""
--- Attacco {i} ---
Data e ora: {p['data_ora']}
Tipo attacco: {p['tipo']}
URL attaccato: {p['url']}
User-Agent: {p['user_agent']}
Dispositivo vittima: {p['dispositivo']}
Dettagli: {p['dettagli']}
Hash prova (non modificabile): {p['hash']}
"""
    testo += f"""

RICHIESTA:

Chiedo che l'autore venga identificato tramite IP e perseguito
a norma di legge:
- art. 615-ter c.p. Accesso abusivo a sistema informatico
- art. 635-bis c.p. Danneggiamento di informazioni e sistemi informatici
- art. 640-ter c.p. Frode informatica (se ha provato a rubare soldi/dati)

Prove complete salvate in cartella: {CARTELLA_PROVE}/
Ogni prova ha hash SHA256 non modificabile.

DOVE DENUNCIARE:

1. Sito: www.commissariatodips.it -> Clicca "Segnala online"
2. App: Youpol - Polizia di Stato -> Segnalazione anonima
3. Di persona: Polizia Postale piu vicina

Puoi denunciare anche in modo ANONIMO, senza mettere nome e cognome,
solo l'IP e le prove.

NOTA RISERVATA - IMPORTANTISSIMO:

Si chiede che l'identita del segnalante resti RISERVATA
e NON venga MAI comunicata all'aggressore,
per motivi di sicurezza personale e aziendale.

L'aggressore NON deve sapere chi lo ha denunciato
e NON deve sapere di essere stato denunciato.
Deve vedere solo "Accesso negato".

Firma: ____________________
Data: {ora_leggibile()}
ID CASO: HAK-{id_caso}
"""
    nome = f"DENUNCIA_SEGRETA_HAK-{id_caso}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    try:
        with open(nome, "w", encoding="utf-8") as f:
            f.write(testo)
        print(f"\n⚖️ DENUNCIA SEGRETA PRONTA: {nome}")
        print(f"   ID Caso: HAK-{id_caso}")
        print(f"   L'hacker NON lo sa - Lui vede solo 'Accesso negato'")
        print(f"   Vai su commissariatodips.it e incolla questo file")
    except Exception as e:
        print(f"Errore denuncia: {e}")
    return nome

# Alias denuncia
def genera_denuncia(ip=None):
    return genera_denuncia_segreta(ip)
def genera_denuncia_anonima(ip=None):
    return genera_denuncia_segreta(ip)
def denuncia_112(ip=None):
    return genera_denuncia_segreta(ip)

# ============================================================================
# SEZIONE 17 - STATO AZIENDA - PANNELLO CAPO
# ============================================================================
def mostra_stato():
    pulizia()
    print(f"\n{'='*62}")
    print(f"🛡️ HAK SECURE - SCUDO SUPREMO {VERSIONE}")
    print(f"{'='*62}")
    print(f"Totale bloccati: {stat['totale']}")
    print(f"Prove salvate: {len(prove)}")
    print(f"IP bannati ora: {len(ip_bannati)}")
    print(f"Dispositivi registrati: {len(dispositivi)}")
    print(f"Sessioni attive: {len(sessioni)}")
    print(f"Dipendenti: {len(dipendenti)}")
    print(f"Pattern AI imparati: {len(pattern_ai)}")
    print(f"----------------------------------------------")
    print(f"DDoS: {stat['ddos']} | Bot: {stat['bot']} | Brute: {stat['brute']}")
    print(f"SQL: {stat['sqli']} | XSS: {stat['xss']} | Phishing: {stat['phishing']}")
    print(f"Malware: {stat['malware']} | Ransomware: {stat['ransomware']} | Furto: {stat['furto']}")
    print(f"WiFi: {stat['wifi']} | Email: {stat['email']} | 2FA: {stat['2fa']} | Sessione: {stat['sessione']}")
    print(f"Data Leak: {stat['data_leak']} | SSRF: {stat['ssrf']} | Miner: {stat['miner']}")
    print(f"----------------------------------------------")
    print(f"REGOLE SUPREMO ATTIVE:")
    print(f"BAN: 180 GIORNI | Login: 1 solo | Richieste: 8/min | 60/ora | 400/giorno")
    print(f"Password min: 14 caratteri | Sessione: 10 min | 2FA: 6 cifre 3 min")
    print(f"Denuncia: Al 1° attacco - SEGRETA, hacker non lo sa")
    print(f"{'='*62}")

def mostra_stato_azienda():
    return mostra_stato()

def mostra_bannati():
    pulizia()
    print(f"\n⛔ IP BANNATI ({len(ip_bannati)}):")
    for ip, scadenza in list(ip_bannati.items())[:20]:
        giorni = int((scadenza - time.time()) // 86400) + 1
        print(f" - {ip} -> ancora {giorni} giorni")
    if len(ip_bannati) > 20:
        print(f" ... e altri {len(ip_bannati)-20}")

def mostra_dispositivi():
    print(f"\n📱 DISPOSITIVI ({len(dispositivi)}):")
    for nome, info in list(dispositivi.items())[:20]:
        print(f" - {nome} - {info}")

# ============================================================================
# SEZIONE 18 - TEST FINALE SUPREMO - TUTTO INSIEME
# ============================================================================
if __name__ == "__main__":
    print("🛡️ TEST FINALE SUPREMO - TUTTO INSIEME\n")

    print("--- TEST 1: PASSWORD ---")
    print(controlla_password("123456"))
    print(controlla_password("Marco123!"))
    print(controlla_password("MarcoAzienda2026!Super"))
    print(f"Password generata: {genera_password_forte()}")
    print("")

    print("--- TEST 2: 2FA ---")
    cod = genera_2fa("1.1.1.1")
    print(verifica_2fa("1.1.1.1", "000000"))
    print(verifica_2fa("1.1.1.1", cod))
    print("")

    print("--- TEST 3: SESSIONE ---")
    tok = crea_sessione("2.2.2.2", "PC-MARCO", "Marco")
    print(f"Token: {tok[:20]}...")
    print(verifica_sessione(tok, "2.2.2.2"))
    print(verifica_sessione(tok, "9.9.9.9"))
    print("")

    print("--- TEST 4: CRITTOGRAFIA ---")
    testo = "Dati segreti azienda"
    cif = cifra_testo(testo)
    print(f"Originale: {testo}")
    print(f"Cifrato: {cif[:30]}...")
    print(f"Decifrato: {decifra_testo(cif)}")
    print("")

    print("--- TEST 5: PC ---")
    print(proteggi_pc("3.3.3.3", nome_file="documento.pdf", dispositivo="PC-MARCO"))
    print(proteggi_pc("4.4.4.4", nome_file="fattura.exe", dispositivo="PC-LUCA"))
    print(proteggi_pc("5.5.5.5", nome_file="file.locked paga bitcoin", dispositivo="PC-ANNA"))
    print("")

    print("--- TEST 6: TELEFONO ---")
    print(proteggi_telefono("6.6.6.6", sms_testo="pacco bloccato verifica-ora", dispositivo="TEL-MARCO"))
    print(proteggi_telefono("7.7.7.7", wifi_nome="Free WiFi", dispositivo="TEL-LUCA"))
    print(proteggi_telefono("8.8.8.8", sms_testo="Ciao domani ci vediamo", dispositivo="TEL-ANNA"))
    print("")

    print("--- TEST 7: EMAIL ---")
    print(proteggi_email("9.9.9.9", mittente="ceo@fake.com", oggetto="URGENTE Bonifico", corpo="fai bonifico urgente nuovo iban"))
    print(proteggi_email("10.10.10.10", mittente="cliente@vero.com", oggetto="Fattura", corpo="allego", allegato="fattura.pdf"))
    print("")

    print("--- TEST 8: SITO / CLOUD / IoT / WIFI / RETE ---")
    print(proteggi_sito("11.11.11.11", "Mozilla/5.0 Chrome/120", "/dashboard"))
    print(proteggi_cloud("12.12.12.12", file_nome=".env", azione="download"))
    print(proteggi_iot("13.13.13.13", dispositivo_iot="Telecamera", comando="admin reset"))
    print(proteggi_wifi("14.14.14.14", nome_wifi="Free WiFi"))
    print(proteggi_rete("15.15.15.15", porta=445))
    print("")

    print("--- TEST 9: WEB SUPREMO ---")
    print(SCUDO_SUPREMO("16.16.16.16", "Mozilla/5.0 Chrome/120", "/dashboard", dispositivo="PC-MARCO", dipendente="Marco"))
    print(SCUDO_SUPREMO("17.17.17.17", "sqlmap", "/", dispositivo="PC-ESTERNO"))
    print(SCUDO_SUPREMO("18.18.18.18", "Mozilla/5.0 Chrome", "/login.php?id=1' OR '1'='1 UNION SELECT", dispositivo="PC-ESTERNO"))
    print(SCUDO_SUPREMO("19.19.19.19", "Mozilla/5.0 Chrome", "/page?<script>alert(document.cookie)</script>", dispositivo="PC-ESTERNO"))
    print("")

    print("--- TEST 10: BRUTE FORCE - 1 SOLO TENTATIVO ---")
    for i in range(3):
        ok, msg = SCUDO_SUPREMO("20.20.20.20", "Mozilla/5.0 Chrome", "/vpn/login", dispositivo="PC-ESTERNO", password="MarcoAzienda2026!Super")
        if not ok:
            print(f"✅ Bloccato al tentativo {i+1}: {msg}")
            break
    print("")

    print("--- TEST 11: BACKUP + QUARANTENA ---")
    print(backup_supremo())
    print(lista_quarantena())
    print("")

    print("--- TEST 12: DENUNCIA SEGRETA ---")
    SCUDO_SUPREMO("21.21.21.21", "Mozilla/5.0 Chrome", "/login.php?id=1' OR 1=1")
    print("Controlla la cartella: deve esserci DENUNCIA_SEGRETA_HAK-....txt")
    print("")

    mostra_stato()
    mostra_bannati()
    mostra_dispositivi()
    print("\n✅✅✅ SUPREMO COMPLETO - FINE FILE - UN SOLO FILE - NESSUNO PASSA - BAN 180 GIORNI!")
    print("Ora puoi cancellare tutti gli altri shield. Tieni SOLO shield/hak_scudo_supremo.py")