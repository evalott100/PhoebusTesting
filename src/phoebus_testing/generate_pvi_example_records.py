"""
Generate records and add PVI info, should output to `testing_pvi.bob`.

Unfortunately, Out records can't have their alarm set in softioc so
we use In records for Write widgets bere.
"""

from enum import Enum

from pvi.device import (
    LED,
    ArrayTrace,
    BitField,
    ButtonPanel,
    CheckBox,
    ComboBox,
    DeviceRef,
    ImageRead,
    Plot,
    ProgressBar,
    SignalR,
    SignalRW,
    TextRead,
    TextWrite,
)
from softioc import builder

from phoebus_testing import (
    EXAMPLE_IMAGE,
    EXAMPLE_WAVEFORM,
    ROW_LENGTH,
    AlarmSeverities,
    SignalRWidgets,
    WidgetRecord,
    cycle_severities,
    set_alarm,
)
from phoebus_testing.pvi_wrapper import Pvi


# It would be nice to add these in the future
class PviGroupNotImplemented(Enum):
    ARRAY_WRITE = "ARRAY-WRITE"  # Not really sure what this is actually...?


class PviGroup(Enum):
    LED = "LED"
    BUTTON_PANEL = "BUTTON-PANEL"
    COMBO_BOX = "COMBO-BOX"
    DEVICE_REF = "DEVICE-REF"
    TEXT_READ = "TEXT-READ"
    TEXT_WRITE = "TEXT-WRITE"
    BIT_FIELD = "BIT-FIELD"
    IMAGE_READ = "IMAGE-READ"
    PROGRESS_BAR = "PROGRESS-BAR"
    CHECK_BOX = "CHECK-BOX"
    PLOT = "PLOT"
    # ARRAY_TRACE = "ARRAY-TRACE"


PVI_WIDGET_RECORDS = [
    WidgetRecord(
        "LED",
        widget=LED,
        widget_kwargs={},
        record_creation_function=builder.mbbIn,
        record_creation_function_args=(0, 1, 2, 3),
        record_creation_function_kwargs={"initial_value": 1},
    ),
    WidgetRecord(
        "ButtonPanel",
        widget=ButtonPanel,
        widget_kwargs={"actions": dict(On="1", Off="0")},
        record_creation_function=builder.boolIn,
        record_creation_function_args=(),
        record_creation_function_kwargs={
            "ONAM": "On",
            "ZNAM": "Off",
            "initial_value": 0,
        },
    ),
    WidgetRecord(
        "ComboBox",
        widget=ComboBox,
        widget_kwargs={"choices": ["CLOSED", "OPEN"]},
        record_creation_function=builder.mbbIn,
        record_creation_function_args=(0, "CLOSED", "OPEN"),
        record_creation_function_kwargs={"initial_value": 1},
    ),
    WidgetRecord(
        "DeviceRef",
        widget=DeviceRef,
        widget_kwargs={
            "name": "NoAlarmsOnDeviceRefs",
            "pv": "FakePV",
            "ui": "another_bobfile",
        },
        record_creation_function=None,
        record_creation_function_args=(),
        record_creation_function_kwargs={},
    ),
    WidgetRecord(
        "TextRead",
        widget=TextRead,
        widget_kwargs={},
        record_creation_function=builder.aIn,
        record_creation_function_args=(),
        record_creation_function_kwargs={"initial_value": 1234.567, "EGU": "mm"},
    ),
    WidgetRecord(
        "TextWrite",
        widget=TextWrite,
        widget_kwargs={},
        record_creation_function=builder.aIn,
        record_creation_function_args=(),
        record_creation_function_kwargs={"initial_value": 1234.567, "EGU": "mm"},
    ),
    WidgetRecord(
        "BitField",
        widget=BitField,
        widget_kwargs={
            "labels": ["a", "b", "c", "d", "e", "f", "g", "h"],
        },
        record_creation_function=builder.longIn,
        record_creation_function_args=(),
        record_creation_function_kwargs={"initial_value": 0b00110011},
    ),
    WidgetRecord(
        "ImageRead",
        widget=ImageRead,
        widget_kwargs={},
        record_creation_function=builder.WaveformIn,
        record_creation_function_args=(),
        record_creation_function_kwargs={
            "initial_value": EXAMPLE_IMAGE,
            "NELM": int(len(EXAMPLE_IMAGE)),
        },
    ),
    WidgetRecord(
        "ProgressBar",
        widget=ProgressBar,
        widget_kwargs={},
        record_creation_function=builder.aIn,
        record_creation_function_args=(),
        record_creation_function_kwargs={"initial_value": 0.66},
    ),
    WidgetRecord(
        "CheckBox",
        widget=CheckBox,
        widget_kwargs={},
        record_creation_function=builder.boolIn,
        record_creation_function_args=(),
        record_creation_function_kwargs={"initial_value": True},
    ),
]

GroupToWidgetRecord = zip(PviGroup, PVI_WIDGET_RECORDS)


def generate_records_for_pvi_generated_screen():
    for pvi_group, widget_record in GroupToWidgetRecord:
        builder_method = widget_record.record_creation_function
        widget = widget_record.widget(**widget_record.widget_kwargs)
        if not builder_method:
            assert widget_record.widget == DeviceRef
            Pvi.add_pvi_info("PVI_GENERATED:DEVICE-REF", pvi_group, widget)
            continue

        for pv_name, severity in cycle_severities(
            ROW_LENGTH, prefix=f"PVI_GENERATED:{pvi_group.value}"
        ):
            if severity != AlarmSeverities.DISCONNECTED:
                record = builder_method(
                    pv_name,
                    *widget_record.record_creation_function_args,
                    **widget_record.record_creation_function_kwargs,
                )
                set_alarm(record, severity)

            if widget_record.widget in SignalRWidgets:
                component = SignalR(name=severity.name, pv=pv_name, widget=widget)
            else:
                component = SignalRW(name=severity.name, pv=pv_name, widget=widget)
            Pvi.add_pvi_info(pv_name, pvi_group, component)

            if widget_record.widget in (ImageRead, Plot):  # Only want one of these.
                break
