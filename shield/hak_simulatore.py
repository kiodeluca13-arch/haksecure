"""
🔍 HAK SECURE - SIMULATORE ATTACCHI
Testa lo Scudo Supremo ogni 2 settimane
Se trova 1 falla -> NOTIFICA URGENTE
Se tutto ok -> NESSUNA NOTIFICA, solo "Tutto passato"
Usa: python shield/hak_simulatore.py
"""

import time
import sys
sys.path.insert(0, ".")
sys.path.insert(0, "shield")

try:
    from shield.hak_scudo_supremo import SCUDO_SUPREMO, proteggi_pc, proteggi_telefono, proteggi_email, mostra_stato
    print("✅ Scudo Supremo collegato")
except Exception as e:
    print(f"❌ Scudo non trovato: {e}")
    print("Controlla che esista shield/hak_scudo_supremo.py")
    sys.exit(1)

def test(nome, funzione, deve_bloccare=True):
    try:
        ok, msg = funzione()
        bloccato = not ok
        # Se deve bloccare e ha bloccato = PASS
        # Se deve passare e è passato = PASS
        # Altrimenti = FALLA
        if deve_bloccare and bloccato:
            print(f"✅ PASS - {nome} - Bloccato come deve: {msg[:60]}")
            return True
        elif not deve_bloccare and ok:
            print(f"✅ PASS - {nome} - Passato come deve: {msg[:60]}")
            return True
        else:
            print(f"🚨 FALLA! - {nome} - Doveva {'bloccare' if deve_bloccare else 'passare'} ma ha fatto il contrario: {msg}")
            return False
    except Exception as e:
        print(f"🚨 FALLA CRITICA! - {nome} - Errore: {e}")
        return False

