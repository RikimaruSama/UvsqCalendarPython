Utilisation :
```python
calendrier = UvsqCalendar()
le15fevrier = calendrier.request_dict(date_debut="15/02/2024", date_fin="15/02/2024", section="M1 SECRETS gr 1")
print(le15fevrier)
# [{'matiere': 'MIN17213', 'type': 'TD', 'date': '15-02-2024', ...

# Pour la date du 16/02/2024
aujourdhui = calendrier.request_dict(section="S6 INFO TD01")
print(aujourdhui)
# [{'matiere': 'LSIN611', 'type': 'Temps personnel', 'date': '16-02-2024', 'heure': '09:40:00', 'duree': '3:10:00', 'lieu': ''} ...
```
#TODO :
- Pour le dimanche 18, Cours : None et Salle : None... On n'affiche pas les dimanches ou soit try...expect et on passe.
