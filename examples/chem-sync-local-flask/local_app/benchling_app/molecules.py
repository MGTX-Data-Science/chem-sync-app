from typing import Any

from benchling_sdk.apps.framework import App
from benchling_sdk.helpers.serialization_helpers import fields
from benchling_sdk.models import (
    Molecule,
    MoleculeCreate,
    MoleculeStructure,
    MoleculeStructureStructureFormat,
    CustomEntityCreate
)

from local_app.lib.logger import get_logger

logger = get_logger()


def create_molecule(app: App, chemical_result: dict[str, Any]) -> Molecule:
    logger.debug("Chemical to create: %s", chemical_result)

    logger.debug(chemical_result)
    print(chemical_result)

    molecule_structure = MoleculeStructure(
        structure_format=MoleculeStructureStructureFormat.SMILES,
        value=chemical_result["smiles"],
    )

    config = app.config_store.config_by_path

    # Retrieve schema ID for "Molecules"
    schema_id = config(["Molecules"]).required().value_str()

    # Retrieve field IDs for Molecular Weight & MonoIsotopic
    molecular_weight_field = config(["Molecules", "Molecular Weight"]).required().value_str()
    mono_isotopic_field = config(["Molecules", "MonoIsotopic"]).required().value_str()
    cas_number_field = config(["Molecules", "Cas Number"]).required().value_str()
    name_field = config(["Molecules", "Molecule Name"]).required().value_str()

    # Retrieve Sync Folder ID (Ensure this exists in config!)
    folder_id = config(["molecules"]).required().value_str()

    entity_create = CustomEntityCreate(
        name=chemical_result["name"],
        schema_id=schema_id,  # Use the Custom Entity schema ID
        folder_id=folder_id,
        fields=fields(
            {
                molecular_weight_field: {"value": chemical_result["molecularWeight"]},
                mono_isotopic_field: {"value": chemical_result["monoisotopic"]},
                cas_number_field: {"value": chemical_result["casNumber"]},
                name_field: {"value": chemical_result["name"]},

            },
        ),
        aliases=[f"cid:{chemical_result['cid']}"],  # Optional aliases
    )

    return app.benchling.custom_entities.create(entity_create)

