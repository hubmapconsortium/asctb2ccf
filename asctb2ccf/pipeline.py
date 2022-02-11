import logging

from asctb2ccf.client import AsctbReporterClient
from asctb2ccf.ontology import BSOntology


def run(args):
    """
    """
    client = AsctbReporterClient({
        'BoneMarrow': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1tnqtCAWSA6atiUBUOOjAHdOrjDw_fsIoCd5RkAmw310/edit#gid=771476671',
            'latest': 'https://docs.google.com/spreadsheets/d/16MUBNsMrE1kAyoY1sjCKsGSIHCRw7TnwTys8DHM17j0/edit#gid=771476671'
        },
        'Brain': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1TiwW1NZJ5kdCzJ4zwCpY3Gzv3WE5WUoBDWIAkU5gXd0/edit#gid=2056967441',
            'latest': 'https://docs.google.com/spreadsheets/d/1Dzbu_yNfQ-AyOgiScZq7rcoG4oINqO1qEU-MnEE4mPw/edit#gid=2056967441'
        },
        'Blood': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1ZYcSWnFHmzR9XKy_002f_oA4PfzokiW4IxkaZZOusvg/edit#gid=360436225',
            'latest': 'https://docs.google.com/spreadsheets/d/1LRgU3VGi7Jlxh4EtHZaQiHtzcPYvvxYLGXrMB6oxdvQ/edit#gid=543201897'
        },
        'Eye': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1u7IbxnPABRpYL5rFxOba8cmlvG1yGp-dwD3TV3V26K4/edit#gid=44026578',
            'latest': 'https://docs.google.com/spreadsheets/d/1SFGfjkZeDxY_9FaQqNERzq4XRjWDUpwKC9FCqONlbuk/edit#gid=695483621'
        },
        'FallopianTube': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/16tAvAmjwKwbq5SDz7UZ-T1N_KUHRGqPDbMqffFuInMI/edit#gid=1739942440',
            'latest': 'https://docs.google.com/spreadsheets/d/1DFGmDSU75eMF6Fgwzk7W2u20DGJRdXN00TP7sO3kTug/edit#gid=991519552'
        },
        'Heart': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1UhEZpDxQLCJLLx0gnWYDMQP8M-dwjZo_vIyPfjBCcVM/edit#gid=1759721736',
            'latest': 'https://docs.google.com/spreadsheets/d/1eSzDzv_wOpMGTrSShmy_S7IXs8_H_Kp3QZg-gfKyUWk/edit#gid=1759721736'
        },
        'Kidney': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1PgjYp4MEWANfbxGIxFsJ9vkfEU90MP-v3p5oVlH8U-E/edit#gid=949267305',
            'latest': 'https://docs.google.com/spreadsheets/d/1NMfu1bEGNFcTYTFT-jCao_lSbFD8n0ti630iIpRj-hw/edit#gid=949267305'
        },
        'Knee': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1QidDho8DxBYjsxaqApiIZA__Z7aWnB61KvC422g2kx8/edit#gid=1824489301',
            'latest': 'https://docs.google.com/spreadsheets/d/1zDCnaoMdSx09OGxjeeG2Sxokw4c_0bnNyDOJC6IMPCw/edit#gid=1815525900'
        },
        'LargeIntestine': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1vU6mQmnzAAxctbNYPoFxJ8NvbUql8pbipsGdt7YCOQQ/edit#gid=2043181688',
            'latest': 'https://docs.google.com/spreadsheets/d/1d_KWKnQq3HT5nzDmfhlvFG4P_qdviu0vyhGZ6QHgNIk/edit#gid=2043181688'
        },
        'Liver': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1tPDKw_znxqWhZYPTeVN4AN2_F4-JecsdeUgp2lj4P8g/edit#gid=1460762432',
            'latest': 'https://docs.google.com/spreadsheets/d/1F8ZXt1naE1pJFjfsAd6wK7x22D3qRW5O0E2d9gUKAik/edit#gid=1694828397'
        },
        'Lung': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1OBw0k7PUclVX2oG-L1Qx3LQCDb03tyn-rquMOJFN5uo/edit#gid=1523836586',
            'latest': 'https://docs.google.com/spreadsheets/d/1iF4vx9EuQ2tQMBOm6awd9sf-2e_EHsPlcgzrF_YDtis/edit#gid=1523836586'
        },
        'LymphNode': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1aK9gJ2_kMb2B8zrQgScDgxpEWAcCs7kl-gnQGwV3LHM/edit#gid=1223566381',
            'latest': 'https://docs.google.com/spreadsheets/d/1_VWj_dD1dbmnBf8t0wptXvpy1oyyllZ1tXc0aKo2MSA/edit#gid=1223566381'
        },
        'LymphVasculature': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1SILRNUI71BEVWl1fpsi_32DSuSA-bAPgXv5pTfKnrOE/edit#gid=1700987638',
            'latest': 'https://docs.google.com/spreadsheets/d/1FNoQthhgP0OXEZuwIVL0XZA8SVYzCcVPm4_n20dt--8/edit#gid=2087685463'
        },
        'Ovary': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1FE2XufrruExUWqcai3XRFqtMjeEdzoLKJ-YNa-nRZ1M/edit#gid=1997082517',
            'latest': 'https://docs.google.com/spreadsheets/d/1K5LWhMaT_IryNxuK1Vko0Ud49VUB8RnMltL5jYhJUak/edit#gid=756296951'
        },
        'Pancreas': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1CIWqIygz2OzxMECIvhudFN14Kt7-JFUBLpzn5uuH5Xs/edit#gid=801179416',
            'latest': 'https://docs.google.com/spreadsheets/d/1_cmA0CWUzVz1lNMpNOXqzrnmWgXv3GANqN7W18N4crA/edit#gid=439021026'
        },
        'Peripheral_nervous_system': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1KifiEDn3PpJ8pjz9_ka4TWkT085wLIzIQP5NKSvb2Ac/edit#gid=714133140',
            'latest': 'https://docs.google.com/spreadsheets/d/1TQsd657v-Jfcme4ftmpq7Zaegu0HxHOmGJKUPL8QqyU/edit#gid=917578386'
        },
        'Prostate': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1_O5yXOesG93dobMHRSIvVAt9xj7mDnEAYdRJcHYJ84U/edit#gid=1757780481',
            'latest': 'https://docs.google.com/spreadsheets/d/1hlSptGNXzyM7vxsH930YMf6gZkHVgHUE-Qc_4uFAmoU/edit#gid=1239199370'
        },
        'Skin': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1Pmi3g26vhbg9HU6GDpIvxKbIP985JM-5eytOHxJUdZs/edit#gid=269383687',
            'latest': 'https://docs.google.com/spreadsheets/d/16E07Ia3opnjBzBVswS7iQccd2Y_fw7m8-mNUNjwv80E/edit#gid=269383687'
        },
        'Small_intestine': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1Xlds8FzZ8ecmy3cxYJt1ijQC9FifamZRZ5KzH4Yt-MQ/edit#gid=1762589435',
            'latest': 'https://docs.google.com/spreadsheets/d/1pZDLDiAHD-QDi-OTF4GtUHf6bkKkDc2qc0eIFnIqS_s/edit#gid=247140941'
        },
        'Spleen': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1HL7aHx5A2KOa1KsJ0PIagqxdshVavFIEJZP6_YDtUww/edit#gid=69626346',
            'latest': 'https://docs.google.com/spreadsheets/d/1bairJs37srg0hF4MGIfsdtb000YtrA1hI45D8KI5Gxc/edit#gid=69626346'
        },
        'Thymus': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1nSiz2yFDMJSqIXbnAP_EXIQZfN6ZflOs-WBdZ6LVhUY/edit#gid=863370556',
            'latest': 'https://docs.google.com/spreadsheets/d/14KY4dp6YwVf0GSiCOcxhuy9L_aJ8FjTX_jidrIq7E_c/edit#gid=863370556'
        },
        'Ureter': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1ivVU53FPInUwK4ZIha8YUvJM_8keizoJGaM3rT-TZRY/edit#gid=676299490',
            'latest': 'https://docs.google.com/spreadsheets/d/1ZUmHX22NYMfBgFoni4zK6bsEYFn4rGSk9oYBNPcebZQ/edit#gid=73126811'
        },
        'Urinary_bladder': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1ohOG5jMf9d9eqjbVK6_u3CvgfG3wcLfs_pxB2838wOo/edit#gid=1342577957',
            'latest': 'https://docs.google.com/spreadsheets/d/1iCZpti7fYupWhQjDz_tE01ii2WH23hIno9kYggMjDZo/edit#gid=1057183099'
        },
        'Uterus': {
            'v1.0': 'https://docs.google.com/spreadsheets/d/1yEcbJMrUIzJY-4JNtF1Y_eUpAQsgKF6DX2-5Z3UXBeE/edit#gid=1434605386',
            'latest': 'https://docs.google.com/spreadsheets/d/1RasOQCB4oP_1kvZL7Xv40TID6_365FQ-cgX2fGR54gw/edit#gid=603441642'
        },
        'Blood_vasculature': {
            'v1.1': 'https://docs.google.com/spreadsheets/d/1IlELzPwpWoHUcDAmNBWofXfislAaF_oR8yVpwy-zl18/edit#gid=997949803',
            'latest': 'https://docs.google.com/spreadsheets/d/1pBO70FENOlSyPJukxHYjeMXW0SYTLj4lbcw2oGsjuf0/edit#gid=1789898267'
        }
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
