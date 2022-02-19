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

    organ_name = args.organ_name
    response = client.get_data(organ_name)
    o = BSOntology.new(args.ontology_iri)
    for index, data_item in enumerate(response['data']):
        try:
            o = o.mutate(data_item)
        except ValueError as e:
            logging.warning(str(e) +
                f', row {index}, in <spreadsheet> {organ_name}')
    o.serialize(args.output)
