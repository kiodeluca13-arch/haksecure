"""
🛡️⚖️ Hak Secure - SCUDO CHE DENUNCIA E RESPINGE v11.0
Blocca l'aggressore, salva le prove, prepara la denuncia per Polizia Postale
NON attacca indietro - denuncia e basta. Questo è legale.
"""

import time
import json
import os
import hashlib
from datetime import datetime
from collections import defaultdict

VERSIONE = "11.0 DENUNCIA E RESPINGE"

# --- MEMORIA ---
ip_bannati = {}
prove = []  # Tutte le prove salvate
richieste_ip = defaultdict(list)
tentativi_login = defaultdict(list)

CARTELLA_PROVE = "prove_hak_secure"
os.makedirs(CARTELLA_PROVE, exist_ok=True)

def ora_leggibile():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def salva_prova(ip, tipo_attacco, url, user_agent, dettagli=""):
    """Salva la prova dell'attacco - serve per la denuncia"""
    prova = {
        "data_ora": ora_leggibile(),
        "timestamp": time.time(),
        "ip_aggressore": ip,
        "tipo_attacco": tipo_attacco,
        "url_attaccato": url,
        "user_agent": user_agent,
        "dettagli": dettagli,
        "hash_prova": hashlib.sha256(f"{ip}{url}{time.time()}".encode()).hexdigest()[:16]
    }
    prove.append(prova)
    # Salva su file subito, così non si perde
    nome_file = f"{CARTELLA_PROVE}/prova_{len(prove):03d}_{tipo_attacco}_{ip.replace('.','_')}.json"
    with open(nome_file, "w", encoding="utf-8") as f:
        json.dump(prova, f, indent=2, ensure_ascii=False)
    print(f"📸 PROVA SALVATA: {nome_file}")
    return prova

def respingi_e_denuncia(ip, tipo_attacco, url, user_agent):
    """1. RESPINGE - banna subito 2. DENUNCIA - salva prova"""
    # 1. RESPINGE
    ip_bannati[ip] = time.time() + 86400  # Ban 24h
    print(f"\n⛔🛡️ AGGRESSORE RESPINTO!")
    print(f"   IP: {ip}")
    print(f"   Attacco: {tipo_attacco}")
    print(f"   Ban: 24 ore")
    
    # 2. SALVA PROVA PER DENUNCIA
    prova = salva_prova(ip, tipo_attacco, url, user_agent, "Bloccato e bannato da Hak Secure")
    
    # 3. SE SONO 3+ ATTACCHI DALLO STESSO IP -> DENUNCIA AUTOMATICA
    attacchi_ip = [p for p in prove if p["ip_aggressore"] == ip]
    if len(attacchi_ip) >= 3:
        print(f"🚨 ATTENZIONE: {ip} ha attaccato {len(attacchi_ip)} volte!")
        print(f"   -> Genero DENUNCIA AUTOMATICA")
        genera_denuncia(ip)
    
    return False, f"⛔ RESPINTO + DENUNCIATO - {tipo_attacco}"

def controlla_e_respingi(ip, user_agent, url):
    ora = time.time()
    
    # Se già bannato
    if ip in ip_bannati and ora < ip_bannati[ip]:
        return False, "⛔ SEI BANNATO - Sei stato denunciato"

    u = url.lower()
    ua = (user_agent or "").lower()

    # BOT / HACKER TOOL
    if any(b in ua for b in ["sqlmap","nmap","nikto","hydra","curl","wget"]):
        return respingi_e_denuncia(ip, "BOT_HACKER_TOOL", url, user_agent)

    # SQL INJECTION
    if any(p in u for p in ["' or ", "union select", "drop table", "1=1"]):
        return respingi_e_denuncia(ip, "SQL_INJECTION", url, user_agent)

    # XSS
    if "<script" in u or "javascript:" in u or "onerror=" in u:
        return respingi_e_denuncia(ip, "XSS", url, user_agent)

    # PHISHING
    if any(p in u for p in ["verifica-ora","pacco-bloccato","premio-vinto"]):
        return respingi_e_denuncia(ip, "PHISHING", url, user_agent)

    # FILE SENSIBILI
    if "/.env" in u or "/etc/passwd" in u or "/wp-config" in u:
        return respingi_e_denuncia(ip, "TENTATIVO_FURTO_DATI", url, user_agent)

    # DDOS
    richieste_ip[ip] = [t for t in richieste_ip[ip] if ora - t < 60]
    richieste_ip[ip].append(ora)
    if len(richieste_ip[ip]) > 30:
        return respingi_e_denuncia(ip, "DDOS", url, user_agent)

    # BRUTE FORCE
    if "/login" in u or "/admin" in u:
        tentativi_login[ip] = [t for t in tentativi_login[ip] if ora - t < 300]
        tentativi_login[ip].append(ora)
        if len(tentativi_login[ip]) > 5:
            return respingi_e_denuncia(ip, "BRUTE_FORCE_LOGIN", url, user_agent)

    return True, "✅ OK - Protetto"

