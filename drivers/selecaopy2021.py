from datetime import datetime
from instabuy.store import product
from locale import atof
import csv


class ProductsPyDev2021(product.Driver):
    """
    Seleção py Dev 2021, integration
    """

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'r', encoding='utf-8')
        self.reader = csv.reader(self.file, delimiter=';')

        # Skip header
        next(self.reader)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def load(self):
        """
        Load products from csv file into the queue.
        :return: The returned object is an iterator. Each iteration returns a product from the CSV file.
        """

        for raw_data in self.reader:
            new_product = product.Product()

            new_product.internal_code = raw_data[0]
            new_product.name = raw_data[2].strip()
            try:
                new_product.price = atof(raw_data[3])
            except ValueError as e:
                new_product.price = 0
                # print('Price parser error' + str(e))

            new_product.visible = raw_data[7].strip().lower() in 'true'
            try:
                new_product.stock = int(raw_data[6])
            except ValueError as e:
                new_product.stock = 0
                # print('Stock parser error' + str(e))

            new_product.barcodes = [raw_data[1].strip()]
            try:
                new_product.promo_price = atof(raw_data[4])
            except ValueError as e:
                new_product.promo_price = 0
                # print('Promo price parser error' + str(e))

            new_product.promo_end_at = None

            promo_date_end = raw_data[5].strip().title()
            date_parser_error = ''
            if len(promo_date_end) > 0:

                try:
                    new_product.promo_end_at = datetime.strptime(promo_date_end, '%d-%b-%y')

                except ValueError as e:
                    date_parser_error = '1: ' + str(e)

                    try:
                        new_product.promo_end_at = datetime.strptime(promo_date_end, '%d-%b-%Y')

                    except ValueError as e:
                        date_parser_error += ' - 2: ' + str(e)

            if new_product.promo_end_at is None:
                new_product.promo_end_at = datetime.utcnow()
                # print('Date parser error: %s, product code: %d' % (date_parser_error, new_product.internal_code))

            self.append(new_product)
            yield new_product
