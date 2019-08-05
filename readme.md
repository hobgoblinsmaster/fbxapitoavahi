## Freebox api to avahi service file

Comme indiqué dans le bug https://dev.freebox.fr/bugs/task/22301, la nouvelle version du Compagnon Freebox (depuis la sortie de la Delta) ne parvient plus à trouver la freebox en mode bridge et donc à générer une nouvelle association.

Après avoir testé avec succès la création manuelle d’un fichier de service avahi permettant de diffuser _fbx-api._tcp.local, j’ai écris ce script python capable de le créer automatiquement et de le mettre à jour en cas de mise à jour de la Freebox ou de remplacement…

### Utilisation

```
/opt/fbxapitoavahi/apitoavahi.py -h
usage: apitoavahi.py [-h] [--debug | --silent] output_file

Générateur de service AVAHI pour Freebox en mode bridge

Lit les informations depuis http://mafreebox.freebox.fr/api_version
Crée un fichier utilisable comme service avahi.

Permet d’utiliser Freebox Compagnon avec une Freebox en mode Bridge :
    https://dev.freebox.fr/bugs/task/22301

positional arguments:
  output_file   Write to

optional arguments:
  -h, --help    show this help message and exit
  --debug, -d   enable debugging (default: False)
  --silent, -s  don't log to console (default: False)
```
