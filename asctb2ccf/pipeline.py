import json
import logging
import pkg_resources

from asctb2ccf.client import AsctbReporterClient
from asctb2ccf.ontology import BSOntology


def run(args):
    """
    """
    client = AsctbReporterClient()

    ontology_iri = args.ontology_iri
    gsheet_url = args.gsheet_url
    organ_name = args.organ_name

    o = BSOntology.new(organ_name, ontology_iri)

    if (gsheet_url):
        if args.cell_biomarkers_only:
            response = client.get_data_by_gsheet_url(gsheet_url)
            for index, data_item in enumerate(response['data']):
                try:
                    o = o.mutate_cell_biomarker(data_item)
                except ValueError as e:
                    logging.warning(str(e) +
                        f", row {index}, in <spreadsheet> {organ_name}")
        else:
            response = client.get_data_by_gsheet_url(gsheet_url)
            for index, data_item in enumerate(response['data']):
                try:
                    o = o.mutate_anatomical_structure(data_item)
                    o = o.mutate_cell_type(data_item)
                    o = o.mutate_biomarker(data_item)
                    o = o.mutate_partonomy(data_item)
                    o = o.mutate_cell_hierarchy(data_item)
                    o = o.mutate_cell_location(data_item)
                except ValueError as e:
                    logging.warning(str(e) +
                        f", row {index}, in <spreadsheet> {organ_name}")
    o.serialize(args.output)
