from urllib.parse import urlparse, parse_qs, quote_plus
from asctb2ccf.utils import json_handler


class AsctbReporterClient:
    """ASCT+B Reporter API client
    Provides functions to easily access the ASCT+B Reporter API
    (https://asctb-api.herokuapp.com/) in Python.

    Attributes:
        get_ontology: Retrieves the ontology resource in JSON-LD format given
        the organ name.
    """

    _BASE_URL = "https://asctb-api.herokuapp.com"
    _VERSION = "v2"
    _CSV = "csv"
    _OUTPUT = "output"
    _CSV_URL = "csvUrl"

    def __init__(self, organ_to_sheet_dict):
        self.organ_to_sheet_dict = organ_to_sheet_dict

    def get_data(self, organ_name, format="json"):
        """Returns the ontology resource in JSON-LD format given
           the organ name.

        Args:
            organ_name (str): The human organ name.

        Returns:
            An object containing the ontology resource.
        """
        csvUrl = self.get_export_csv_url(organ_name)
        base_endpoint = f'{self._BASE_URL}/{self._VERSION}/{self._CSV}'
        url = f'{base_endpoint}?{self._OUTPUT}={format}&{self._CSV_URL}={csvUrl}'
        response = json_handler(url)

        return response

    def get_export_csv_url(self, organ_name):
        sheet_url = self.organ_to_sheet_dict[organ_name]['latest']
        export_url = sheet_url.replace('edit#', 'export?')
        return quote_plus(f'{export_url}&format=csv')
