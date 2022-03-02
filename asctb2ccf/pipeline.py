import json
import logging
import pkg_resources

from asctb2ccf.client import AsctbReporterClient
from asctb2ccf.ontology import BSOntology


def run(args):
    """
    """
    res_file = pkg_resources.\
        resource_stream("asctb2ccf",
                        "asctb-gid.json")
    gid_map = json.load(res_file)
    client = AsctbReporterClient(gid_map)

    o = BSOntology.new(args.ontology_iri)
    organ_name = args.organ_name

    if args.cell_biomarkers_only:
        response = client.get_json_data(organ_name)
        for index, data_item in enumerate(response['data']):
            try:
                o = o.mutate_cell_biomarker(data_item)
            except ValueError as e:
                logging.warning(str(e) +
                    f', row {index}, in <spreadsheet> {organ_name}')
    else:
        response = client.get_jsonld_data(organ_name)
        for data_item in response:
            o = o.mutate_biological_structure(data_item)

    o.serialize(args.output)
