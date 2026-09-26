import os
from celery import Celery

# Indique à Celery où trouver les settings Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
# namespace="CELERY" : toutes les options Celery dans settings.py doivent
# commencer par CELERY_ (ex. CELERY_BROKER_URL), pour ne pas les confondre
# avec les autres réglages Django.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Cherche automatiquement un fichier tasks.py dans chaque app installée
app.autodiscover_tasks()