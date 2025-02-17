from typing import Any, List, Dict, Type
from dataclasses import is_dataclass
import numpy as np

from .environment import (
    Entity,
    ObsSpace,
)


def obs_space_from_dataclasses(*dss: Type) -> ObsSpace:
    entities = {}
    for ds in dss:
        if not is_dataclass(ds):
            raise ValueError(f"{ds} is not a dataclass")
        # TODO: check field types are valid
        entities[ds.__name__] = Entity(
            features=list(
                [
                    key
                    for key in ds.__dataclass_fields__.keys()
                    if not key.startswith("_")
                ]
            ),
        )
    return ObsSpace(entities)


def extract_features(
    entities: Dict[str, List[Any]], obs_filter: ObsSpace
) -> Dict[str, np.ndarray]:
    selectors = {}
    for entity_name, entity in obs_filter.entities.items():
        selectors[entity_name] = np.array(
            [[getattr(e, f) for f in entity.features] for e in entities[entity_name]],
            dtype=np.float32,
        ).reshape(-1, len(entity.features))
    return selectors
