"""
==================================================================================
محرك الرؤية الحاسوبية وخوارزميات التتبع (Vision Tracker Engine & Algorithms)
Computer Vision Pipeline, Hand Gestures & Nose Pointer Algorithm
==================================================================================
مسؤول عن:
1. تهيئة نماذج MediaPipe (FaceLandmarker و HandLandmarker) ومعالجة الفشل الاحتياطي.
2. تنفيذ خوارزمية NosePointerAlgorithm (المنطقة الميتة الصارمة والتنعيم التدريجي المتصل).
3. استخراج المقاييس الحيوية (EAR, Head Pose, Distance) وإيماءات اليد.
4. إدارة ملف المعايرة (calibration.json) بالقيم الافتراضية الآمنة.
==================================================================================
"""

import os
import sys
import time
import json
import math
import urllib.request
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Dict, Any

import cv2
import numpy as np
import mediapipe as mp

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_CURRENT_DIR)

for _p in [_CURRENT_DIR, _PROJECT_ROOT]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from backend.core_math import (
        calculate_ear,
        calculate_head_pose,
        continuous_leash_easing,
        apply_affine_transform,
        euclidean_dist_2d
    )
except ImportError:
    from core_math import (
        calculate_ear,
        calculate_head_pose,
        continuous_leash_easing,
        apply_affine_transform,
        euclidean_dist_2d
    )

FACE_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
HAND_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

