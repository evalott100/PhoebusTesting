from typing import Callable

from softioc import asyncio_dispatcher, builder, softioc

from phoebus_testing import PREFIX
from phoebus_testing.generate_shutter_records import generate_shutter_screens
from phoebus_testing.pvi_wrapper import Pvi

from phoebus_testing import (
    ROW_LENGTH,
    AlarmSeverities,
    cycle_severities,
    set_alarm,
)
from phoebus_testing.generate_shutter_records import generate_shutter_screens


def initRecord(
    pv_name: str,
    builder_method: Callable,
    alarm_severity: int,
    *builder_method_args,
    **builder_method_kwargs,
):
    if alarm_severity != AlarmSeverities.DISCONNECTED and builder_method:
        record = builder_method(pv_name, *builder_method_args, **builder_method_kwargs)
        set_alarm(record, alarm_severity)

def genRecs():
    records = {}

    for i in range(6)(

    ):
        initRecord(
            pv_name,
            builder.boolIn,
            severity,
            initial_value=0,
            ONAM="ON",
            ZNAM="OFF",
        )
    

    return records



def run_softioc():
    Pvi.configure_pvi("bobfiles/pvi", True)
    builder.SetDeviceName(PREFIX.removesuffix(":"))
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    genRecs()
    generate_shutter_screens()
    Pvi.create_pvi_records(PREFIX)

    builder.LoadDatabase()
    softioc.iocInit(dispatcher)
    softioc.interactive_ioc()