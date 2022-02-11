# CEDAR-to-CCF

A Python tool to convert ASCT+B tables to CCF Biological Structure Ontology.

The CCF Biological Structure Ontology (CCF-BSO) models the relationship between a human cell type and its characterizing biomarkers. Each anatomical structure in the human body consists of different cell types and the same cell types might exist in multiple organ locations. The CCF-BSO makes the distinction between the cell types that are found in several locations by naming them differently, for example, the 'fibroblast' cell has various names such as "fibroblast of anterior cardiac vein", "fibroblast of coronary sinus", "fibroblast of epicardium", etc. The distinction is important in developing a human atlas because those cells may inherit different properties, such as their characterizing biomarkers.

The creation of the CCF-BSO starts by working with organ experts to manually construct the relevant partonomies of anatomical structure and describe the cell types present in the anatomical structure by presenting a set of their characterizing biomarkers (e.g., gene, protein, lipid and metabolite expression profiles). Additionally, the experts may add some publication DOIs that contain the conclusion about the cell type and its biomarkers. These acquired metadata are then converted into OWL axioms which are the building blocks of the CCF-BSO.

## Installing the tool

You can install the application using `pip` after you clone the repository.
```
$ cd asctb2ccf
$ pip install .
```

## Using the tool

Type the command below to begin the data conversion:
```
$ asctb2cct --organ-name Kidney --ontology-iri http://purl.org/ccf/data/asctb-kidney.owl -o asctb-kidney.owl
```

Possible options for the `--organ-name` argument are:
* `BoneMarrow`
* `Brain`
* `Blood`
* `Eye`
* `FallopianTube`
* `Heart`
* `Kidney`
* `Knee`
* `LargeIntestine`
* `Liver`
* `Lung`
* `LymphNode`
* `LymphVasculature`
* `Ovary`
* `Pancreas`
* `PeripheralNervousSystem`
* `Prostate`
* `Skin`
* `SmallIntestine`
* `Spleen`
* `Thymus`
* `Ureter`
* `UrinaryBladder`
* `Uterus`
* `BloodVasculature`
