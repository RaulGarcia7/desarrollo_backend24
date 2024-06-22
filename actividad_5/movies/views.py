from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from .serializers import MovieSerializer, DirectorSerializer
from .models import Movie, Director

#Viewsets

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
class DirectorViewSet(viewsets.ModelViewSet):
    queryset= Director.objects.all()
    serializer_class= DirectorSerializer
    
#Generic
    
class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
class MovieRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieUpdateAPIView(generics.UpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDestroyAPIView(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class DirectorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DirectorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DirectorUpdateAPIView(generics.UpdateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DirectorDestroyAPIView(generics.DestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    
    
#API View enlace modelos

class AddMovieDirector(APIView):
    
    def get(self, request):
        movies = Movie.objects.all()
        directors = Director.objects.all()
        movie_serializer = MovieSerializer(movies, many=True)
        director_serializer = DirectorSerializer(directors, many=True)
        return Response({
            'movies': movie_serializer.data,
            'directors': director_serializer.data
        })
    
    def post(self, request):
        movie_data = request.data
        director_data = movie_data.pop('director')
        
        director, created = Director.objects.get_or_create(**director_data)
        movie_data['director'] = director.id
        
        
        serializer = MovieSerializer(data = movie_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

