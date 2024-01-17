"""
Generate records and add PVI info, should output to `testing_pvi.bob`.

Unfortunately, Out records can't have their alarm set in softioc so
we use In records for Write widgets bere.
"""
from functools import partial
from typing import Callable, Dict

from pvi.device import (
    LED,
    ButtonPanel,
    ComboBox,
    DeviceRef,
    SignalR,
    SignalRW,
    TextRead,
    TextWrite,
)
from softioc import builder

from phoebus_testing import (
    ROW_LENGTH,
    AlarmSeverities,
    cycle_severities,
    set_alarm,
)
from phoebus_testing.pvi_wrapper import Pvi, PviGroupBasic


def generate_components():
    Components = [
        lambda alarm_sev, pv_name: SignalRW(name=alarm_sev, pv=pv_name, widget=LED()),
        # ArrayTrace(axis="x"),
        # ArrayWrite(),
        # BitField(["A", "B", "C", "D", "E", "F", "G", "H"]),
        # ButtonPanel(),
        lambda alarm_sev, pv_name: SignalRW(
            name=alarm_sev,
            pv=pv_name,
            read_pv=pv_name,
            widget=ButtonPanel(actions=dict(On=1, Off=0)),
            read_widget=TextRead(),
        ),
        lambda alarm_sev, pv_name: SignalRW(
            name=alarm_sev, pv=pv_name, widget=ComboBox(choices=["CLOSED", "OPEN"])
        ),
        lambda alarm_sev, pv_name: DeviceRef(
            name="NoAlarmsOnDeviceRefs", pv=pv_name, ui="another_bobfile"
        ),
        # ImageRead(),
        # ProgressBar(),
        lambda alarm_sev, pv_name: SignalR(
            name=alarm_sev, pv=pv_name, widget=TextRead()
        ),
        lambda alarm_sev, pv_name: SignalRW(
            name=alarm_sev, pv=pv_name, widget=TextWrite()
        ),
    ]

    GroupToComponent = dict(zip(PviGroupBasic, Components))

    BuildFunctions = [
        lambda pv_name: builder.mbbIn(pv_name, 0, 1, 2, 3, initial_value=1),  # LED
        # partial(builder.WaveformIn, initial_value=EXAMPLE_IMAGE),  # ArrayTrace
        # partial(builder.WaveformIn, initial_value=EXAMPLE_WAVEFORM),  # ArrayWrite
        # partial(builder.longIn, initial_value=0b00110011),  # BitField
        # partial(builder.boolIn, initial_value=1, ONAM="ON", ZNAM="OFF"),  # ButtonPanel
        partial(builder.boolIn, ONAM="ON", ZNAM="OFF", initial_value=0),  # CheckBox
        lambda pv_name: builder.mbbIn(
            pv_name, "CLOSED", "OPEN", initial_value=0
        ),  # ComboBox
        None,  # DeviceRef
        # partial(builder.WaveformIn, initial_value=EXAMPLE_IMAGE),  # Image
        # partial(builder.aIn, initial_value=0.4),  # ProgressBar
        partial(builder.aIn, initial_value=1234.567, EGU="mm"),  # TextRead
        partial(builder.aIn, initial_value=1234.567, EGU="mm"),  # TextWrite
    ]

    GroupToBuildFunction = dict(zip(PviGroupBasic, BuildFunctions))

    return GroupToComponent, GroupToBuildFunction


def create_record_and_pvi_widget(
    pv_name: str,
    builder_method: Callable,
    alarm_severity: AlarmSeverities,
    pvi_group: PviGroupBasic,
    group_to_component: Dict,
):
    if alarm_severity != AlarmSeverities.DISCONNECTED and builder_method:
        record = builder_method(pv_name)
        set_alarm(record, alarm_severity)
    component = group_to_component[pvi_group](alarm_severity.name, pv_name)
    Pvi.add_pvi_info(pv_name, pvi_group, component)


def generate_records_for_pvi_generated_screen() -> Dict:
    records = {}
    group_to_component, group_to_build_function = generate_components()

    for pvi_group, builder_method in group_to_build_function.items():
        if not builder_method:
            create_record_and_pvi_widget(
                "PVI_GENERATED:DEVICE-REF",
                builder_method,
                AlarmSeverities.DISCONNECTED,
                PviGroupBasic._DEVICE_REF,
                group_to_component,
            )
            continue

        for pv_name, severity in cycle_severities(
            ROW_LENGTH, prefix=f"PVI_GENERATED:{pvi_group.value}"
        ):
            create_record_and_pvi_widget(
                pv_name, builder_method, severity, pvi_group, group_to_component
            )
    return records
