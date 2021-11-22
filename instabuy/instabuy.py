from configparser import ConfigParser
import locale


class Instabuy:
    """
    Setup global API static features.
    """

    rest_admin_api: str
    api_key: str

    @staticmethod
    def load_config():
        config_parser = ConfigParser()
        config_parser.read('resources/config.ini')
        Instabuy.rest_admin_api = config_parser.get('api', 'domain')
        Instabuy.api_key = config_parser.get('api', 'api_key')
        locale.setlocale(locale.LC_ALL, config_parser.get('api', 'locale'))

    @staticmethod
    def common_header():
        return {
            'api-key': Instabuy.api_key
        }
