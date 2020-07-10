import json
import random

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.test.client import encode_multipart
from django.urls import reverse
from django.utils.timezone import localtime
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
# from django.core.serializers import serialize
# from django.core.serializers.json import DjangoJSONEncoder

from ..models import Product
from ..views import ProductViewSet
from .factories import ProductFactory, UserFactory


class ProductApiTest(APITestCase):
    # def test_post(self):
    #     user = UserFactory()
    #     fake = Faker()
    #     url = reverse('product-list')
    #     client = Client(enforce_csrf_checks=False)
    #     client.force_login(user)
    #     data = {
    #         'name': fake.word(),
    #         'description': fake.text(),
    #         'price': random.randint(1, 10000),
    #         'amount': random.randint(1, 100),
    #         'image': fake.image_url(),
    #         'owner': user.id
    #     }
    #     content = encode_multipart('BoUnDaRyStRiNg', data)
    #     content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
    #     response = client.post(url, content, content_type=content_type)

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Product.objects.count(), 1)
    #     self.assertEqual(Product.objects.get().name, data['name'])

    def test_post(self):
        # factory = APIRequestFactory()
        fake = Faker()
        user = UserFactory()
        view = ProductViewSet.as_view({'post': 'create'})
        # data = {
        #     'name': fake.word(),
        #     'description': fake.text(),
        #     'price': random.randint(1, 10000),
        #     'amount': random.randint(1, 100),
        #     'image': fake.file_name(),
        #     'owner': user.id
        # }
        filename = 'test_img'
        file = File(open('static/default_icon.jpg', 'rb'))
        uploaded_file = SimpleUploadedFile(
            filename, file.read(), content_type='multipart/form-data')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            'name': 'a',
            'description': 'a',
            'price': 1,
            'amount': 1,
            'image': uploaded_file,
            'owner': 1
        }
        url = reverse('product-list')
        response = client.post(url, data, format='multipart')
        print(uploaded_file)
        print(response)
        print(response.status_code)
        # content = encode_multipart('BoUnDaRyStRiNg', data)
        # content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        # request = factory.post(url, data, content_type='multipart/form-data')
        # force_authenticate(request, user=user)
        # response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

        product = Product.objects.filter(name=data['name'])[0]
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.description, data['description'])
        self.assertEqual(product.price, data['price'])
        self.assertEqual(product.amount, data['amount'])
        self.assertEqual(product.image, data['image'])
        self.assertEqual(product.owner, data['owner'])

    def test_get(self):
        user = UserFactory()
        product = ProductFactory()
        url = reverse('product-detail', kwargs={'pk': product.id})
        client = Client()
        client.force_login(user)
        response = client.get(url)
        created_at = response.data['created_at'].replace('T', ' ')
        response.data['created_at'] = created_at

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'amount': product.amount,
            'image': 'http://testserver' + product.image.url,
            'owner': product.owner.id,
            'created_at': str(localtime(product.created_at))
        })
