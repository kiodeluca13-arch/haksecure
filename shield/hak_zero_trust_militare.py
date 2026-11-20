"""
🛡️ HAK SECURE - ZERO TRUST MILITARE v200.0
IL MASSIMO ASSOLUTO - Oltre questo c'è solo l'esercito
ZERO TRUST = Non mi fido di nessuno, nemmeno se è già dentro
Per AZIENDE + TELEFONI + PC + SERVER + WIFI
NO TRAPPOLE - Legale al 100%
"""

import time, json, os, hashlib, re, threading, sys, random, secrets
from datetime import datetime, timezone
from collections import defaultdict

VERSIONE = "200.0 ZERO TRUST MILITARE"
print(f"🛡️🔥 HAK ZERO TRUST {VERSIONE} CARICATO...")

# ============ CONFIG MILITARE ============
MAX_RICHIESTE_MINUTO = 10
MAX_RICHIESTE_ORA = 80
MAX_LOGIN_5MIN = 1  # 1 SOLO TENTATIVO. Al 2° BAN. Come le banche.
MAX_LOGIN_GIORNO = 5
MAX_EMAIL_ORA = 20
BAN_SECONDI = 86400 * 90  # BAN 90 GIORNI
SOGLIA_DENUNCIA = 1  # Al PRIMO attacco grave = denuncia subito
CARTELLA_PROVE = "prove_azienda"
CARTELLA_LOG = "log_azienda"
CARTELLA_QUARANTENA = "quarantena"
LOCK = threading.Lock()

os.makedirs(CARTELLA_PROVE, exist_ok=True)
os.makedirs(CARTELLA_LOG, exist_ok=True)
os.makedirs(CARTELLA_QUARANTENA, exist_ok=True)

# ============ STATO ============
richieste_ip = defaultdict(list)
richieste_ora = defaultdict(list)
tentativi_login = defaultdict(list)
login_giorno = defaultdict(list)
email_inviate = defaultdict(list)
ip_bannati = {}
ip_sospetti = defaultdict(int)
dispositivi_fidati = {}  # device_id -> fingerprint
sessioni = {}  # token -> info
prove = []
file_quarantena = []
stat = {"totale":0, "ddos":0, "bot":0, "brute":0, "sqli":0, "xss":0, "phishing":0, "malware":0, "ransomware":0, "furto":0, "zero_trust":0, "sessione":0, "fingerprint":0}

