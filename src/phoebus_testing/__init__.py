from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, Tuple

import numpy as np
from pvi.device import WidgetType
from softioc import alarm

PREFIX = "PREFIX"


# EPICS expects int for alarm severity (.SEVR)
class AlarmSeverities(Enum):
    NORMAL = 0
    MINOR = 1
    MAJOR = 2
    CRITICAL = 3
    DISCONNECTED = 4


ROW_LENGTH = len(AlarmSeverities)

EXAMPLE_IMAGE = np.arange(0, 737280, 1, np.uint8)  # 1080 * 720 flattened
EXAMPLE_WAVEFORM = np.sin(np.linspace(0, 2 * np.pi, 100))


@dataclass
class WidgetRecord:
    """
    Used for generating records along with widgets.
    """

    name: str
    widget: WidgetType
    widget_kwargs: Dict
    record_creation_function: Callable
    record_creation_function_args: Tuple
    record_creation_function_kwargs: Dict


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
