from typing import Any

import numpy as np
from softioc import alarm

ALARM_SEVERITIES_NAMES = ["NORMAL", "MINOR", "MAJOR", "CRITICAL", "DISCONNECTED"]
ALARM_SEVERITIES = list(range(len(ALARM_SEVERITIES_NAMES)))


EXAMPLE_IMAGE = np.arange(0, 737280, 1, np.uint8)  # 1080 * 720 flattened
EXAMPLE_WAVEFORM = np.sin(np.linspace(0, 2 * np.pi, 100))


def cycle_severities(n: int, prefix: str = ""):
    """n widgets in a row"""
    gen = enumerate(
        int(n / len(ALARM_SEVERITIES)) * ALARM_SEVERITIES
        + ALARM_SEVERITIES[0 : n % len(ALARM_SEVERITIES)],
        start=1,
    )

    if not prefix:
        return gen
    for i, severity in gen:
        yield f"{prefix}-{i}", severity


def set_alarm(record: Any, severity: int):
    record.set_alarm(severity, alarm.UDF_ALARM, timestamp=None)
