from unicodedata import category
from django.test import TestCase
from rest_framework.test import APITestCase

from django_project.apps.category.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category

class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        category1 = Category(
            name="Terror",
            description="Terror muito terror",
            is_active=False
        )

        category2 = Category(
            name="Romance",
            description="Chato"
        )
        repository = DjangoORMCategoryRepository()
        repository.save(category1)
        repository.save(category2)

        url = "/api/categories/"
        response = self.client.get(url)

        print(f'aqui {response.data}')
        expected_data = [
            {
                "id": str(category1.id),
                "name": "Terror",
                "description": "Terror muito terror",
                "is_active": False,
                "created_date": category1.created_date,
                "updated_date": category1.updated_date
            },
            {
                "id": str(category2.id),
                "name": "Romance",
                "description": "Chato",
                "is_active": True,
                "created_date": category2.created_date,
                "updated_date": category2.updated_date
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
