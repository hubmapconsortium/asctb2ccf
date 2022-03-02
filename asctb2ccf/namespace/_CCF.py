from rdflib.term import URIRef
from asctb2ccf.namespace import DefinedNamespace, Namespace


class CCF(DefinedNamespace):
    """
    CCF Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#ObjectProperty
    has_member: URIRef
    located_in: URIRef
    has_characterizing_biomarker_set: URIRef

    # http://www.w3.org/2002/07/owl#DataProperty

    # http://www.w3.org/2002/07/owl#AnnotationProperty
    ccf_part_of: URIRef
    ccf_located_in: URIRef
    ccf_characterizes: URIRef
    ccf_asctb_type: URIRef

    # http://www.w3.org/2002/07/owl#Class
    biomarker: URIRef
    characterizing_biomarker_set: URIRef

    _NS = Namespace("http://purl.org/ccf/")