from django.urls import path
from .views import (MovieListCreateAPIView, MovieRetrieveAPIView, MovieUpdateAPIView,
MovieDestroyAPIView, DirectorListCreateAPIView, DirectorRetrieveAPIView,
DirectorUpdateAPIView, DirectorDestroyAPIView, AddMovieDirector  
)

urlpatterns = [
    path('movies/', MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieRetrieveAPIView.as_view(), name='movie-retrieve'),
    path('movies/<int:pk>/update/', MovieUpdateAPIView.as_view(), name='movie-update'),
    path('movies/<int:pk>/delete/', MovieDestroyAPIView.as_view(), name='movie-destroy'),
    
    path('directors/', DirectorListCreateAPIView.as_view(), name='director-list-create'),
    path('directors/<int:pk>/', DirectorRetrieveAPIView.as_view(), name='director-retrieve'),
    path('directors/<int:pk>/update/', DirectorUpdateAPIView.as_view(), name='director-update'),
    path('directors/<int:pk>/delete/', DirectorDestroyAPIView.as_view(), name='director-destroy'),
    
    path('movie_complete/', AddMovieDirector.as_view(), name='add-movie-director')
]