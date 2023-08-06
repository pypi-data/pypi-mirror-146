import smtplib
from getpass import getpass
import requests
import re


def smtp(identifiant: str = "", mdp: str = "") -> smtplib.SMTP_SSL:
    """Permet d'initier une session SMTP sécurisée sur le serveur mail de l'UTT, soit de manière manuelle, soit de manière
        automatique en fournissant id et mdp

        :date: Aout 2020
        :Author: Ivann LARUELLE

        :param identifiant: L'identifiant de l'user en mode auto
        :type identifiant: str

        :param mdp: Le mdp de l'user en mode auto
        :type mdp: str

        :return: Une session avec laquelle on peut effectuer des requêtes, ou -1 en mode auto si échec
        :rtype: smtplib.SMTP_SSL

        :raises smtplib.SMTPAuthenticationError: Si le couple id/mdp est invalide
        :raises Exception: si le serveur est injoignable

        """
    server_connecte = smtplib.SMTP_SSL('mail.utt.fr')
    server_connecte.connect('mail.utt.fr')
    server_connecte.ehlo()
    manuel = mdp == "" or identifiant == ""
    while True:
        # On informe l'utilisateur du service sur lequel il se connecte
        if manuel:
            print("Vous allez vous connecter au service de mail de l'UTT\n")
            identifiant = input("Entrez votre identifiant CAS UTT : ")
            mdp = getpass("Entrez votre mot de passe. Ce dernier n'apparaitra pas au cours de la saisie : ")
        try:
            server_connecte.login(identifiant, mdp)
            return server_connecte
        except smtplib.SMTPAuthenticationError as mail_exception:
            print("Combinaison identifiant / mdp invalide")
            if not manuel:
                raise mail_exception
        except Exception as mail_exception:
            print(mail_exception)
            if not manuel:
                raise mail_exception


def cas(service: str, identifiant: str = "", mdp: str = "", session_web: requests.Session = requests.Session())\
        -> requests.Session:
    """Permet d'initier une session web sur un service via le CAS de l'UTT, soit de manière manuelle, soit de manière
    automatique en fournissant id, mdp, et session web si besoin

    :date: Aout 2019
    :Author: Ivann LARUELLE

    :param service: L'url du service auquel on veut accéder via le CAS
    :type service: str

    :param identifiant: L'identifiant de l'user en mode auto

    :param mdp: Le mdp de l'user en mode auto
    :type mdp: str

    :param session_web: On peut ajouter la connexion CAS à une session web déjà existante
    :type session_web: requests.sessions.Session

    :return: Une session avec laquelle on peut effectuer des requêtes, ou -1 en mode auto si échec
    :rtype: requests.sessions.Session

    :raises Exception: Si l'id/mdp ne sont pas corrects ou connexion impossible au CAS

    """
    while True:
        session_web.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'})
        test_connexion_service = session_web.get(service, allow_redirects=True, headers=session_web.headers)
        texte = test_connexion_service.content.decode('utf-8')
        match_valeur_lt = re.search('name=\"lt\" value=\"(.*)?\"', texte)
        manuel = mdp == "" or identifiant == ""
        # On informe l'utilisateur du service sur lequel il se connecte
        if manuel:
            print("Vous allez vous connecter au service suivant : " + service)
            # On lui demande ses identifiants
            identifiant = input("Entrez votre identifiant CAS UTT : ")
            mdp = getpass("Entrez votre mot de passe. Ce dernier n'apparaitra pas au cours de la saisie : ")
        url = "https://cas.utt.fr/cas/login"
        donnees = {"service": service, "username": identifiant, "password": mdp, "_eventId": "submit",
                   "lt": match_valeur_lt.group(1), "submit": "SE CONNECTER"}
        reponse_connexion = session_web.post(url, data=donnees, allow_redirects=True)
        # Si on est toujours sur la page du CAS, la connection a échoué.
        connecte = (reponse_connexion.url.find("https://cas.utt.fr/") == -1)
        # On efface toutes les informations demandées à l'utilisateur
        if not connecte:
            print("Erreur de connexion, veuillez ressaisir vos identifiants !\n")
            if not manuel:
                raise Exception("Identifiants invalides ou connexion au serveur impossible")
        print("\n\nCONNECTE AU SI !\n")
        return session_web
