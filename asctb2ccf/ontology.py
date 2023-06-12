from asctb2ccf.namespace import OBO, CCF, HGNC, OBOINOWL

from string import punctuation
from stringcase import lowercase, snakecase

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, XSD, DCTERMS
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
    def new(organ_name, ontology_iri):
        g = Graph()
        g.bind('ccf', CCF)
        g.bind('obo', OBO)
        g.bind('hgnc', HGNC)
        g.bind('owl', OWL)
        g.bind('rdf', RDF)
        g.bind('rdfs', RDFS)
        g.bind('dcterms', DCTERMS)

        # Ontology properties
        Ontology(identifier=URIRef(ontology_iri), graph=g)

        # Default class hierarchy
        uberon_entity = URIRef("http://purl.obolibrary.org/obo/UBERON_0001062")
        Class(uberon_entity, subClassOf=[CCF.anatomical_structure], graph=g)

        fma_entity = URIRef("http://purl.org/sig/ont/fma/fma62955")
        Class(fma_entity, subClassOf=[CCF.anatomical_structure], graph=g)

        cl_cell_type = URIRef("http://purl.obolibrary.org/obo/CL_0000000")
        Class(cl_cell_type, subClassOf=[CCF.cell_type], graph=g)

        lmha_cell_type = URIRef("http://purl.obolibrary.org/obo/LMHA_00135")
        Class(lmha_cell_type, subClassOf=[CCF.cell_type], graph=g)

        hgnc_gene = URIRef("http://purl.bioontology.org/ontology/HGNC/gene")
        Class(hgnc_gene, subClassOf=[CCF.biomarker], graph=g)

        # Patch classes
        body = URIRef("http://purl.obolibrary.org/obo/UBERON_0013702")
        Class(body, graph=g)
        g.add((body, OBOINOWL.id, Literal("UBERON:0013702")))
        g.add((body, CCF.ccf_asctb_type, Literal("AS")))
        g.add((body, CCF.ccf_pref_label, Literal("body")))

        if organ_name == "Blood":
            blood = URIRef("http://purl.obolibrary.org/obo/UBERON_0000178")
            Class(blood, graph=g)
            g.add((blood, OBOINOWL.id, Literal("UBERON:0000178")))
            g.add((blood, CCF.ccf_asctb_type, Literal("AS")))
            g.add((blood, CCF.ccf_pref_label, Literal("blood")))
            g.add((blood, CCF.ccf_part_of, body))

        elif organ_name == "BloodVasculature":
            blood_vas = URIRef("http://purl.obolibrary.org/obo/UBERON_0004537")
            Class(blood_vas, graph=g)
            g.add((blood_vas, OBOINOWL.id, Literal("UBERON:0004537")))
            g.add((blood_vas, CCF.ccf_asctb_type, Literal("AS")))
            g.add((blood_vas, CCF.ccf_pref_label, Literal("blood vasculature")))
            g.add((blood_vas, CCF.ccf_part_of, body))

        elif organ_name == "BoneMarrow":
            bone_marrow = URIRef("http://purl.obolibrary.org/obo/UBERON_0002371")
            Class(bone_marrow, graph=g)
            g.add((bone_marrow, OBOINOWL.id, Literal("UBERON:0002371")))
            g.add((bone_marrow, CCF.ccf_asctb_type, Literal("AS")))
            g.add((bone_marrow, CCF.ccf_pref_label, Literal("bone marrow")))
            g.add((bone_marrow, CCF.ccf_part_of, body))

        elif organ_name == "Brain":
            brain = URIRef("http://purl.obolibrary.org/obo/UBERON_0000955")
            Class(brain, graph=g)
            g.add((brain, OBOINOWL.id, Literal("UBERON:0000955")))
            g.add((brain, CCF.ccf_asctb_type, Literal("AS")))
            g.add((brain, CCF.ccf_pref_label, Literal("brain")))
            g.add((brain, CCF.ccf_part_of, body))

        elif organ_name == "Eye":
            eye = URIRef("http://purl.obolibrary.org/obo/UBERON_0000970")
            Class(eye, graph=g)
            g.add((eye, OBOINOWL.id, Literal("UBERON:0000970")))
            g.add((eye, CCF.ccf_asctb_type, Literal("AS")))
            g.add((eye, CCF.ccf_pref_label, Literal("eye")))
            g.add((eye, CCF.ccf_part_of, body))

            left_eye = URIRef("http://purl.obolibrary.org/obo/UBERON_0004548")
            Class(left_eye, graph=g)
            g.add((left_eye, OBOINOWL.id, Literal("UBERON:0004548")))
            g.add((left_eye, CCF.ccf_asctb_type, Literal("AS")))
            g.add((left_eye, CCF.ccf_pref_label, Literal("left eye")))
            g.add((left_eye, CCF.ccf_part_of, eye))

            right_eye = URIRef("http://purl.obolibrary.org/obo/UBERON_0004549")
            Class(right_eye, graph=g)
            g.add((right_eye, OBOINOWL.id, Literal("UBERON:0004549")))
            g.add((right_eye, CCF.ccf_asctb_type, Literal("AS")))
            g.add((right_eye, CCF.ccf_pref_label, Literal("right eye")))
            g.add((right_eye, CCF.ccf_part_of, eye))

        elif organ_name == "FallopianTube":
            fallopian_tb = URIRef("http://purl.obolibrary.org/obo/UBERON_0003889")
            Class(fallopian_tb, graph=g)
            g.add((fallopian_tb, OBOINOWL.id, Literal("UBERON:0003889")))
            g.add((fallopian_tb, CCF.ccf_asctb_type, Literal("AS")))
            g.add((fallopian_tb, CCF.ccf_pref_label, Literal("fallopian tube")))
            g.add((fallopian_tb, CCF.ccf_part_of, body))

            left_tube = URIRef("http://purl.obolibrary.org/obo/UBERON_0001303")
            Class(left_tube, graph=g)
            g.add((left_tube, OBOINOWL.id, Literal("UBERON:0001303")))
            g.add((left_tube, CCF.ccf_asctb_type, Literal("AS")))
            g.add((left_tube, CCF.ccf_pref_label, Literal("left fallopian tube")))
            g.add((left_tube, CCF.ccf_part_of, fallopian_tb))

            fallopian_tb = URIRef("http://purl.obolibrary.org/obo/UBERON_0003889")
            right_tube = URIRef("http://purl.obolibrary.org/obo/UBERON_0001302")
            Class(right_tube, graph=g)
            g.add((right_tube, OBOINOWL.id, Literal("UBERON:0001302")))
            g.add((right_tube, CCF.ccf_asctb_type, Literal("AS")))
            g.add((right_tube, CCF.ccf_pref_label, Literal("right fallopian tube")))
            g.add((right_tube, CCF.ccf_part_of, fallopian_tb))

        elif organ_name == "Heart":
            heart = URIRef("http://purl.obolibrary.org/obo/UBERON_0000948")
            Class(heart, graph=g)
            g.add((heart, OBOINOWL.id, Literal("UBERON:0000948")))
            g.add((heart, CCF.ccf_asctb_type, Literal("AS")))
            g.add((heart, CCF.ccf_pref_label, Literal("heart")))
            g.add((heart, CCF.ccf_part_of, body))

        elif organ_name == "Kidney":
            kidney = URIRef("http://purl.obolibrary.org/obo/UBERON_0002113")
            Class(kidney, graph=g)
            g.add((kidney, OBOINOWL.id, Literal("UBERON:0002113")))
            g.add((kidney, CCF.ccf_asctb_type, Literal("AS")))
            g.add((kidney, CCF.ccf_pref_label, Literal("kidney")))
            g.add((kidney, CCF.ccf_part_of, body))

            left_kidney = URIRef("http://purl.obolibrary.org/obo/UBERON_0004538")
            Class(left_kidney, graph=g)
            g.add((left_kidney, OBOINOWL.id, Literal("UBERON:0004538")))
            g.add((left_kidney, CCF.ccf_asctb_type, Literal("AS")))
            g.add((left_kidney, CCF.ccf_pref_label, Literal("left kidney")))
            g.add((left_kidney, CCF.ccf_part_of, kidney))

            right_kidney = URIRef("http://purl.obolibrary.org/obo/UBERON_0004539")
            Class(right_kidney, graph=g)
            g.add((right_kidney, OBOINOWL.id, Literal("UBERON:0004539")))
            g.add((right_kidney, CCF.ccf_asctb_type, Literal("AS")))
            g.add((right_kidney, CCF.ccf_pref_label, Literal("right kidney")))
            g.add((right_kidney, CCF.ccf_part_of, kidney))

        elif organ_name == "Knee":
            knee = URIRef("http://purl.obolibrary.org/obo/UBERON_0001465")
            Class(knee, graph=g)
            g.add((knee, OBOINOWL.id, Literal("UBERON:0001465")))
            g.add((knee, CCF.ccf_asctb_type, Literal("AS")))
            g.add((knee, CCF.ccf_pref_label, Literal("knee")))
            g.add((knee, CCF.ccf_part_of, body))

            left_knee = URIRef("http://purl.org/sig/ont/fma/fma24978")
            Class(left_knee, graph=g)
            g.add((left_knee, OBOINOWL.id, Literal("FMA:24978")))
            g.add((left_knee, CCF.ccf_asctb_type, Literal("AS")))
            g.add((left_knee, CCF.ccf_pref_label, Literal("left knee")))
            g.add((left_knee, CCF.ccf_part_of, knee))

            right_knee = URIRef("http://purl.org/sig/ont/fma/fma24977")
            Class(right_knee, graph=g)
            g.add((right_knee, OBOINOWL.id, Literal("FMA:24977")))
            g.add((right_knee, CCF.ccf_asctb_type, Literal("AS")))
            g.add((right_knee, CCF.ccf_pref_label, Literal("right knee")))
            g.add((right_knee, CCF.ccf_part_of, knee))

        elif organ_name == "LargeIntestine":
            large_intestine = URIRef("http://purl.obolibrary.org/obo/UBERON_0000059")
            Class(large_intestine, graph=g)
            g.add((large_intestine, OBOINOWL.id, Literal("UBERON:0000059")))
            g.add((large_intestine, CCF.ccf_asctb_type, Literal("AS")))
            g.add((large_intestine, CCF.ccf_pref_label, Literal("large intestine")))
            g.add((large_intestine, CCF.ccf_part_of, body))

        elif organ_name == "Liver":
            liver = URIRef("http://purl.obolibrary.org/obo/UBERON_0002107")
            Class(liver, graph=g)
            g.add((liver, OBOINOWL.id, Literal("UBERON:0002107")))
            g.add((liver, CCF.ccf_asctb_type, Literal("AS")))
            g.add((liver, CCF.ccf_pref_label, Literal("liver")))
            g.add((liver, CCF.ccf_part_of, body))

        elif organ_name == "Lung":
            lung = URIRef("http://purl.obolibrary.org/obo/UBERON_0002048")
            Class(lung, graph=g)
            g.add((lung, OBOINOWL.id, Literal("UBERON:0002048")))
            g.add((lung, CCF.ccf_asctb_type, Literal("AS")))
            g.add((lung, CCF.ccf_pref_label, Literal("lung")))
            g.add((lung, CCF.ccf_part_of, body))

            respiratory = URIRef("http://purl.obolibrary.org/obo/UBERON_0001004")
            Class(respiratory, graph=g)
            g.add((respiratory, OBOINOWL.id, Literal("UBERON:0001004")))
            g.add((respiratory, CCF.ccf_asctb_type, Literal("AS")))
            g.add((respiratory, CCF.ccf_pref_label, Literal("respiratory system")))
            g.add((respiratory, CCF.ccf_part_of, lung))

        elif organ_name == "LymphNode":
            lymph_node = URIRef("http://purl.obolibrary.org/obo/UBERON_0000029")
            Class(lymph_node, graph=g)
            g.add((lymph_node, OBOINOWL.id, Literal("UBERON:0000029")))
            g.add((lymph_node, CCF.ccf_asctb_type, Literal("AS")))
            g.add((lymph_node, CCF.ccf_pref_label, Literal("lymph node")))
            g.add((lymph_node, CCF.ccf_part_of, body))

            mesenteric_ln = URIRef("http://purl.obolibrary.org/obo/UBERON_0002509")
            Class(mesenteric_ln, graph=g)
            g.add((mesenteric_ln, OBOINOWL.id, Literal("UBERON:0002509")))
            g.add((mesenteric_ln, CCF.ccf_asctb_type, Literal("AS")))
            g.add((mesenteric_ln, CCF.ccf_pref_label, Literal("mesenteric lymph node")))
            g.add((mesenteric_ln, CCF.ccf_part_of, lymph_node))

        elif organ_name == "LymphVasculature":
            lymph_vas = URIRef("http://purl.obolibrary.org/obo/UBERON_0004536")
            Class(lymph_vas, graph=g)
            g.add((lymph_vas, OBOINOWL.id, Literal("UBERON:0004536")))
            g.add((lymph_vas, CCF.ccf_asctb_type, Literal("AS")))
            g.add((lymph_vas, CCF.ccf_pref_label, Literal("lymph vasculature")))
            g.add((lymph_vas, CCF.ccf_part_of, body))

        elif organ_name == "Ovary":
            ovary = URIRef("http://purl.obolibrary.org/obo/UBERON_0000992")
            Class(ovary, graph=g)
            g.add((ovary, OBOINOWL.id, Literal("UBERON:0000992")))
            g.add((ovary, CCF.ccf_asctb_type, Literal("AS")))
            g.add((ovary, CCF.ccf_pref_label, Literal("ovary")))
            g.add((ovary, CCF.ccf_part_of, body))

            left_ovary = URIRef("http://purl.org/sig/ont/fma/fma7214")
            Class(left_ovary, graph=g)
            g.add((left_ovary, OBOINOWL.id, Literal("FMA:7214")))
            g.add((left_ovary, CCF.ccf_asctb_type, Literal("AS")))
            g.add((left_ovary, CCF.ccf_pref_label, Literal("left ovary")))
            g.add((left_ovary, CCF.ccf_part_of, ovary))

            right_ovary = URIRef("http://purl.org/sig/ont/fma/fma7213")
            Class(right_ovary, graph=g)
            g.add((right_ovary, OBOINOWL.id, Literal("FMA:7213")))
            g.add((right_ovary, CCF.ccf_asctb_type, Literal("AS")))
            g.add((right_ovary, CCF.ccf_pref_label, Literal("right ovary")))
            g.add((right_ovary, CCF.ccf_part_of, ovary))

        elif organ_name == "Pancreas":
            pancreas = URIRef("http://purl.obolibrary.org/obo/UBERON_0001264")
            Class(pancreas, graph=g)
            g.add((pancreas, OBOINOWL.id, Literal("UBERON:0001264")))
            g.add((pancreas, CCF.ccf_asctb_type, Literal("AS")))
            g.add((pancreas, CCF.ccf_pref_label, Literal("pancreas")))
            g.add((pancreas, CCF.ccf_part_of, body))

        elif organ_name == "PeripheralNervousSystem":
            pns = URIRef("http://purl.obolibrary.org/obo/UBERON_0000010")
            Class(pns, graph=g)
            g.add((pns, OBOINOWL.id, Literal("UBERON:0000010")))
            g.add((pns, CCF.ccf_asctb_type, Literal("AS")))
            g.add((pns, CCF.ccf_pref_label, Literal("peripheral nervous system")))
            g.add((pns, CCF.ccf_part_of, body))

        elif organ_name == "Placenta":
            placenta = URIRef("http://purl.obolibrary.org/obo/UBERON_0001987")
            Class(placenta, graph=g)
            g.add((placenta, OBOINOWL.id, Literal("UBERON:0001987")))
            g.add((placenta, CCF.ccf_asctb_type, Literal("AS")))
            g.add((placenta, CCF.ccf_pref_label, Literal("placenta")))
            g.add((placenta, CCF.ccf_part_of, body))

        elif organ_name == "Prostate":
            prostate = URIRef("http://purl.obolibrary.org/obo/UBERON_0002367")
            Class(prostate, graph=g)
            g.add((prostate, OBOINOWL.id, Literal("UBERON:0002367")))
            g.add((prostate, CCF.ccf_asctb_type, Literal("AS")))
            g.add((prostate, CCF.ccf_pref_label, Literal("prostate")))
            g.add((prostate, CCF.ccf_part_of, body))

        elif organ_name == "Skin":
            skin = URIRef("http://purl.obolibrary.org/obo/UBERON_0001003")
            Class(skin, graph=g)
            g.add((skin, OBOINOWL.id, Literal("UBERON:0001003")))
            g.add((skin, CCF.ccf_asctb_type, Literal("AS")))
            g.add((skin, CCF.ccf_pref_label, Literal("skin")))
            g.add((skin, CCF.ccf_part_of, body))

        elif organ_name == "SmallIntestine":
            small_intestine = URIRef("http://purl.obolibrary.org/obo/UBERON_0002108")
            Class(small_intestine, graph=g)
            g.add((small_intestine, OBOINOWL.id, Literal("UBERON:0002108")))
            g.add((small_intestine, CCF.ccf_asctb_type, Literal("AS")))
            g.add((small_intestine, CCF.ccf_pref_label, Literal("small intestine")))
            g.add((small_intestine, CCF.ccf_part_of, body))

        elif organ_name == "Spleen":
            spleen = URIRef("http://purl.obolibrary.org/obo/UBERON_0002106")
            Class(spleen, graph=g)
            g.add((spleen, OBOINOWL.id, Literal("UBERON:0002106")))
            g.add((spleen, CCF.ccf_asctb_type, Literal("AS")))
            g.add((spleen, CCF.ccf_pref_label, Literal("spleen")))
            g.add((spleen, CCF.ccf_part_of, body))

        elif organ_name == "Thymus":
            thymus = URIRef("http://purl.obolibrary.org/obo/UBERON_0002370")
            Class(thymus, graph=g)
            g.add((thymus, OBOINOWL.id, Literal("UBERON:0002370")))
            g.add((thymus, CCF.ccf_asctb_type, Literal("AS")))
            g.add((thymus, CCF.ccf_pref_label, Literal("thymus")))
            g.add((thymus, CCF.ccf_part_of, body))

        elif organ_name == "Ureter":
            ureter = URIRef("http://purl.obolibrary.org/obo/UBERON_0000056")
            Class(ureter, graph=g)
            g.add((ureter, OBOINOWL.id, Literal("UBERON:0000056")))
            g.add((ureter, CCF.ccf_asctb_type, Literal("AS")))
            g.add((ureter, CCF.ccf_pref_label, Literal("ureter")))
            g.add((ureter, CCF.ccf_part_of, body))

            left_ureter = URIRef("http://purl.obolibrary.org/obo/UBERON_0001223")
            Class(left_ureter, graph=g)
            g.add((left_ureter, OBOINOWL.id, Literal("UBERON:0001223")))
            g.add((left_ureter, CCF.ccf_asctb_type, Literal("AS")))
            g.add((left_ureter, CCF.ccf_pref_label, Literal("left ureter")))
            g.add((left_ureter, CCF.ccf_part_of, ureter))

            right_ureter = URIRef("http://purl.obolibrary.org/obo/UBERON_0001222")
            Class(right_ureter, graph=g)
            g.add((right_ureter, OBOINOWL.id, Literal("UBERON:0001222")))
            g.add((right_ureter, CCF.ccf_asctb_type, Literal("AS")))
            g.add((right_ureter, CCF.ccf_pref_label, Literal("right ureter")))
            g.add((right_ureter, CCF.ccf_part_of, ureter))

        elif organ_name == "UrinaryBladder":
            urinary_bladder = URIRef("http://purl.obolibrary.org/obo/UBERON_0001255")
            Class(urinary_bladder, graph=g)
            g.add((urinary_bladder, OBOINOWL.id, Literal("UBERON:0001255")))
            g.add((urinary_bladder, CCF.ccf_asctb_type, Literal("AS")))
            g.add((urinary_bladder, CCF.ccf_pref_label, Literal("urinary bladder")))
            g.add((urinary_bladder, CCF.ccf_part_of, body))

        elif organ_name == "Uterus":
            uterus = URIRef("http://purl.obolibrary.org/obo/UBERON_0000995")
            Class(uterus, graph=g)
            g.add((uterus, OBOINOWL.id, Literal("UBERON:0000995")))
            g.add((uterus, CCF.ccf_asctb_type, Literal("AS")))
            g.add((uterus, CCF.ccf_pref_label, Literal("uterus")))
            g.add((uterus, CCF.ccf_part_of, body))

        elif organ_name == "SpinalCord":
            spinal_cord = URIRef("http://purl.obolibrary.org/obo/UBERON_0002240")
            Class(spinal_cord, graph=g)
            g.add((spinal_cord, OBOINOWL.id, Literal("UBERON:0002240")))
            g.add((spinal_cord, CCF.ccf_asctb_type, Literal("AS")))
            g.add((spinal_cord, CCF.ccf_pref_label, Literal("spinal cord")))
            g.add((spinal_cord, CCF.ccf_part_of, body))

        elif organ_name == "MammaryGland":
            mammary_gland = URIRef("http://purl.obolibrary.org/obo/UBERON_0001911")
            Class(mammary_gland, graph=g)
            g.add((mammary_gland, OBOINOWL.id, Literal("UBERON:0001911")))
            g.add((mammary_gland, CCF.ccf_asctb_type, Literal("AS")))
            g.add((mammary_gland, CCF.ccf_pref_label, Literal("mammary gland")))
            g.add((mammary_gland, CCF.ccf_part_of, body))

            left_mammary_gland = URIRef("http://purl.org/sig/ont/fma/fma57991")
            Class(left_mammary_gland, graph=g)
            g.add((left_mammary_gland, OBOINOWL.id, Literal("FMA:57991")))
            g.add((left_mammary_gland, CCF.ccf_asctb_type, Literal("AS")))
            g.add((left_mammary_gland, CCF.ccf_pref_label, Literal("left mammary gland")))
            g.add((left_mammary_gland, CCF.ccf_part_of, mammary_gland))

            right_mammary_gland = URIRef("http://purl.org/sig/ont/fma/fma57987")
            Class(right_mammary_gland, graph=g)
            g.add((right_mammary_gland, OBOINOWL.id, Literal("FMA:57987")))
            g.add((right_mammary_gland, CCF.ccf_asctb_type, Literal("AS")))
            g.add((right_mammary_gland, CCF.ccf_pref_label, Literal("right mammary gland")))
            g.add((right_mammary_gland, CCF.ccf_part_of, mammary_gland))

            breast = URIRef("http://purl.obolibrary.org/obo/UBERON_0000310")
            Class(breast, graph=g)
            g.add((breast, OBOINOWL.id, Literal("UBERON:0000310")))
            g.add((breast, CCF.ccf_asctb_type, Literal("AS")))
            g.add((breast, CCF.ccf_pref_label, Literal("breast")))
            g.add((breast, CCF.ccf_part_of, body))

        elif organ_name == "Pelvis":
            pelvis = URIRef("http://purl.obolibrary.org/obo/UBERON_0001270")
            Class(pelvis, graph=g)
            g.add((pelvis, OBOINOWL.id, Literal("UBERON:0001270")))
            g.add((pelvis, CCF.ccf_asctb_type, Literal("AS")))
            g.add((pelvis, CCF.ccf_pref_label, Literal("pelvis")))
            g.add((pelvis, CCF.ccf_part_of, body))

        elif organ_name == "Tonsil":
            tonsil = URIRef("http://purl.obolibrary.org/obo/UBERON_0002372")
            Class(tonsil, graph=g)
            g.add((tonsil, OBOINOWL.id, Literal("UBERON:0002372")))
            g.add((tonsil, CCF.ccf_asctb_type, Literal("AS")))
            g.add((tonsil, CCF.ccf_pref_label, Literal("tonsil")))
            g.add((tonsil, CCF.ccf_part_of, body))

            left_palatine_tonsil = URIRef("http://purl.org/sig/ont/fma/fma54974")
            Class(left_palatine_tonsil, graph=g)
            g.add((left_palatine_tonsil, OBOINOWL.id, Literal("FMA:54974")))
            g.add((left_palatine_tonsil, CCF.ccf_asctb_type, Literal("AS")))
            g.add((left_palatine_tonsil, CCF.ccf_pref_label, Literal("left palatine tonsil")))
            g.add((left_palatine_tonsil, CCF.ccf_part_of, tonsil))

            right_palatine_tonsil = URIRef("http://purl.org/sig/ont/fma/fma54973")
            Class(right_palatine_tonsil, graph=g)
            g.add((right_palatine_tonsil, OBOINOWL.id, Literal("FMA:54973")))
            g.add((right_palatine_tonsil, CCF.ccf_asctb_type, Literal("AS")))
            g.add((right_palatine_tonsil, CCF.ccf_pref_label, Literal("right palatine tonsil")))
            g.add((right_palatine_tonsil, CCF.ccf_part_of, tonsil))           

        # Some definitions
        Property(DCTERMS.references, baseType=OWL.AnnotationProperty, graph=g)
        Property(OBO.IAO_0000115, baseType=OWL.AnnotationProperty, graph=g)
        Property(OBOINOWL.id, baseType=OWL.AnnotationProperty, graph=g)
        Property(CCF.ccf_pref_label, baseType=OWL.AnnotationProperty, graph=g)
        Property(CCF.ccf_part_of, baseType=OWL.AnnotationProperty, graph=g)
        Property(CCF.ccf_located_in, baseType=OWL.AnnotationProperty, graph=g)
        Property(CCF.ccf_characterizes, baseType=OWL.AnnotationProperty, graph=g)
        Property(CCF.ccf_asctb_type, baseType=OWL.AnnotationProperty, graph=g)
        Property(CCF.ccf_ct_isa, baseType=OWL.AnnotationProperty, graph=g)
        Property(CCF.ccf_is_provisional, baseType=OWL.AnnotationProperty, graph=g)

        return BSOntology(g)

    def mutate_anatomical_structure(self, obj):
        anatomical_structures = self._get_named_anatomical_structures(obj)
        for anatomical_structure in anatomical_structures:
            as_id, is_provisional = self._get_as_id(anatomical_structure)
            as_iri = URIRef(self._expand_anatomical_entity_id(as_id))

            term_id = Literal(as_id)
            term_name = anatomical_structure['name']
            if not term_name:
                term_name = anatomical_structure['rdfs_label']
            pref_label = Literal(term_name.lower())
            asctb_type = Literal("AS")

            # If not a provisional term, the rdfs:label and rdf:SubClassOf rels
            # will be obtained from the reference ontology on another pipeline.
            self._add_term_to_graph(
                as_iri,
                annotations=[(OBOINOWL.id, [term_id]),
                             (CCF.ccf_pref_label, [pref_label]),
                             (CCF.ccf_asctb_type, [asctb_type])])

            # Otherwise, the rdfs:label equals to the preferred label and
            # the term is always a subclass of CCF:anatomical_structure
            if is_provisional:
                self._add_term_to_graph(
                    as_iri,
                    label=pref_label,
                    subClassOf=CCF.anatomical_structure)
                self._add_provisional_definition(as_iri)

        return BSOntology(self.graph)

    def mutate_cell_type(self, obj):
        cell_types = self._get_named_cell_types(obj)
        for cell_type in cell_types:
            ct_id, is_provisional = self._get_ct_id(cell_type)
            ct_iri = URIRef(self._expand_cell_type_id(ct_id))
            term_id = Literal(ct_id)
            term_name = cell_type['name']
            if not term_name:
                term_name = cell_type['rdfs_label']
            pref_label = Literal(term_name.lower())
            asctb_type = Literal("CT")

            # If not a provisional term, the rdfs:label and rdf:SubClassOf rels
            # will be obtained from the reference ontology on another pipeline.
            self._add_term_to_graph(
                ct_iri,
                annotations=[(OBOINOWL.id, [term_id]),
                             (CCF.ccf_pref_label, [pref_label]),
                             (CCF.ccf_asctb_type, [asctb_type])])

            # Otherwise, the rdfs:label equals to the preferred label and
            # the term is always a subclass of CCF:cell_type
            if is_provisional:
                self._add_term_to_graph(
                    ct_iri,
                    label=pref_label,
                    subClassOf=CCF.cell_type)
                self._add_provisional_definition(ct_iri)

        return BSOntology(self.graph)

    def mutate_biomarker(self, obj):
        markers = self._get_named_biomarkers(obj)
        for marker in markers:
            bm_id, is_provisional = self._get_bm_id(marker)
            bm_iri = URIRef(self._expand_biomarker_id(bm_id))

            term_id = Literal(bm_id)
            term_name = marker['name']
            if not term_name:
                term_name = marker['rdfs_label']
            pref_label = Literal(term_name)
            asctb_type = Literal("BM")
            biomarker_type = Literal(marker['b_type'])

            # If not a provisional term, the rdfs:label and rdf:SubClassOf rels
            # will be obtained from the reference ontology on another pipeline.
            self._add_term_to_graph(
                bm_iri,
                annotations=[(OBOINOWL.id, [term_id]),
                             (CCF.ccf_pref_label, [pref_label]),
                             (CCF.ccf_asctb_type, [asctb_type]),
                             (CCF.ccf_biomarker_type, [biomarker_type])])

            # Otherwise, the rdfs:label equals to the preferred label
            if is_provisional:
                self._add_term_to_graph(
                    bm_iri,
                    subClassOf=CCF.biomarker,
                    label=pref_label)
                self._add_provisional_definition(bm_iri)

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
            as_id, is_provisional = self._get_as_id(anatomical_structure)
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
            ct_id, is_provisional = self._get_ct_id(cell_type)
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
            ct_id, is_provisional = self._get_ct_id(cell_type)
            ct_iri = URIRef(self._expand_cell_type_id(ct_id))
            for anatomical_structure in anatomical_structures:
                as_id, is_provisional = self._get_as_id(anatomical_structure)
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
        as_id, is_provisional = self._get_as_id(last_anatomical_structure)
        as_iri = URIRef(self._expand_anatomical_entity_id(as_id))
        anatomical_structure = self._add_term_to_graph(as_iri)

        ######################################################
        # Construct the axioms about cell types
        ######################################################
        cell_types = obj['cell_types']
        if not cell_types:
            raise ValueError("Cell type data are missing")

        last_cell_type = self._get_last_item(cell_types)
        ct_id, is_provisional = self._get_ct_id(last_cell_type)
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
                    self._add_term_to_graph(iri)

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
        is_provisional = False
        if not as_id or ":" not in as_id:
            as_pref_label = anatomical_structure['name']
            if not as_pref_label:
                as_pref_label = anatomical_structure['rdfs_label']
            as_id = self._generate_provisional_id(as_pref_label)
            is_provisional = True
        return as_id, is_provisional

    def _get_ct_id(self, cell_type):
        ct_id = cell_type['id']
        is_provisional = False
        if not ct_id or ":" not in ct_id:
            ct_pref_label = cell_type['name']
            if not ct_pref_label:
                ct_pref_label = cell_type['rdfs_label']
            ct_id = self._generate_provisional_id(ct_pref_label)
            is_provisional = True
        if "PCL:" in ct_id:
            is_provisional = True
        return ct_id, is_provisional

    def _get_bm_id(self, marker):
        bm_id = marker['id']
        is_provisional = False
        if not self._is_valid_marker(marker):
            bm_pref_label = marker['name']
            if not bm_pref_label:
                bm_pref_label = marker['rdfs_label']
            bm_id = self._generate_provisional_id(bm_pref_label)
            is_provisional = True
        return bm_id, is_provisional

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

    def _add_provisional_definition(self, iri):
        provisional_definition =\
            Literal("This term is a temporary placeholder based on expert recommendation and it is NOT in a stable version")
        is_provisional = Literal("true", datatype=XSD.boolean)
        self.graph.add((iri, OBO.IAO_0000115, provisional_definition))
        self.graph.add((iri, CCF.ccf_is_provisional, is_provisional))

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
        elif "PCL:" in str:
            return self._expand_pcl_id(str)
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

    def _expand_pcl_id(self, str):
        pcl_pattern = re.compile("PCL:", re.IGNORECASE)
        return pcl_pattern.sub(
            "http://purl.obolibrary.org/obo/PCL_", str)

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
