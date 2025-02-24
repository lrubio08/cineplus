
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import random
from .forms import  RegistroForm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

def index(request):
    #obtener lista de peliculas populares
    api_key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1'
    response = requests.get(url)
    data = response.json()
    peliculas = data.get('results', [])
    
    #seleccionar aleatoreamente algunas peliculas 
    random_peliculas = random.sample(peliculas, min(20, len(peliculas)))
    
    context = {'peliculas': random_peliculas}
    return render(request, 'app_moviplus/index.html', context)

    def registro(request):
        try:
            if request.method == 'POST':
                print(f"Datos POST recibidos: {request.POST}")
                form = RegistroForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    print(user)
                    messages.success(request, 'Te has registrado exitosamente. Ahora puedes iniciar sesión.')
                    return redirect('iniciar_sesion')
            else:
                form = RegistroForm()
            return render(request, 'app_moviplus/registro.html', {'form': form})
        except Exception as e:
            print(f"Error en la vista de registro: {e}")
            raise

def registro_exitoso(request):
    return render(request,'app_moviplus/registro_exitoso.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # El inicio de sesión es exitoso, redirigir a la vista sesion_iniciada
            login(request, user)
        else:
            messages.error(request, '¡Nombre de usuario o contraseña incorrectos!')
            return render(request, 'app_moviplus/login.html')
        return redirect('sala_privada')
    return render(request, 'app_moviplus/login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('index')

@login_required
def sala_privada(request):
    api_key = settings.TMDB_API_KEY
    url_generos = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=es'
    response_generos = requests.get(url_generos)
    data_generos = response_generos.json()
    generos = data_generos.get('genres', [])
    
    # diccionario que mapea los IDs de los géneros a sus nombres
    generos_dict = {genero['id']: genero['name'] for genero in generos}
    
    #obtener genero seleccionado
    genero_seleccionado = request.GET.get('genero')
    
    #Si se selecicona un genero obtener las peliculas de ese genero 
    if genero_seleccionado:
        url_peliculas = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=es&with_genres={genero_seleccionado}'
    # si no se selecciona ningun genero obtener las peliculas populares 
    else:
        url_peliculas= f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=es&page=1'
    
    response_peliculas = requests.get(url_peliculas)
    data_peliculas = response_peliculas.json()
    peliculas = data_peliculas.get('results', [])
    
    #seleccionar aleatoreamente algunas peliculas 
    random_peliculas = random.sample(peliculas, min(20, len(peliculas)))
    
    # Se busca  el nombre del género usando el ID en el diccionario
    nombre_genero = generos_dict.get(int(genero_seleccionado)) if genero_seleccionado else None
    
    context = {'peliculas': random_peliculas, 'generos': generos, 'nombre_genero': nombre_genero, 'genero_seleccionado': str(genero_seleccionado)}
    return render(request, 'app_moviplus/sala_privada.html', context)


def obtener_info_pelicula(pelicula_id):
    api_key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/movie/{pelicula_id}?api_key={api_key}&language=es&append_to_response=credits,videos'
    response = requests.get(url)
    data = response.json()
    
    for persona in data.get('credits', {}).get('crew', []):
        if persona.get('job') == 'Director':
            data['director'] = persona.get('name')
            break
    data['genres'] = [genre['name'] for genre in data.get('genres', [])]
    data['runtime'] = data.get('runtime')
    data['vote_average'] = data.get('vote_average')
    return data

def pelicula_seleccionada(request, pelicula_id):
    pelicula = obtener_info_pelicula(pelicula_id)
    trailers = pelicula.get('videos', {}).get('results', [])
    trailer_url = trailers[0]['key'] if trailers else None
    trailers_json = json.dumps(trailers)
    return render(request, 'app_moviplus/pelicula_seleccionada.html', {'pelicula': pelicula,'trailer_url': trailer_url, 'trailers': trailers_json})

def actor(request):
    api_key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/person/popular?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    actores = data.get('results', [])
    # seleccionar aleatoreamente algunas actores
    random_actores = random.sample(actores, min(20, len(actores)) )
    
    context = {'actores': random_actores}
    return render(request, 'app_moviplus/actores.html', context)

def detalles_actor( actor_id):
    api_key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/person/{actor_id}?api_key={api_key}&language=es'
    response = requests.get(url)
    data = response.json()
    return data

def actor_buscado(request, actor_id=None):
    api_key = settings.TMDB_API_KEY

    if actor_id is not None:
        # Acceder directamente por ID
        url = f'https://api.themoviedb.org/3/person/{actor_id}?api_key={api_key}&language=es'
        response = requests.get(url)
        data = response.json()
        actor_buscado = [data]
        query = data.get('name')
    else:
        query = request.GET.get('q')
        # Buscar actor por nombre
        url = f'https://api.themoviedb.org/3/search/person?api_key={api_key}&query={query}'
        response = requests.get(url)
        data = response.json()
        actor_buscado = data.get('results', [])
        if actor_buscado:
            actor_id = actor_buscado[0].get("id")

    # Obtener detalles del actor
    if actor_id:
        actor_detalles = detalles_actor(actor_id)
    else:
        actor_detalles = None

    context = {'actor_buscado': actor_buscado, 'query': query, 'actor_detalles': actor_detalles}
    return render(request, 'app_moviplus/actor_buscado.html', context)

def pelicula_actor (request, actor_id):
    api_key = settings.TMDB_API_KEY

    # Obtener los créditos de las películas del actor
    url_credits = f'https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={api_key}&language=es'
    response_credits = requests.get(url_credits)
    data_credits = response_credits.json()
    peliculas_actor = data_credits.get('cast', [])

    # Obtener los detalles del actor
    url_details = f'https://api.themoviedb.org/3/person/{actor_id}?api_key={api_key}&language=es'
    response_details = requests.get(url_details)
    data_details = response_details.json()
    actor_name = data_details.get('name', '')

    context = {'peliculas_actor': peliculas_actor, 'actor_name': actor_name}
    return render(request, 'app_moviplus/pelicula_actor.html', context)

def ver_reparto(request, pelicula_id):
    pelicula_info = obtener_info_pelicula(pelicula_id)
    reparto = pelicula_info.get('credits', {}).get('cast', [])
    return render(request, 'app_moviplus/reparto.html', {'reparto': reparto, 'pelicula': pelicula_info})

def resultado_busqueda(request):
    query =request.GET.get('q')
    api_key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}'
    response = requests.get(url)
    data = response.json()
    peliculas = data.get('results', [])
    context = {'peliculas': peliculas,  'query': query}
    return render(request, 'app_moviplus/resultado_busqueda.html', context)