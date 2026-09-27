"""
==================================================================================
وحدة اختبارات ضمان الجودة واختبارات الوحدات (Unit Testing & QA Suite)
Comprehensive Test Suite for Math, State Machine, Tracking & Fail-safes
==================================================================================
"""

import unittest
import math
import os
import json
import time

from core_math import (
    euclidean_dist_2d,
    calculate_ear,
    calculate_head_pose,
    continuous_leash_easing,
    solve_affine_transform,
    apply_affine_transform,
    ExponentialFilter,
    OneEuroFilter
)
from state_machine import SystemState, AppStateMachine
from tracking_engine import NosePointerAlgorithm, VisionTrackerEngine


class TestCoreMath(unittest.TestCase):
    """اختبارات الدوال الرياضية والحسابية الصرفة."""

    def test_euclidean_distance(self):
        p1 = (0.0, 0.0)
        p2 = (3.0, 4.0)
        self.assertAlmostEqual(euclidean_dist_2d(p1, p2), 5.0, places=5)

    def test_calculate_ear(self):
        # محاكاة عين مفتوحة بنقاط هندسية
        # Left eye: 33 (outer), 160, 158 (top), 133 (inner), 153, 144 (bottom)
        # Right eye: 263, 385, 387, 362, 373, 380
        dummy_landmarks = {
            # Left Eye
            33: (0.30, 0.40),
            160: (0.33, 0.38),
            158: (0.37, 0.38),
            133: (0.40, 0.40),
            153: (0.37, 0.42),
            144: (0.33, 0.42),
            # Right Eye
            263: (0.60, 0.40),
            385: (0.63, 0.38),
            387: (0.67, 0.38),
            362: (0.70, 0.40),
            373: (0.67, 0.42),
            380: (0.63, 0.42)
        }
        avg_ear, left_ear, right_ear = calculate_ear(dummy_landmarks, w=640, h=480)
        self.assertGreater(avg_ear, 0.18, "Open eye EAR should be above 0.18")
        self.assertAlmostEqual(left_ear, right_ear, places=2)

        # محاكاة عين مغلقة (تقارب الجفن العلوي والسفلي)
        dummy_closed = dict(dummy_landmarks)
        dummy_closed[160] = (0.33, 0.40)
        dummy_closed[158] = (0.37, 0.40)
        dummy_closed[153] = (0.37, 0.40)
        dummy_closed[144] = (0.33, 0.40)
        dummy_closed[385] = (0.63, 0.40)
        dummy_closed[387] = (0.67, 0.40)
        dummy_closed[373] = (0.67, 0.40)
        dummy_closed[380] = (0.63, 0.40)
        closed_ear, _, _ = calculate_ear(dummy_closed, w=640, h=480)
        self.assertLess(closed_ear, 0.10, "Closed eye EAR should be very small (< 0.10)")

    def test_calculate_head_pose(self):
        # وضعية أمامية مثالية
        nose = (0.50, 0.50)
        forehead = (0.50, 0.30)
        chin = (0.50, 0.70)
        left_t = (0.35, 0.50)
        right_t = (0.65, 0.50)

        is_front, yaw_deg, pitch_deg, y_rat, p_rat = calculate_head_pose(
            nose, forehead, chin, left_t, right_t
        )
        self.assertTrue(is_front)
        self.assertAlmostEqual(yaw_deg, 0.0, places=1)
        self.assertAlmostEqual(pitch_deg, 0.0, places=1)

        # التفات قوي إلى اليمين
        nose_turned = (0.72, 0.50)
        is_front_turn, yaw_turn, _, _, _ = calculate_head_pose(
            nose_turned, forehead, chin, left_t, right_t, max_yaw_tol=1.2
        )
        self.assertFalse(is_front_turn)
        self.assertGreater(abs(yaw_turn), 25.0)

    def test_continuous_leash_easing_strict_deadband(self):
        """اختبار القفل الصارم في المنطقة الميتة (Zero Jitter / Strict Deadband)."""
        smooth_x, smooth_y = 100.0, 100.0
        deadband = 2.0

        # حركة ميكروية بمسافة 1.0 بكسل (أقل من deadband 2.0px)
        new_x, new_y = continuous_leash_easing(
            target_x=100.8,
            target_y=100.6,
            smooth_x=smooth_x,
            smooth_y=smooth_y,
            deadband=deadband
        )
        # يجب أن تبقى الإحداثيات مجمدة تماماً بدون أي تغيير
        self.assertEqual(new_x, smooth_x, "Coordinates must remain strictly locked inside deadband")
        self.assertEqual(new_y, smooth_y, "Coordinates must remain strictly locked inside deadband")

    def test_continuous_leash_easing_continuous_movement(self):
        """اختبار التنعيم التدريجي المتصل عند تجاوز المنطقة الميتة."""
        smooth_x, smooth_y = 100.0, 100.0
        deadband = 1.8

        # حركة 10 بكسل (تتجاوز المنطقة الميتة)
        new_x, new_y = continuous_leash_easing(
            target_x=110.0,
            target_y=100.0,
            smooth_x=smooth_x,
            smooth_y=smooth_y,
            deadband=deadband
        )
        # يجب أن تتحرك الإحداثيات بنعومة مقاسة
        self.assertGreater(new_x, 100.0)
        self.assertLess(new_x, 110.0)
        self.assertEqual(new_y, 100.0)

    def test_solve_affine_transform(self):
        """اختبار حساب مصفوفة التحويل التآلفي Affine Transform."""
        # 9 نقاط في شبكة 3x3 متماثلة
        sources = [
            (0.2, 0.2), (0.5, 0.2), (0.8, 0.2),
            (0.2, 0.5), (0.5, 0.5), (0.8, 0.5),
            (0.2, 0.8), (0.5, 0.8), (0.8, 0.8)
        ]
        # أهداف مطابقة مع تحجيم وتكبير
        targets = [
            (0.1, 0.1), (0.5, 0.1), (0.9, 0.1),
            (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),
            (0.1, 0.9), (0.5, 0.9), (0.9, 0.9)
        ]

        sol_x, sol_y, is_valid, mean_err = solve_affine_transform(sources, targets)
        self.assertTrue(is_valid, "Affine matrix should be mathematically valid")
        self.assertIsNotNone(sol_x)
        self.assertIsNotNone(sol_y)
        self.assertLess(mean_err, 0.05, "Residual error should be near zero for linear grid")

        # تجربة التحويل على المركز (0.5, 0.5)
        tx, ty = apply_affine_transform(sol_x, sol_y, 0.5, 0.5)
        self.assertAlmostEqual(tx, 0.5, places=2)
        self.assertAlmostEqual(ty, 0.5, places=2)


