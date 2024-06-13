from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pelicula, Horario, Reserva
from .serializers import PeliculaSerializer, HorarioSerializer, ReservaSerializer
from datetime import date
from django.core.mail import send_mail


class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer
    
class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    
    def create(self, request):
        fecha_actual = date.today()
        
        fecha_request = request.data.get('fecha')
        if fecha_request:
            fecha_request = date.fromisoformat(fecha_request)
            if fecha_request < fecha_actual:
                return Response({"error": "No se pueden crear horarios con fechas pasadas"}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request)

def mail_confirmation(reserva, tipo):
    if tipo == 'confirmacion':
        subject = 'Confirmación de reserva'
        message =   f'¡Gracias por confiar en CineFilm! Su reserva para la película {reserva.horario.pelicula.titulo} ha sido confirmada.\n\n' \
                    f'Detalles de la reserva:\n' \
                    f'ID de Reserva: {reserva.id}\n' \
                    f'Usuario: {reserva.usuario}\n' \
                    f'Correo electrónico: {reserva.email}\n' \
                    f'Cantidad de asientos: {reserva.cantidad_asientos}\n' \
                    f'Fecha: {reserva.horario.fecha}\n' \
                    f'Hora: {reserva.horario.hora}\n' 
    elif tipo == 'actualizacion':
        subject = 'Actualización de reserva'
        message =   f'Su reserva para la película {reserva.horario.pelicula.titulo} ha sido actualizada.\n\n' \
                    f'Detalles de la reserva actualizada:\n' \
                    f'ID de Reserva: {reserva.id}\n' \
                    f'Nuevo Horario: {reserva.horario.fecha} {reserva.horario.hora}\n' \
                    f'Nueva Cantidad de asientos: {reserva.cantidad_asientos}\n'
    elif tipo == 'cancelacion':
        subject = 'Confirmación de eliminación de reserva'
        message =   f'Su reserva para la película {reserva.horario.pelicula.titulo} ha sido cancelada.\n\n' \
                    f'ID de Reserva: {reserva.id}\n' \
                    f'Fecha de la Reserva: {reserva.horario.fecha}\n' \
                    f'Hora de la Reserva: {reserva.horario.hora}\n'
    email_from = 'cinefilmmadrid@gmail.com'
    recipient_list = [reserva.email]
    send_mail(subject, message, email_from, recipient_list)
    
class ReservaAPIView(APIView):
    
    def get(self, request):
        reservas = Reserva.objects.all()
        serializer = ReservaSerializer(reservas, many = True)
        return Response({
            'reservas': serializer.data
        })
    
    def post(self, request):
        try:
            horario_id = request.data.get('horario_id')
            horario = Horario.objects.get(id=horario_id)
            cantidad_asientos = int(request.data.get('cantidad_asientos'))
            
            if horario.disponibilidad_asientos >= cantidad_asientos:
                horario.disponibilidad_asientos -= cantidad_asientos
                horario.save()
                
                reserva = Reserva.objects.create(
                    horario=horario,
                    usuario=request.data.get('usuario'),
                    email = request.data.get('email'),
                    cantidad_asientos=cantidad_asientos
                )
                
                mail_confirmation(reserva, 'confirmacion')
                
                serializer = ReservaSerializer(reserva)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "No hay suficientes asientos disponibles"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Horario.DoesNotExist:
            return Response({"error": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        
    def put(self, request, pk):
        try:
            reserva = Reserva.objects.get(pk = pk)
            horario = reserva.horario
            n_horario_id = request.data.get('horario_id')
            n_cantidad_asientos = int(request.data.get('cantidad_asientos'))
            
            if n_horario_id:
                n_horario = Horario.objects.get(id = n_horario_id)
            else:
                n_horario = horario
            
            if n_horario.disponibilidad_asientos + reserva.cantidad_asientos >= n_cantidad_asientos:
                horario.disponibilidad_asientos += reserva.cantidad_asientos - n_cantidad_asientos
                horario.save()
            
                n_horario.disponibilidad_asientos -= n_cantidad_asientos
                n_horario.save()
                
                reserva.horario = n_horario
                reserva.cantidad_asientos = n_cantidad_asientos
                reserva.email = request.data.get('email', reserva.email)
                reserva.save()
                
                mail_confirmation(reserva, 'actualizacion')
            
                serializer = ReservaSerializer(reserva)
                return Response(serializer.data)
            else:
                return Response({"error": "No hay suficientes asientos disponibles"}, status=status.HTTP_400_BAD_REQUEST)
        except Reserva.DoesNotExist:
            return Response({"error": "Reserva no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Horario.DoesNotExist:
            return Response({"error": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try: 
            reserva = Reserva.objects.get(pk = pk)
            horario = reserva.horario
            
            horario.disponibilidad_asientos += reserva.cantidad_asientos
            horario.save()
            
            mail_confirmation(reserva, 'cancelacion')
            
            reserva.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Reserva.DoesNotExist:
            return Response({"error": "Reserva no encontrada"}, status=status.HTTP_404_NOT_FOUND)