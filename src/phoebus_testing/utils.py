import numpy as np
from softioc import alarm

ALARM_SEVERITIES = list(range(4))

EXAMPLE_IMAGE = np.reshape(np.arange(0, 737280, 1, np.uint8), (1024, 720))
EXAMPLE_WAVEFORM = np.sin(np.linspace(0, 2 * np.pi, 100))


def cycle_severities(n, prefix=""):
    """n widgets in a row"""
    gen = enumerate(
        int(n / 4) * ALARM_SEVERITIES + ALARM_SEVERITIES[0 : n % 4], start=1
    )

    if not prefix:
        return gen
    for i, severity in gen:
        yield f"{prefix}-{i}", severity


def set_alarm(record, severity):
    record.set_alarm(severity, alarm.UDF_ALARM, timestamp=None)
