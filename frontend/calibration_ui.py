"""
==================================================================================
نافذة المعايرة الهندسية التفاعلية (9-Point Interactive Calibration Window)
Independent 9-Point Calibration Window with Affine Transformation Solver
==================================================================================
تتيح للمستخدم معايرة دقيقة لـ 9 نقاط تفاعلية على الشاشة:
- استخراج عينات حركة الأنف وحساب مصفوفة التحويل التآلفي (Affine Transform).
- التنسيق مع آلة الحالات (State Machine) لضمان حجب الإيماءات ومنع أي تداخل.
- واجهة مستخدم تفاعلية انسيابية ومريحة مع مؤشرات بصرية وصوتية للتثبيت.
==================================================================================
"""

import time
import threading
import tkinter as tk
from typing import Optional, Callable, List, Tuple, Any
import numpy as np

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

import os
import sys

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_CURRENT_DIR)
_BACKEND_DIR = os.path.join(_PROJECT_ROOT, "backend")

for _p in [_CURRENT_DIR, _PROJECT_ROOT, _BACKEND_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from backend.core_math import solve_affine_transform
except ImportError:
    from core_math import solve_affine_transform


class CalibrationWindow(tk.Toplevel):
    """نافذة مستقلة لمعايرة 9 نقاط بدقة عالية واستخراج مصفوفة التحويل الهندسي."""
    def __init__(
        self,
        parent: tk.Tk,
        tracker: Any,
        state_machine: Any,
        get_tracking_data_fn: Callable[[], Any],
        on_complete_callback: Optional[Callable[[], None]] = None
    ):
        super().__init__(parent)
        self.parent = parent
        self.tracker = tracker
        self.state_machine = state_machine
        self.get_tracking_data_fn = get_tracking_data_fn
        self.on_complete_callback = on_complete_callback

        self.title("🎯 معايرة دقيقة للأنف — 9-Point Calibration Matrix")
        self.geometry("960x700")
        self.minsize(800, 600)
        self.configure(bg="#0b0f19")
        self.transient(parent)
        self.grab_set()

        # إشعار آلة الحالات ببدء المعايرة
        if self.state_machine:
            self.state_machine.start_calibration()

        # مصفوفة النقاط التسع (شبكة 3x3)
        self.points: List[Tuple[float, float]] = [
            (0.15, 0.15), (0.50, 0.15), (0.85, 0.15),
            (0.15, 0.50), (0.50, 0.50), (0.85, 0.50),
            (0.15, 0.85), (0.50, 0.85), (0.85, 0.85)
        ]
        self.current_pt_idx = 0
        self.samples_per_point: List[Tuple[float, float]] = []
        self.all_calibration_data: List[Tuple[float, float, float, float]] = []

        self.pt_start_time = time.time()
        self.dwell_time_required = 1.25  # ثانية تثبيت لكل نقطة

        self._build_ui()

        self.running = True
        self.bind("<Escape>", lambda e: self.close())
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.update_loop()

    def _build_ui(self) -> None:
        header = tk.Frame(self, bg="#111827", pady=10)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🎯 المعايرة المكانية الدقيقة (Affine Geometry Calibration)",
            font=("Segoe UI", 14, "bold"),
            fg="#38bdf8", bg="#111827"
        ).pack()

        self.canvas = tk.Canvas(self, bg="#0b0f19", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.footer = tk.Frame(self, bg="#111827", pady=8, padx=15)
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)

        self.info_lbl = tk.Label(
            self.footer,
            text="وجّه أنفك نحو الهدف الأخضر وثبّت رأسك حتى تكتمل حلقة التحميل",
            font=("Segoe UI", 11, "bold"),
            fg="#38bdf8", bg="#111827"
        )
        self.info_lbl.pack(side=tk.LEFT)

        tk.Button(
            self.footer,
            text="إلغاء المعايرة [Esc]",
            font=("Segoe UI", 9, "bold"),
            bg="#ef4444", fg="white", activebackground="#dc2626",
            relief=tk.FLAT, cursor="hand2", padx=10, pady=4,
            command=self.close
        ).pack(side=tk.RIGHT)

    def update_loop(self) -> None:
        if not self.running:
            return

        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        self.canvas.delete("all")

        if cw > 50 and ch > 50 and self.current_pt_idx < len(self.points):
            pt_rel_x, pt_rel_y = self.points[self.current_pt_idx]
            px = pt_rel_x * cw
            py = pt_rel_y * ch

            now = time.time()
            elapsed = now - self.pt_start_time
            progress = min(1.0, elapsed / self.dwell_time_required)

            # الحصول على بيانات التتبع اللحظية
            data = self.get_tracking_data_fn()

            if data and getattr(data, "face_found", False):
                sx = getattr(data, "smooth_norm_x", getattr(data, "raw_x", 0.5))
                sy = getattr(data, "smooth_norm_y", getattr(data, "raw_y", 0.5))
                self.samples_per_point.append((sx, sy))

            # رسم شبكة مساعدة خفيفة
            for p in self.points:
                gpx, gpy = p[0] * cw, p[1] * ch
                self.canvas.create_oval(gpx - 4, gpy - 4, gpx + 4, gpy + 4, fill="#1f2937", outline="#374151")

            # رسم النقطة المستهدفة الحالية
            r = 22
            self.canvas.create_oval(px - r, py - r, px + r, py + r, fill="#065f46", outline="#10b981", width=2)
            self.canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill="#ffffff", outline="")

            # رسم حلقة التقدم الزمني الدائرية
            if progress > 0.0:
                angle = -(progress * 360.0)
                self.canvas.create_arc(
                    px - (r + 8), py - (r + 8), px + (r + 8), py + (r + 8),
                    start=90, extent=angle, style=tk.ARC, outline="#38bdf8", width=5
                )

            self.canvas.create_text(
                px, py + r + 20,
                text=f"نقطة {self.current_pt_idx + 1} من 9",
                font=("Segoe UI", 10, "bold"), fill="#94a3b8"
            )

            # رسم مؤشر الأنف الفعلي للمستخدم
            if data and getattr(data, "face_found", False):
                nx = getattr(data, "nose_norm_x", 0.5) * cw
                ny = getattr(data, "nose_norm_y", 0.5) * ch
                self.canvas.create_oval(nx - 5, ny - 5, nx + 5, ny + 5, fill="#ef4444", outline="#ffffff")

                smx = getattr(data, "smooth_norm_x", 0.5) * cw
                smy = getattr(data, "smooth_norm_y", 0.5) * ch
                self.canvas.create_oval(smx - 4, smy - 4, smx + 4, smy + 4, fill="#10b981", outline="")

            # اكتمال النقطة الحالية
            if progress >= 1.0:
                if len(self.samples_per_point) >= 4:
                    avg_rx = float(np.mean([s[0] for s in self.samples_per_point]))
                    avg_ry = float(np.mean([s[1] for s in self.samples_per_point]))
                    self.all_calibration_data.append((pt_rel_x, pt_rel_y, avg_rx, avg_ry))

                if HAS_WINSOUND:
                    threading.Thread(target=lambda: winsound.Beep(1200, 60), daemon=True).start()

                self.current_pt_idx += 1
                self.samples_per_point = []
                self.pt_start_time = time.time()

        elif self.current_pt_idx >= len(self.points):
            self._finalize_calibration()
            return

        self.after(20, self.update_loop)

    def _finalize_calibration(self) -> None:
        """معالجة العينات وحساب مصفوفة Affine Transform مع فحص السلامة وضبط الحساسية."""
        self.canvas.delete("all")
        self.info_lbl.config(text="✅ تمت المعايرة بنجاح! جاري معالجة البيانات الهندسية وحفظها...", fg="#10b981")

        if len(self.all_calibration_data) >= 6:
            target_pts = [(d[0], d[1]) for d in self.all_calibration_data]
            source_pts = [(d[2], d[3]) for d in self.all_calibration_data]

            raw_xs = [p[0] for p in source_pts]
            raw_ys = [p[1] for p in source_pts]

            # 1. المركز المحايد من النقطة المركزية (5 = index 4) أو المتوسط الحسابي
            center_idx = None
            for i, d in enumerate(self.all_calibration_data):
                if abs(d[0] - 0.50) < 0.08 and abs(d[1] - 0.50) < 0.08:
                    center_idx = i
                    break

            if center_idx is not None:
                center_raw_x = raw_xs[center_idx]
                center_raw_y = raw_ys[center_idx]
            else:
                center_raw_x = float(np.mean(raw_xs))
                center_raw_y = float(np.mean(raw_ys))

            fw = float(self.tracker.nose_algo._last_frame_w)
            fh = float(self.tracker.nose_algo._last_frame_h)
            self.tracker.nose_algo.calibrate(center_raw_x, center_raw_y, fw, fh)

            # 2. حساب الحساسية التكيفية بشكل آمن (مع تصحيح متغيرات النطاق)
            raw_range_x = float(max(raw_xs) - min(raw_xs))
            raw_range_y = float(max(raw_ys) - min(raw_ys))

            if raw_range_x > 0.02:
                target_range_px = (raw_range_x * fw) / 1.4
                calc_sens_x = self.tracker.nose_algo.base_head_range_x / max(15.0, target_range_px)
                self.tracker.nose_algo.head_sensitivity_x = float(np.clip(calc_sens_x, 0.6, 2.0))
            else:
                self.tracker.nose_algo.head_sensitivity_x = 1.0

            if raw_range_y > 0.02:
                target_range_py = (raw_range_y * fh) / 1.4
                calc_sens_y = self.tracker.nose_algo.base_head_range_y / max(12.0, target_range_py)
                self.tracker.nose_algo.head_sensitivity_y = float(np.clip(calc_sens_y, 0.6, 2.0))
            else:
                self.tracker.nose_algo.head_sensitivity_y = 1.0

            # 3. حساب مصفوفة التحويل التآلفي Affine عبر الدالة النقية
            aff_x, aff_y, is_valid, mean_err = solve_affine_transform(source_pts, target_pts)

            if is_valid and aff_x is not None and aff_y is not None:
                self.tracker.affine_x = aff_x
                self.tracker.affine_y = aff_y
                self.tracker.is_calibrated = True
                print(f"[OK] Affine Calibration succeeded! Mean error: {mean_err:.4f}")
            else:
                self.tracker.affine_x = None
                self.tracker.affine_y = None
                self.tracker.is_calibrated = False
                print(f"[Warning] Affine validation failed (err: {mean_err:.3f}) -> using calibrated linear fallback.")

            self.tracker.nose_algo.reset_smoothing()
            self.tracker.save_calibration()

            if HAS_WINSOUND:
                threading.Thread(target=lambda: winsound.Beep(1600, 150), daemon=True).start()

        # إشعار باكتمال المعايرة وإرجاع الحالة
        if self.state_machine:
            self.state_machine.finish_calibration(success=True)

        if self.on_complete_callback:
            self.on_complete_callback()

        self.after(1200, self.close)

    def close(self) -> None:
        self.running = False
        if self.state_machine and self.state_machine.current_state.name == "CALIBRATING":
            self.state_machine.finish_calibration(success=False)
        self.destroy()
