from phoebus_testing.generate_manual_records import (
    generate_records_for_manually_created_screen,
)
from phoebus_testing.generate_pvi_records import (
    generate_records_for_pvi_generated_screen,
)
from softioc import asyncio_dispatcher, builder, softioc

PREFIX = "PHOEBUS-TEST-PREFIX"
builder.SetDeviceName(PREFIX)


def run_softioc():
    generate_records_for_pvi_generated_screen()
    generate_records_for_manually_created_screen()
    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)

    softioc.interactive_ioc()


if __name__ == "__main__":
    run_softioc()
