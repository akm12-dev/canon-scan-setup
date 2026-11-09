"""Génère la fiche des réglages à saisir dans l'interface Web de l'imprimante Canon (Remote UI)."""
from datetime import datetime

from . import netutil
from .mailer import SECURITY_LABELS


def build(cfg: dict) -> str:
    ip = netutil.local_ip()
    host = netutil.hostname()
    s, up, rl = cfg["share"], cfg["upstream"], cfg["relay"]
    L = []
    add = L.append
    add("FICHE DE RÉGLAGES — IMPRIMANTE CANON")
    add(f"Générée le {datetime.now():%d/%m/%Y à %H:%M} — PC : {host} ({ip})")
    if cfg.get("printer_ip"):
        add(f"Interface Web de l'imprimante : http://{cfg['printer_ip']}  (Remote UI, connexion administrateur)")
    add("")
    add("════════ 1. SCAN VERS DOSSIER (SMB) ════════")
    add("Remote UI › Carnet d'adresses › Liste d'adresses › Enregistrer nouveau destinataire › Fichier")
    add("")
    add("  Protocole ............ Windows (SMB)")
    add(f"  Nom d'hôte ........... \\\\{ip}\\{s['share_name']}")
    add("  Chemin du dossier .... (laisser vide)")
    add(f"  Nom d'utilisateur .... {s['username']}")
    add(f"  Mot de passe ......... {s['password'] or '(celui défini dans le logiciel)'}")
    add("")
    add(f"  Si refus : essayer Nom d'utilisateur = {host}\\{s['username']}")
    add(f"  Les fichiers arrivent dans : {s['folder']}")
    add("  Conseil : fixez l'IP du PC (réservation DHCP dans la box) pour que l'adresse ne change pas.")
    add("")
    add("════════ 2. SCAN VERS E-MAIL (SMTP) ════════")
    add("Remote UI › Paramètres/Enregistrement › Paramètres de fonction › Envoi ›")
    add("           Paramètres E-mail/I-Fax › Paramètres de communication")
    add("  (i-SENSYS / MF : Paramètres/Enregistrement › Paramètres réseau › Paramètres E-mail/I-Fax)")
    add("")
    if rl.get("mode") == "relay":
        add("Mode : RELAIS VIA CE PC (le PC doit être allumé et le relais démarré)")
        add("")
        add(f"  Serveur SMTP ......... {ip}")
        add(f"  Port SMTP ............ {rl['listen_port']}" + ("" if int(rl["listen_port"]) == 25 else
                                                               "   (si le port n'est pas réglable sur le Canon, utilisez 25)"))
        add(f"  Adresse e-mail ....... {up.get('from_addr') or up.get('username') or 'scanner@votre-domaine.fr'}")
        add("  Utiliser TLS / SSL ... NON (désactivé)")
        add("  Vérif. certificat .... NON")
        if rl.get("auth_user"):
            add("  Authentification SMTP  OUI")
            add(f"    Nom d'utilisateur .. {rl['auth_user']}")
            add(f"    Mot de passe ....... {rl['auth_password']}")
        else:
            add("  Authentification SMTP  NON")
        add("  POP avant SMTP ....... NON")
        add("")
        add(f"  Le PC retransmet ensuite via {up['host'] or '(fournisseur à configurer)'}:{up['port']} "
            f"({SECURITY_LABELS.get(up['security'], '')})")
        if rl.get("save_attachments"):
            add(f"  Les pièces jointes sont aussi copiées dans : {rl['save_folder']}")
    else:
        add("Mode : DIRECT (l'imprimante contacte directement le fournisseur)")
        add("")
        add(f"  Serveur SMTP ......... {up['host']}")
        add(f"  Port SMTP ............ {up['port']}")
        add(f"  Adresse e-mail ....... {up.get('from_addr') or up.get('username')}")
        add(f"  Utiliser TLS / SSL ... {'OUI' if up['security'] != 'none' else 'NON'}"
            f"  ({SECURITY_LABELS.get(up['security'], '')})")
        add("  Authentification SMTP  OUI")
        add(f"    Nom d'utilisateur .. {up['username']}")
        add("    Mot de passe ....... (mot de passe d'application du compte)")
        add("")
        add("  ⚠ Les Canon anciens ne gèrent pas toujours TLS 1.2/1.3 : en cas d'erreur #801/#802,")
        add("    passez en mode « Relais via ce PC ».")
    add("")
    add("════════ 3. CODES D'ERREUR COURANTS ════════")
    add("  #751 / #752 .. serveur introuvable : vérifier l'IP / le DNS / la passerelle de l'imprimante")
    add("  #755 ......... réseau de l'imprimante non opérationnel (câble, IP)")
    add("  #766 ......... certificat expiré / invalide (désactiver la vérification ou utiliser le relais)")
    add("  #801 ......... délai dépassé ou connexion refusée (pare-feu, port, SMB)")
    add("  #802 ......... nom de serveur incorrect")
    add("  #810 ......... erreur de connexion POP : désactiver « POP avant SMTP »")
    add("  Codes indicatifs : la signification exacte dépend du modèle (voir le manuel en ligne Canon).")
    return "\n".join(L)
