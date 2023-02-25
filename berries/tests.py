from django.test import TestCase

# Create your tests here.

# berries/tests.py

from rest_framework.test import APITestCase


class AllBerryStatsViewTestCase(APITestCase):
    def test_all_berry_stats(self):
        response = self.client.get('/allBerryStats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('berries_names', response.data)
        self.assertIn('min_growth_time', response.data)
