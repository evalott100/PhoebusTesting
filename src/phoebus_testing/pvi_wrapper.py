from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pvi._format.dls import DLSFormatter
from pvi.device import (
    Component,
    Device,
    Grid,
    Group,
    Tree,
)


class Pvi:
    _screens_dir: Optional[Path] = None
    _clear_bobfiles: bool = False
    pvi_info_dict: Dict[str, Dict[Enum, List[Component]]] = {}

    @staticmethod
    def configure_pvi(screens_dir: Optional[str], clear_bobfiles: bool):
        if screens_dir:
            Pvi._screens_dir = Path(screens_dir)
            assert Pvi._screens_dir.is_dir(), "Screens directory must exist"

        Pvi._clear_bobfiles = clear_bobfiles

    @staticmethod
    def add_pvi_info(record_name: str, group: Enum, component: Component):
        record_base, _ = record_name.split(":", 1)

        if record_base in Pvi.pvi_info_dict:
            if group in Pvi.pvi_info_dict[record_base]:
                Pvi.pvi_info_dict[record_base][group].append(component)
            else:
                Pvi.pvi_info_dict[record_base][group] = [component]
        else:
            Pvi.pvi_info_dict[record_base] = {group: [component]}

    @staticmethod
    def create_pvi_records(record_prefix: str):
        """Create the :PVI records, one for each block and one at the top level"""

        devices: List[Device] = []
        for block_name, v in Pvi.pvi_info_dict.items():
            children: Tree = []

            for group, components in v.items():
                children.append(Group(group.name, Grid(), components))

            device = Device(block_name, children=children)
            devices.append(device)

        formatter = DLSFormatter(label_width=250)

        if Pvi._screens_dir:
            for device in devices:
                bobfile_path = Pvi._screens_dir / Path(f"{device.label}.bob")
                formatter.format(device, record_prefix + ":", bobfile_path)
