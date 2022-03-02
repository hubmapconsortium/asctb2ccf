from asctb2ccf.namespace import OBO, CCF, OBOINOWL

from string import punctuation
from stringcase import lowercase, snakecase

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, SKOS, DCTERMS
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
        g.bind('skos', SKOS)
        g.bind('dcterms', DCTERMS)

        # Ontology properties
        Ontology(identifier=URIRef(ontology_iri), graph=g)

        # Some definitions
        Property(CCF.has_member, baseType=OWL.ObjectProperty, graph=g)
        Property(CCF.located_in, baseType=OWL.ObjectProperty, graph=g)

        return BSOntology(g)

    def mutate_biological_structure(self, obj):
        """
        """
        obj_type = self._get_object_type(obj)
        if obj_type == "http://www.w3.org/2002/07/owl#Class":
            asctb_type = self._get_asctb_type(obj)
            iri = self._get_term_iri(obj)
            labels = self._get_term_labels(obj)
            pref_labels = self._get_term_prefLabels(obj)
            term_ids = self._get_term_ids(obj)
            object_restrictions = self._get_object_restrictions(obj)
            if asctb_type.eq("AS"):
                self._add_term_to_graph(
                    iri,
                    annotations=[(RDFS.label, labels),
                                 (OBOINOWL.id, term_ids),
                                 (SKOS.prefLabel, pref_labels),
                                 (CCF.ccf_asctb_type, [asctb_type]),
                                 (CCF.ccf_part_of, object_restrictions)])
            elif asctb_type.eq("CT"):
                self._add_term_to_graph(
                    iri,
                    annotations=[(RDFS.label, labels),
                                 (OBOINOWL.id, term_ids),
                                 (SKOS.prefLabel, pref_labels),
                                 (CCF.ccf_asctb_type, [asctb_type]),
                                 (CCF.ccf_located_in, object_restrictions)])
            elif asctb_type.eq("gene") or asctb_type.eq("protein"):
                self._add_term_to_graph(
                    iri,
                    subClassOf=CCF.biomarker,
                    annotations=[(RDFS.label, labels),
                                 (OBOINOWL.id, term_ids),
                                 (SKOS.prefLabel, pref_labels),
                                 (CCF.ccf_asctb_type, [asctb_type]),
                                 (CCF.ccf_characterizes, object_restrictions)])
        return BSOntology(self.graph)

    def _get_object_type(self, obj):
        return obj['@type'][0]

    def _get_asctb_type(self, obj):
        asctb_type = 'http://purl.org/ccf/latest/ccf.owl#asctb_type'
        return Literal(obj[asctb_type][0]['@value'])

    def _get_term_iri(self, obj):
        return URIRef(obj['@id'])

    def _get_term_labels(self, obj):
        return [Literal(label['@value']) for
                label in
                obj['http://www.w3.org/2000/01/rdf-schema#label']]

    def _get_term_prefLabels(self, obj):
        return [Literal(pref_label['@value']) for
                pref_label in
                obj['http://purl.org/ccf/latest/ccf.owl#ccf_preferred_label']]

    def _get_term_ids(self, obj):
        return [Literal(term_id['@value']) for
                term_id in
                obj['http://www.geneontology.org/formats/oboInOwl#id']]

    def _get_object_restrictions(self, obj):
        some_values_from = 'http://www.w3.org/2002/07/owl#someValuesFrom'
        if 'http://www.w3.org/2000/01/rdf-schema#subClassOf' in obj:
            return [URIRef(restriction[some_values_from][0]['@id']) for
                    restriction in
                    obj['http://www.w3.org/2000/01/rdf-schema#subClassOf']]
        else:
            return []

    def mutate_cell_biomarker(self, obj):
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
        anatomical_structure_name = last_anatomical_structure['name']
        if not anatomical_structure_id:
            anatomical_structure_id =\
                self._generate_provisional_id(anatomical_structure_name)
        anatomical_structure_label = last_anatomical_structure['rdfs_label']
        if not anatomical_structure_label:
            anatomical_structure_label = anatomical_structure_name

        iri = URIRef(self._expand_anatomical_entity_id(anatomical_structure_id))
        label = Literal(anatomical_structure_label)
        term_id = Literal(anatomical_structure_id)
        anatomical_structure = self._add_term_to_graph(
            iri,
            annotations=[(RDFS.label, [label]),
                         (OBOINOWL.id, [term_id])])

        ######################################################
        # Construct the axioms about cell types
        ######################################################
        cell_types = obj['cell_types']
        if not cell_types:
            raise ValueError("Cell type data are missing")

        last_cell_type = cell_types[-1]
        cell_type_id = last_cell_type['id']
        cell_type_name = last_cell_type['name']
        if not cell_type_id or ":" not in cell_type_id:
            cell_type_id = self._generate_provisional_id(cell_type_name)
        cell_type_label = last_cell_type['rdfs_label']
        if not cell_type_label:
            cell_type_label = cell_type_name

        term_id = Literal(cell_type_id)
        iri = URIRef(self._expand_cell_type_id(cell_type_id))
        label = Literal(cell_type_label)
        cell_type = self._add_term_to_graph(
            iri,
            annotations=[(RDFS.label, [label]),
                         (OBOINOWL.id, [term_id])])

        ######################################################
        # Construct the "cell type 'located in' anatomical_entity" axiom
        ######################################################
        cell_type.subClassOf =\
            [self._some_values_from(OBO.RO_0001025, anatomical_structure)]

        ######################################################
        # Construct the characterizing biomarker set class
        ######################################################
        biomarkers = obj['biomarkers']
        valid_biomarkers = [marker for marker in biomarkers
                            if "HGNC:" in marker['id']]
        # Apply when the valid biomarkers are not empty
        if valid_biomarkers:
            characterizing_biomarker_set_label =\
                "characterizing biomarker set of " + cell_type_label
            iri = URIRef(CCF._NS + snakecase(
                self._remove_punctuations(
                    lowercase(characterizing_biomarker_set_label))))
            label = Literal(characterizing_biomarker_set_label)

            characterizing_biomarker_set = Class(iri, graph=self.graph)
            self.graph.add((iri, RDFS.label, label))

            characterizing_biomarker_set.equivalentClass =\
                [BooleanClass(
                    operator=OWL.intersectionOf,
                    members=[self._some_values_from(
                        CCF.has_member,
                        Class(
                            URIRef(self._expand_biomarker_id(marker['id'])),
                            graph=self.graph
                        )) for marker in valid_biomarkers]
                    + [CCF.characterizing_biomarker_set],
                    graph=self.graph
                )]
            characterizing_biomarker_set_expression =\
                self._some_values_from(
                    OBO.RO_0015004,
                    characterizing_biomarker_set)
            cell_type.subClassOf = [characterizing_biomarker_set_expression]

        ######################################################
        # Construct the biomarker axioms
        ######################################################
        biomarker_types = ['gene', 'protein']
        for biomarker_type in biomarker_types:
            for marker in obj['biomarkers_' + biomarker_type]:
                marker_id = marker['id']
                if marker_id and "HGNC:" in marker_id:
                    marker_name = marker['name']
                    term_id = Literal(marker_id)
                    iri = URIRef(self._expand_biomarker_id(marker_id))
                    label = Literal(marker_name)
                    self._add_term_to_graph(
                        iri,
                        subClassOf=CCF.biomarker,
                        annotations=[(RDFS.label, [label]),
                                     (OBOINOWL.id, [term_id])])

        ######################################################
        # Construct the reference annotation
        ######################################################
        references = obj['references']
        if references and valid_biomarkers:
            bn = BNode()
            cell_type_iri = URIRef(self._expand_cell_type_id(cell_type_id))
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

    def _add_term_to_graph(self, iri, subClassOf=None, annotations=[]):
        term = Class(iri, graph=self.graph)
        if subClassOf is not None:
            self.graph.add((iri, RDFS.subClassOf, subClassOf))
        for annotation_tuple in annotations:
            property_name, values = annotation_tuple
            for value in values:
                self.graph.add((iri, property_name, value))
        return term

    def _generate_provisional_id(self, str):
        str = str.strip()
        str = lowercase(str)
        str = re.sub('\\s+', '-', str)
        str = re.sub('[^a-z0-9-]+', '', str)
        return f'ASCTB-TEMP:{str}'

    def _some_values_from(self, property, filler):
        return Restriction(property,
                           someValuesFrom=filler,
                           graph=self.graph)

    def _remove_punctuations(self, str):
        punctuation_excl_dash = punctuation.replace('-', '')
        return str.translate(str.maketrans('', '', punctuation_excl_dash))

    def _expand_anatomical_entity_id(self, str):
        if "ASCTB-TEMP:" in str:
            return self._expand_asctb_temp_id(str)
        elif "FMA:" in str:
            return self._expand_fma_id(str)
        elif "UBERON:" in str:
            return self._expand_uberon_id(str)
        return str

    def _expand_fma_id(self, str):
        fma_pattern = re.compile("FMA:", re.IGNORECASE)
        return fma_pattern.sub(
            "http://purl.org/sig/ont/fma/fma", str)

    def _expand_uberon_id(self, str):
        uberon_pattern = re.compile("UBERON:", re.IGNORECASE)
        return uberon_pattern.sub(
            "http://purl.obolibrary.org/obo/UBERON_", str)

    def _expand_cell_type_id(self, str):
        if "ASCTB-TEMP:" in str:
            return self._expand_asctb_temp_id(str)
        elif "CL:" in str:
            return self._expand_cl_id(str)
        elif "LMHA:" in str:
            return self._expand_lmha_id(str)
        elif "FMA:" in str:
            return self._expand_fma_id(str)

    def _expand_cl_id(self, str):
        cl_pattern = re.compile("CL:", re.IGNORECASE)
        return cl_pattern.sub(
            "http://purl.obolibrary.org/obo/CL_", str)

    def _expand_lmha_id(self, str):
        lmha_pattern = re.compile("LMHA:", re.IGNORECASE)
        return lmha_pattern.sub(
            "http://purl.obolibrary.org/obo/LMHA_", str)

    def _expand_biomarker_id(self, str):
        if "ASCTB-TEMP:" in str:
            return self._expand_asctb_temp_id(str)
        elif "HGNC:" in str:
            return self._expand_hgnc_id(str)

    def _expand_hgnc_id(self, str):
        hgnc_pattern = re.compile("HGNC:", re.IGNORECASE)
        return hgnc_pattern.sub(
            "http://identifiers.org/hgnc/", str)

    def _expand_asctb_temp_id(self, str):
        asctb_temp_pattern = re.compile("ASCTB-TEMP:", re.IGNORECASE)
        return asctb_temp_pattern.sub(
            "https://purl.org/ccf/ASCTB-TEMP_", str)

    def _expand_doi(self, str):
        doi_pattern = re.compile("doi:\\s*", re.IGNORECASE)
        return doi_pattern.sub("http://doi.org/", str)

    def serialize(self, destination):
        """
        """
        self.graph.serialize(format='ttl', destination=destination)
