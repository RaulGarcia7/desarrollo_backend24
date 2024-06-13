from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PeliculaViewSet, HorarioViewSet, ReservaAPIView

router = DefaultRouter()

router.register(r'peliculas', PeliculaViewSet)
router.register(r'horarios', HorarioViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('reservas/', ReservaAPIView.as_view(), name='reserva-list-create'),
    path('reservas/<int:pk>/', ReservaAPIView.as_view(), name='reserva-detail')
]