from rdflib.term import URIRef
from asctb2ccf.namespace import DefinedNamespace, Namespace


class CCF(DefinedNamespace):
    """
    CCF Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#ObjectProperty
    has_marker_component: URIRef

    # http://www.w3.org/2002/07/owl#DataProperty

    # http://www.w3.org/2002/07/owl#AnnotationProperty
    ccf_pref_label: URIRef
    ccf_part_of: URIRef
    ccf_located_in: URIRef
    ccf_characterizes: URIRef
    ccf_asctb_type: URIRef
    ccf_ct_isa: URIRef
    ccf_is_provisional: URIRef

    # http://www.w3.org/2002/07/owl#Class
    anatomical_structure: URIRef
    cell_type: URIRef
    biomarker: URIRef
    characterizing_biomarker_set: URIRef

    _NS = Namespace("http://purl.org/ccf/")