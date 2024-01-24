"""
Builds the records for the Master Timing Controller screen.
The screen doens't use pvi.
"""

from softioc import builder

from phoebus_testing import Record


def do_nothing(*args, **kwargs):
    pass


# the bobfile was built manually so we just need to define the records.
MASTER_TIMING_GENERATOR_RECORDS = [
    Record("STATUS:DESC", builder.longStringIn, (), {"initial_value": "Standby"}),
    Record("STATUS:BUSY", builder.boolIn, (), {}),
    Record("STATUS:SB-ENABLED", builder.boolIn, (), {}),
    Record("STATUS:MB-ENABLED", builder.boolIn, (), {}),
    Record("STATUS:LINAC-PRE", builder.boolIn, (), {}),
    Record("STATUS:TOP-UP", builder.boolIn, (), {}),
    Record("STATUS:SOFT-SYNC", builder.boolIn, (), {"initial_value": True}),
    Record("STATUS:TIMESTAMP", builder.boolIn, (), {"initial_value": True}),
    Record("STATUS:COINCIDENCE", builder.boolIn, (), {"initial_value": True}),
    Record("STATUS:FILL-ABORTED", builder.boolIn, (), {"initial_value": True}),
    Record("STATUS:MACHINE-TIME", builder.longStringIn, (), {"initial_value": "0"}),
    Record("STATUS:GUN", builder.aIn, (), {"initial_value": 5.0}),
    Record("STATUS:AC", builder.aIn, (), {"initial_value": 49.97}),
    Record("STATUS:STORED-CURRENT", builder.aIn, (), {"initial_value": 299.35}),
    Record(
        "FILL-MODE:MODE",
        builder.mbbOut,
        ("Standby", "Fill", "Drain"),
        {"initial_value": 0},
    ),
    Record(
        "FILL-MODE:START",
        builder.boolOut,
        (),
        {"initial_value": 0, "ZNAM": "Stop", "ONAM": "Start"},
    ),
    Record(
        "FILL-MODE:TARGET-CURRENT",
        builder.aOut,
        (),
        {"initial_value": 302, "EGU": "mA"},
    ),
    Record(
        "FILL-MODE:DELAY-GAP", builder.aOut, (), {"initial_value": 0, "EGU": "bkts"}
    ),
    Record(
        "FILL-MODE:WIDTH-BKTS", builder.aOut, (), {"initial_value": 900, "EGU": "bkts"}
    ),
    Record("FILL-MODE:REPEAT", builder.longOut, (), {"initial_value": 0}),
    Record(
        "FILL-MODE:MB-WIDTH-ADJUST",
        builder.aOut,
        (),
        {"initial_value": 0, "EGU": "bkts"},
    ),
    Record(
        "FILL-MODE:PHASE-SHIFT",
        builder.mbbOut,
        ("0-119", "120-239"),
        {"initial_value": 0},
    ),
    Record("MPS:TS", builder.longStringIn, (), {}),
    Record("AUTO-STOP-FILL:LATCH", builder.boolIn, (), {}),
    Record(
        "AUTO-STOP-FILL:CLEAR",
        builder.Action,
        (),
        {"on_update": do_nothing, "initial_value": 0},
    ),
    Record("AUTO-STOP-FILL:REASON", builder.stringIn, (), {}),
    Record("SOCS-LIMIT:LATCH", builder.boolIn, (), {}),
    Record(
        "SOCS-LIMIT:CLEAR",
        builder.Action,
        (),
        {"on_update": do_nothing, "initial_value": 0},
    ),
    Record("SOCS-LIMIT:SOCS", builder.stringIn, (), {}),
    Record("SOCS-LIMIT:LIMIT", builder.longOut, (), {"initial_value": 0}),
    Record("CHARGE-LIMIT:LATCH", builder.boolIn, (), {}),
    Record(
        "CHARGE-LIMIT:CLEAR",
        builder.Action,
        (),
        {"on_update": do_nothing, "initial_value": 0},
    ),
    Record("CHARGE-LIMIT:MAX-CHARGE", builder.stringIn, (), {}),
    Record("CHARGE-LIMIT:LIMIT", builder.longOut, (), {"initial_value": 0}),
    Record(
        "BR-PRE-INJ",
        builder.boolOut,
        (),
        {"ONAM": "On", "ZNAM": "Off", "initial_value": 0},
    ),
    Record(
        "BR-PRE-EXTR",
        builder.boolOut,
        (),
        {"ONAM": "On", "ZNAM": "Off", "initial_value": 0},
    ),
    Record(
        "SR-PRE-INJ",
        builder.boolOut,
        (),
        {"ONAM": "On", "ZNAM": "Off", "initial_value": 0},
    ),
    Record(
        "SR-INJ-SEPT",
        builder.boolOut,
        (),
        {"ONAM": "On", "ZNAM": "Off", "initial_value": 1},
    ),
    Record(
        "LB-DI-TRG", builder.mbbOut, ("Every Shot", "Every 10"), {"initial_value": 1}
    ),
    Record(
        "BS-DI-TRG", builder.mbbOut, ("Every Shot", "Every 10"), {"initial_value": 0}
    ),
    Record(
        "SR-DI-TRG",
        builder.boolOut,
        (),
        {"ONAM": "On", "ZNAM": "Off", "initial_value": 0},
    ),
    Record(
        "AUTO-STOP-FILL:ENABLE",
        builder.boolOut,
        (),
        {"ONAM": "On", "ZNAM": "Off", "initial_value": 0},
    ),
    Record(
        "SOCS-LIMIT:ENABLE",
        builder.boolOut,
        (),
        {"ONAM": "On", "ZNAM": "Off", "initial_value": 1},
    ),
    Record(
        "CHARGE-LIMIT:ENABLE",
        builder.boolOut,
        (),
        {"ONAM": "On", "ZNAM": "Off", "initial_value": 0},
    ),
]


def generate_records_for_master_timing_controller():
    for record in MASTER_TIMING_GENERATOR_RECORDS:
        record.record_creation_function(
            f"MTG:{record.pv_name}",
            *record.record_creation_function_args,
            **record.record_creation_function_kwargs,
        )
