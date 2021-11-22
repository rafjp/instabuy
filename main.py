"""
Instabuy seleção pydev 2021
https://docs.instabuy.com.br/admin.html#product-properties
"""

from instabuy.instabuy import *
from drivers.selecaopy2021 import *


def one_by_one():
    """
    An example, reading and sending one CSV row by request.
    """

    with ProductsPyDev2021('resources/data2.csv') as driver:
        for row in driver.load():
            if input('%s\nInclude?: ' % str(row)) in ('true', 't', 'yes', 'y'):
                driver.put()
            else:
                driver.clear()


def fully_load():
    """
    Sending all products from the CSV file.
    """

    with ProductsPyDev2021('resources/data.csv') as driver:
        """
        Sending requests with 1024 products at a time, 0 means trying to send all products in the current queue.
        """

        driver.auto_load(1024)


def main():
    Instabuy.load_config()
    fully_load()


if __name__ == '__main__':
    main()

