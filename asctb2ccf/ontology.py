from asctb2ccf.namespace import OBO, CCF

from string import punctuation
from stringcase import lowercase, snakecase

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, DCTERMS
from rdflib.extras.infixowl import Ontology, Property, Class, Restriction,\
    BNode, BooleanClass

import re


class BSOntology:
    """CCF Biological Structure Ontology
    Represents the Biological Structure Ontology graph that can
    be mutated by supplying the ASCT+B table data
    """
    def __init__(self, graph=None):
        self.graph = graph

    @staticmethod
    def new(ontology_iri):
        g = Graph()
        g.bind('ccf', CCF)
        g.bind('obo', OBO)
        g.bind('owl', OWL)
        g.bind('dcterms', DCTERMS)

        # Ontology properties
        Ontology(identifier=URIRef(ontology_iri), graph=g)

        # Some definitions
        Class(CCF.characterizing_biomarker_set, graph=g)
        Property(DCTERMS.references,
                 baseType=OWL.AnnotationProperty,
                 graph=g)

        return BSOntology(g)

    def mutate(self, obj):
        """
        """
        ######################################################
        # Construct the axioms about anatomical structures
        ######################################################
        anatomical_structures = obj['anatomical_structures']
        if not anatomical_structures:
            raise ValueError("Anatomical structure data are missing")
        last_anatomical_structure = anatomical_structures[-1]
        anatomical_structure_id = last_anatomical_structure['id']
        iri = URIRef(self._expand_uberon_id(anatomical_structure_id))
        label = Literal(last_anatomical_structure['rdfs_label'])
        anatomical_structure = Class(iri, graph=self.graph)
        self.graph.add((iri, RDFS.label, label))

        ######################################################
        # Construct the axioms about cell types
        ######################################################
        cell_types = obj['cell_types']
        if not cell_types:
            raise ValueError("Cell type data are missing")

        last_cell_type = cell_types[-1]
        cell_type_id = last_cell_type['id']
        if not cell_type_id:
            raise ValueError("Cell type has empty identifier")
        cell_type_label = last_cell_type['rdfs_label']
        if not cell_type_label:
            raise ValueError("Cell type has empty label")

        cell_type_iri = URIRef(self._expand_cl_id(cell_type_id))
        label = Literal(last_cell_type['rdfs_label'])
        cell_type = Class(cell_type_iri, graph=self.graph)
        self.graph.add((cell_type_iri, RDFS.label, label))

        ######################################################
        # Construct the "cell type 'located in' anatomical_entity" axiom
        ######################################################
        cell_type.subClassOf =\
            [self._some_values_from(OBO.RO_0001025, anatomical_structure)]

        ######################################################
        # Construct the characterizing biomarker set class
        ######################################################
        characterizing_biomarker_set_label =\
            "characterizing biomarker set of " + cell_type_label
        iri = URIRef(CCF._NS + snakecase(
            self._remove_punctuations(
                lowercase(characterizing_biomarker_set_label))))
        label = Literal(characterizing_biomarker_set_label)

        characterizing_biomarker_set = Class(iri, graph=self.graph)
        self.graph.add((iri, RDFS.label, label))
        characterizing_biomarker_set.subClassOf =\
            [CCF.characterizing_biomarker_set]

        ######################################################
        # Construct the "cell type 'has gene marker' gene" axioms
        ######################################################
        for marker in obj['biomarkers_gene']:
            if marker:
                marker_iri = marker['id']
                marker_name = marker['name']
                iri = URIRef(marker_iri)
                label = Literal(marker_name)
                cls_gm = Class(iri, graph=self.graph)
                self.graph.add((iri, RDFS.label, label))
                cell_type.subClassOf =\
                    [self._some_values_from(
                        CCF.cell_type_has_gene_marker,
                        cls_gm)]
                cls_gm.subClassOf =\
                    [self._some_values_from(
                        CCF.is_gene_marker_of_cell_type,
                        cell_type)]

        ######################################################
        # Construct the "cell type 'has protein marker' gene" axioms
        ######################################################
        for marker in obj['biomarkers_protein']:
            if marker:
                marker_iri = marker['id']
                marker_name = marker['name']
                iri = URIRef(marker_iri)
                label = Literal(marker_name)
                cls_pm = Class(iri, graph=self.graph)
                self.graph.add((iri, RDFS.label, label))
                cell_type.subClassOf =\
                    [self._some_values_from(
                        CCF.cell_type_has_protein_marker,
                        cls_pm)]
                cls_pm.subClassOf =\
                    [self._some_values_from(
                        CCF.is_protein_marker_of_cell_type,
                        cell_type)]

        ######################################################
        # Construct the "cell type 'has protein marker' gene" axioms
        ######################################################
        biomarkers = obj['biomarkers']
        characterizing_biomarker_set.equivalentClass =\
            [BooleanClass(
                operator=OWL.intersectionOf,
                members=[self._some_values_from(
                    CCF.has_member,
                    Class(
                        URIRef(marker['id']), graph=self.graph
                    )) for marker in biomarkers],
                graph=self.graph
            )]

        characterizing_biomarker_set_expression =\
            self._some_values_from(
                CCF.cell_type_has_characterizing_biomarker_set,
                characterizing_biomarker_set)
        cell_type.subClassOf = [characterizing_biomarker_set_expression]

        ######################################################
        # Construct the reference annotation
        ######################################################
        references = obj['references']
        if references:
            bn = BNode()
            self.graph.add((bn, RDF.type, OWL.Axiom))
            self.graph.add((bn, OWL.annotatedSource,
                           cell_type_iri))
            self.graph.add((bn, OWL.annotatedProperty,
                           RDFS.subClassOf))
            self.graph.add((bn, OWL.annotatedTarget,
                           characterizing_biomarker_set_expression
                           .identifier))
            for reference in references:
                if 'doi' in reference:
                    doi = reference['doi']
                    if doi is None:
                        continue
                    if "doi:" in doi or "DOI:" in doi:
                        iri = URIRef(self._expand_doi(doi))
                        self.graph.add((bn, DCTERMS.references, iri))

        return BSOntology(self.graph)

    def _some_values_from(self, property, filler):
        return Restriction(property,
                           someValuesFrom=filler,
                           graph=self.graph)

    def _remove_punctuations(self, str):
        punctuation_excl_dash = punctuation.replace('-', '')
        return str.translate(str.maketrans('', '', punctuation_excl_dash))

    def _expand_uberon_id(self, str):
        uberon_pattern = re.compile("UBERON:", re.IGNORECASE)
        return uberon_pattern.sub(
            "http://purl.obolibrary.org/obo/UBERON_", str)

    def _expand_cl_id(self, str):
        cl_pattern = re.compile("CL:", re.IGNORECASE)
        return cl_pattern.sub(
            "http://purl.obolibrary.org/obo/CL_", str)

    def _expand_doi(self, str):
        doi_pattern = re.compile("doi:\\s*", re.IGNORECASE)
        return doi_pattern.sub("http://doi.org/", str)

    def serialize(self, destination):
        """
        """
        self.graph.serialize(format='application/rdf+xml',
                             destination=destination)
