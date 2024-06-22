from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Movie, Director


class MovieTest(APITestCase):

    def setUp(self):
        self.movie = Movie.objects.create(
            title='Ghostland',
            release_date='2018-03-14',
            genre='Terror'
        )

    def test_create_movie(self):
        url = reverse('movie-list-create')
        data = {"title": "Insidious",
                "release_date": "2011-06-10",
                "genre": "Terror"
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Movie.objects.count(), 2)
        
        created_movie = Movie.objects.get(title="Insidious")
        self.assertEqual(created_movie.title, "Insidious")
        self.assertEqual(created_movie.release_date.strftime('%Y-%m-%d'), '2011-06-10')
        self.assertEqual(created_movie.genre, "Terror")
        
    
    def test_retrieve_movie(self):
        url = reverse('movie-retrieve', args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.movie.title)
        self.assertEqual(response.data['release_date'], str(self.movie.release_date))
        self.assertEqual(response.data['genre'], self.movie.genre)
        
    def test_update_movie(self):
        url = reverse('movie-update', args=[self.movie.id])
        data = {
            "title": "Indiana Jones",
            "release_date": "1981-10-05",
            "genre": "Aventura"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_movie = Movie.objects.get(id = self.movie.id)
        self.assertEqual(updated_movie.title, 'Indiana Jones')
        self.assertEqual(updated_movie.release_date.strftime('%Y-%m-%d'), '1981-10-05')  
        self.assertEqual(updated_movie.genre, 'Aventura')
        
    def test_delete_movie(self):
        url = reverse('movie-destroy', args=[self.movie.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)
        
class MovieViewSetTest(APITestCase):
    
    def setUp(self):
        self.movie = Movie.objects.create(
            title='Ghostland',
            release_date='2018-03-14',
            genre='Terror'
        )
        
    def test_list_movies(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.movie.title)
        
    def test_retrieve_movie(self):
        url = reverse('movie-detail', args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.movie.title)
        
    def test_create_movie(self):
        url = reverse('movie-list')
        data = {
            "title": "Insidious",
            "release_date": "2011-06-10",
            "genre": "Terror"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
        
        created_movie = Movie.objects.get(title="Insidious")
        self.assertEqual(created_movie.title, "Insidious")
        self.assertEqual(created_movie.release_date.strftime('%Y-%m-%d'), '2011-06-10')
        self.assertEqual(created_movie.genre, "Terror")
        
        
    def test_update_movie(self):
        url = reverse('movie-detail', args=[self.movie.id])
        data = {
            "title": "Indiana Jones",
            "release_date": "1981-10-05",
            "genre": "Aventura"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_movie = Movie.objects.get(id = self.movie.id)
        self.assertEqual(updated_movie.title, 'Indiana Jones')
        self.assertEqual(updated_movie.release_date.strftime('%Y-%m-%d'), '1981-10-05')  
        self.assertEqual(updated_movie.genre, 'Aventura')
        
    def test_delete_movie(self):
        url = reverse('movie-detail', args=[self.movie.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)
        
        
class DirectorTest(APITestCase):
    
    def setUp(self):
        self.director = Director.objects.create(
            name='Quentin Tarantino',
            birth_date='1963-03-27',
            nationality='American'
        )
    
    def test_create_director(self):
        url = reverse('director-list-create')
        data = {
            "name": "Martin Scorsese",
            "birth_date": "1942-11-17",
            "nationality": "American"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Director.objects.count(), 2)
        
        created_director = Director.objects.get(name="Martin Scorsese")
        self.assertEqual(created_director.name, "Martin Scorsese")
        self.assertEqual(created_director.birth_date.strftime('%Y-%m-%d'), '1942-11-17')
        self.assertEqual(created_director.nationality, "American")
        
    def test_retrieve_director(self):
        url = reverse('director-retrieve', args=[self.director.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.director.name)
        self.assertEqual(response.data['birth_date'], str(self.director.birth_date))
        self.assertEqual(response.data['nationality'], self.director.nationality)
        
    def test_update_director(self):
        url = reverse('director-update', args=[self.director.id])
        data = {
            "name": "Christopher Nolan",
            "birth_date": "1970-07-30",
            "nationality": "British"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_director = Director.objects.get(id=self.director.id)
        self.assertEqual(updated_director.name, 'Christopher Nolan')
        self.assertEqual(updated_director.birth_date.strftime('%Y-%m-%d'), '1970-07-30')  
        self.assertEqual(updated_director.nationality, 'British')
        
    def test_delete_director(self):
        url = reverse('director-destroy', args=[self.director.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Director.objects.count(), 0)
        
class DirectorViewSetTest(APITestCase):
    
    def setUp(self):
        self.director = Director.objects.create(
            name='Quentin Tarantino',
            birth_date='1963-03-27',
            nationality='American'
        )
        
    def test_list_directors(self):
        url = reverse('director-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.director.name)
        
    def test_retrieve_director(self):
        url = reverse('director-detail', args=[self.director.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.director.name)
        
    def test_create_director(self):
        url = reverse('director-list')
        data = {
            "name": "Martin Scorsese",
            "birth_date": "1942-11-17",
            "nationality": "American"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Director.objects.count(), 2)
        
        created_director = Director.objects.get(name="Martin Scorsese")
        self.assertEqual(created_director.name, "Martin Scorsese")
        self.assertEqual(created_director.birth_date.strftime('%Y-%m-%d'), '1942-11-17')
        self.assertEqual(created_director.nationality, "American")
        
        
    def test_update_director(self):
        url = reverse('director-detail', args=[self.director.id])
        data = {
            "name": "Christopher Nolan",
            "birth_date": "1970-07-30",
            "nationality": "British"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_director = Director.objects.get(id=self.director.id)
        self.assertEqual(updated_director.name, 'Christopher Nolan')
        self.assertEqual(updated_director.birth_date.strftime('%Y-%m-%d'), '1970-07-30')  
        self.assertEqual(updated_director.nationality, 'British')
        
    def test_delete_director(self):
        url = reverse('director-destroy', args=[self.director.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Director.objects.count(), 0)
        
class AddMovieDirectorTest(APITestCase):
    
    def test_get_moviecomplete(self):
        url = reverse('add-movie-director')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('movies', response.data)
        self.assertIn('directors', response.data)
    
    def test_create_movie_complete(self):
        url = reverse('add-movie-director')
        data = {
            "title": "Pulp Fiction",
            "release_date": "1994-05-12",
            "genre": "Drama",
            "director": {
                "name": "Quentin Tarantino",
                "birth_date": "1963-03-27",
                "nationality": "American"
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        