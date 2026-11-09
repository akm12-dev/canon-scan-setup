# Canon Scan Setup

Utilitaire **AKM12** qui configure le **scan vers dossier (SMB)** et le **scan vers e-mail (SMTP)**
des imprimantes multifonctions Canon compatibles (Remote UI).

Fiche officielle et téléchargements : https://akm12.com/logiciels/canon-scan-setup

## Fonctionnalités

- Création du dossier partagé SMB, du compte local « scanner » et de la règle de pare-feu (Windows et macOS).
- Relais SMTP local : reçoit les scans de l'imprimante et les transmet au fournisseur de messagerie (TLS),
  avec file d'attente en cas d'échec.
- Préréglages : Gmail, Outlook, Microsoft 365, OVH, IONOS, Infomaniak, Orange, Free, SFR, Yahoo, iCloud.
- Test de l'imprimante, ouverture de Remote UI, fiche des réglages Canon à copier ou exporter.
- Journal des opérations et démarrage automatique du relais.

## Prérequis

- Python 3.9 ou plus récent ([python.org](https://www.python.org/downloads/)). Aucune autre dépendance.
- Droits administrateur pour créer le partage et le compte local.

## Démarrer depuis le code source

```bash
git clone <adresse du dépôt>
cd canon-scan-setup
```

- **Windows** : double-cliquer sur `Lancer_Windows.bat`
- **macOS** : clic droit sur `Lancer_Mac.command` › Ouvrir
- Ligne de commande : `python CanonScanSetup.py`
- Relais SMTP sans interface : `python CanonScanSetup.py --relay`

Pour une utilisation en intervention, préférez la version officielle publiée dans les
[Releases](../../releases) du dépôt.

## Créer un exécutable (facultatif)

Nécessite PyInstaller (`pip install pyinstaller`).

- Windows : `build_windows.bat` → `dist\CanonScanSetup.exe`
- macOS : `bash build_mac.sh` → `dist/CanonScanSetup.app`

## Structure

```
CanonScanSetup.py          point d'entrée
canonscan/
  gui.py                   interface graphique (tkinter)
  sharing.py               création du partage SMB (Windows / macOS)
  smtp_relay.py            relais SMTP local
  mailer.py                envoi vers le fournisseur, pièces jointes, file d'attente
  autostart.py             démarrage automatique, pare-feu
  canon_summary.py         fiche des réglages Canon
  config.py, netutil.py    configuration, outils réseau
docs/
  Guide_Canon_Scan_Setup.pdf   guide utilisateur illustré
  build/                       fabrication du guide et tests (voir ci-dessous)
```

## Configuration et sécurité

La configuration est enregistrée dans `%APPDATA%\CanonScanSetup\` (Windows) ou
`~/Library/Application Support/CanonScanSetup/` (macOS). Le fichier `config.json` contient les
mots de passe : il ne doit **jamais** être partagé ni ajouté à un dépôt Git (il est exclu par `.gitignore`).
Retirez toute information sensible des journaux avant de les transmettre.

## Tests et documentation

Depuis `docs/build/` :

- `py test_relay.py` : test de bout en bout du relais SMTP (authentification, transfert, pièces jointes, file d'attente).
- `py check_scripts.py <dossier>` : génère les scripts de partage SMB pour contrôle.
- `powershell -ExecutionPolicy Bypass -File build_guide.ps1` : régénère `docs/Guide_Canon_Scan_Setup.pdf`
  (nécessite ReportLab).

## Contribuer

Les signalements et propositions sont bienvenus via les Issues. Les modifications passent par une
Pull Request, relue et validée avant intégration : la branche `main` et les versions officielles sont
gérées uniquement par AKM12.

## Licence

Code consultable, tous droits réservés — voir [LICENSE](LICENSE). Vous pouvez lire, cloner et compiler ce code
pour votre propre usage ; sa redistribution, sa modification publiée et sa réutilisation demandent l'accord
d'AKM12. Les versions officielles gratuites sont publiées sur https://akm12.com et
https://github.com/akm12-dev/releases.
