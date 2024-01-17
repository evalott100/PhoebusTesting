"""
Generate the records for the screen `testing_no_pvi.bob`, not generated with PVI!

Unfortunately, Out records can't have their alarm set in softioc so
we use In records for Write widgets bere.
"""

from typing import Callable

from softioc import builder

from phoebus_testing import (
    ROW_LENGTH,
    AlarmSeverities,
    cycle_severities,
    set_alarm,
)


def create_record(
    pv_name: str,
    builder_method: Callable,
    alarm_severity: int,
    *builder_method_args,
    **builder_method_kwargs,
):
    if alarm_severity != AlarmSeverities.DISCONNECTED and builder_method:
        record = builder_method(pv_name, *builder_method_args, **builder_method_kwargs)
        set_alarm(record, alarm_severity)


def generate_records_for_manually_created_screen():
    records = {}
    for pv_name, severity in cycle_severities(
        2 * ROW_LENGTH, prefix="MANUALLY-GENERATED:TEXT-ENTRY"
    ):
        create_record(pv_name, builder.aIn, severity, initial_value=12345.67, EGU="mm")

    for pv_name, severity in cycle_severities(
        2 * ROW_LENGTH, prefix="MANUALLY-GENERATED:TEXT-UPDATE"
    ):
        create_record(pv_name, builder.aIn, severity, initial_value=12345.67, EGU="mm")

    for pv_name, severity in cycle_severities(
        2 * ROW_LENGTH, prefix="MANUALLY-GENERATED:COMBO-BOX"
    ):
        create_record(
            pv_name,
            builder.mbbIn,
            severity,
            "CLOSED",
            "OPEN",
            initial_value=1,
        )

    for pv_name, severity in cycle_severities(4, prefix="MANUALLY-GENERATED:LED-MULTI"):
        create_record(pv_name, builder.mbbIn, severity, 0, 1, 2, 3, 4, initial_value=1)

    for pv_name, severity in cycle_severities(
        ROW_LENGTH, prefix="MANUALLY-GENERATED:BYTE-MONITOR"
    ):
        create_record(
            pv_name,
            builder.longIn,
            severity,
            initial_value=0b00111001,
        )

    for pv_name, severity in cycle_severities(
        2 * ROW_LENGTH, prefix="MANUALLY-GENERATED:CHOICE-BUTTON"
    ):
        create_record(
            pv_name,
            builder.boolIn,
            severity,
            initial_value=0,
            ONAM="ON",
            ZNAM="OFF",
        )

    for pv_name, severity in cycle_severities(
        ROW_LENGTH, prefix="MANUALLY-GENERATED:BOOL-BUTTON"
    ):
        create_record(
            pv_name,
            builder.boolIn,
            severity,
            ONAM="ON",
            ZNAM="OFF",
            initial_value=1,
        )
    return records
