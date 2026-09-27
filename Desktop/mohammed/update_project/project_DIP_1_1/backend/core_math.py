"""
==================================================================================
وحدة العمليات الحسابية والهندسية الصرفة (Pure Math & Geometric Transforms)
Core Mathematics, Transforms, and Ergonomic Metrics for Nose Virtual Keyboard
==================================================================================
تصميم معياري مستقل تماماً عن مكتبات واجهة المستخدم (Tkinter) أو كاميرا الفيديو.
جميع الدوال هنا دوال نقية (Pure Functions) قابلة للاختبار المباشر (Unit-Testable).
==================================================================================
"""

import math
from typing import List, Tuple, Optional, Dict, Any
import numpy as np


def euclidean_dist_2d(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """حساب المسافة الإقليدية الثنائية بين نقطتين."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def calculate_ear(landmarks_dict_or_list: Any, w: float = 640.0, h: float = 480.0) -> Tuple[float, float, float]:
    """
    حساب نسبة انفتاح العين (Eye Aspect Ratio - EAR) للعينين اليمنى واليسرى.
    
    المعادلة:
        EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
    
    النقاط القياسية وفق MediaPipe Mesh:
        العين اليسرى: 33 (الزاوية الخارجية), 160, 158 (الجفن العلوي), 133 (الزاوية الداخلية), 153, 144 (الجفن السفلي)
        العين اليمنى: 263 (الزاوية الخارجية), 385, 387 (الجفن العلوي), 362 (الزاوية الداخلية), 373, 380 (الجفن السفلي)
        
    المخرجات:
        (avg_ear, left_ear, right_ear)
    """
    try:
        def get_pt(idx: int) -> Tuple[float, float]:
            if isinstance(landmarks_dict_or_list, (list, tuple)):
                p = landmarks_dict_or_list[idx]
                if hasattr(p, 'x') and hasattr(p, 'y'):
                    return p.x * w, p.y * h
                elif isinstance(p, (list, tuple)):
                    return p[0] * w, p[1] * h
            elif isinstance(landmarks_dict_or_list, dict):
                p = landmarks_dict_or_list[idx]
                return p[0] * w, p[1] * h
            raise ValueError("Unsupported landmarks format")

        # العين اليسرى
        l_p1 = get_pt(33)
        l_p2 = get_pt(160)
        l_p3 = get_pt(158)
        l_p4 = get_pt(133)
        l_p5 = get_pt(153)
        l_p6 = get_pt(144)

        l_v1 = euclidean_dist_2d(l_p2, l_p6)
        l_v2 = euclidean_dist_2d(l_p3, l_p5)
        l_h = euclidean_dist_2d(l_p1, l_p4)
        left_ear = (l_v1 + l_v2) / (2.0 * max(1e-4, l_h))

        # العين اليمنى
        r_p1 = get_pt(263)
        r_p2 = get_pt(385)
        r_p3 = get_pt(387)
        r_p4 = get_pt(362)
        r_p5 = get_pt(373)
        r_p6 = get_pt(380)

        r_v1 = euclidean_dist_2d(r_p2, r_p6)
        r_v2 = euclidean_dist_2d(r_p3, r_p5)
        r_h = euclidean_dist_2d(r_p1, r_p4)
        right_ear = (r_v1 + r_v2) / (2.0 * max(1e-4, r_h))

        avg_ear = (left_ear + right_ear) / 2.0
        return float(avg_ear), float(left_ear), float(right_ear)
    except Exception:
        return 0.30, 0.30, 0.30


def calculate_head_pose(
    nose_pt: Tuple[float, float],
    forehead_pt: Tuple[float, float],
    chin_pt: Tuple[float, float],
    left_temple_pt: Tuple[float, float],
    right_temple_pt: Tuple[float, float],
    max_yaw_tol: float = 1.6,
    max_pitch_tol: float = 1.6
) -> Tuple[bool, float, float, float, float]:
    """
    تقدير وضعية الرأس وزوايا التوجيه (Head Pose / Yaw & Pitch) للأمان والصحة الرقمية.
    
    المدخلات إحداثيات نسبية [0.0, 1.0].
    
    المخرجات:
        (is_frontal, yaw_deg, pitch_deg, yaw_ratio, pitch_ratio)
    """
    try:
        mid_x = (left_temple_pt[0] + right_temple_pt[0]) / 2.0
        mid_y = (forehead_pt[1] + chin_pt[1]) / 2.0
        face_w = max(1e-4, abs(right_temple_pt[0] - left_temple_pt[0]))
        face_h = max(1e-4, abs(chin_pt[1] - forehead_pt[1]))

        # النسب المعيارية للانحراف
        yaw_ratio = (nose_pt[0] - mid_x) / (face_w * 0.45)
        pitch_ratio = (nose_pt[1] - mid_y) / (face_h * 0.45)

        # تحويل تقريبي للدرجات الهندسية
        yaw_deg = float(yaw_ratio * 45.0)
        pitch_deg = float(pitch_ratio * 40.0)

        is_frontal = (abs(yaw_ratio) <= max_yaw_tol and abs(pitch_ratio) <= max_pitch_tol)
        return is_frontal, yaw_deg, pitch_deg, float(yaw_ratio), float(pitch_ratio)
    except Exception:
        return True, 0.0, 0.0, 0.0, 0.0


def continuous_leash_easing(
    target_x: float,
    target_y: float,
    smooth_x: Optional[float],
    smooth_y: Optional[float],
    deadband: float = 1.8,
    leash_outer: float = 8.0
) -> Tuple[float, float]:
    """
    خوارزمية المنطقة الميتة الصارمة والتنعيم التدريجي المتصل (Strict Deadband & Continuous Leash Easing):
    
    1. السكون التام (Strict Deadband / Laser Lock):
       إذا كانت المسافة dist <= deadband: الإحداثيات تتجمد تماماً بدون أي ارتعاش فسيولوجي.
       
    2. التنعيم التدريجي المتصل بحبل الجر (Continuous Leash Easing):
       عند تجاوز المنطقة الميتة، يتم حساب الحركة الفائضة:
           d_excess = dist - deadband
       ويتم تطبيق دالة تسارع انسيابية تضمن اتصال المشتقة C^0 و C^1،
       مع استجابة فورية بدون مطاطية عند الحركات الواسعة.
    """
    if smooth_x is None or smooth_y is None:
        return float(target_x), float(target_y)

    dx = float(target_x) - smooth_x
    dy = float(target_y) - smooth_y
    dist = math.hypot(dx, dy)

    # 1. القفل الصارم في المنطقة الميتة (Zero Jitter)
    if dist <= deadband:
        return smooth_x, smooth_y

    # 2. التنعيم التدريجي المتصل
    excess = dist - deadband
    ratio = excess / max(1e-4, dist)

    # منحنى تكيفي للسرعة:
    # حركات دقيقة (تصحيح موضع): تنعيم فائق ومستقر (alpha ~ 0.30)
    # حركات سريعة وواسعة: متابعة فورية بدون تباطؤ (alpha ~ 0.92)
    speed_norm = min(1.0, excess / max(1.0, leash_outer))
    adaptive_alpha = 0.30 + 0.62 * (speed_norm ** 1.35)
    factor = ratio * adaptive_alpha

    new_x = smooth_x + dx * factor
    new_y = smooth_y + dy * factor
    return new_x, new_y


def solve_affine_transform(
    source_points: List[Tuple[float, float]],
    target_points: List[Tuple[float, float]]
) -> Tuple[Optional[List[float]], Optional[List[float]], bool, float]:
    """
    حساب مصفوفة التحويل الهندسية التآلفية (Affine Transformation Matrix) باستخدام المربعات الصغرى (Least Squares).
    
    العلاقة الرياضية:
        u = a1 * x + a2 * y + a3
        v = b1 * x + b2 * y + b3
        
    يتم فحص صلاحية المصفوفة واستقرارها الرياضي (Conditioning / Residual Error) لمنع قفل المؤشر في الزوايا.
    
    المخرجات:
        (affine_x [a1, a2, a3], affine_y [b1, b2, b3], is_valid, mean_residual_error)
    """
    if len(source_points) < 6 or len(source_points) != len(target_points):
        return None, None, False, 999.0

    try:
        src_x = [p[0] for p in source_points]
        src_y = [p[1] for p in source_points]
        tgt_x = [p[0] for p in target_points]
        tgt_y = [p[1] for p in target_points]

        M = np.column_stack([src_x, src_y, np.ones(len(src_x))])

        sol_x, residuals_x, rank_x, _ = np.linalg.lstsq(M, tgt_x, rcond=None)
        sol_y, residuals_y, rank_y, _ = np.linalg.lstsq(M, tgt_y, rcond=None)

        if rank_x < 3 or rank_y < 3:
            return None, None, False, 999.0

        # التحقق من دقة التنبؤ على نقاط المعايرة نفسها
        residuals = []
        is_valid = True
        for i in range(len(source_points)):
            pred_x = sol_x[0] * src_x[i] + sol_x[1] * src_y[i] + sol_x[2]
            pred_y = sol_y[0] * src_y[i] + sol_y[1] * src_y[i] + sol_y[2]

            # التأكد أن الإحداثيات المتوقعة لا تقفز خارج حدود الشاشة المعقولة
            if not (-0.25 <= pred_x <= 1.25 and -0.25 <= pred_y <= 1.25):
                is_valid = False
                break

            err = math.hypot(pred_x - tgt_x[i], pred_y - tgt_y[i])
            residuals.append(err)

        mean_error = float(np.mean(residuals)) if residuals else 999.0

        # فحص سلامة التناغم: التحقق من عدم وجود تداخل محاور مفرط (Cross-Axis Skewing)
        if abs(sol_x[1]) > abs(sol_x[0]) * 2.2 or abs(sol_y[0]) > abs(sol_y[1]) * 2.2:
            is_valid = False

        if is_valid and mean_error < 0.35:
            return [float(v) for v in sol_x], [float(v) for v in sol_y], True, mean_error
        else:
            return None, None, False, mean_error

    except Exception:
        return None, None, False, 999.0


def apply_affine_transform(
    affine_x: List[float],
    affine_y: List[float],
    x: float,
    y: float
) -> Tuple[float, float]:
    """تطبيق مصفوفة التحويل التآلفي على إحداثي (x, y)."""
    nx = affine_x[0] * x + affine_x[1] * y + affine_x[2]
    ny = affine_y[0] * x + affine_y[1] * y + affine_y[2]
    return float(nx), float(ny)


class ExponentialFilter:
    """مرشح التنعيم الأسّي الكلاسيكي (EMA) مع منطقة ميتة."""
    def __init__(self, alpha: float = 0.26, deadzone: float = 3.5):
        self.alpha = alpha
        self.deadzone = deadzone
        self.x: Optional[float] = None
        self.y: Optional[float] = None

    def update(self, target_x: float, target_y: float) -> Tuple[float, float]:
        if self.x is None or self.y is None:
            self.x, self.y = float(target_x), float(target_y)
            return self.x, self.y

        dist = math.hypot(target_x - self.x, target_y - self.y)
        if dist < self.deadzone:
            return self.x, self.y

        self.x = self.x * (1.0 - self.alpha) + target_x * self.alpha
        self.y = self.y * (1.0 - self.alpha) + target_y * self.alpha
        return self.x, self.y

    def reset(self) -> None:
        self.x = None
        self.y = None


class OneEuroFilter:
    """مرشح One Euro الرياضي المتكيف لحظياً مع السرعة الحركية."""
    def __init__(self, min_cutoff: float = 1.2, beta: float = 0.008, d_cutoff: float = 1.0, deadzone: float = 0.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.deadzone = deadzone
        self.x_prev: Optional[float] = None
        self.y_prev: Optional[float] = None
        self.dx_prev = 0.0
        self.dy_prev = 0.0
        self.t_prev: Optional[float] = None

    def _smoothing_factor(self, t_e: float, cutoff: float) -> float:
        r = 2.0 * math.pi * cutoff * t_e
        return r / (r + 1.0)

    def _exp_smooth(self, a: float, x: float, x_prev: float) -> float:
        return a * x + (1.0 - a) * x_prev

    def filter(self, x: float, y: float, timestamp: float) -> Tuple[float, float]:
        if self.t_prev is None or self.x_prev is None or self.y_prev is None:
            self.x_prev = float(x)
            self.y_prev = float(y)
            self.dx_prev = 0.0
            self.dy_prev = 0.0
            self.t_prev = timestamp
            return x, y

        dist = math.hypot(x - self.x_prev, y - self.y_prev)
        if dist < self.deadzone:
            return self.x_prev, self.y_prev

        t_e = max(1e-4, timestamp - self.t_prev)
        self.t_prev = timestamp

        dx = (x - self.x_prev) / t_e
        dy = (y - self.y_prev) / t_e

        a_d = self._smoothing_factor(t_e, self.d_cutoff)
        dx_hat = self._exp_smooth(a_d, dx, self.dx_prev)
        dy_hat = self._exp_smooth(a_d, dy, self.dy_prev)
        self.dx_prev = dx_hat
        self.dy_prev = dy_hat

        speed = math.hypot(dx_hat, dy_hat)
        cutoff = self.min_cutoff + self.beta * speed
        a = self._smoothing_factor(t_e, cutoff)

        x_filtered = self._exp_smooth(a, x, self.x_prev)
        y_filtered = self._exp_smooth(a, y, self.y_prev)

        self.x_prev = x_filtered
        self.y_prev = y_filtered
        return x_filtered, y_filtered

    def reset(self) -> None:
        self.x_prev = None
        self.y_prev = None
        self.dx_prev = 0.0
        self.dy_prev = 0.0
        self.t_prev = None
