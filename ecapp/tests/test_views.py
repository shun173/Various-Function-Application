import random

from django.test import TestCase, Client
from django.test.client import encode_multipart
from django.urls import reverse
from django.utils.timezone import localtime
from faker import Faker

from ..models import Product
# from ..views import ProductViewSet
from .factories import ProductFactory, UserFactory

# class EcViewTest(TestCase):
#     def test_sell(self):
#         user = UserFactory()
#         fake = Faker()
#         url = reverse('ecapp:sell')
#         client = Client(enforce_csrf_checks=False)
#         client.force_login(user)
#         data = {
#             'name': fake.word(),
#             'description': fake.text(),
#             'price': random.randint(1, 10000),
#             'amount': random.randint(1, 100),
#             'image': fake.image_url(),
#             'owner': user.email,
#         }
#         response = client.post(url, json.dumps(
#             data), content_type='application/json')

#         self.assertEqual(Product.objects.count(), 1)
#         self.assertEqual(Product.objects.get().name, data['name'])

#     def test_cart(self):
