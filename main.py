# coding: utf-8

import html
import requests, json
from datetime import datetime, timedelta
import re
import unittest

class UvsqCalendar:
    """ Classe faisant des requetes sur le site edt.uvsq.fr afin d'avoir l'emploi du temps. """
    def __init__(self):
        self.url = 'https://edt.uvsq.fr/Home/GetCalendarData'
        self.today = datetime.today().date().strftime("%d/%m/%Y")
        self.groupes = ["S6 INFO", "S6 INFO TD01", "S6 INFO TD02", "S6 INFO TD03","S6 INFO TD04", "M1 SECRETS", "M1 SECRETS gr 1", "M1 SECRETS gr 2", "M1 SECRETS gr 3", "M1 SECRETS gr 4"]

    def __pretifly(cls, old):
        """ Méthode privé qui prend une chaine de characteres et nous renvoie la chaine sans tout les accents. """
        new = re.sub(r'[àáâãäå]', 'a', old)
        new = re.sub(r'[èéêë]', 'e', new)
        new = re.sub(r'[ìíîï]', 'i', new)
        new = re.sub(r'[òóôõö]', 'o', new)
        new = re.sub(r'[ùúûü]', 'u', new)
        new = re.sub(r'[ÀÁÂÃÄÅ]', 'A', new)
        new = re.sub(r'[ÈÉÊË]', 'E', new)
        new = re.sub(r'[ÌÍÎÏ]', 'I', new)
        new = re.sub(r'[ÒÓÔÕÖ]', 'O', new)
        new = re.sub(r'[ÙÚÛÜ]', 'U', new)
        return new

    def request_json(self, date_debut=None, date_fin=None, section='S6 INFO TD01'):
        """ Méthode qui renvoie une liste contenant un String sous format d'écriture Json. """
        # Gestion d'erreurs
        if date_debut is None and date_fin is None:
            date_debut = self.today
            date_fin = self.today
        if datetime.strptime(date_debut, "%d/%m/%Y") > datetime.strptime(date_fin, "%d/%m/%Y"):
            raise ValueError("Les dates ne sont pas en accords entre elles.")
        if section not in self.groupes:
            raise ValueError("La section fournie n'est pas valide, le groupe n'est pas implémenté.")
        
        # Definition de la requete
        req = {
            'start': date_debut,
            'end': date_fin,
            'resType': '103',
            'calView': 'agendaDay',
            'federationIds[]': section
        }
        try:
            response = requests.post(self.url, data=req)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print("Http Error:",e)
            raise
        except requests.exceptions.ConnectionError as e:
            print("Error Connecting:",e)
            raise
        except requests.exceptions.Timeout as e:
            print("Timeout Error:",e)
            raise
        except requests.RequestException as e:
            print("Request Error:", e)
            raise
    
    def request_dict(self, date_debut=None, date_fin=None, section='S6 INFO TD01'):
        """ Méthode qui renvoie une liste contenant un String sous forme de dictionnaire. """
        data, evenements = self.request_json(date_debut, date_fin, section), []
        for event in data:
            debut = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M:%S")
            fin = datetime.strptime(event["end"], "%Y-%m-%dT%H:%M:%S")
            matiere = self.__pretifly(event["modules"][0])
            description = html.unescape(event["description"])
            description = description.replace("\n", "").replace("\r", "").replace("<br />", "⁣")
            type_enseig, site, _ = self.__pretifly(description).split("⁣")[:3]
            evenements.append(  
                {
                    'matiere': matiere,
                    'type': type_enseig,
                    'date': debut.strftime("%d-%m-%Y"),
                    'heure': debut.strftime("%H:%M:%S"),
                    'duree': str(fin - debut),
                    'lieu': site,
                }
            )
        return sorted(evenements, key= lambda x: (x['date'], x['heure']))