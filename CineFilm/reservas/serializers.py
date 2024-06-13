from rest_framework import serializers
from .models import Pelicula, Horario, Reserva

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ['id', 'titulo', 'genero', 'duracion']
        

        
        
class HorarioSerializer(serializers.ModelSerializer):
    pelicula_id = serializers.PrimaryKeyRelatedField(queryset=Pelicula.objects.all(), source='pelicula', write_only=True)
    pelicula_titulo = serializers.CharField(source='pelicula.titulo', read_only=True)
    
    class Meta:
        model = Horario
        fields = ['id', 'pelicula_id', 'pelicula_titulo', 'fecha', 'hora', 'disponibilidad_asientos']

    def get_disponibilidad_asientos(self, obj):
        if obj.disponibilidad_asientos == 0:
            return 'Asientos completos'
        else:
            return obj.disponibilidad_asientos
        
        
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'horario', 'usuario', 'email', 'cantidad_asientos']