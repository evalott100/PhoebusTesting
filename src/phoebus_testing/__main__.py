from softioc import asyncio_dispatcher, builder, softioc

from phoebus_testing import PREFIX
from phoebus_testing.generate_manual_records import (
    generate_records_for_manually_created_screen,
)
from phoebus_testing.generate_pvi_example_records import (
    generate_records_for_pvi_generated_screen,
)
from phoebus_testing.generate_shutter_records import generate_shutter_screens
from phoebus_testing.generate_timing_records import (
    generate_records_for_master_timing_controller,
)
from phoebus_testing.pvi_wrapper import Pvi


def run_softioc():
    Pvi.configure_pvi("bobfiles/pvi", True)
    builder.SetDeviceName(PREFIX.removesuffix(":"))
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    generate_records_for_pvi_generated_screen()
    generate_records_for_manually_created_screen()
    generate_records_for_master_timing_controller()
    generate_shutter_screens()
    Pvi.create_pvi_records(PREFIX)

    builder.LoadDatabase()
    softioc.iocInit(dispatcher)
    softioc.interactive_ioc()


if __name__ == "__main__":
    run_softioc()
