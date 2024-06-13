from django.db import models

class Pelicula(models.Model):
    titulo = models.CharField(max_length=80)
    genero = models.CharField(max_length=60)
    duracion = models.IntegerField()
    
    def __str__(self):
        return self.titulo
    
class Horario(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete= models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    disponibilidad_asientos = models.IntegerField()
    
    def __str__(self):
        return f"{self.pelicula} - {self.fecha} {self.hora}"
    
class Reserva(models.Model):
    horario = models.ForeignKey(Horario, on_delete= models.CASCADE)
    usuario = models.CharField(max_length=100)
    email = models.EmailField()
    cantidad_asientos = models.IntegerField()
    
    def __str__(self):
        return f"{self.usuario} - {self.horario.pelicula} - {self.horario} - {self.cantidad_asientos} asientos"