import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np
from pvi.device import (
    LED,
    ArrayTrace,
    BitField,
    ImageRead,
    ProgressBar,
    TextRead,
    WidgetUnion,
)
from softioc import alarm

PREFIX = "PREFIX:"

# Have to use a signalR for a TextRead
SignalRWidgets = [
    TextRead,
    LED,
    BitField,
    ImageRead,
    ProgressBar,
    ArrayTrace,
]


# EPICS expects int for alarm severity (.SEVR)
class AlarmSeverities(Enum):
    NORMAL = 0
    MINOR = 1
    MAJOR = 2
    CRITICAL = 3
    DISCONNECTED = 4


ROW_LENGTH = len(AlarmSeverities)


EXAMPLE_IMAGE = np.fromfile(
    Path(__file__).parent / "test_image.raw", dtype=np.uint8
).flatten()

EXAMPLE_WAVEFORM = 100 * np.sin(np.linspace(0, 2 * np.pi, 100))


def name_to_pv(name: str):
    words = re.findall(r"[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+", name)
    return "-".join(map(str.lower, words)).upper()


@dataclass
class WidgetRecord:
    """
    Used for generating records along with widgets.
    """

    name: str
    widget: Optional[WidgetUnion]  # For Reads xor Writes
    widget_kwargs: Optional[Dict]
    record_creation_function: Callable
    record_creation_function_args: Tuple
    record_creation_function_kwargs: Dict
    widgets: Optional[Tuple[WidgetUnion, WidgetUnion]] = None  # For ReadWrites
    read_widget_kwargs: Optional[Dict] = None
    write_widget_kwargs: Optional[Dict] = None


@dataclass
class Record:
    pv_name: str
    record_creation_function: Callable
    record_creation_function_args: Tuple
    record_creation_function_kwargs: Dict
    severity: AlarmSeverities = AlarmSeverities.NORMAL


def cycle_severities(n: int, prefix: str = ""):
    """n widgets in a row"""

    gen = enumerate(
        int(n / len(AlarmSeverities)) * list(AlarmSeverities)
        + list(AlarmSeverities)[0 : n % len(AlarmSeverities)],
        start=1,
    )

    if prefix:
        prefix += "-"
    for i, severity in gen:
        yield f"{prefix}{i}", severity


def set_alarm(record: Any, severity: AlarmSeverities):
    record.set_alarm(severity.value, alarm.UDF_ALARM, timestamp=None)
