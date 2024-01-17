from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from epicsdbbuilder import RecordName
from pvi._format.dls import DLSFormatter
from pvi.device import (
    Component,
    Device,
    Grid,
    Group,
    Tree,
)
from softioc import builder


# All the widgets we'll use
class PviGroupBasic(Enum):
    _LED = "LED"
    _BUTTON_PANEL = "BUTTON-PANEL"
    _COMBO_BOX = "COMBO-BOX"
    _DEVICE_REF = "DEVICE-REF"
    _TEXT_READ = "TEXT-READ"
    _TEXT_WRITE = "TEXT-WRITE"


# All the widgets we won't use
class PviGroupNotImplemented(Enum):
    _ARRAY_TRACE = "ARRAY-TRACE"
    _ARRAY_WRITE = "ARRAY-WRITE"
    _BIT_FIELD = "BIT-FIELD"
    _CHECK_BOX = "CHECK-BOX"
    _IMAGE_READ = "IMAGE-READ"
    _PROGRESS_BAR = "PROGRESS-BAR"


# Adapted from pandablocks-ioc
class Pvi:
    _screens_dir: Optional[Path] = None
    _clear_bobfiles: bool = False
    pvi_info_dict: Dict[str, Dict[PviGroupBasic, List[Component]]] = {}

    @staticmethod
    def configure_pvi(screens_dir: Optional[str], clear_bobfiles: bool):
        if screens_dir:
            Pvi._screens_dir = Path(screens_dir)
            assert Pvi._screens_dir.is_dir(), "Screens directory must exist"

        Pvi._clear_bobfiles = clear_bobfiles

    @staticmethod
    def add_pvi_info(record_name: str, group: PviGroupBasic, component: Component):
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
        pvi_records: List[str] = []
        for block_name, v in Pvi.pvi_info_dict.items():
            children: Tree = []

            for group, components in v.items():
                children.append(Group(group.name, Grid(), components))

            device = Device(block_name, children=children)
            devices.append(device)

            """
            # Add -PVI structure. Unfortunately we need something in the database
            # that holds the PVI PV, and the QSRV records we have made so far aren't
            # in the database, so have to make an extra record here just to hold the
            # PVI PV name
            pvi_record_name = block_name + ":PVI"
            block_pvi = builder.longStringIn(
                pvi_record_name + "_PV",
                initial_value=RecordName(pvi_record_name),
            )
            block_name_suffixed = f"pvi.{block_name.lower()}.d"
            block_pvi.add_info(
                "Q:group",
                {
                    RecordName("PVI"): {
                        block_name_suffixed: {
                            "+channel": "VAL",
                            "+type": "plain",
                            "+trigger": block_name_suffixed,
                        }
                    }
                },
            )

            pvi_records.append(pvi_record_name)
            """

        formatter = DLSFormatter(label_width=250)

        if Pvi._screens_dir:
            for device in devices:
                bobfile_path = Pvi._screens_dir / Path(f"{device.label}.bob")
                formatter.format(device, record_prefix + ":", bobfile_path)
