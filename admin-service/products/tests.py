from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product, User


class ProductViewSetTests(APITestCase):

    def setUp(self) -> None:
        Product.objects.create(title='title1', image='image1', likes=1)
        Product.objects.create(title='title2', image='image2', likes=2)

    def test_create(self) -> None:
        data = dict(title='title_test', image='image_test')
        response = self.client.post(reverse('product-list'), data=data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_list(self) -> None:
        response = self.client.get(reverse('product-list'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))

    def test_retrieve(self) -> None:
        response = self.client.get(reverse('product-detail', args=[1]), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update(self) -> None:
        product = Product.objects.create(title='title_to_update', image='image_to_update', likes=0)
        data = dict(title='title_updated', image='image_updated', likes=3)
        response = self.client.put(reverse('product-detail', args=[product.id]), data=data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data.get('title'), response.data.get('title'))
        self.assertEqual(data.get('image'), response.data.get('image'))
        self.assertEqual(data.get('likes'), response.data.get('likes'))

    def test_delete(self) -> None:
        product = Product.objects.create(title='title_to_delete', image='image_to_delete', likes=5)
        response = self.client.delete(reverse('product-detail', args=[product.id]), format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())


class UserAPIViewTests(APITestCase):

    def test_get_user(self) -> None:
        User.objects.create(id=1)
        User.objects.create(id=2)
        User.objects.create(id=3)
        response = self.client.get(reverse('user-detail'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn(response.data.get('id'), [1, 2, 3])
