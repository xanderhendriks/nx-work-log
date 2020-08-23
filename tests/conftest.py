import pytest
from nx_work_log.win_app import MinuteTimer


@pytest.fixture()
def minute_timer(minute_timer_callback):
    minute_timer = MinuteTimer(minute_timer_callback)

    yield minute_timer

    minute_timer.cancel()
