# Cartographer

### MAJ IMPORTANTE À VENIR
Le projet, de base un worm discord, va avoir des mises à jours majeures pour le transformer en toolkit complet d'outils d'OSINT Discord.

![osinttheplanet](https://cdn.discordapp.com/attachments/490080977289478145/727514075860566036/unknown.png)

### 
Collecte et l'analyse automatisées d'informations sur les guildes et les utilisateurs discord (dans le but de faire de l'OSINT)

Pour l'instant le code découpe en trois parties :
- Une partie de crawling des id serveur et de requetes à embed.json et widget.json pour récupérer des données sur les serveur
- Une seconde partie qui crawl tout les messages d'un serveur pour chercher les invitations discord
- Et une dernière partie selfbot qui leave et rejoint les discord automatiquement grâce aux invitations fournis
