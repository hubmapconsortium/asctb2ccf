from rdflib.term import URIRef
from asctb2ccf.namespace import DefinedNamespace, Namespace


class OBO(DefinedNamespace):
    """
    OBO Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#ObjectProperty
    RO_0001025: URIRef  # located_in
    RO_0015004: URIRef  # has characterizing marker set
    SO_0001260: URIRef  # sequence_collection

    # http://www.w3.org/2002/07/owl#DataProperty

    # http://www.w3.org/2002/07/owl#AnnotationProperty
    IAO_0000115: URIRef  # definition

    # http://www.w3.org/2002/07/owl#Class
    UBERON_0001062: URIRef  # anatomical entity
    CL_0000000: URIRef      #cell

    _NS = Namespace("http://purl.obolibrary.org/obo/")