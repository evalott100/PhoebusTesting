"""
Generate records and add PVI info, should output to `testing_pvi.bob`.

Unfortunately, Out records can't have their alarm set in softioc so
we use In records for Write widgets bere.
"""

from typing import Callable, Dict

from pvi.device import SignalRW

from phoebus_testing import PREFIX
from phoebus_testing.pvi_wrapper import (
    GroupToBuildFunction,
    GroupToWidget,
    Pvi,
    PviGroup,
)
from phoebus_testing.utils import cycle_severities, set_alarm

Pvi.configure_pvi("bobfiles/pvi", True)


def create_record_and_pvi_widget(
    pv_name: str,
    builder_method: Callable,
    alarm_severity: int,
    pvi_group: PviGroup,
):
    record = builder_method(pv_name)
    set_alarm(record, alarm_severity)
    component = SignalRW(
        name=str(alarm_severity),
        pv=pv_name,
        widget=GroupToWidget[pvi_group],
    )
    Pvi.add_pvi_info(pv_name, pvi_group, component)


def generate_records_for_pvi_generated_screen() -> Dict:
    records = {}

    for pvi_group, builder_method in GroupToBuildFunction.items():
        if pvi_group == PviGroup._DEVICE_REF:
            continue

        for pv_name, severity in cycle_severities(
            4, prefix=f"PVI_GENERATED:{pvi_group.value}"
        ):
            create_record_and_pvi_widget(
                pv_name,
                builder_method,
                severity,
                pvi_group=pvi_group,
            )
    Pvi.create_pvi_records(PREFIX)
    return records
