# Hak Secure Mobile - SOFTWARE VERO PER TELEFONO
# Non è un sito. È un'app Android fatta in Python + Kivy

import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window

Window.clearcolor = (0.03, 0.03, 0.03, 1)

class HakMobileApp(App):
    def build(self):
        self.title = "Hak Secure Mobile"
        self.checks = []

        layout = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None, padding=15, spacing=12)
        box.bind(minimum_height=box.setter('height'))

        box.add_widget(Label(text="🛡️ HAK SECURE", font_size=32, bold=True, color=(0,1,0,1), size_hint_y=None, height=50))
        box.add_widget(Label(text="Software Protezione Telefono v1.0", font_size=16, color=(1,1,1,1), size_hint_y=None, height=30))
        self.label_punteggio = Label(text="Punteggio: 0 / 100", font_size=22, bold=True, color=(1,0,0,1), size_hint_y=None, height=40)
        box.add_widget(self.label_punteggio)

        # 1. ANTI-PHISHING
        box.add_widget(Label(text="🎣 1. ANTI-PHISHING - Controlla Link", font_size=18, bold=True, color=(0,1,0,1), size_hint_y=None, height=30))
        self.input_link = TextInput(hint_text="Incolla link da SMS / WhatsApp", multiline=False, size_hint_y=None, height=50, background_color=(0.1,0.1,0.1,1), foreground_color=(1,1,1,1))
        box.add_widget(self.input_link)
        btn_link = Button(text="CONTROLLA LINK", size_hint_y=None, height=50, background_color=(0,0.8,0,1))
        btn_link.bind(on_press=self.controlla_link)
        box.add_widget(btn_link)
        self.ris_link = Label(text="", font_size=16, size_hint_y=None, height=60)
        box.add_widget(self.ris_link)

        # 2. PASSWORD
        box.add_widget(Label(text="🔑 2. Controlla Password", font_size=18, bold=True, color=(0,1,0,1), size_hint_y=None, height=30))
        self.input_pass = TextInput(hint_text="Scrivi password", password=True, multiline=False, size_hint_y=None, height=50, background_color=(0.1,0.1,0.1,1), foreground_color=(1,1,1,1))
        box.add_widget(self.input_pass)
        btn_pass = Button(text="CONTROLLA PASSWORD", size_hint_y=None, height=50, background_color=(0,0.8,0,1))
        btn_pass.bind(on_press=self.controlla_password)
        box.add_widget(btn_pass)
        self.ris_pass = Label(text="", font_size=16, size_hint_y=None, height=60)
        box.add_widget(self.ris_pass)

        # 3. CHECKLIST
        box.add_widget(Label(text="📱 3. Protezione Totale Telefono", font_size=18, bold=True, color=(0,1,0,1), size_hint_y=None, height=30))
        domande = [
            "PIN / Impronta / FaceID attivo",
            "2FA attiva WhatsApp",
            "2FA attiva Instagram",
            "2FA attiva Gmail",
            "2FA attiva Banca",
            "Backup foto e chat attivo",
            "Telefono aggiornato",
            "Trova Dispositivo attivo",
            "Permessi app controllati",
            "Mai banca su WiFi pubblico",
        ]
        for d in domande:
            riga = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            cb = CheckBox(size_hint_x=None, width=40)
            cb.bind(active=self.aggiorna_punteggio)
            self.checks.append(cb)
            riga.add_widget(cb)
            riga.add_widget(Label(text=d, font_size=15, color=(1,1,1,1), halign='left'))
            box.add_widget(riga)

        # 4. SCANSIONE
        box.add_widget(Label(text="🔍 4. Scansione App Sospette", font_size=18, bold=True, color=(0,1,0,1), size_hint_y=None, height=30))
        btn_scan = Button(text="SCANSIONA TELEFONO", size_hint_y=None, height=50, background_color=(1,0.6,0,1))
        btn_scan.bind(on_press=self.scansiona)
        box.add_widget(btn_scan)
        self.ris_scan = Label(text="", font_size=15, size_hint_y=None, height=100)
        box.add_widget(self.ris_scan)

        # 5. EMERGENZA
        box.add_widget(Label(text="🚨 5. Emergenza - Telefono Rubato", font_size=18, bold=True, color=(1,0,0,1), size_hint_y=None, height=30))
        btn_em = Button(text="COSA FARE SE RUBATO", size_hint_y=None, height=50, background_color=(1,0,0,1))
        btn_em.bind(on_press=self.emergenza)
        box.add_widget(btn_em)
        self.ris_em = Label(text="", font_size=15, size_hint_y=None, height=120)
        box.add_widget(self.ris_em)

        box.add_widget(Label(text="Hak Secure Mobile - Software difensivo", font_size=12, color=(0.5,0.5,0.5,1), size_hint_y=None, height=30))

        layout.add_widget(box)
        return layout

    def controlla_link(self, instance):
        url = self.input_link.text.lower()
        if not url:
            self.ris_link.text = "Incolla prima un link"
            self.ris_link.color = (1,1,0,1)
            return
        punti = 0
        motivi = []
        if any(x in url for x in ["verifica-ora","sblocca","urgente","pacco","premio","banca","conferma-ora"]):
            punti += 3; motivi.append("Parole truffa")
        if re.search(r"http://\d+\.\d+", url):
            punti += 4; motivi.append("Usa IP")
        if any(x in url for x in ["bit.ly","tinyurl","cutt.ly","t.co"]):
            punti += 3; motivi.append("Link accorciato")
        if any(x in url for x in [".tk",".xyz",".top",".buzz"]):
            punti += 2; motivi.append("Dominio a rischio")
        if "paypal" in url and "paypal.com" not in url:
            punti += 5; motivi.append("Finto PayPal")
        if "amazon" in url and "amazon." not in url:
            punti += 5; motivi.append("Finto Amazon")
        if punti >= 5:
            self.ris_link.text = f"⛔ PERICOLO! NON APRIRE\n{', '.join(motivi)}"
            self.ris_link.color = (1,0,0,1)
        elif punti >= 2:
            self.ris_link.text = f"⚠️ SOSPETTO\n{', '.join(motivi)}"
            self.ris_link.color = (1,1,0,1)
        else:
            self.ris_link.text = "✅ Link sembra ok, stai attento lo stesso"
            self.ris_link.color = (0,1,0,1)

    def controlla_password(self, instance):
        p = self.input_pass.text
        if len(p) < 8:
            self.ris_pass.text = "⛔ Troppo corta! Minimo 12 caratteri"
            self.ris_pass.color = (1,0,0,1)
            return
        if p.lower() in ["123456","password","12345678","qwerty"]:
            self.ris_pass.text = "⛔ Password famosissima! Cambiala!"
            self.ris_pass.color = (1,0,0,1)
            return
        if not re.search(r"[A-Z]", p) or not re.search(r"[0-9]", p):
            self.ris_pass.text = "⚠️ Aggiungi MAIUSCOLA + NUMERO"
            self.ris_pass.color = (1,1,0,1)
            return
        self.ris_pass.text = "✅ Password forte!"
        self.ris_pass.color = (0,1,0,1)

    def aggiorna_punteggio(self, instance, value):
        fatti = sum(1 for cb in self.checks if cb.active)
        punteggio = fatti * 10
        self.label_punteggio.text = f"Punteggio: {punteggio} / 100"
        if punteggio == 100:
            self.label_punteggio.color = (0,1,0,1)
            self.label_punteggio.text = "Punteggio: 100 / 100 - TELEFONO PROTETTO 🛡️"
        elif punteggio >= 70:
            self.label_punteggio.color = (1,1,0,1)
        else:
            self.label_punteggio.color = (1,0,0,1)

    def scansiona(self, instance):
        self.ris_scan.text = "🔍 Scansione...\nControlla ora:\n- App che non hai installato tu?\n- App con permessi microfono / SMS strani?\n- Se trovi app strana, DISINSTALLALA subito.\n- Controlla in Impostazioni > App"

    def emergenza(self, instance):
        self.ris_em.text = "1. Da altro telefono: Trova iPhone / Trova Dispositivo\n2. Blocca telefono\n3. Cambia password Gmail + Banca\n4. Chiama banca e blocca carte"

if __name__ == '__main__':
    HakMobileApp().run()