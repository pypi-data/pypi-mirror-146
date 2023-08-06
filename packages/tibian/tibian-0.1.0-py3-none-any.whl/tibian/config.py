from typing import Any, Dict, Sequence, Type, Union

import yaml

import tibian.vars
from tibian.sources import POSSIBLE_SOURCES
from tibian.sources.ticketsource import TicketSource
from tibian.targets import POSSIBLE_DESTINATIONS
from tibian.targets.target import Target


def load_config(filepath=tibian.vars.get_std_config_filepath()):

    with open(filepath) as c:
        config = yaml.safe_load(c)

    return config


def get_cls_from_possible(
    entry_type: str, possible: Sequence[Union[Type[TicketSource], Type[Target]]]
):

    for pos in possible:
        if pos.TYPENAME == entry_type:
            return pos


def construct_objects_based_on_config_type(configs: Sequence[Dict[str, Any]]) -> Any:
    objects = []
    for entry in configs:
        entry_type = entry["type"]
        cls = get_cls_from_possible(entry_type, POSSIBLE_SOURCES + POSSIBLE_DESTINATIONS)
        obj = cls(entry["name"], entry["config"])
        objects.append(obj)

    return objects
