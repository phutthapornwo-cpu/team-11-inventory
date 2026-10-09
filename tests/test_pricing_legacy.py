"""Characterization tests ของ pricing_legacy.calc

บันทึก "พฤติกรรมจริง" ของโค้ดเดิม (ได้ค่ามาจากการรันจริง) ไม่ใช่สิ่งที่ "ควรเป็น"
ถ้าค่าไหนดูแปลก ให้แก้ค่าใน test ห้ามแก้ฟังก์ชัน

ขั้นที่ 8: เมื่อได้ไฟล์ที่ refactor แล้ว ให้แก้เฉพาะบรรทัด import ด้านล่าง
(ไฟล์ใหม่ต้องมี calc, member_points, LOG ชื่อเดิม)
"""
import datetime

import pytest

import pricing_legacy as pricing  # <- ขั้นที่ 8 เปลี่ยนตรงนี้บรรทัดเดียว


@pytest.fixture(autouse=True)
def reset_state():
    """ล้างค่าที่ค้างข้ามการเรียก (global state) ก่อนและหลังทุก test"""
    pricing.member_points.clear()
    pricing.LOG.clear()
    yield
    pricing.member_points.clear()
    pricing.LOG.clear()


D = datetime.date


# ---------- 1. ราคาปกติ ----------
def test_normal_price_single_item():
    # 2 x 10 = 20, + VAT 7% = 21.4
    assert pricing.calc([("pen", 2, 10)]) == 21.4


def test_normal_price_multiple_items_are_summed():
    # (1x10) + (2x5) = 20 -> 21.4
    assert pricing.calc([("a", 1, 10), ("b", 2, 5)]) == 21.4


def test_normal_call_has_no_member_points_side_effect():
    pricing.calc([("pen", 2, 10)])
    assert pricing.member_points == {}


# ---------- 2. ซื้อจำนวนมาก (ค่าขอบทุกขั้น) ----------
@pytest.mark.parametrize(
    "qty, expected",
    [
        (49, 524.3),    # ยังไม่ลด: 490 * 1.07
        (50, 508.25),   # ลด 5% ที่ 50 พอดี: 500*0.95*1.07
        (99, 1006.34),  # ยังลด 5%
        (100, 963.0),   # ลด 10% ที่ 100 พอดี: 1000*0.9*1.07
    ],
)
def test_bulk_discount_thresholds(qty, expected):
    assert pricing.calc([("a", qty, 10)]) == expected


# ---------- 3. จำนวนเป็นศูนย์ / ติดลบ / ว่าง ----------
def test_zero_quantity_item_gives_zero():
    assert pricing.calc([("a", 0, 10)]) == 0.0


def test_negative_quantity_item_is_skipped():
    assert pricing.calc([("a", -3, 10)]) == 0.0


def test_empty_items_gives_zero():
    assert pricing.calc([]) == 0.0


def test_zero_quantity_item_is_skipped_among_valid_items():
    assert pricing.calc([("a", 0, 10), ("b", 2, 10)]) == 21.4


# ---------- 4. สมาชิก (ยอดเงิน + แต้ม) ----------
def test_member_gets_5_percent_discount_and_points():
    # 1000 -> 950 (สมาชิก) -> 1016.5 (VAT) | แต้ม = int(950/100) = 9
    assert pricing.calc([("a", 10, 100)], member="somchai") == 1016.5
    assert pricing.member_points == {"somchai": 9}


def test_member_points_zero_when_total_below_100():
    assert pricing.calc([("a", 1, 10)], member="somchai") == 10.16
    assert pricing.member_points == {"somchai": 0}


def test_member_points_truncate_not_round():
    # 199 -> 189.05 หลังลดสมาชิก; 189.05/100 = 1.89 แต่ได้แค่ 1 แต้ม (int ตัดทิ้ง)
    assert pricing.calc([("a", 1, 199)], member="x") == 202.28
    assert pricing.member_points == {"x": 1}


def test_member_points_accumulate_across_calls():
    pricing.calc([("a", 10, 100)], member="m")
    pricing.calc([("a", 10, 100)], member="m")
    assert pricing.member_points == {"m": 18}


