import pytest
import time

timer_time = time.time()


def minute_timer_callback():
    global timer_time
    timer_time = time.time()


@pytest.mark.parametrize('minute_timer_callback', [minute_timer_callback])
def test_timer(minute_timer):
    check_time = timer_time
    counter = 0

    while counter < 2:
        if check_time != timer_time:
            assert (timer_time - check_time) == pytest.approx(60.0, 0.01), 'Incorrect timer callback timing'
            check_time = timer_time
            counter += 1
