"""
Generate records and add PVI info, should output to `testing_pvi.bob`.

Unfortunately, Out records can't have their alarm set in softioc so
we use In records for Write widgets bere.
"""
from enum import Enum

from pvi.device import (
    LED,
    ButtonPanel,
    ComboBox,
    DeviceRef,
    SignalRW,
    TextRead,
    TextWrite,
)
from softioc import builder

from phoebus_testing import (
    ROW_LENGTH,
    AlarmSeverities,
    WidgetRecord,
    cycle_severities,
    set_alarm,
)
from phoebus_testing.pvi_wrapper import Pvi


# It would be nice to add these in the future
class PviGroupNotImplemented(Enum):
    _ARRAY_TRACE = "ARRAY-TRACE"
    _ARRAY_WRITE = "ARRAY-WRITE"
    _BIT_FIELD = "BIT-FIELD"
    _CHECK_BOX = "CHECK-BOX"
    _IMAGE_READ = "IMAGE-READ"
    _PROGRESS_BAR = "PROGRESS-BAR"


class PviGroup(Enum):
    _LED = "LED"
    _BUTTON_PANEL = "BUTTON-PANEL"
    _COMBO_BOX = "COMBO-BOX"
    _DEVICE_REF = "DEVICE-REF"
    _TEXT_READ = "TEXT-READ"
    _TEXT_WRITE = "TEXT-WRITE"


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
        widget_kwargs={"actions": dict(On=1, Off=0)},
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
        record_creation_function_args=(0, 1),
        record_creation_function_kwargs={"initial_value": 0},
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

            component = SignalRW(severity.name, pv_name, widget=widget)
            Pvi.add_pvi_info(pv_name, pvi_group, component)