def test_member_with_empty_items_is_registered_with_zero_points():
    assert pricing.calc([], member="z") == 0.0
    assert pricing.member_points == {"z": 0}


def test_empty_string_member_still_counts_as_member():
    # member="" ไม่ใช่ None จึงได้สิทธิ์สมาชิก
    assert pricing.calc([("a", 1, 10)], member="") == 10.16
    assert pricing.member_points == {"": 0}


def test_points_are_computed_before_coupon_is_applied():
    # แต้มคิดจาก 950 (ก่อนคูปอง HALF) ไม่ใช่ 475
    assert pricing.calc([("a", 10, 100)], member="m", coupon="HALF") == 508.25
    assert pricing.member_points == {"m": 9}


# ---------- 5. คูปอง ----------
def test_coupon_save50_subtracts_50_before_tax():
    # 200 - 50 = 150 -> 160.5
    assert pricing.calc([("a", 10, 20)], coupon="SAVE50") == 160.5


def test_coupon_half_halves_total():
    # 200 * 0.5 = 100 -> 107.0
    assert pricing.calc([("a", 10, 20)], coupon="HALF") == 107.0


def test_coupon_newyear_applies_in_january():
    # 200 * 0.8 = 160 -> 171.2
    assert pricing.calc([("a", 10, 20)], coupon="NEWYEAR", today=D(2026, 1, 15)) == 171.2


def test_coupon_newyear_applies_on_last_day_of_january():
    assert pricing.calc([("a", 10, 20)], coupon="NEWYEAR", today=D(2026, 1, 31)) == 171.2


@pytest.mark.parametrize("day", [D(2026, 2, 1), D(2025, 12, 31), D(2026, 7, 4)])
def test_coupon_newyear_ignored_outside_january(day):
    assert pricing.calc([("a", 10, 20)], coupon="NEWYEAR", today=day) == 214.0


def test_unknown_coupon_is_silently_ignored():
    assert pricing.calc([("a", 10, 20)], coupon="FOO") == 214.0


def test_coupon_code_is_case_sensitive():
    assert pricing.calc([("a", 10, 20)], coupon="save50") == 214.0


def test_today_is_ignored_for_non_newyear_coupons():
    assert pricing.calc([("a", 10, 20)], coupon="SAVE50", today=D(2026, 1, 1)) == 160.5


def test_member_and_coupon_stack_member_first_then_coupon():
    # 1000*0.9=900 -> *0.95=855 -> -50=805 -> *1.07 = 861.35
    assert pricing.calc([("a", 100, 10)], member="m", coupon="SAVE50") == 861.35
    assert pricing.member_points == {"m": 8}


def test_member_and_half_coupon_stack():
    assert pricing.calc([("a", 100, 10)], member="m", coupon="HALF") == 457.43


# ---------- 6. ยอดติดลบ ----------
def test_discount_larger_than_total_is_clamped_to_zero():
    # 20 - 50 < 0 -> 0 (ไม่คิดภาษีบนยอดติดลบ)
    assert pricing.calc([("a", 1, 20)], coupon="SAVE50") == 0.0


# ---------- 7. ค่าที่ฟังก์ชันเก็บไว้ (LOG) ----------
def test_log_records_member_and_final_total_for_each_call():
    pricing.calc([("a", 10, 100)], member="m")
    pricing.calc([("a", 1, 1)], member="n")
    pricing.calc([("a", 1, 1)])
    assert pricing.LOG == [("m", 1016.5), ("n", 1.02), (None, 1.07)]


def test_log_records_zero_total_calls_too():
    pricing.calc([])
    assert pricing.LOG == [(None, 0.0)]


# ---------- ปัดเศษ ----------
def test_result_is_rounded_to_two_decimals():
    # 3 x 3.33 = 9.99 -> * 1.07 = 10.6893 -> 10.69
    assert pricing.calc([("a", 3, 3.33)]) == 10.69


def test_tiny_price_rounds_to_cent():
    assert pricing.calc([("a", 1, 0.01)]) == 0.01
