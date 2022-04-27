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
    version_tag = args.version_tag

    if args.cell_biomarkers_only:
        response = client.get_json_data(organ_name, version_tag)
        for index, data_item in enumerate(response['data']):
            try:
                o = o.mutate_cell_biomarker(data_item)
            except ValueError as e:
                logging.warning(str(e) +
                    f', row {index}, in <spreadsheet> {organ_name}')
    else:
        # Construct the ontology base
        response = client.get_jsonld_data(organ_name, version_tag)
        for data_item in response:
            o = o.mutate_biological_structure(data_item)

        # Enrich the ontology base with cell location annotations
        response = client.get_json_data(organ_name, version_tag)
        for index, data_item in enumerate(response['data']):
            try:
                o = o.mutate_cell_name(data_item)
                o = o.mutate_cell_hierarchy(data_item)
                o = o.mutate_cell_location(data_item)
            except ValueError as e:
                logging.warning(str(e) +
                    f', row {index}, in <spreadsheet> {organ_name}')
    o.serialize(args.output)