# ============ REGEX MILITARI ============
RE_SQL = re.compile(r"('|\"|%27|%22|%60)\s*(or|and)\s+('|\"|%27|%22|1)\s*=\s*('|\"|%27|%22|1)|union(\s+all)?\s+select|drop\s+table|delete\s+from|insert\s+into|update\s+.*set|xp_cmdshell|information_schema|sleep\s*\(|benchmark\s*\(|load_file\s*\(|into\s+(outfile|dumpfile)|waitfor\s+delay|1\s*=\s*1|0x[0-9a-f]+", re.I)
RE_XSS = re.compile(r"<script|</script|javascript:|on\w+\s*=|<iframe|<svg|<object|<embed|<form|<img[^>]+on|alert\s*\(|document\.cookie|document\.domain|eval\s*\(|innerHTML|fromCharCode|base64", re.I)
RE_PHISH = re.compile(r"verifica-ora|pacco-bloccato|premio-vinto|banca-verifica|conferma-carta|sblocca-ora|account-sospeso|verifica-identita|rimborso-attesa|fattura-scaduta|bonifico-urgente|password-scaduta|account-bloccato|aggiorna-dati", re.I)
RE_TRAVERSAL = re.compile(r"\.\./|\.\.\\|%2e%2e|%252e|/etc/passwd|/etc/shadow|/\.env|/wp-config|/config\.php|/\.git|/\.htaccess|/proc/self|/windows/system32|C:\\\\", re.I)
RE_CMD = re.compile(r";\s*(cat|ls|id|whoami|pwd|uname|wget|curl|nc|bash|sh|powershell|cmd|net\s+user|reg\s+add)\b|\|\s*cat|&&\s*cat|`[^`]+`|\$\([^)]+\)|;.*rm\s+-rf|;.*del\s+|powershell.*-enc", re.I)
RE_LFI = re.compile(r"php://|file://|expect://|data://|zip://|phar://|gopher://|dict://", re.I)
RE_RANSOM = re.compile(r"\.locked|\.encrypted|\.crypto|\.lockbit|\.conti|wannacry|lockbit|revil|conti|ryuk|blackcat|darkside|decrypt.*bitcoin|pagare.*bitcoin|bitcoin.*sbloccare|your files.*encrypted", re.I)
RE_MALWARE = re.compile(r"mimikatz|keylogger|trojan|backdoor|meterpreter|shell\.php|reverse.*shell|psexec|bloodhound|stealer|rat\.exe|cobalt.*strike|beacon\.exe|credential.*dump", re.I)
RE_BOT = re.compile(r"sqlmap|nmap|nikto|hydra|masscan|zgrab|go-http|scrapy|headless|phantomjs|python-requests|python-urllib|curl|wget|nuclei|dirbuster|gobuster|ffuf|wpscan|burp|zap", re.I)
RE_EMAIL_PERICOLO = re.compile(r"\.exe$|\.scr$|\.bat$|\.vbs$|\.ps1$|\.jar$|\.com$|\.pif$|\.msi$|\.iso$|\.img$|\.hta$", re.I)
RE_CREDIT_CARD = re.compile(r"\b(?:\d[ -]*?){13,16}\b", re.I)
RE_CODICE_FISCALE = re.compile(r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b", re.I)

IP_CATTIVI = {"45.148.10.", "185.220.101.", "91.240.118.", "103.75.190.", "193.32.162.", "45.155.204.", "185.220.102.", "194.165.16.", "103.159.196.", "45.134.26.", "194.36.178.", "91.192.103.", "193.142.146.", "45.148.11."}
PAESI_BLOCCATI = ["KP", "IR", "SY", "RU", "BY"]  # Più stretti per aziende
WIFI_PERICOLOSI = ["free wifi", "free_wifi", "wifi gratis", "wifi free", "xfinitywifi", "linksys", "default", "admin", "guest", "free internet", "open wifi"]

# ============ CARICA TUTTI GLI SCUDI VECCHI ============
scudi_extra = []
try:
    sys.path.insert(0, ".")
    from shield.hak_scudo_finale import controlla as _s1
    scudi_extra.append(("v12", _s1))
except: pass
try:
    from shield.hak_super_scudo_completo import scudo as _s2
    scudi_extra.append(("v20", _s2))
except: pass
try:
    from shield.hak_azienda_super import scudo_azienda as _s3
    scudi_extra.append(("v30", _s3))
except: pass
try:
    from shield.hak_scudo_definitivo import SCUDO_DEFINITIVO as _s4
    scudi_extra.append(("v100", _s4))
except: pass
print(f"🛡️ Scudi vecchi collegati: {len(scudi_extra)} - Ora comando io")

# ============ UTILS ============
def ora_leggibile():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def log_militare(tipo, msg, ip=""):
    riga = f"[{ora_leggibile()}] [{tipo}] IP:{ip} {msg}\n"
    try:
        with open(f"{CARTELLA_LOG}/log_{datetime.now().strftime('%Y%m%d')}.txt", "a", encoding="utf-8") as f:
            f.write(riga)
    except: pass
    print(riga.strip())

def pulizia():
    ora = time.time()
    with LOCK:
        for ip in list(ip_bannati.keys()):
            if ora > ip_bannati[ip]:
                del ip_bannati[ip]
        for d, lim in [(richieste_ip,60),(richieste_ora,3600),(tentativi_login,300),(login_giorno,86400),(email_inviate,3600)]:
            for ip in list(d.keys()):
                d[ip] = [t for t in d[ip] if ora - t < lim]
                if not d[ip]:
                    del d[ip]
        for tok in list(sessioni.keys()):
            if ora > sessioni[tok]["scade"]:
                del sessioni[tok]

def salva_prova(ip, tipo, url, user_agent, dettagli="", dispositivo=""):
    ts = time.time()
    prova = {
        "data_ora": ora_leggibile(), "iso": datetime.now(timezone.utc).isoformat(), "timestamp": ts,
        "ip": ip, "tipo": tipo, "url": (url or "")[:700], "user_agent": (user_agent or "")[:300],
        "dispositivo": dispositivo, "dettagli": dettagli,
        "hash": hashlib.sha256(f"{ip}|{tipo}|{url}|{ts}|{secrets.token_hex(4)}".encode()).hexdigest(),
        "versione": VERSIONE, "livello": "ZERO TRUST MILITARE"
    }
    with LOCK:
        prove.append(prova)
        ip_safe = re.sub(r"[^0-9a-zA-Z]", "_", ip)
        tipo_safe = re.sub(r"[^0-9a-zA-Z_]", "_", tipo)
        nome = f"{CARTELLA_PROVE}/prova_{len(prove):04d}_{tipo_safe}_{ip_safe}.json"
        try:
            with open(nome, "w", encoding="utf-8") as f:
                json.dump(prova, f, indent=2, ensure_ascii=False)
        except: pass
    return prova

def banna(ip, tipo, url, user_agent, dispositivo=""):
    with LOCK:
        ip_bannati[ip] = time.time() + BAN_SECONDI
        stat["totale"] += 1
        mappa = {"DDOS":"ddos","BOT":"bot","BRUTE_FORCE":"brute","SQL_INJECTION":"sqli","XSS":"xss","PHISHING":"phishing","MALWARE":"malware","RANSOMWARE":"ransomware","FURTO_DATI":"furto","ZERO_TRUST":"zero_trust","SESSIONE_RUBATA":"sessione","FINGERPRINT_FALSO":"fingerprint"}
        if tipo in mappa:
            stat[mappa[tipo]] += 1
    log_militare("BAN-90GG", f"⛔ BANNATO 90 GIORNI - {tipo} - {url} - {dispositivo}", ip)
    salva_prova(ip, tipo, url, user_agent, "Bloccato da Zero Trust Militare - Denuncia segreta pronta", dispositivo)
    # Denuncia AL PRIMO attacco grave
    if tipo in ["SQL_INJECTION","XSS","RANSOMWARE","FURTO_DATI","BRUTE_FORCE","MALWARE"]:
        genera_denuncia_segretissima(ip)
    return False, "⛔ Accesso negato"

# ============ ZERO TRUST 1: FINGERPRINT DISPOSITIVO ============
def calcola_fingerprint(user_agent, ip, lingua="it-IT", schermo="1920x1080", timezone="Europe/Rome"):
    """Impronta unica del dispositivo. Se cambia, è un ladro che ha rubato la sessione."""
    dati = f"{user_agent}|{lingua}|{schermo}|{timezone}"
    return hashlib.sha256(dati.encode()).hexdigest()[:16]

def verifica_dispositivo(ip, user_agent, device_id, lingua="it-IT", schermo="1920x1080", timezone="Europe/Rome"):
    fp = calcola_fingerprint(user_agent, ip, lingua, schermo, timezone)
    if device_id in dispositivi_fidati:
        fp_vecchio = dispositivi_fidati[device_id]["fingerprint"]
        if fp != fp_vecchio:
            log_militare("ZERO-TRUST", f"🚨 FINGERPRINT CAMBIATO! Device {device_id} - Era {fp_vecchio} ora {fp} - Possibile furto sessione", ip)
            return banna(ip, "FINGERPRINT_FALSO", f"device:{device_id}", user_agent, device_id)
        return True, "✅ Dispositivo riconosciuto"
    else:
        # Primo accesso: registra ma con avviso
        dispositivi_fidati[device_id] = {"fingerprint": fp, "ip": ip, "primo_accesso": ora_leggibile(), "fidato": False}
        log_militare("ZERO-TRUST", f"🆕 Nuovo dispositivo da approvare: {device_id} IP {ip} - Il capo deve approvarlo", ip)
        return False, "⚠️ NUOVO DISPOSITIVO - Il capo deve approvarlo prima. Contatta l'amministratore."

def approva_dispositivo(device_id, capo="Admin"):
    if device_id in dispositivi_fidati:
        dispositivi_fidati[device_id]["fidato"] = True
        dispositivi_fidati[device_id]["approvato_da"] = capo
        log_militare("ZERO-TRUST", f"✅ Dispositivo {device_id} approvato da {capo}")
        return True
    return False

# ============ ZERO TRUST 2: SESSIONE SICURA ============
def crea_sessione(ip, device_id, dipendente):
    token = secrets.token_hex(32)
    with LOCK:
        sessioni[token] = {"ip": ip, "device": device_id, "dipendente": dipendente, "creata": time.time(), "scade": time.time() + 1800, "ultima_azione": time.time()}  # Scade dopo 30 min
    return token

def verifica_sessione(token, ip_attuale, user_agent):
    if token not in sessioni:
        return False, "⛔ Sessione non valida - Rifai login"
    s = sessioni[token]
    if time.time() > s["scade"]:
        del sessioni[token]
        return False, "⛔ Sessione scaduta dopo 30 min - Rifai login per sicurezza"
    if s["ip"] != ip_attuale:
        # IP cambiato = sessione rubata
        log_militare("SESSIONE", f"🚨 IP sessione cambiato! Era {s['ip']} ora {ip_attuale} - Possibile furto", ip_attuale)
        del sessioni[token]
        return banna(ip_attuale, "SESSIONE_RUBATA", f"sessione rubata dipendente {s['dipendente']}", user_agent, s["device"])
    s["ultima_azione"] = time.time()
    s["scade"] = time.time() + 1800  # Rinnova 30 min
    return True, "✅ Sessione OK"

# ============ ZERO TRUST 3: QUARANTENA FILE ============
def metti_in_quarantena(ip, nome_file, contenuto=""):
    """Invece di cancellare, isola il file pericoloso. Così hai la prova."""
    nome_safe = re.sub(r"[^0-9a-zA-Z._-]", "_", nome_file)
    percorso = f"{CARTELLA_QUARANTENA}/{int(time.time())}_{nome_safe}.quarantena"
    try:
        with open(percorso, "w", encoding="utf-8", errors="ignore") as f:
            f.write(f"QUARANTENA HAK - {ora_leggibile()} - IP {ip} - File {nome_file}\n---\n{contenuto[:2000]}")
        file_quarantena.append({"file": nome_file, "percorso": percorso, "ip": ip, "data": ora_leggibile()})
        log_militare("QUARANTENA", f"🦠 File messo in quarantena: {nome_file} -> {percorso}", ip)
    except Exception as e:
        print(f"Errore quarantena: {e}")
    return percorso

# ============ ZERO TRUST 4: PROTEZIONE DATI SENSIBILI ============
def controlla_fuga_dati(ip, testo, url):
    """Se qualcuno prova a far uscire carta di credito, codice fiscale, password aziendali"""
    if RE_CREDIT_CARD.search(testo or ""):
        return banna(ip, "FURTO_DATI", f"Tentativo fuga carta di credito - {url}", "DLP", "DLP")
    if RE_CODICE_FISCALE.search(testo or ""):
        # Se è un dipendente che mette il suo CF in un form normale è ok, ma se lo manda fuori...
        if "esterno" in url.lower() or "http" in url.lower():
            return banna(ip, "FURTO_DATI", f"Tentativo fuga codice fiscale - {url}", "DLP", "DLP")
    if "password" in (testo or "").lower() and "admin" in (testo or "").lower() and len(testo or "") > 100:
        log_militare("DLP", f"⚠️ Possibile fuga password in {url}", ip)
    return True, "✅ Nessuna fuga dati"

# ============ PROTEZIONE PC / TELEFONO / EMAIL ============
def proteggi_pc_militare(ip, nome_file="", processo="", usb_collegata=False, dispositivo="PC", contenuto=""):
    if nome_file and RE_RANSOM.search(nome_file):
        metti_in_quarantena(ip, nome_file, contenuto)
        return banna(ip, "RANSOMWARE", nome_file, "PC", dispositivo)
    if nome_file and RE_MALWARE.search(nome_file):
        metti_in_quarantena(ip, nome_file, contenuto)
        return banna(ip, "MALWARE", nome_file, "PC", dispositivo)
    if processo and (RE_MALWARE.search(processo) or RE_RANSOM.search(processo)):
        return banna(ip, "MALWARE", processo, "PC", dispositivo)
    if usb_collegata and nome_file and RE_EMAIL_PERICOLO.search(nome_file):
        metti_in_quarantena(ip, nome_file, contenuto)
        return banna(ip, "MALWARE", f"USB: {nome_file}", "USB", dispositivo)
    return True, "✅ PC MILITARE OK"

def proteggi_telefono_militare(ip, sms_testo="", app_nome="", wifi_nome="", dispositivo="TEL"):
    if sms_testo and RE_PHISH.search(sms_testo):
        return banna(ip, "PHISHING", sms_testo[:120], "SMS", dispositivo)
    if app_nome and RE_MALWARE.search(app_nome):
        return banna(ip, "MALWARE", app_nome, "APP", dispositivo)
    if wifi_nome and wifi_nome.lower().strip() in WIFI_PERICOLOSI:
        return False, f"⚠️ WIFI PERICOLOSO: {wifi_nome} - NON collegarti, potrebbe rubare dati aziendali"
    return True, "✅ TELEFONO MILITARE OK"

def proteggi_email_militare(ip, mittente="", oggetto="", corpo="", allegato=""):
    testo = f"{oggetto} {corpo}".lower()
    if RE_PHISH.search(testo):
        return banna(ip, "PHISHING", oggetto, mittente, "EMAIL")
    if allegato and RE_EMAIL_PERICOLO.search(allegato):
        metti_in_quarantena(ip, allegato, corpo)
        return banna(ip, "MALWARE", allegato, mittente, "EMAIL")
    if RE_RANSOM.search(testo) or RE_MALWARE.search(testo):
        return banna(ip, "MALWARE", oggetto, mittente, "EMAIL")
    if ("ceo" in mittente.lower() or "direttore" in mittente.lower() or "amministratore" in mittente.lower()) and "urgente" in testo and "bonifico" in testo:
        return False, "⚠️ EMAIL SOSPETTA: Finge di essere il capo e chiede bonifico - NON RISPONDERE, CHIAMA IL CAPO AL TELEFONO"
    return True, "✅ EMAIL MILITARE OK"

# ============ SCUDO PRINCIPALE ZERO TRUST ============
def SCUDO_ZERO_TRUST(ip, user_agent, url, paese="IT", usa_tor=False, dispositivo="PC", dipendente="", device_id="", session_token=""):
    if not ip or not isinstance(ip, str):
        return False, "⛔ IP non valido"
    ip = ip.strip()
    url = url or "/"
    user_agent = user_agent or ""
    pulizia()
    ora = time.time()

    # Bannato?
    if ip in ip_bannati and ora < ip_bannati[ip]:
        giorni = int((ip_bannati[ip] - ora) // 86400) + 1
        return False, f"⛔ Accesso negato - Riprova tra {giorni} giorni"

    # 1. PASSA DAGLI SCUDI VECCHI
    for nome_scudo, funz in scudi_extra:
        try:
            try:
                ok, msg = funz(ip, user_agent, url)
            except TypeError:
                try:
                    ok, msg = funz(ip, user_agent, url, paese, usa_tor)
                except:
                    ok, msg = funz(ip, user_agent, url, paese, usa_tor, dispositivo, dipendente)
            if not ok:
                return False, "⛔ Accesso negato"
        except: pass

    # 2. ZERO TRUST - DISPOSITIVO
    if device_id:
        ok, msg = verifica_dispositivo(ip, user_agent, device_id)
        if not ok:
            # Se è nuovo dispositivo, non banna, chiede approvazione capo
            if "NUOVO DISPOSITIVO" in msg:
                return False, msg
            return False, "⛔ Accesso negato"

    # 3. ZERO TRUST - SESSIONE
    if session_token:
        ok, msg = verifica_sessione(session_token, ip, user_agent)
        if not ok:
            return False, msg

    # 4. FIREWALL MILITARE
    for cattivo in IP_CATTIVI:
        if ip.startswith(cattivo):
            return banna(ip, "FURTO_DATI", url, user_agent, dispositivo)
    if usa_tor:
        return banna(ip, "FURTO_DATI", url, user_agent, dispositivo)
    if paese in PAESI_BLOCCATI:
        return banna(ip, "FURTO_DATI", url, user_agent, dispositivo)

    # 5. BOT
    if RE_BOT.search(user_agent) and "mozilla" not in user_agent.lower():
        return banna(ip, "BOT", url, user_agent, dispositivo)

    # 6. HACKER WEB + FUGA DATI
    if RE_SQL.search(url):
        return banna(ip, "SQL_INJECTION", url, user_agent, dispositivo)
    if RE_XSS.search(url):
        return banna(ip, "XSS", url, user_agent, dispositivo)
    if RE_PHISH.search(url):
        return banna(ip, "PHISHING", url, user_agent, dispositivo)
    if RE_TRAVERSAL.search(url) or RE_CMD.search(url) or RE_LFI.search(url):
        return banna(ip, "FURTO_DATI", url, user_agent, dispositivo)
    if RE_RANSOM.search(url):
        return banna(ip, "RANSOMWARE", url, user_agent, dispositivo)
    ok, msg = controlla_fuga_dati(ip, url, url)
    if not ok:
        return False, msg

    # 7. ANTI-DDOS MILITARE - 10/min, 80/ora
    with LOCK:
        richieste_ip[ip] = [t for t in richieste_ip[ip] if ora - t < 60]
        richieste_ip[ip].append(ora)
        richieste_ora[ip] = [t for t in richieste_ora[ip] if ora - t < 3600]
        richieste_ora[ip].append(ora)
        c_min = len(richieste_ip[ip])
        c_ora = len(richieste_ora[ip])
    if c_min > MAX_RICHIESTE_MINUTO or c_ora > MAX_RICHIESTE_ORA:
        return banna(ip, "DDOS", url, user_agent, dispositivo)

    # 8. BRUTE FORCE MILITARE - 1 SOLO TENTATIVO
    if "/login" in url.lower() or "/admin" in url.lower() or "/vpn" in url.lower():
        with LOCK:
            tentativi_login[ip] = [t for t in tentativi_login[ip] if ora - t < 300]
            tentativi_login[ip].append(ora)
            login_giorno[ip] = [t for t in login_giorno[ip] if ora - t < 86400]
            login_giorno[ip].append(ora)
            lc = len(tentativi_login[ip])
            lg = len(login_giorno[ip])
        if lc > MAX_LOGIN_5MIN:
            log_militare("BRUTE", f"🚨 Brute Force MILITARE su {dispositivo} dipendente {dipendente} - 1 tentativo bastava", ip)
            return banna(ip, "BRUTE_FORCE", url, user_agent, dispositivo)
        if lg > MAX_LOGIN_GIORNO:
            return banna(ip, "BRUTE_FORCE", url, user_agent, dispositivo)

    log_militare("OK", f"Accesso ZERO TRUST OK - {dispositivo} {dipendente} -> {url}", ip)
    return True, f"✅ ZERO TRUST OK - Protetto livello militare"

def scudo(ip, user_agent, url, **k): return SCUDO_ZERO_TRUST(ip, user_agent, url, **k)
def controlla(ip, user_agent, url): return SCUDO_ZERO_TRUST(ip, user_agent, url)
def SCUDO_DEFINITIVO(ip, user_agent, url, **k): return SCUDO_ZERO_TRUST(ip, user_agent, url, **k)

# ============ DENUNCIA SEGRETISSIMA ============
def genera_denuncia_segretissima(ip=None):
    attacchi = prove if ip is None else [p for p in prove if p["ip"] == ip]
    if not attacchi:
        return None
    ip_t = attacchi[0]["ip"]
    id_caso = hashlib.sha256(f"{ip_t}|{len(attacchi)}|{time.time()}".encode()).hexdigest()[:10].upper()
    testo = f"""DENUNCIA ATTACCO INFORMATICO - HAK ZERO TRUST MILITARE {VERSIONE}
ID CASO: HAK-{id_caso}
Data: {ora_leggibile()}
Livello: ZERO TRUST MILITARE

IP AGGRESSORE: {ip_t}
ATTACCHI: {len(attacchi)}
"""
    for i, p in enumerate(attacchi, 1):
        testo += f"\n--- {i} ---\nData: {p['data_ora']}\nTipo: {p['tipo']}\nURL: {p['url']}\nDispositivo: {p['dispositivo']}\nHash: {p['hash']}\n"
    testo += f"\nRICHIESTA: art. 615-ter, 635-bis c.p.\nProve: {CARTELLA_PROVE}/\nDOVE: www.commissariatodips.it -> Segnala online\nOPPURE App Youpol - Segnalazione anonima\n\nNOTA: Identità segnalante RISERVATA, non comunicare all'aggressore.\n"
    nome = f"DENUNCIA_SEGRETISSIMA_HAK-{id_caso}_{dat