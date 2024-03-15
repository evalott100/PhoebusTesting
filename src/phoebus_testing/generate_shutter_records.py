"""
The screen shutter.bob is manually created in phoebus. Motor control is generated by phoebus.
"""

from enum import Enum

from pvi.device import (
    LED,
    ButtonPanel,
    ComboBox,
    SignalR,
    SignalRW,
    TextRead,
    TextWrite,
)
from softioc import builder

from phoebus_testing import SignalRWidgets, WidgetRecord, name_to_pv, PREFIX
from phoebus_testing.pvi_wrapper import Pvi

NUMBER_OF_MOTORS = 8
NUMBER_OF_THERMOMETERS = 4


def generate_manual_motor_records():
    for motor_number in range(1, NUMBER_OF_MOTORS + 1):
        builder.longOut(f"MOTOR_{motor_number}:TWR", initial_value=0)
        builder.longOut(f"MOTOR_{motor_number}:TWF", initial_value=0)
        builder.longOut(f"MOTOR_{motor_number}:VAL", initial_value=0)
        builder.longOut(f"MOTOR_{motor_number}:RBV", initial_value=0)
        builder.boolOut(f"MOTOR_{motor_number}:STOP", initial_value=0)
        builder.longOut(f"MOTOR_{motor_number}:LOLO", initial_value=0)
        builder.longOut(f"MOTOR_{motor_number}:HIHI", initial_value=0)
        builder.longOut(f"MOTOR_{motor_number}:TWV", initial_value=0)


class MotorScreenGroup(Enum):
    STATUS = "Status"
    ELOSS = "Eloss"
    LIMIT_VIOLATION = "Limit Violation"
    KILL = "Kill"
    SYNC_VAL_RBV = "Sync Val RBV"
    COMMANDS = "Commands"
    CALIBRATION = "Calibration"
    RESOLUTION = "Resolution"
    MOTION = "Motion"
    OTHER = "Other"