class TestStateMachine(unittest.TestCase):
    """اختبارات آلة الحالات (Latching State Machine) وتجنب التداخل."""

    def setUp(self):
        self.sm = AppStateMachine()

    def test_initial_state(self):
        self.assertEqual(self.sm.current_state, SystemState.ACTIVE)
        self.assertTrue(self.sm.can_dwell())
        self.assertTrue(self.sm.can_move_cursor())

    def test_latching_pause_and_resume(self):
        t0 = 1000.0

        # أول إطار للقبضة: لا يجب أن يتوقف فوراً (يحتاج تأكيد زمني 0.35s)
        self.sm.process_hand_gesture("FIST", t0)
        self.assertEqual(self.sm.current_state, SystemState.ACTIVE)

        # بعد مرور 0.40 ثانية: يجب أن يتحول إلى PAUSED
        act = self.sm.process_hand_gesture("FIST", t0 + 0.40)
        self.assertEqual(act, "PAUSED_BY_FIST")
        self.assertEqual(self.sm.current_state, SystemState.PAUSED)
        self.assertFalse(self.sm.can_dwell())

        # استئناف عبر كف اليد
        t1 = 1005.0
        self.sm.process_hand_gesture("OPEN_PALM", t1)
        self.assertEqual(self.sm.current_state, SystemState.PAUSED)
        act_res = self.sm.process_hand_gesture("OPEN_PALM", t1 + 0.40)
        self.assertEqual(act_res, "RESUMED_BY_PALM")
        self.assertEqual(self.sm.current_state, SystemState.ACTIVE)

    def test_calibrating_ignores_all_gestures(self):
        """
        ⭐ اختبار القاعدة الهندسية الحاسمة:
        أثناء المعايرة (CALIBRATING)، يجب تجاهل إيماءات اليد تماماً لمنع التداخل.
        """
        self.sm.start_calibration()
        self.assertEqual(self.sm.current_state, SystemState.CALIBRATING)

        now = 2000.0
        # محاولة إيقاف بالقبضة
        self.sm.process_hand_gesture("FIST", now)
        self.sm.process_hand_gesture("FIST", now + 1.0)
        self.assertEqual(self.sm.current_state, SystemState.CALIBRATING, "FIST must be ignored in CALIBRATING")

        # محاولة قفل صف بالأصابع
        self.sm.process_hand_gesture("FINGER_2", now + 2.0)
        self.sm.process_hand_gesture("FINGER_2", now + 2.5)
        self.assertEqual(self.sm.current_state, SystemState.CALIBRATING, "Finger gesture must be ignored in CALIBRATING")
        self.assertIsNone(self.sm.active_locked_row)

        # إنهاء المعايرة
        self.sm.finish_calibration(success=True)
        self.assertEqual(self.sm.current_state, SystemState.ACTIVE)

    def test_safe_freeze_fail_safe(self):
        """اختبار التجميد الآمن عند فقدان إشارة الوجه."""
        self.sm.handle_tracking_loss("فقدان الوجه")
        self.assertEqual(self.sm.current_state, SystemState.SAFE_FREEZE)
        self.assertFalse(self.sm.can_dwell())

        # استعادة الرصد
        self.sm.handle_tracking_restored()
        self.assertEqual(self.sm.current_state, SystemState.ACTIVE)


class TestNosePointerAlgorithm(unittest.TestCase):
    """اختبارات خوارزمية التحكم بالمؤشر عبر الأنف."""

    def test_calibration_and_center_mapping(self):
        algo = NosePointerAlgorithm()
        algo.set_frame_size(640, 480)
        algo.calibrate(0.50, 0.50)

        # عندما يكون الأنف في المركز المحايد، يجب أن يكون المخرج (0.5, 0.5)
        nx, ny, _, _ = algo.process(0.50, 0.50, 640, 480)
        self.assertAlmostEqual(nx, 0.50, places=2)
        self.assertAlmostEqual(ny, 0.50, places=2)

    def test_screen_clamping(self):
        algo = NosePointerAlgorithm()
        algo.calibrate(0.50, 0.50)
        # حركة متطرفة جداً
        nx, ny, _, _ = algo.process(0.99, 0.99, 640, 480)
        self.assertLessEqual(nx, 0.985)
        self.assertLessEqual(ny, 0.980)


if __name__ == "__main__":
    unittest.main()
