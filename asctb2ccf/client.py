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

    def get_data_by_gsheet_url(self,
                               gsheet_url,
                               format="json"):
        """Returns the ASCT+B table in a specific output format given
           the Google Sheet URL.

        Args:
            gsheet_url (str): The Google Sheet URL that contains
                the ASCT+B table data. Do a copy-and-paste from the
                web browser to get the URL. Make sure the URL
                structure looks like the following example:
                https://docs.google.com/spreadsheets/d/1PgjYp4MEWANfbxGIxFsJ9vkfEU90MP-v3p5oVlH8U-E/edit#gid=949267305
            format (str): The output format (default="json")

        Returns:
            The ASCT+B table in the given output format
        """
        export_csv_url = self._get_export_csv_url_by_gsheet_url(gsheet_url)
        return self._get_data(export_csv_url, format)

    def _get_data(self, export_csv_url, format):
        base_endpoint = f"{self._BASE_URL}/{self._VERSION}/{self._CSV}"
        options = f"{self._OUTPUT}={format}&{self._CSV_URL}={export_csv_url}"
        url = f"{base_endpoint}?{options}"
        response = json_handler(url)
        return response

    def _get_export_csv_url_by_gsheet_url(self, gsheet_url):
        export_url = gsheet_url.replace('edit#', 'export?')
        return quote_plus(f'{export_url}&format=csv')