def _resolve_resource_path(filename: str, subfolder: str = "") -> str:
    """البحث المرن عن مسارات النماذج وملفات الإعدادات عبر مجلدات المشروع."""
    candidates = [
        os.path.join(_PROJECT_ROOT, subfolder, filename) if subfolder else "",
        os.path.join(_PROJECT_ROOT, filename),
        os.path.join(_CURRENT_DIR, subfolder, filename) if subfolder else "",
        os.path.join(_CURRENT_DIR, filename),
        os.path.join(os.getcwd(), subfolder, filename) if subfolder else "",
        os.path.join(os.getcwd(), filename),
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return os.path.abspath(p)
    # مسار افتراضي مستهدف
    target = os.path.join(_PROJECT_ROOT, subfolder, filename) if subfolder else os.path.join(_PROJECT_ROOT, filename)
    return os.path.abspath(target)

FACE_MODEL_FILENAME = _resolve_resource_path("face_landmarker.task", "models")
HAND_MODEL_FILENAME = _resolve_resource_path("hand_landmarker.task", "models")
CALIBRATION_FILE = _resolve_resource_path("calibration.json", "config")


@dataclass
class TrackingResult:
    """بنية بيانات متكاملة وآمنة لنقل نتائج التتبع بين الخيوط (Thread-Safe DTO)."""
    face_found: bool = False
    hand_found: bool = False
    is_frontal: bool = True
    eyes_open: bool = True
    avg_ear: float = 0.30
    yaw_deg: float = 0.0
    pitch_deg: float = 0.0
    yaw_ratio: float = 0.0
    pitch_ratio: float = 0.0
    distance_cm: float = 60.0
    distance_factor: float = 1.0

    # إحداثيات الشاشة المعالجة النهائية [0.0 - 1.0]
    norm_x: float = 0.5
    norm_y: float = 0.5

    # إحداثيات الكاميرا المنعمة والخام [0.0 - 1.0]
    nose_norm_x: float = 0.5
    nose_norm_y: float = 0.5
    smooth_norm_x: float = 0.5
    smooth_norm_y: float = 0.5
    raw_x: float = 0.5
    raw_y: float = 0.5

    # إيماءات اليد
    gesture_name: str = "NONE"
    fingers_count: int = 0
    finger_states: List[bool] = field(default_factory=lambda: [False] * 5)

    # أبعاد الإطار
    frame_w: int = 640
    frame_h: int = 480


class NosePointerAlgorithm:
    """
    خوارزمية التحكم بالمؤشر عبر الأنف:
    - المنطقة الميتة الصارمة (Strict Deadband / Laser Lock): ثبات مطلق فوق المفاتيح ومنع الارتعاش الفسيولوجي.
    - التنعيم التدريجي المتصل (Continuous Leash Easing): انسيابية تكيفية تجمع بين الدقة الفائقة والسرعة بدون بطء أو مطاطية.
    - معايرة مركزية ذكية (Center Auto/Manual Calibration).
    """
    def __init__(self):
        # مركز الأنف المحايد
        self.calibrated_norm_x: Optional[float] = None
        self.calibrated_norm_y: Optional[float] = None

        # حالة الإحداثيات المنعمة (بالبكسل)
        self.smooth_px_x: Optional[float] = None
        self.smooth_px_y: Optional[float] = None

        # المعاملات الفيزيائية
        self.head_sensitivity_x: float = 1.0
        self.head_sensitivity_y: float = 1.0
        self.head_deadband: float = 1.8           # بكسل لمنطقة القفل الصارم
        self.leash_outer: float = 8.0             # مدى الحركة السريعة

        # المدى الحركي المريح لمستخدمي الكيبورد (بكسل كاميرا 640x480)
        self.base_head_range_x: float = 48.0
        self.base_head_range_y: float = 34.0

        # أبعاد الإطار
        self._last_frame_w: int = 640
        self._last_frame_h: int = 480
        self._init_frames_count: int = 0

    def set_frame_size(self, w: int, h: int) -> None:
        self._last_frame_w = max(100, int(w))
        self._last_frame_h = max(100, int(h))

    def calibrate(self, nose_norm_x: float, nose_norm_y: float, frame_w: Optional[int] = None, frame_h: Optional[int] = None) -> None:
        """ضبط مركز الأنف الحالي كنقطة الصفر في منتصف الشاشة (0.5, 0.5)."""
        self.calibrated_norm_x = float(nose_norm_x)
        self.calibrated_norm_y = float(nose_norm_y)

        fw = frame_w or self._last_frame_w
        fh = frame_h or self._last_frame_h
        self.smooth_px_x = self.calibrated_norm_x * fw
        self.smooth_px_y = self.calibrated_norm_y * fh

    def reset_smoothing(self) -> None:
        """إعادة ضبط حالة التنعيم لتفادي القفزات المفاجئة عند تغيير الإعدادات."""
        if self.calibrated_norm_x is not None:
            self.smooth_px_x = self.calibrated_norm_x * self._last_frame_w
            self.smooth_px_y = self.calibrated_norm_y * self._last_frame_h
        else:
            self.smooth_px_x = None
            self.smooth_px_y = None

    def process(
        self,
        nose_norm_x: float,
        nose_norm_y: float,
        frame_w: int,
        frame_h: int,
        affine_x: Optional[List[float]] = None,
        affine_y: Optional[List[float]] = None
    ) -> Tuple[float, float, float, float]:
        """
        معالجة حركة الأنف وتحويلها إلى إحداثيات الشاشة:
        1. تطبيق التنعيم التدريجي والمنطقة الميتة الصارمة.
        2. التحويل الهندسي (عبر Affine Transform المعتمدة أو Linear Range).
        
        المخرجات:
            (screen_norm_x, screen_norm_y, smooth_norm_x, smooth_norm_y)
        """
        self.set_frame_size(frame_w, frame_h)

        # معايرة تلقائية في الإطارات الأولى عند بدء التشغيل
        if self.calibrated_norm_x is None or self.calibrated_norm_y is None:
            self._init_frames_count += 1
            if self._init_frames_count >= 2:
                self.calibrate(nose_norm_x, nose_norm_y, frame_w, frame_h)

        # تحويل الأنف إلى بكسل الكاميرا
        nose_px_x = float(nose_norm_x) * frame_w
        nose_px_y = float(nose_norm_y) * frame_h

        # تطبيق المنطقة الميتة الصارمة والتنعيم التدريجي
        new_sx, new_sy = continuous_leash_easing(
            target_x=nose_px_x,
            target_y=nose_px_y,
            smooth_x=self.smooth_px_x,
            smooth_y=self.smooth_px_y,
            deadband=self.head_deadband,
            leash_outer=self.leash_outer
        )
        self.smooth_px_x = new_sx
        self.smooth_px_y = new_sy

        # إحداثيات الأنف المنعمة نسبياً
        smooth_norm_x = self.smooth_px_x / frame_w
        smooth_norm_y = self.smooth_px_y / frame_h

        # حساب الموضع النهائي للشاشة
        use_affine = False
        if affine_x is not None and affine_y is not None:
            test_nx, test_ny = apply_affine_transform(affine_x, affine_y, smooth_norm_x, smooth_norm_y)
            if 0.0 <= test_nx <= 1.0 and 0.0 <= test_ny <= 1.0:
                norm_x = test_nx
                norm_y = test_ny
                use_affine = True

        if not use_affine:
            if self.calibrated_norm_x is None or self.calibrated_norm_y is None:
                norm_x, norm_y = 0.5, 0.5
            else:
                head_range_x = self.base_head_range_x / max(0.2, self.head_sensitivity_x)
                head_range_y = self.base_head_range_y / max(0.2, self.head_sensitivity_y)

                # إزاحة بكسل الأنف عن المركز المحايد
                delta_px_x = self.smooth_px_x - (self.calibrated_norm_x * frame_w)
                delta_px_y = self.smooth_px_y - (self.calibrated_norm_y * frame_h)

                norm_x = 0.5 + (delta_px_x / (2.0 * head_range_x))
                norm_y = 0.5 + (delta_px_y / (2.0 * head_range_y))

        # تقييد آمن داخل حدود الكيبورد
        norm_x = float(np.clip(norm_x, 0.015, 0.985))
        norm_y = float(np.clip(norm_y, 0.02, 0.98))

        return norm_x, norm_y, smooth_norm_x, smooth_norm_y


class VisionTrackerEngine:
    """
    محرك الرؤية الحاسوبية المعياري:
    - مسؤول عن استخراج النقاط من MediaPipe.
    - حساب مقاييس السلامة (EAR, Head Pose).
    - تصنيف إيماءات اليد بدقة واستقرار.
    - حفظ وتحميل المعايرة مع الحماية من الملفات المفقودة أو التالفة.
    """
    def __init__(
        self,
        face_model_path: str = FACE_MODEL_FILENAME,
        hand_model_path: str = HAND_MODEL_FILENAME,
        calibration_path: str = CALIBRATION_FILE
    ):
        self.face_model_path = face_model_path
        self.hand_model_path = hand_model_path
        self.calibration_path = calibration_path

        self.face_detector = None
        self.hand_detector = None
        self.legacy_face_mesh = None

        # خوارزمية التحكم بالمؤشر
        self.nose_algo = NosePointerAlgorithm()

        # إعدادات السلامة
        self.max_yaw_tolerance = 1.70
        self.max_pitch_tolerance = 1.70
        self.ear_threshold = 0.16

        # المعايرة الهندسية التآلفية 9 نقاط
        self.is_calibrated = False
        self.affine_x: Optional[List[float]] = None
        self.affine_y: Optional[List[float]] = None
        self.reference_distance_cm = 60.0

        self._init_models()
        self.load_calibration()

    def _init_models(self) -> None:
        """تهيئة نماذج MediaPipe مع التنزيل التلقائي والفشل الاحتياطي."""
        # 1. Face Landmarker
        try:
            if hasattr(mp, 'tasks') and hasattr(mp.tasks, 'vision'):
                if not os.path.exists(self.face_model_path):
                    print(f"[Info] Downloading Face Landmarker from {FACE_MODEL_URL}...")
                    urllib.request.urlretrieve(FACE_MODEL_URL, self.face_model_path)
                    print("[OK] Face model downloaded.")

                from mediapipe.tasks import python
                from mediapipe.tasks.python import vision

                face_options = vision.FaceLandmarkerOptions(
                    base_options=python.BaseOptions(model_asset_path=self.face_model_path),
                    output_face_blendshapes=False,
                    output_facial_transformation_matrixes=False,
                    num_faces=1
                )
                self.face_detector = vision.FaceLandmarker.create_from_options(face_options)
                print("[OK] Face Landmarker initialized successfully.")
        except Exception as e:
            print(f"[Warning] Face Landmarker initialization failed: {e}")

        # 2. Hand Landmarker
        try:
            if hasattr(mp, 'tasks') and hasattr(mp.tasks, 'vision'):
                if not os.path.exists(self.hand_model_path):
                    print(f"[Info] Downloading Hand Landmarker from {HAND_MODEL_URL}...")
                    urllib.request.urlretrieve(HAND_MODEL_URL, self.hand_model_path)
                    print("[OK] Hand model downloaded.")

                from mediapipe.tasks import python
                from mediapipe.tasks.python import vision

                hand_options = vision.HandLandmarkerOptions(
                    base_options=python.BaseOptions(model_asset_path=self.hand_model_path),
                    num_hands=1,
                    min_hand_detection_confidence=0.55,
                    min_hand_presence_confidence=0.55,
                    min_tracking_confidence=0.55
                )
                self.hand_detector = vision.HandLandmarker.create_from_options(hand_options)
                print("[OK] Hand Landmarker initialized successfully.")
        except Exception as e:
            print(f"[Warning] Hand Landmarker initialization failed: {e}")

        # 3. Fallback للحلول السابقة إذا فشلت المهام الحديثة
        if self.face_detector is None and hasattr(mp, 'solutions'):
            try:
                self.legacy_face_mesh = mp.solutions.face_mesh.FaceMesh(
                    max_num_faces=1, refine_landmarks=True,
                    min_detection_confidence=0.5, min_tracking_confidence=0.5
                )
                print("[OK] Legacy FaceMesh fallback initialized.")
            except Exception as e:
                print(f"[Warning] Legacy FaceMesh fallback failed: {e}")

    def load_calibration(self, filepath: Optional[str] = None) -> None:
        """تحميل المعايرة مع الحماية من الأخطاء والتهيئة الافتراضية الآمنة."""
        path = filepath or self.calibration_path
        if not os.path.exists(path):
            self.reset_calibration(save=False)
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.is_calibrated = bool(data.get("calibrated", False))
            self.reference_distance_cm = float(data.get("reference_distance_cm", 60.0))

            cx = data.get("algo_center_x")
            cy = data.get("algo_center_y")
            if self.is_calibrated and cx is not None and cy is not None:
                cx_f = float(cx)
                cy_f = float(cy)
                if 0.15 <= cx_f <= 0.85 and 0.15 <= cy_f <= 0.85:
                    self.nose_algo.calibrated_norm_x = cx_f
                    self.nose_algo.calibrated_norm_y = cy_f
                else:
                    self.nose_algo.calibrated_norm_x = None
                    self.nose_algo.calibrated_norm_y = None
            else:
                self.nose_algo.calibrated_norm_x = None
                self.nose_algo.calibrated_norm_y = None

            sx = data.get("algo_sens_x", 1.0)
            sy = data.get("algo_sens_y", 1.0)
            db = data.get("algo_deadband", 1.8)
            self.nose_algo.head_sensitivity_x = float(np.clip(sx, 0.3, 3.0)) if sx else 1.0
            self.nose_algo.head_sensitivity_y = float(np.clip(sy, 0.3, 3.0)) if sy else 1.0
            self.nose_algo.head_deadband = float(np.clip(db, 0.5, 10.0)) if db else 1.8

            if self.is_calibrated and data.get("affine_transform_x") and data.get("affine_transform_y"):
                self.affine_x = [float(v) for v in data["affine_transform_x"]]
                self.affine_y = [float(v) for v in data["affine_transform_y"]]
            else:
                self.affine_x = None
                self.affine_y = None

            self.nose_algo.reset_smoothing()
            print(f"[OK] Calibration loaded successfully from {path}.")
        except Exception as e:
            print(f"[Warning] Failed to load calibration ({e}) -> Initializing safe defaults.")
            self.reset_calibration(save=False)

    def save_calibration(self, filepath: Optional[str] = None) -> bool:
        """حفظ إعدادات المعايرة الحالية."""
        path = filepath or self.calibration_path
        data = {
            "version": "5.0-Enterprise",
            "calibrated": self.is_calibrated,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "reference_distance_cm": self.reference_distance_cm,
            "algo_center_x": self.nose_algo.calibrated_norm_x,
            "algo_center_y": self.nose_algo.calibrated_norm_y,
            "algo_sens_x": round(self.nose_algo.head_sensitivity_x, 3),
            "algo_sens_y": round(self.nose_algo.head_sensitivity_y, 3),
            "algo_deadband": round(self.nose_algo.head_deadband, 2),
            "affine_transform_x": [round(float(v), 5) for v in self.affine_x] if self.affine_x else None,
            "affine_transform_y": [round(float(v), 5) for v in self.affine_y] if self.affine_y else None,
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[OK] Calibration saved to {path}.")
            return True
        except Exception as e:
            print(f"[Warning] Failed to save calibration: {e}")
            return False

    def reset_calibration(self, save: bool = True) -> None:
        """استعادة الإعدادات الافتراضية بالكامل."""
        self.nose_algo.calibrated_norm_x = None
        self.nose_algo.calibrated_norm_y = None
        self.nose_algo.head_sensitivity_x = 1.0
        self.nose_algo.head_sensitivity_y = 1.0
        self.nose_algo.head_deadband = 1.8
        self.nose_algo.reset_smoothing()
        self.affine_x = None
        self.affine_y = None
        self.is_calibrated = False
        if save:
            self.save_calibration()

    def estimate_distance(self, landmarks: Any, w: float, h: float) -> Tuple[float, float]:
        """تقدير مسافة المستخدم عن الشاشة بالسنتيمتر."""
        try:
            p_left = landmarks[234]
            p_right = landmarks[454]
            face_w_px = abs(p_right.x - p_left.x) * w
            if face_w_px < 10:
                return 60.0, 1.0
            distance_cm = (170.0 * 60.0) / max(20.0, face_w_px)
            distance_cm = float(np.clip(distance_cm, 25.0, 140.0))
            factor = float(np.clip(self.reference_distance_cm / max(25.0, distance_cm), 0.75, 1.35))
            return round(distance_cm, 1), round(factor, 3)
        except Exception:
            return 60.0, 1.0

    def detect_hand_gesture(self, landmarks: Any) -> Tuple[str, int, List[bool]]:
        """
        تصنيف إيماءات اليد المعيارية:
        - FIST: قبضة اليد (إيقاف مؤقت).
        - OPEN_PALM: الكف المفتوح (استئناف/إلغاء قفل).
        - FINGER_1 .. FINGER_4: قفل الصفوف المقابلة.
        """
        try:
            # حالة الأصابع الأربعة العلوية
            idx_up = bool(landmarks[8].y < landmarks[6].y - 0.015)
            mid_up = bool(landmarks[12].y < landmarks[10].y - 0.015)
            rng_up = bool(landmarks[16].y < landmarks[14].y - 0.015)
            pnk_up = bool(landmarks[20].y < landmarks[18].y - 0.015)

            # حالة الإبهام
            wrist = landmarks[0]
            thumb_tip = landmarks[4]
            pinky_mcp = landmarks[17]
            d_tp = math.hypot(thumb_tip.x - pinky_mcp.x, thumb_tip.y - pinky_mcp.y)
            d_tw = math.hypot(thumb_tip.x - wrist.x, thumb_tip.y - wrist.y)
            thumb_open = bool(d_tp > 0.16 and d_tw > 0.16)

            count_main = sum([idx_up, mid_up, rng_up, pnk_up])
            finger_states = [thumb_open, idx_up, mid_up, rng_up, pnk_up]

            # فحص القبضة
            all_folded = (
                landmarks[8].y > landmarks[6].y and
                landmarks[12].y > landmarks[10].y and
                landmarks[16].y > landmarks[14].y and
                landmarks[20].y > landmarks[18].y
            )
            if all_folded and not thumb_open:
                return "FIST", 0, [False, False, False, False, False]

            # فحص الكف المفتوح
            if count_main == 4 and thumb_open:
                return "OPEN_PALM", 5, [True, True, True, True, True]

            # فحص عدد الأصابع لقفل الصفوف
            if count_main == 1 and idx_up:
                return "FINGER_1", 1, finger_states
            elif count_main == 2 and idx_up and mid_up:
                return "FINGER_2", 2, finger_states
            elif count_main == 3 and idx_up and mid_up and rng_up:
                return "FINGER_3", 3, finger_states
            elif count_main == 4:
                return "FINGER_4", 4, finger_states

            return "OTHER", count_main + (1 if thumb_open else 0), finger_states
        except Exception:
            return "NONE", 0, [False, False, False, False, False]

    def process_frame(self, frame: np.ndarray, debug: bool = False) -> TrackingResult:
        """
        المعالجة الكثيفة للإطار (تُنفذ داخل الخيط المستقل Background Thread):
        - رصد الوجه واستخراج إحداثيات الأنف والعينين ووضعية الرأس.
        - رصد اليد واستخراج الإيماءات.
        - تطبيق خوارزمية التحكم بالمؤشر NosePointerAlgorithm.
        - رسم التغذية البصرية على الإطار المباشر.
        """
        h, w = frame.shape[:2]
        res = TrackingResult(frame_w=w, frame_h=h)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        face_landmarks = None
        hand_landmarks = None

        # 1. كشف الوجه
        if self.face_detector:
            try:
                face_out = self.face_detector.detect(mp_img)
                if face_out.face_landmarks and len(face_out.face_landmarks) > 0:
                    face_landmarks = face_out.face_landmarks[0]
                    res.face_found = True
            except Exception:
                res.face_found = False
        elif self.legacy_face_mesh:
            try:
                out = self.legacy_face_mesh.process(rgb_frame)
                if out.multi_face_landmarks and len(out.multi_face_landmarks) > 0:
                    face_landmarks = out.multi_face_landmarks[0].landmark
                    res.face_found = True
            except Exception:
                res.face_found = False

        # 2. كشف اليد
        if self.hand_detector:
            try:
                hand_out = self.hand_detector.detect(mp_img)
                if hand_out.hand_landmarks and len(hand_out.hand_landmarks) > 0:
                    hand_landmarks = hand_out.hand_landmarks[0]
                    res.hand_found = True
                    g_name, f_cnt, f_states = self.detect_hand_gesture(hand_landmarks)
                    res.gesture_name = g_name
                    res.fingers_count = f_cnt
                    res.finger_states = f_states
            except Exception:
                res.hand_found = False

        # 3. معالجة بيانات الوجه والأنف
        if res.face_found and face_landmarks is not None:
            # حساب نسبة انفتاح العين EAR
            avg_ear, _, _ = calculate_ear(face_landmarks, float(w), float(h))
            res.avg_ear = avg_ear
            res.eyes_open = bool(avg_ear >= self.ear_threshold)

            # تقدير المسافة
            res.distance_cm, res.distance_factor = self.estimate_distance(face_landmarks, float(w), float(h))

            # حساب Head Pose
            nose = face_landmarks[1]
            forehead = face_landmarks[10]
            chin = face_landmarks[152]
            left_t = face_landmarks[234]
            right_t = face_landmarks[454]

            is_front, y_deg, p_deg, y_rat, p_rat = calculate_head_pose(
                (nose.x, nose.y),
                (forehead.x, forehead.y),
                (chin.x, chin.y),
                (left_t.x, left_t.y),
                (right_t.x, right_t.y),
                self.max_yaw_tolerance,
                self.max_pitch_tolerance
            )
            res.is_frontal = is_front
            res.yaw_deg = y_deg
            res.pitch_deg = p_deg
            res.yaw_ratio = y_rat
            res.pitch_ratio = p_rat

            # خوارزمية التحكم بالمؤشر عبر الأنف
            res.nose_norm_x = float(nose.x)
            res.nose_norm_y = float(nose.y)
            res.raw_x = res.nose_norm_x
            res.raw_y = res.nose_norm_y

            affine_x = self.affine_x if (self.is_calibrated and self.affine_x) else None
            affine_y = self.affine_y if (self.is_calibrated and self.affine_y) else None

            scr_x, scr_y, sm_nx, sm_ny = self.nose_algo.process(
                res.nose_norm_x, res.nose_norm_y, w, h, affine_x, affine_y
            )
            res.norm_x = scr_x
            res.norm_y = scr_y
            res.smooth_norm_x = sm_nx
            res.smooth_norm_y = sm_ny

            # الرسم التوضيحي على الإطار
            nose_px = (int(nose.x * w), int(nose.y * h))
            cv2.circle(frame, nose_px, 8, (0, 0, 255), 2)
            cv2.circle(frame, nose_px, 3, (0, 0, 255), -1)

            if self.nose_algo.smooth_px_x is not None:
                sm_px = (int(self.nose_algo.smooth_px_x), int(self.nose_algo.smooth_px_y))
                cv2.circle(frame, sm_px, 5, (0, 255, 120), -1)
                cv2.line(frame, nose_px, sm_px, (0, 255, 255), 1)

            # إطار السلامة
            border_color = (0, 255, 120) if (res.is_frontal and res.eyes_open) else (0, 165, 255)
            cv2.rectangle(frame, (4, 4), (w - 4, h - 4), border_color, 2)

            if debug:
                cv2.putText(frame, f"EAR: {avg_ear:.2f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                cv2.putText(frame, f"Yaw: {y_deg:.1f}deg", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                cv2.putText(frame, f"Pitch: {p_deg:.1f}deg", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                cv2.putText(frame, f"Dist: {res.distance_cm:.0f}cm", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        # رسم هيكل اليد
        if res.hand_found and hand_landmarks is not None:
            connections = [
                (0,1), (1,2), (2,3), (3,4),
                (0,5), (5,6), (6,7), (7,8),
                (0,9), (9,10), (10,11), (11,12),
                (0,13), (13,14), (14,15), (15,16),
                (0,17), (17,18), (18,19), (19,20),
                (5,9), (9,13), (13,17)
            ]
            for p1_i, p2_i in connections:
                p1 = hand_landmarks[p1_i]
                p2 = hand_landmarks[p2_i]
                cv2.line(frame, (int(p1.x * w), int(p1.y * h)), (int(p2.x * w), int(p2.y * h)), (255, 180, 0), 2)

            for lm in hand_landmarks:
                cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 3, (0, 255, 120), -1)

            wrist = hand_landmarks[0]
            wx, wy = int(wrist.x * w), max(20, int(wrist.y * h) - 15)
            cv2.putText(frame, f"Hand: {res.gesture_name}", (wx - 30, wy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        return res

    def close(self) -> None:
        try:
            if self.face_detector and hasattr(self.face_detector, 'close'):
                self.face_detector.close()
        except Exception:
            pass
        try:
            if self.hand_detector and hasattr(self.hand_detector, 'close'):
                self.hand_detector.close()
        except Exception:
            pass
