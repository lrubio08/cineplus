
# CinePlus

Aplicación web de cartelera de cine hecha con Django. Consume la API de TMDB para mostrar películas, trailers, reparto y actores populares.

Demo: https://cineplus.luisrubiodev.tech

La demo corre en Heroku con SQLite, así que las cuentas de prueba pueden borrarse cuando la aplicación se reinicia.

## Capturas 
<img width="700"  alt="home" src="https://github.com/user-attachments/assets/19be66d4-7f4f-4d29-9122-73b3f39ccb4e" />
<img width="700"  alt="image" src="https://github.com/user-attachments/assets/7c01f495-c701-473f-9660-2a9b84779858" />





## Cómo funciona

- **Sin iniciar sesión:** solo se ve el Home, con un carrusel de películas populares.
- **Con sesión iniciada:** se habilita la **Sala Privada**, donde se listan las películas y, al entrar a una, se ven todos sus detalles: sinopsis, director, género, trailer y reparto.
- **Actores Populares:** listado de actores con su biografía y filmografía.
- **Buscador:** búsqueda de películas por título, y filtro por género.

Los datos de las películas no se guardan en mi base de datos: se piden a TMDB cada vez. En la base solo quedan los usuarios registrados.

## Tecnologías

- Python 3.13 y Django 6
- HTML, CSS, JavaScript y Bootstrap
- API de TMDB (con la librería `requests`)
- Gunicorn y WhiteNoise
- Despliegue en Heroku

## Estructura

```
cineplus/
├── app_moviplus/          # app principal: vistas, plantillas y lógica
├── moviplus/
│   └── settings/
│       ├── base.py        # configuración común
│       ├── development.py # entorno local
│       └── production.py  # entorno de producción (Heroku)
├── static/
├── Procfile
├── requirements.txt
└── manage.py
```

## Ejecutar en local

```bash
git clone https://github.com/lrubio08/cineplus.git
cd cineplus
python -m venv venv
venv\Scripts\activate        # en macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz (no se sube a Git):

```
SECRET_KEY=una-clave-secreta-larga
TMDB_API_KEY=tu_clave_de_tmdb
```

La clave de TMDB se pide gratis en https://www.themoviedb.org/settings/api. Después:

```bash
python manage.py migrate
python manage.py runserver
```

## Despliegue en Heroku

El `Procfile` aplica las migraciones y arranca Gunicorn:

```
web: python manage.py migrate --noinput && gunicorn moviplus.wsgi --log-file -
```

Variables de entorno que hay que cargar en Heroku: `DJANGO_SETTINGS_MODULE`, `SECRET_KEY`, `TMDB_API_KEY`, `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`.

## Problemas que tuve que resolver

- **Trailers con "Error 153" de YouTube.** Django envía por defecto `Referrer-Policy: same-origin` y YouTube exige el encabezado Referer para el reproductor incrustado. Lo arreglé con `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'` en `base.py`.
- **Migrar de un servidor propio a Heroku.** Pasé de MySQL a SQLite para la demo, saqué las claves a variables de entorno y configuré WhiteNoise para los archivos estáticos.

## Atribución

This product uses the TMDB API but is not endorsed or certified by TMDB.

## Autor

* Luis Rubio, desarrollador Full Stack Python.
* Portafolio: https://luisrubiodev.tech/
* GitHub: https://github.com/lrubio08
* LinkedIn: [https://www.linkedin.com/in/luis-rubio-ramirez/](https://www.linkedin.com/in/luis-rubio-ram%C3%ADrez/)
