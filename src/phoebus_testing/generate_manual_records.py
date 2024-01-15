"""
Generate the records for the screen `testing_no_pvi.bob`, not generated with PVI!

Unfortunately, Out records can't have their alarm set in softioc so
we use In records for Write widgets bere.
"""
from phoebus_testing.utils import cycle_severities, set_alarm
from softioc import builder


def generate_records_for_manually_created_screen():
    records = {}
    for pv_name, severity in cycle_severities(8, prefix="MANUAL-TEXT-ENTRY"):
        records[pv_name] = builder.aIn(pv_name, initial_value=12345.67, EGU="mm")
        set_alarm(records[pv_name], severity)

    for pv_name, severity in cycle_severities(8, prefix="MANUAL-TEXT-UPDATE"):
        records[pv_name] = builder.aIn(pv_name, initial_value=12345.67, EGU="mm")
        set_alarm(records[pv_name], severity)

    for pv_name, severity in cycle_severities(8, prefix="MANUAL-COMBO-BOX"):
        records[pv_name] = builder.mbbIn(
            pv_name,
            "CLOSED",
            "OPEN",
            initial_value=1,
        )
        set_alarm(records[pv_name], severity)

    for pv_name, severity in cycle_severities(4, prefix="MANUAL-LED-MULTI"):
        records[pv_name] = builder.mbbIn(
            pv_name,
            0,
            1,
            2,
            3,
            4,
            initial_value=1,
        )
        set_alarm(records[pv_name], severity)

    for pv_name, severity in cycle_severities(4, prefix="BYTE-MONITOR"):
        records[pv_name] = builder.longIn(
            pv_name,
            initial_value=0b00111001,
        )
        set_alarm(records[pv_name], severity)

    for pv_name, severity in cycle_severities(8, prefix="MANUAL-CHOICE-BUTTON"):
        records[pv_name] = builder.boolIn(
            pv_name,
            ONAM="ON",
            ZNAM="OFF",
            initial_value=0,
        )
        set_alarm(records[pv_name], severity)

    for pv_name, severity in cycle_severities(4, prefix="MANUAL-BOOL-BUTTON"):
        records[pv_name] = builder.boolIn(
            pv_name,
            ONAM="ON",
            ZNAM="OFF",
            initial_value=1,
        )
        set_alarm(records[pv_name], severity)
    return records
