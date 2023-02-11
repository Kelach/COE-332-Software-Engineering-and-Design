from analyze_water import calc_turbidity, avg_turbidity, turbidity_waitime
import pytest

def test_calc_turbidity():
    calib_key = "cal"
    detect_cur_key = "dc"
    data = [
        {
            "cal": 1,
            "dc": 2
        },
        {
            "cal": 2,
            "dc": 3
        },
        {
            "cal": 3,
            "dc": 4
        }
    ]
    assert calc_turbidity(data[0][calib_key], data[0][detect_cur_key]) == 2
    assert calc_turbidity(data[1][calib_key], data[1][detect_cur_key]) == 6
    assert calc_turbidity(data[2][calib_key], data[2][detect_cur_key]) == 12

def test_avg_turbidity():
    calib_key = "cal"
    detect_cur_key = "dc"
    data = [
        {
            "cal": 1,
            "dc": 2
        },
        {
            "cal": 2,
            "dc": 3
        },
        {
            "cal": 3,
            "dc": 4
        }
    ]
    assert avg_turbidity(data, calib_key, detect_cur_key) == 20/3


def test_turbidity_waitime():
    avg_turb = 1.1992
    assert turbidity_waitime(avg_turb, 1.0, 0.02) == pytest.approx(8.99, abs=1e-2 )
