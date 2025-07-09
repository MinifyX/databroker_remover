import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT_STR = os.getenv("SMTP_PORT")
SMTP_BENUTZER = os.getenv("SMTP_USER")
SMTP_PASSWORT = os.getenv("SMTP_PASSWORD")

IDENTITIES_ORDNER = "identities"
DATABROKER_DATEI = "databroker.txt"

def erstelle_email_vorlage(identitaet, datenpunkt, datenpunkt_typ):
    """Erstellt eine universelle E-Mail-Vorlage."""
    name = identitaet.get("Name", ["N/A"])[0]
    adresse = identitaet.get("Adresse", ["N/A"])[0]

    removal_type = "Email Address" if datenpunkt_typ == "Email" else "Phone Number"

    text = f"""
To Whom It May Concern,

I am writing to request the implementation of my rights under applicable privacy legislation (including GDPR Art. 17 and CCPA Sec. 1798.105).

First, in accordance with my right of access (GDPR Art. 15), I request that you provide me with clear information regarding the source of my personal data. Specifically, please disclose from where you obtained the email address listed below.

Following the fulfillment of this access request, I request the complete and irreversible erasure of all personal data linked to this identifier, as is my right (including under GDPR Art. 17 and CCPA Sec. 1798.105).

This request concerns the personal data associated with the following identifier:

{removal_type}: {datenpunkt}

I hereby request the complete and irreversible erasure of all personal data linked to this identifier. This includes, but is not limited to, associated account details, activity records, backups, and any derived data.

My identifying details to help you locate the data are:
Name: {name}
Address: {adresse}

{removal_type}: {datenpunkt}

Please confirm your compliance with this request in writing without undue delay to {SMTP_BENUTZER}.

Thank you for your cooperation.

Sincerely,
{name}
"""
    return text, f"Formal Request for Data Access (GDPR Art. 15) and Erasure (GDPR Art. 17 / CCPA)"


# --- Hauptlogik ---
def hauptprogramm():
    # Überprüfen, ob alle Umgebungsvariablen geladen wurden
    if not all([SMTP_SERVER, SMTP_PORT_STR, SMTP_BENUTZER, SMTP_PASSWORT]):
        print(
            "Fehler: Nicht alle notwendigen Umgebungsvariablen (SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD) sind in der .env-Datei gesetzt.")
        return  # Beendet das Programm, wenn die Konfiguration fehlt

    # Port-String in eine Ganzzahl umwandeln
    try:
        smtp_port = int(SMTP_PORT_STR)
    except ValueError:
        print(f"Fehler: Der SMTP_PORT '{SMTP_PORT_STR}' in der .env-Datei ist keine gültige Zahl.")
        return

    try:
        # Datenbroker-Liste einlesen
        with open(DATABROKER_DATEI, 'r', encoding='utf-8') as f:
            databroker_emails = [line.strip() for line in f if line.strip()]

        # SMTP-Verbindung aufbauen
        print(f"Verbinde mit {SMTP_SERVER} auf Port {smtp_port}...")
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, smtp_port)
        else:
            server = smtplib.SMTP(SMTP_SERVER, smtp_port)
            server.starttls()

        server.login(SMTP_BENUTZER, SMTP_PASSWORT)
        print("Erfolgreich verbunden.")

        # Durch den Identities-Ordner iterieren
        for dateiname in os.listdir(IDENTITIES_ORDNER):
            if dateiname.endswith(".txt"):
                filepath = os.path.join(IDENTITIES_ORDNER, dateiname)

                identitaet = {}
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip()
                            value = value.strip()
                            if key not in identitaet:
                                identitaet[key] = []
                            identitaet[key].append(value)

                print(f"\n--- Verarbeite Identität: {identitaet.get('Name', ['Unbekannt'])[0]} ---")

                # Anfragen für jede E-Mail-Adresse und Telefonnummer senden
                for daten_typ, daten_liste in [("Email", identitaet.get("Email", [])),
                                               ("Telefon", identitaet.get("Telefon", []))]:
                    for datenpunkt in daten_liste:
                        for broker in databroker_emails:
                            email_text, betreff = erstelle_email_vorlage(identitaet, datenpunkt, daten_typ)
                            sende_email(server, broker, betreff, email_text)
                            print(f"  -> Anfrage für {daten_typ} '{datenpunkt}' an '{broker}' gesendet.")

        server.quit()
        print("\nAlle Anfragen wurden erfolgreich versendet.")

    except FileNotFoundError as e:
        print(f"Fehler: Die Datei oder der Ordner '{e.filename}' wurde nicht gefunden.")
    except smtplib.SMTPAuthenticationError:
        print("Fehler: Die SMTP-Anmeldedaten sind falsch. Bitte überprüfen Sie die .env-Datei.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


def sende_email(server, empfaenger, betreff, text):
    """Hilfsfunktion zum Senden einer einzelnen E-Mail."""
    nachricht = MIMEMultipart()
    nachricht["From"] = SMTP_BENUTZER
    nachricht["To"] = empfaenger
    nachricht["Subject"] = betreff
    nachricht.attach(MIMEText(text, "plain", "utf-8"))
    server.sendmail(SMTP_BENUTZER, empfaenger, nachricht.as_string())


# Das Skript ausführen
if __name__ == "__main__":
    hauptprogramm()
