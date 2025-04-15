from django.db import models

class Frontera(models.Model):
    """
    Stores information related to a frontier registration.
    """
    requerimiento = models.CharField(max_length=100)
    frontera = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    equipo_medida = models.CharField(max_length=100)
    curva_tipica = models.CharField(max_length=100)
    certificaciones = models.TextField()
    adjunto = models.FileField(upload_to='adjuntos/', null=True, blank=True)

    def __str__(self):
        return self.requerimiento
