# Automated Data Removal Script 🛡️

Dieses Python-Skript automatisiert den Versand von Löschanfragen (gemäß DSGVO/GDPR & CCPA) an eine Liste von Datenbrokern und anderen Organisationen. Es ermöglicht die Verwaltung mehrerer Identitäten und sendet für jede E-Mail-Adresse und Telefonnummer eine separate, personalisierte Anfrage.

## Features

  * **Verwaltung mehrerer Identitäten:** Verwalte Löschanfragen für verschiedene Personen oder Aliase, jeweils in eigenen, übersichtlichen Textdateien.
  * **Sichere Konfiguration:** Sensible Daten wie Passwörter und Serverdetails werden sicher in einer `.env`-Datei außerhalb des Quellcodes gespeichert.
  * **Flexible SMTP-Unterstützung:** Kompatibel mit SMTP-Servern, die SSL/TLS (Port 465) oder STARTTLS (Port 587) verwenden.
  * **Automatisierbar:** Entwickelt für den regelmäßigen, automatischen Betrieb durch Cronjobs oder ähnliche Scheduler.
  * **Anpassbare Vorlagen:** Der Text für die Löschanfragen kann einfach im Skript angepasst werden.

-----

## Voraussetzungen

Stelle sicher, dass die folgende Software auf deinem System installiert ist:

  * Python 3.x
  * pip (Python package installer)

-----

## 🚀 Setup-Anleitung

Befolge diese Schritte, um das Projekt einzurichten und lauffähig zu machen.

### 1\. Projektdateien herunterladen

Klone dieses Repository oder lade die Dateien herunter und lege sie in einem Ordner deiner Wahl ab. Die Ordnerstruktur sollte wie folgt aussehen:

```
data_removal_tool/
├── identities/
├── databroker.txt
├── main.py
└── .env
```

### 2\. Abhängigkeiten installieren

Öffne ein Terminal im Projektordner und installiere die benötigte Python-Bibliothek:

```bash
pip install python-dotenv
```

### 3\. `.env`-Datei konfigurieren

Erstelle eine Datei namens `.env` im Hauptverzeichnis und füge deine SMTP-Serverdaten ein. Diese Datei enthält sensible Daten und sollte **niemals** in ein öffentliches Repository hochgeladen werden.

**`.env`-Beispiel:**

```env
# Konfiguration für den E-Mail-Versand
SMTP_SERVER="dein-mailserver.de"
SMTP_PORT="465"
SMTP_USER="deine-email@dein-mailserver.de"
SMTP_PASSWORD="dein-sehr-sicheres-passwort"
```

### 4\. Identitäten anlegen

Lege im `identities/`-Ordner für jede Person oder Identität eine separate `.txt`-Datei an.

  * Jede Datei muss dem `Schlüssel: Wert`-Format folgen.
  * Gültige Schlüssel sind `Name`, `Adresse`, `Email` und `Telefon`.
  * Du kannst mehrere `Email`- oder `Telefon`-Einträge pro Datei haben.

**Beispiel: `identities/max_mustermann.txt`**

```
Name: Max Mustermann
Adresse: Musterstr. 123, 45678 Musterstadt, DE
Email: m.muster@mustermail.de
Telefon: +4917612345678
```

### 5\. Datenbroker-Liste füllen

Öffne die Datei `databroker.txt` und trage dort die E-Mail-Adressen der Empfänger ein, an die die Löschanfragen gesendet werden sollen (eine Adresse pro Zeile).

**Beispiel: `databroker.txt`**

```
privacy@some-broker.com
support@another-company.org
dsgvo-anfragen@service.net
```

-----

## Verwendung

Nachdem alles konfiguriert ist, kannst du das Skript manuell ausführen. Öffne dazu ein Terminal im Projektverzeichnis und starte das Skript:

```bash
python3 main.py
```

Das Skript gibt im Terminal aus, welche Anfragen es gerade versendet.

-----

## 🤖 Automatisierung (Cronjob)

Um den wahren Nutzen aus dem Skript zu ziehen, solltest du es automatisch in regelmäßigen Abständen ausführen lassen. Unter Linux oder macOS ist ein **Cronjob** dafür ideal.

1.  Öffne den Cronjob-Editor:

    ```bash
    crontab -e
    ```

2.  Füge die folgende Zeile am Ende der Datei hinzu, um das Skript z.B. **jeden ersten Tag des Monats um 02:30 Uhr** auszuführen.

    ```crontab
    # Führe das Skript jeden Tag um 02:30 Uhr aus, das Skript selbst prüft, ob 90 Tage vergangen sind
    30 2 * * * if [ $(($(date +%s) / 86400 % 90)) -eq 0 ]; then /usr/bin/python3 /pfad/zu/deinem/projekt/main.py; fi
    ```

    **Wichtig:** Ersetze `/pfad/zu/deinem/projekt/` durch den vollständigen, absoluten Pfad zu deinem Projektordner.

-----

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](https://opensource.org/licenses/MIT).
