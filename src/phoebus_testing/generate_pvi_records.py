"""
Generate records and add PVI info, should output to `testing_pvi.bob`.

Unfortunately, Out records can't have their alarm set in softioc so
we use In records for Write widgets bere.
"""

from typing import Any, Callable, Dict

from phoebus_testing.pvi_wrapper import GroupToComponent, Pvi, PviGroup
from phoebus_testing.utils import set_alarm


def create_record_and_pvi_widget(
    pv_name: str,
    builder_method: Callable,
    initial_value: Any,
    alarm_severity: int,
    pvi_group: PviGroup,
    **extra_builder_args: Dict[str, Any],
):
    record = builder_method(pv_name, **extra_builder_args, initial_value=initial_value)
    set_alarm(record, alarm_severity)
    component = GroupToComponent[pvi_group]
    Pvi.add_pvi_info(pv_name, pvi_group, component)


def generate_records_for_pvi_generated_screen():
    records = {}
    return records