MOTOR_WIDGET_RECORDS = [
    [
        WidgetRecord("Homed", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("LowLimit", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("CommsError", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("GainSupport", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("Moving", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("Problem", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("EncoderPresent", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("AtHome", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("FollowingError", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("ClosedLoop", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("Unused", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("HomeLimit", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("HighLimit", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("Done", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("DirectionPositive", LED, {}, builder.boolIn, (), {"initial_value": 0}),
    ],
    [
        WidgetRecord("SysFail", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("AmplifierLoss", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("EncoderLoss", LED, {}, builder.boolIn, (), {"initial_value": 0}),
        WidgetRecord("ElossClear", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0}),
    ],
    [
        WidgetRecord("UserHighLimit", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("UserLowLimit", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("DialHighLimit", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("DialLowLimit", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
    ],
    [
        WidgetRecord("Kill", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0}),
    ],
    [WidgetRecord("SyncValRBV", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0})],
    [
        WidgetRecord("HomeForward", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0}),
        WidgetRecord("HomeReverse", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0}),
        WidgetRecord("JogForward", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0}),
        WidgetRecord("JogReverse", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0}),
        WidgetRecord("TweakForward", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0}),
        WidgetRecord("TweakReverse", ButtonPanel, {}, builder.boolOut, (), {"initial_value": 0}),
        WidgetRecord("TweakStep", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
    ],
    [
        WidgetRecord("Calibration", TextRead, {}, builder.aIn, (), {"initial_value": 0}),
        WidgetRecord(
            "Direction",
            ComboBox,
            {
                "choices": ["Neg", "Pos"],
            },
            builder.mbbOut,
            ("Neg", "Pos"),
            {"initial_value": 0},
        ),
        WidgetRecord("UserOffset", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord(
            "SetUse",
            ComboBox,
            {
                "choices": ["Set", "Use"],
            },
            builder.mbbOut,
            ("Set", "Use"),
            {"initial_value": 0},
        ),
        WidgetRecord(
            "Offset",
            ComboBox,
            {
                "choices": ["Variable", "Fixed"],
            },
            builder.mbbOut,
            ("Variable", "Fixed"),
            {"initial_value": 0},
        ),
        WidgetRecord(
            "UseEncoder",
            ComboBox,
            {
                "choices": ["No", "Yes"],
            },
            builder.mbbOut,
            ("No", "Yes"),
            {"initial_value": 0},
        ),
    ],
    [
        WidgetRecord(
            "Resolution",
            ComboBox,
            {
                "choices": ["1", "10", "100"],
            },
            builder.mbbOut,
            ("1", "10", "100"),
            {"initial_value": 0},
        ),
        WidgetRecord(
            "MotorStepSize",
            TextWrite,
            {},
            builder.aOut,
            (),
            {"initial_value": 0},
        ),
        WidgetRecord(
            "StepsPerRev",
            TextRead,
            {},
            builder.aIn,
            (),
            {"EGU": "steps/r", "initial_value": 0},
        ),
        WidgetRecord(
            "EGUsPerRev",
            TextRead,
            {},
            builder.aIn,
            (),
            {"EGU": "mm/rev", "initial_value": 0},
        ),
        WidgetRecord(
            "EncodeStepSize",
            TextWrite,
            {},
            builder.aOut,
            (),
            {"initial_value": 0, "initial_value": 0},
        ),
        WidgetRecord(
            "ReadBackStepSize",
            TextRead,
            {},
            builder.aIn,
            (),
            {"EGU": "mm", "initial_value": 0},
        ),
        WidgetRecord("UseEncoderIfPresent", TextRead, {}, builder.mbbIn, (), {"initial_value": 0}),
    ],
    [
        WidgetRecord("MaxVelocity", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("BaseVelocity", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("Velocity", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("SecsToVelocity", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("JVEL", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("JogAcceleration", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("BacklashDistance", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("BacklashVelocity", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("BacklashSecsToVelocity", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("MoveFraction", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("RetryDeadband", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("MaxRetries", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
    ],
    [
        WidgetRecord("PREC", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
        WidgetRecord("EGU", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
    ],
]

MotorGroupToWidgetRecord = zip(MotorScreenGroup, MOTOR_WIDGET_RECORDS)


def generate_motor_settings_screen():
    for group, widget_records in MotorGroupToWidgetRecord:
        for widget_record in widget_records:
            widget_name_in_pv_format = name_to_pv(widget_record.name)
            for motor_number in range(1, NUMBER_OF_MOTORS + 1):
                pv_name = (
                    f"MOTOR_{motor_number}:{group.name}:{widget_name_in_pv_format}"
                )
                widget_record.record_creation_function(
                    pv_name,
                    *widget_record.record_creation_function_args,
                    **widget_record.record_creation_function_kwargs,
                )

            generic_pv_name = f"MOTOR_$(M):{group.name}:{widget_name_in_pv_format}"
            pv_name_no_number = f"MOTOR:{group.name}:{widget_name_in_pv_format}"
            if widget_record.widget in SignalRWidgets:
                component = SignalR(
                    name=widget_record.name,
                    read_pv=PREFIX + generic_pv_name,
                    read_widget=widget_record.widget(**widget_record.widget_kwargs),
                )
            else:
                component = SignalRW(
                    name=widget_record.name,
                    write_pv=PREFIX + generic_pv_name,
                    write_widget=widget_record.widget(**widget_record.widget_kwargs),
                )
                Pvi.add_pvi_info(pv_name_no_number, group, component)


def generate_manual_temperature_records():
    for thermometer_number in range(1, NUMBER_OF_THERMOMETERS + 1):
        builder.longOut(f"TEMP_{thermometer_number}:VAL", initial_value=22)


class TemperatureGroup(Enum):
    GENERAL = "General"


THERMOMETER_WIDGET_RECORDS = [
    [
        WidgetRecord(
            "CurrentTemp",
            TextRead,
            {},
            builder.aIn,
            (),
            {"initial_value": 0},
        ),
        WidgetRecord(
            "ErrorLevel",
            TextWrite,
            {},
            builder.aOut,
            (),
            {"initial_value": 0},
        ),
        WidgetRecord(
            "ErrorLevelRBV",
            TextWrite,
            {},
            builder.aIn,
            (),
            {"initial_value": 0},
        ),
        WidgetRecord("WarningLevel", TextWrite, {}, builder.aOut, (), {"initial_value": 0}),
    ]
]

TemperatureGroupToWidgetRecord = zip(TemperatureGroup, THERMOMETER_WIDGET_RECORDS)


def generate_temperature_settings_screen():
    for group, widget_records in TemperatureGroupToWidgetRecord:
        for widget_record in widget_records:
            widget_name_in_pv_format = name_to_pv(widget_record.name)
            for thermometer_number in range(1, NUMBER_OF_THERMOMETERS + 1):
                pv_name = (
                    f"TEMP_{thermometer_number}:{group.name}:{widget_name_in_pv_format}"
                )
                widget_record.record_creation_function(
                    pv_name,
                    *widget_record.record_creation_function_args,
                    **widget_record.record_creation_function_kwargs,
                )

            generic_pv_name = f"TEMP_$(T):{group.name}:{widget_name_in_pv_format}"
            pv_name_no_number = f"TEMP:{group.name}:{widget_name_in_pv_format}"
            if widget_record.widget in SignalRWidgets:
                component = SignalR(
                    name=widget_record.name,
                    read_pv=PREFIX + generic_pv_name,
                    read_widget=widget_record.widget(**widget_record.widget_kwargs),
                )
            else:
                component = SignalRW(
                    name=widget_record.name,
                    write_pv= PREFIX + generic_pv_name,
                    write_widget=widget_record.widget(**widget_record.widget_kwargs),
                )
            Pvi.add_pvi_info(pv_name_no_number, group, component)


def generate_shutter_screens():
    generate_manual_motor_records()
    generate_motor_settings_screen()
    generate_manual_temperature_records()
    generate_temperature_settings_screen()
