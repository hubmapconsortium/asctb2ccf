from rdflib.term import URIRef
from asctb2ccf.namespace import DefinedNamespace, Namespace


class HGNC(DefinedNamespace):
    """
    HGNC Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#ObjectProperty

    # http://www.w3.org/2002/07/owl#DataProperty

    # http://www.w3.org/2002/07/owl#AnnotationProperty

    # http://www.w3.org/2002/07/owl#Class
    gene: URIRef  # gene

    _NS = Namespace("http://purl.bioontology.org/ontology/HGNC/")