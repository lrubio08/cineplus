from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistroTests(TestCase):
    def test_registro_exitoso(self):
        response = self.client.post(reverse('registro'), {'username': 'testuser', 'password1': 'testpassword123', 'password2': 'testpassword123'})
        self.assertEqual(response.status_code, 302)  # Verifica que la respuesta sea un redireccionamiento (éxito)

        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)  # Verifica que el usuario se haya creado en la base de datos

