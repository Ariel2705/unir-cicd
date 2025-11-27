import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError

import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.base_url = BASE_URL.rstrip('/') if BASE_URL else None
        if not self.base_url:
            from app.api import api_application

            self.client = api_application.test_client()

    def fetch(self, path):
        if self.base_url:
            url = f"{self.base_url}{path}"
            return urlopen(url, timeout=DEFAULT_TIMEOUT)

        resp = self.client.get(path)

        class R:
            def __init__(self, resp):
                self._resp = resp

            @property
            def status(self):
                return self._resp.status_code

            def read(self):
                return self._resp.get_data()
            
            @property
            def body(self):
                return self._resp.get_data().decode().strip()

        return R(resp)

    def test_api_add(self):
        fetch = self.fetch("/calc/add/2/2")
        self.assertEqual(fetch.status, http.client.OK, "Error en la petición API")
        
    def test_api_add_invalid_inputs_return_400(self):
        fetch = self.fetch("/calc/add/2/a")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Operator cannot be converted to number", fetch.body)        

    def test_api_subtract(self):
        fetch = self.fetch("/calc/subtract/6/2")
        self.assertEqual(fetch.status, http.client.OK, "Error en la petición API")
    
    def test_api_subtract_invalid_inputs_return_400(self):
        fetch = self.fetch("/calc/subtract/pruebas/54")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Operator cannot be converted to number", fetch.body)  

    def test_api_divide(self):
        fetch = self.fetch("/calc/divide/6/2")
        self.assertEqual(fetch.status, http.client.OK, "Error en la petición API")
    
    def test_api_divide_invalid_inputs_return_400(self):
        fetch = self.fetch("/calc/divide/pruebas/54")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Operator cannot be converted to number", fetch.body)  

    def test_api_divide_by_zero_returns_400(self):
        fetch = self.fetch("/calc/divide/1/0")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Division by zero", fetch.body)

    def test_api_multiply(self):
        fetch = self.fetch("/calc/multiply/3/4")
        self.assertEqual(fetch.status, http.client.OK, "Error en la petición API")
    
    def test_api_multiply_invalid_inputs_return_400(self):
        fetch = self.fetch("/calc/multiply/pruebas/54")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Operator cannot be converted to number", fetch.body)  

    def test_api_power(self):
        fetch = self.fetch("/calc/power/2/3")
        self.assertEqual(fetch.status, http.client.OK, "Error en la petición API")
    
    def test_api_power_invalid_inputs_return_400(self):
        fetch = self.fetch("/calc/power/pruebas/54")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Operator cannot be converted to number", fetch.body)  

    def test_api_sqrt_and_log10(self):
        fetch = self.fetch("/calc/sqrt/9")
        self.assertEqual(fetch.status, http.client.OK, "Error en la petición API")

        fetch = self.fetch("/calc/log10/100")
        self.assertEqual(fetch.status, http.client.OK, "Error en la petición API")

    def test_api_sqrt_invalid_inputs_return_400(self):
        fetch = self.fetch("/calc/sqrt/-1")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Square root of negative", fetch.body)

        fetch = self.fetch("/calc/sqrt/abc")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Operator cannot be converted to number", fetch.body)

    def test_api_log10_invalid_inputs_return_400(self):
        fetch = self.fetch("/calc/log10/0")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Logarithm base 10 requires a positive number", fetch.body)

        fetch = self.fetch("/calc/log10/-10")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Logarithm base 10 requires a positive number", fetch.body)

        fetch = self.fetch("/calc/log10/xyz")
        self.assertEqual(fetch.status, http.client.BAD_REQUEST)
        self.assertIn("Operator cannot be converted to number", fetch.body)
