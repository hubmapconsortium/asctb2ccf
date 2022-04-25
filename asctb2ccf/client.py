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

    def __init__(self, gid_map):
        self.gid_map = gid_map

    def get_json_data(self, organ_name, version_tag="latest"):
        return self.get_data(organ_name, version_tag, "json")

    def get_jsonld_data(self, organ_name, version_tag="latest"):
        return self.get_data(organ_name, version_tag, "jsonld")

    def get_data(self, organ_name, version_tag="latest", format="json"):
        """Returns the ontology resource in a specific format given
           the organ name.

        Args:
            organ_name (str): The human organ name.

        Returns:
            An object containing the ontology resource.
        """
        csvUrl = self.get_export_csv_url(organ_name, version_tag)
        base_endpoint = f'{self._BASE_URL}/{self._VERSION}/{self._CSV}'
        url = f'{base_endpoint}?{self._OUTPUT}={format}&{self._CSV_URL}={csvUrl}'
        response = json_handler(url)

        return response

    def get_export_csv_url(self, organ_name, version_tag="latest"):
        sheet_url = self.gid_map[organ_name][version_tag]
        export_url = sheet_url.replace('edit#', 'export?')
        return quote_plus(f'{export_url}&format=csv')
