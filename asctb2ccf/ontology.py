from asctb2ccf.namespace import OBO, CCF, OBOINOWL

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
        g.bind('rdf', RDF)
        g.bind('rdfs', RDFS)
        g.bind('dcterms', DCTERMS)

        # Ontology properties
        Ontology(identifier=URIRef(ontology_iri), graph=g)

        # Some definitions
        Property(DCTERMS.references, baseType=OWL.AnnotationProperty, graph=g)
        Property(CCF.has_marker_component, baseType=OWL.ObjectProperty, graph=g)

        return BSOntology(g)

    def mutate_anatomical_structure(self, obj):
        anatomical_structures = self._get_named_anatomical_structures(obj)
        for anatomical_structure in anatomical_structures:
            as_id = self._get_as_id(anatomical_structure)
            as_iri = URIRef(self._expand_anatomical_entity_id(as_id))

            term_id = Literal(as_id)
            term_name = anatomical_structure['name']
            if not term_name:
                term_name = anatomical_structure['rdfs_label']
            pref_label = Literal(term_name.lower())
            asctb_type = Literal("AS")

            self._add_term_to_graph(
                as_iri,
                annotations=[(OBOINOWL.id, [term_id]),
                             (CCF.ccf_pref_label, [pref_label]),
                             (CCF.ccf_asctb_type, [asctb_type])])
        return BSOntology(self.graph)

    def mutate_cell_type(self, obj):
        cell_types = self._get_named_cell_types(obj)
        for cell_type in cell_types:
            ct_id = self._get_ct_id(cell_type)
            ct_iri = URIRef(self._expand_cell_type_id(ct_id))

            term_id = Literal(ct_id)
            term_name = cell_type['name']
            if not term_name:
                term_name = cell_type['rdfs_label']
            pref_label = Literal(term_name.lower())
            asctb_type = Literal("CT")

            self._add_term_to_graph(
                ct_iri,
                annotations=[(OBOINOWL.id, [term_id]),
                             (CCF.ccf_pref_label, [pref_label]),
                             (CCF.ccf_asctb_type, [asctb_type])])
        return BSOntology(self.graph)

    def mutate_biomarker(self, obj):
        markers = self._get_named_biomarkers(obj)
        for marker in markers:
            bm_id = self._get_bm_id(marker)
            bm_iri = URIRef(self._expand_biomarker_id(bm_id))

            term_id = Literal(bm_id)
            term_name = marker['name']
            if not term_name:
                term_name = marker['rdfs_label']
            pref_label = Literal(term_name.lower())
            asctb_type = Literal("BM")

            self._add_term_to_graph(
                bm_iri,
                subClassOf=CCF.biomarker,
                annotations=[(OBOINOWL.id, [term_id]),
                             (CCF.ccf_pref_label, [pref_label]),
                             (CCF.ccf_asctb_type, [asctb_type])])
        return BSOntology(self.graph)

    def mutate_partonomy(self, obj):
        anatomical_structures = self._get_named_anatomical_structures(obj)

        body = URIRef("http://purl.obolibrary.org/obo/UBERON_0013702")
        self._add_term_to_graph(
            body,
            annotations=[(OBOINOWL.id, [Literal("UBERON:0013702")]),
                         (CCF.ccf_pref_label, [Literal("body")])])
        parent_part = body

        for anatomical_structure in anatomical_structures:
            as_id = self._get_as_id(anatomical_structure)
            as_iri = URIRef(self._expand_anatomical_entity_id(as_id))

            self._add_term_to_graph(
                as_iri,
                annotations=[(CCF.ccf_part_of, [parent_part])])

            # The current anatomical structure is the parent part for
            # the next anatomical structure.
            parent_part = as_iri
        return BSOntology(self.graph)

    def mutate_cell_hierarchy(self, obj):
        cell_types = self._get_named_cell_types(obj)

        cell = URIRef("http://purl.obolibrary.org/obo/CL_0000000")
        self._add_term_to_graph(
            cell,
            annotations=[(OBOINOWL.id, [Literal("CL:0000000")]),
                         (CCF.ccf_pref_label, [Literal("cell")])])
        parent_cell = cell

        for cell_type in cell_types:
            ct_id = self._get_ct_id(cell_type)
            ct_iri = URIRef(self._expand_cell_type_id(ct_id))

            self._add_term_to_graph(
                ct_iri,
                annotations=[(CCF.ccf_ct_isa, [parent_cell])])

            # The current cell type is the parent cell for the next cell type.
            parent_cell = ct_iri
        return BSOntology(self.graph)

    def mutate_cell_location(self, obj):
        anatomical_structures = self._get_named_anatomical_structures(obj)
        cell_types = self._get_named_cell_types(obj)
        for cell_type in cell_types:
            ct_id = self._get_ct_id(cell_type)
            ct_iri = URIRef(self._expand_cell_type_id(ct_id))
            for anatomical_structure in anatomical_structures:
                as_id = self._get_as_id(anatomical_structure)
                as_iri = URIRef(self._expand_anatomical_entity_id(as_id))
                self.graph.add((ct_iri, CCF.ccf_located_in, as_iri))
        return BSOntology(self.graph)

    def mutate_cell_biomarker(self, obj):
        """
        """
        ######################################################
        # Construct the axioms about anatomical structures
        ######################################################
        anatomical_structures = obj['anatomical_structures']
        if not anatomical_structures:
            raise ValueError("Anatomical structure data are missing")

        last_anatomical_structure = self._get_last_item(anatomical_structures)
        as_id = self._get_as_id(last_anatomical_structure)
        as_iri = URIRef(self._expand_anatomical_entity_id(as_id))
        anatomical_structure = self._add_term_to_graph(as_iri)

        ######################################################
        # Construct the axioms about cell types
        ######################################################
        cell_types = obj['cell_types']
        if not cell_types:
            raise ValueError("Cell type data are missing")

        last_cell_type = self._get_last_item(cell_types)
        ct_id = self._get_ct_id(last_cell_type)
        ct_iri = URIRef(self._expand_cell_type_id(ct_id))
        cell_type = self._add_term_to_graph(ct_iri)

        ######################################################
        # Construct the axioms about biomarkers
        ######################################################
        biomarker_types = ['gene', 'protein']
        for biomarker_type in biomarker_types:
            for marker in obj['biomarkers_' + biomarker_type]:
                if self._is_valid_marker(marker):
                    bm_id = marker['id']
                    iri = URIRef(self._expand_biomarker_id(bm_id))
                    self._add_term_to_graph(
                        iri,
                        subClassOf=CCF.biomarker)

        ######################################################
        # Construct the characterizing biomarker set class
        ######################################################
        biomarkers = obj['biomarkers']
        if not biomarkers:
            raise ValueError("Biomarker data are missing")

        # Pick only valid HGNC markers. Markers with an empty ID are
        # excluded, including ones with the ASCTB-TEMP prefix
        valid_biomarkers = [marker for marker in biomarkers
                            if self._is_valid_marker(marker)]
        if valid_biomarkers:
            # Construct the characterizing biomarker set definition
            characterizing_biomarker_set =\
                BooleanClass(
                    operator=OWL.intersectionOf,
                    members=[OBO.SO_0001260] + [self._some_values_from(
                        CCF.has_marker_component,
                        Class(
                            URIRef(self._expand_biomarker_id(marker['id'])),
                            graph=self.graph
                        )) for marker in valid_biomarkers],
                    graph=self.graph
                )
            characterizing_biomarker_set_expression =\
                self._some_values_from(
                    OBO.RO_0015004,
                    characterizing_biomarker_set)
            cell_type.subClassOf = [characterizing_biomarker_set_expression]

            # Construct the reference annotations
            references = obj['references']
            if references:
                bn = BNode()
                self.graph.add((bn, RDF.type, OWL.Axiom))
                self.graph.add((bn, OWL.annotatedSource, ct_iri))
                self.graph.add((bn, OWL.annotatedProperty, RDFS.subClassOf))
                self.graph.add((bn, OWL.annotatedTarget,
                               characterizing_biomarker_set_expression
                               .identifier))
                for reference in references:
                    if 'doi' in reference:
                        doi = reference['doi']
                        if doi is None:
                            continue
                        if "doi:" in doi or "DOI:" in doi:
                            doi_str = Literal(self._expand_doi(doi))
                            self.graph.add((bn, DCTERMS.references, doi_str))

        return BSOntology(self.graph)

    def _get_named_anatomical_structures(self, obj):
        anatomical_structures = obj['anatomical_structures']
        return [anatomical_structure for anatomical_structure
                in anatomical_structures
                if anatomical_structure['name']
                or anatomical_structure['rdfs_label']]

    def _get_named_cell_types(self, obj):
        cell_types = obj['cell_types']
        return [cell_type for cell_type in cell_types
                if cell_type['name'] or cell_type['rdfs_label']]

    def _get_named_biomarkers(self, obj):
        markers = obj['biomarkers']
        return [marker for marker in markers
                if marker['name'] or marker['rdfs_label']]

    def _get_as_id(self, anatomical_structure):
        as_id = anatomical_structure['id']
        if not as_id or ":" not in as_id:
            as_pref_label = anatomical_structure['name']
            if not as_pref_label:
                as_pref_label = anatomical_structure['rdfs_label']
            as_id = self._generate_provisional_id(as_pref_label)
        return as_id

    def _get_ct_id(self, cell_type):
        ct_id = cell_type['id']
        if not ct_id or ":" not in ct_id:
            ct_pref_label = cell_type['name']
            if not ct_pref_label:
                ct_pref_label = cell_type['rdfs_label']
            ct_id = self._generate_provisional_id(ct_pref_label)
        return ct_id

    def _get_bm_id(self, marker):
        bm_id = marker['id']
        if not self._is_valid_marker(marker):
            bm_pref_label = marker['name']
            if not bm_pref_label:
                bm_pref_label = marker['rdfs_label']
            bm_id = self._generate_provisional_id(bm_pref_label)
        return bm_id

    def _add_term_to_graph(self, iri, subClassOf=None, label=None,
                           annotations=[]):
        term = Class(iri, graph=self.graph)
        if subClassOf is not None:
            self.graph.add((iri, RDFS.subClassOf, subClassOf))
        if label is not None:
            self.graph.add((iri, RDFS.label, label))
        for annotation_tuple in annotations:
            property_name, values = annotation_tuple
            for value in values:
                self.graph.add((iri, property_name, value))
        return term

    def _get_last_item(self, arr):
        return next(item for item in reversed(arr) if item and 'id' in item)

    def _generate_provisional_id(self, str):
        str = str.strip()
        str = lowercase(str)
        str = re.sub('\\W+', '-', str)
        str = re.sub('[^a-z0-9-]+', '', str)
        return f'ASCTB-TEMP:{str}'

    def _is_valid_marker(self, marker):
        return marker['id'] and re.match(r"HGNC:[0-9]+", marker['id'])

    def _some_values_from(self, property, filler):
        return Restriction(property,
                           someValuesFrom=filler,
                           graph=self.graph)

    def _expand_anatomical_entity_id(self, str):
        if "ASCTB-TEMP:" in str:
            return self._expand_asctb_temp_id(str)
        elif "FMA:" in str:
            return self._expand_fma_id(str)
        elif "UBERON:" in str:
            return self._expand_uberon_id(str)
        else:
            raise ValueError("Invalid anatomical structure ID: " + str)

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
        else:
            raise ValueError("Invalid cell type ID: " + str)

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
        else:
            raise ValueError("Invalid biomarker ID: " + str)

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
        self.graph.serialize(format='application/rdf+xml',
                             destination=destination)