def simula_tutto():
    print("\n" + "="*60)
    print("🔍 SIMULATORE HAK - TEST ATTACCHI - Ogni 2 settimane")
    print("="*60 + "\n")
    falle = []
    passati = 0
    totale = 0

    prove = [
        # --- WEB ---
        ("SQL Injection", lambda: SCUDO_SUPREMO("90.0.0.1", "Mozilla/5.0", "/login?id=1' OR '1'='1"), True),
        ("SQL Union Select", lambda: SCUDO_SUPREMO("90.0.0.2", "Mozilla/5.0", "/x?u=1 UNION SELECT password FROM users"), True),
        ("XSS Script", lambda: SCUDO_SUPREMO("90.0.0.3", "Mozilla/5.0", "/x?<script>alert(document.cookie)</script>"), True),
        ("XSS Onerror", lambda: SCUDO_SUPREMO("90.0.0.4", "Mozilla/5.0", "/x?<img src=x onerror=alert(1)>"), True),
        ("Traversal /etc/passwd", lambda: SCUDO_SUPREMO("90.0.0.5", "Mozilla/5.0", "/../../etc/passwd"), True),
        ("Traversal .env", lambda: SCUDO_SUPREMO("90.0.0.6", "Mozilla/5.0", "/.env"), True),
        ("Command Injection", lambda: SCUDO_SUPREMO("90.0.0.7", "Mozilla/5.0", "/x?cmd=; cat /etc/passwd"), True),
        ("Phishing URL", lambda: SCUDO_SUPREMO("90.0.0.8", "Mozilla/5.0", "/verifica-ora-pacco-bloccato"), True),
        ("Ransomware URL", lambda: SCUDO_SUPREMO("90.0.0.9", "Mozilla/5.0", "/file.locked paga bitcoin"), True),
        ("Bot sqlmap", lambda: SCUDO_SUPREMO("90.0.0.10", "sqlmap/1.0", "/"), True),
        ("Bot nmap", lambda: SCUDO_SUPREMO("90.0.0.11", "nmap", "/"), True),
        ("Tor", lambda: SCUDO_SUPREMO("90.0.0.12", "Mozilla/5.0", "/", usa_tor=True), True),
        ("Paese bloccato", lambda: SCUDO_SUPREMO("90.0.0.13", "Mozilla/5.0", "/", paese="KP"), True),
        # --- BRUTE FORCE ---
        ("Brute Force login - 2° tentativo deve bloccare", lambda: (lambda: [SCUDO_SUPREMO("90.0.0.14", "Mozilla/5.0", "/login", password="MarcoAzienda2026!Super"), SCUDO_SUPREMO("90.0.0.14", "Mozilla/5.0", "/login", password="MarcoAzienda2026!Super")][1])(), True),
        # --- PC ---
        ("PC Ransomware file", lambda: proteggi_pc("90.0.0.15", nome_file="file.locked paga bitcoin", dispositivo="PC-TEST"), True),
        ("PC Malware exe", lambda: proteggi_pc("90.0.0.16", nome_file="fattura.exe", dispositivo="PC-TEST"), True),
        ("PC File pulito deve passare", lambda: proteggi_pc("90.0.0.17", nome_file="documento.pdf", dispositivo="PC-TEST"), False),
        # --- TELEFONO ---
        ("Telefono SMS Phishing", lambda: proteggi_telefono("90.0.0.18", sms_testo="pacco bloccato verifica-ora", dispositivo="TEL-TEST"), True),
        ("Telefono WiFi pericoloso", lambda: proteggi_telefono("90.0.0.19", wifi_nome="Free WiFi", dispositivo="TEL-TEST"), True),
        ("Telefono SMS pulito", lambda: proteggi_telefono("90.0.0.20", sms_testo="Ciao domani ci vediamo", dispositivo="TEL-TEST"), False),
        # --- EMAIL ---
        ("Email truffa CEO", lambda: proteggi_email("90.0.0.21", mittente="ceo@fake.com", oggetto="URGENTE Bonifico", corpo="fai bonifico urgente nuovo iban"), True),
        ("Email allegato exe", lambda: proteggi_email("90.0.0.22", mittente="x@fake.com", oggetto="Fattura", corpo="apri", allegato="fattura.exe"), True),
        ("Email pulita", lambda: proteggi_email("90.0.0.23", mittente="cliente@vero.com", oggetto="Fattura", corpo="allego", allegato="fattura.pdf"), False),
        # --- UTENTE VERO DEVE PASSARE ---
        ("Utente vero dashboard", lambda: SCUDO_SUPREMO("90.0.0.24", "Mozilla/5.0 Chrome/120", "/dashboard", dispositivo="PC-MARCO"), False),
    ]

    for nome, funz, deve_bloccare in prove:
        totale += 1
        if test(nome, funz, deve_bloccare):
            passati += 1
        else:
            falle.append(nome)
        time.sleep(0.1)

    # --- DDoS ---
    print("\n--- TEST DDoS - 20 richieste veloci ---")
    totale += 1
    bloccato_ddos = False
    for i in range(20):
        ok, msg = SCUDO_SUPREMO("90.0.0.99", "Mozilla/5.0 Chrome", f"/pagina{i}")
        if not ok:
            bloccato_ddos = True
            print(f"✅ PASS - DDoS bloccato alla richiesta {i+1}: {msg}")
            break
    if bloccato_ddos:
        passati += 1
    else:
        print("🚨 FALLA! - DDoS NON bloccato dopo 20 richieste")
        falle.append("DDoS non bloccato")

    print("\n" + "="*60)
    print(f"RISULTATO: {passati}/{totale} test passati")
    if falle:
        print(f"🚨🚨🚨 FALLA TROVATA: {len(falle)} falle!")
        for f in falle:
            print(f"  - {f}")
        print("\n⚠️ AZIONE: Controlla subito lo scudo, una di queste protezioni non funziona.")
        print("Se vuoi, mandami lo screenshot e ti sistemo la falla.")
    else:
        print("✅✅✅ TUTTO PASSATO - Nessuna falla - Scudo Supremo perfetto")
    print("="*60)
    return falle

if __name__ == "__main__":
    falle = simula_tutto()
    # Codice uscita: 0 = tutto ok, 1 = falle
    sys.exit(1 if falle else 0)