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

    # http://www.w3.org/2002/07/owl#DataProperty

    # http://www.w3.org/2002/07/owl#AnnotationProperty

    # http://www.w3.org/2002/07/owl#Class
    UBERON_0001062: URIRef  # anatomical entity
    CL_0000000: URIRef      #cell

    _NS = Namespace("http://purl.obolibrary.org/obo/")