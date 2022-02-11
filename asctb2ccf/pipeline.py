import logging

from asctb2ccf.client import AsctbReporterClient
from asctb2ccf.ontology import BSOntology


def run(args):
    """
    """
    client = AsctbReporterClient({
        'BoneMarrow': {
            'version': '1.1',
            'id_comp': [
                '1tnqtCAWSA6atiUBUOOjAHdOrjDw_fsIoCd5RkAmw310',
                '771476671']
        },
        'Brain': {
            'version': '1.1',
            'id_comp': [
                '1TiwW1NZJ5kdCzJ4zwCpY3Gzv3WE5WUoBDWIAkU5gXd0',
                '2056967441']
        },
        'Blood': {
            'version': '1.1',
            'id_comp': [
                '1ZYcSWnFHmzR9XKy_002f_oA4PfzokiW4IxkaZZOusvg',
                '360436225']
        },
        'Eye': {
            'version': '1.0',
            'id_comp': [
                '1u7IbxnPABRpYL5rFxOba8cmlvG1yGp-dwD3TV3V26K4',
                '44026578']
        },
        'Fallopian_tube': '1417514103',  # Fallopian_Tube_v1.0
        'Heart': '2133445058',  # Heart_v1.1
        'Kidney': {
            'version': '1.1',
            'id_comp': [
                '1PgjYp4MEWANfbxGIxFsJ9vkfEU90MP-v3p5oVlH8U-E',
                '949267305']
        },
        'Knee': '1572314003', # Knee_v1.0
        'Large_intestine': '512613979', # Large_Intestine_v1.1
        'Liver': '2079993346', # Liver_v1.0
        'Lung': '1824552484', # Lung_v1.1
        'Lymph_node': '1440276882', # Lymph_Node_v1.1
        'Lymph_vasculature': '598065183', # Lymph_Vasculature_v1.0
        'Ovary': '1072160013', # Ovary_v1.0
        'Pancreas': '1044871154', # Pancreas_v1.0
        'Peripheral_nervous_system': '887132317', # Peripheral_Nervous_System_v1.0
        'Prostate': '1921589208', # Prostate_v1.0
        'Skin': '1158675184', # Skin_v1.1
        'Small_intestine': '1247909220', # Small_Intestine_v1.0
        'Spleen': '984946629', # Sleen_v1.1
        'Thymus': '1823527529', # Thymus_v1.1
        'Ureter': '1106564583', # Ureter_v1.0
        'Urinary_bladder': '498800030', # Urinary_Bladder_v1.0
        'Uterus': '877379009', # Uterus_v1.0
        'Blood_vasculature': '361657182' # Blood_Vasculature_v1.1
    })

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
