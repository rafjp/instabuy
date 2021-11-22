from datetime import datetime
import urllib.parse
import json
import requests
from instabuy.instabuy import *


class Product:
    """
    Product info for ERP integration.
    """

    def __init__(self):
        self.internal_code = ''
        self.name = ''
        self.price = 0.0
        self.visible = False
        self.stock = 0
        self.barcodes = []
        self.promo_price = 0.0
        self.promo_start_at = datetime.utcnow()
        self.promo_end_at = datetime.utcnow()

    def __str__(self):
        return str(self.dict_object())

    def dict_object(self):
        info = dict(self.__dict__)
        info['name'] = urllib.parse.quote(self.name)
        info['promo_start_at'] = self.promo_start_at.isoformat()
        info['promo_end_at'] = self.promo_end_at.isoformat()
        return info


class Driver(list):
    """
    Product queue.
    """

    def load(self):
        """
        Loads products from somewhere. Expects a generator.
        """
        pass

    def put(self):
        """
        Send current products to the server.
        """

        if not self:
            return

        payload = {
                'products': [product.dict_object() for product in self]
            }

        response = requests.put(
            Instabuy.rest_admin_api + 'products', json.dumps(payload), headers=Instabuy.common_header()
        )

        if 200 <= response.status_code < 300:
            response_json = response.json()
            data = json.loads(response.content)['data']
            print('Data status: %s, items count: %s' % (response_json['status'], data['count']))
            print('Updated: %s, Registered: %s, Created: %s' % (data['updated'], data['registered'], data['created']))
        else:
            print('Request error: %s' % str(response.status_code))

        self.clear()
        return response

    def auto_load(self, products_by_request):
        """
        Load and send x products to the server.
        :param products_by_request: Products count to send by request.
        """

        counter = 0
        for row in self.load():
            counter += 1

            if 0 < products_by_request <= counter:
                counter = 0
                self.put()

        self.put()