def genera_denuncia(ip=None):
    """Genera il testo della denuncia pronta per Polizia Postale"""
    attacchi = prove if ip is None else [p for p in prove if p["ip_aggressore"] == ip]
    if not attacchi:
        print("Nessuna prova da denunciare")
        return None

    testo = f"""

DENUNCIA PER ATTACCO INFORMATICO
Generata da Hak Secure - Scudo v11.0
Data: {ora_leggibile()}


Io sottoscritto, vittima di attacco informatico, denuncio:

IP AGGRESSORE: {attacchi[0]['ip_aggressore']}
NUMERO ATTACCHI REGISTRATI: {len(attacchi)}

ELENCO ATTACCHI CON PROVE:
"""
    for i, p in enumerate(attacchi, 1):
        testo += f"""
--- Attacco {i} ---
Data e Ora: {p['data_ora']}
Tipo: {p['tipo_attacco']}
URL Attaccato: {p['url_attaccato']}
User Agent: {p['user_agent']}
Hash Prova (non modificabile): {p['hash_prova']}
"""

    testo += f"""

RICHIESTA:
Chiedo che venga identificato l'autore tramite IP
e perseguito a norma di legge (art. 615-ter c.p. - Accesso abusivo
a sistema informatico, art. 635-bis - Danneggiamento informatico)

Prove allegate in cartella: {CARTELLA_PROVE}/
Totale file prove: {len(os.listdir(CARTELLA_PROVE))}

Firma: ____________________
Data: {ora_leggibile()}

DOVE DENUNCIARE:
1. Vai su www.commissariatodips.it (Polizia Postale)
2. Porta questo file + cartella prove_hak_secure/
3. Oppure vai in Questura / Carabinieri con questo testo stampato
"""

    nome = f"DENUNCIA_{attacchi[0]['ip_aggressore'].replace('.','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(nome, "w", encoding="utf-8") as f:
        f.write(testo)
    
    print(f"\n⚖️ DENUNCIA GENERATA: {nome}")
    print("Portala alla Polizia Postale su commissariatodips.it")
    print("Oppure in Questura con la cartella prove_hak_secure/")
    return nome

def mostra_stato():
    print(f"\n🛡️ SCUDO DENUNCIA - Stato")
    print(f"Prove salvate: {len(prove)}")
    print(f"IP bannati: {len(ip_bannati)}")
    for ip in ip_bannati:
        n = len([p for p in prove if p["ip_aggressore"] == ip])
        print(f"  - {ip} -> {n} attacchi - RESPINTO + DENUNCIATO")

if __name__ == "__main__":
    print("🛡️⚖️ SCUDO CHE DENUNCIA E RESPINGE ATTIVO!")
    print("Ogni attacco = Ban + Prova salvata + Denuncia\n")

    # SIMULA 3 ATTACCHI DALLO STESSO AGGRESSORE
    aggressore = "45.67.89.10"
    test = [
        (aggressore, "sqlmap", "/login.php?id=1' OR '1'='1"),
        (aggressore, "Mozilla/5.0", "/page?<script>alert(1)</script>"),
        (aggressore, "Mozilla/5.0", "/.env"),
    ]
    for ip, ua, url in test:
        ok, msg = controlla_e_respingi(ip, ua, url)
        print(f"{msg} | {url}")
        time.sleep(0.5)

    mostra_stato()
    print("\n--- Ora genera denuncia manuale ---")
    genera_denuncia(aggressore)