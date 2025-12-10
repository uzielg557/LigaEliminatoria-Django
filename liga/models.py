from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)

    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)

    jugado = models.BooleanField(default=False)

    jornada = models.IntegerField()

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} (J {self.jornada})"