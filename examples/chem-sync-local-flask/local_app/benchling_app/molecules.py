from typing import Any

from benchling_sdk.apps.framework import App
from benchling_sdk.helpers.serialization_helpers import fields
from benchling_sdk.models import (
    Molecule,
    MoleculeCreate,
    MoleculeStructure,
    MoleculeStructureStructureFormat,
    CustomEntityCreate,
    CustomEntity,
    NamingStrategy
)

from local_app.lib.logger import get_logger

logger = get_logger()


def create_molecule(app: App, chemical_result: dict[str, Any]) -> Molecule:
    logger.debug("Chemical to create: %s", chemical_result)
    logger.debug(chemical_result)
    print(chemical_result)

    config = app.config_store.config_by_path

    cid_alias = f"{chemical_result['name']}-{chemical_result['cid']}"
    logger.debug("CID alias: %s", cid_alias)
    # Search for existing entity by alias
    existing_entity = app.benchling.custom_entities.list(
        schema_id = 'ts_NDUzuVlK',
        schema_fields={"CID Number":str(chemical_result['cid'])},
        page_size=100,
    ).first()

    # You might need to filter manually if 'list' doesn't accept alias search
    if existing_entity:
        logger.info("Entity already exists for alias %s", cid_alias)
        return existing_entity, True

    # Create MoleculeStructure
    molecule_structure = MoleculeStructure(
        structure_format=MoleculeStructureStructureFormat.SMILES,
        value=chemical_result["smiles"],
    )

    

    # Retrieve necessary config values
    schema_id = config(["Molecules"]).required().value_str()
    molecular_weight_field = config(["Molecules", "Molecular Weight"]).required().value_str()
    mono_isotopic_field = config(["Molecules", "MonoIsotopic"]).required().value_str()
    cid_number_field = config(["Molecules", "CID Number"]).required().value_str()
    name_field = config(["Molecules", "Molecule Name"]).required().value_str()
    folder_id = config(["molecules"]).required().value_str()

    # Create entity
    entity_create = CustomEntityCreate(
        name=chemical_result["name"],
        schema_id=schema_id,
        folder_id=folder_id,
        registry_id='src_eiUlVDOn',
        naming_strategy=NamingStrategy.REPLACE_NAMES_FROM_PARTS,
        fields=fields(
            {
                molecular_weight_field: {"value": chemical_result["molecularWeight"]},
                mono_isotopic_field: {"value": chemical_result["monoisotopic"]},
                cid_number_field: {"value": str(chemical_result['cid'])},
                name_field: {"value": chemical_result["name"]},
            }
        ),
    )
    entity = app.benchling.custom_entities.create(entity_create)
    return entity,False