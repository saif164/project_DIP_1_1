"""
==================================================================================
مشروع: كيبورد افتراضي ذكي فائق الكفاءة بتتبع الأنف وإيماءات اليد المتقدمة
Nose-Controlled Virtual Keyboard with Hand Gesture Controls & 9-Point Calibration
==================================================================================
الإصدار: 5.0 — Enterprise Architecture & Modern Ergonomic UI Edition
التقنيات: Python, OpenCV, MediaPipe Tasks, Tkinter Multi-threading, Vector Math
==================================================================================
المعمارية البرمجية (Software Architecture):
- Core Math: [core_math.py] حسابات التحويل الهندسي، EAR، Head Pose، والتنعيم.
- State Machine: [state_machine.py] آلة حالات دقيقة (Latching State Machine) لمنع التداخل.
- Tracking Engine: [tracking_engine.py] محرك الرؤية، تتبع الأنف واليد، وإدارة المعايرة.
- Calibration UI: [calibration_ui.py] نافذة تفاعلية لمعايرة 9 نقاط بدقة عالية.
- Main GUI App: [gaze_keyboard.py] واجهة المستخدم المتطورة، التزامن متعدد الخيوط، والكانفاس.
==================================================================================
saif sayyad

"""

import os
import sys
import time
import math
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Dict, Any, Tuple

import cv2
import numpy as np
from PIL import Image, ImageTk

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# استيراد الوحدات المعمارية النظيفة
from core_math import (
    calculate_ear,
    calculate_head_pose,
    continuous_leash_easing,
    ExponentialFilter,
    OneEuroFilter
)
from state_machine import SystemState, AppStateMachine
from tracking_engine import (
    TrackingResult,
    NosePointerAlgorithm,
    VisionTrackerEngine,
    CALIBRATION_FILE
)
from calibration_ui import CalibrationWindow


class GazeVirtualKeyboardApp:
    """
    تطبيق الكيبورد الافتراضي الذكي بالكامل:
    - إدارة واجهة المستخدم الرسومية الحديثة (Tkinter Main Thread).
    - التزامن الآمن (Concurrency / Threading.Lock) مع خيط الرؤية الحاسوبية الكثيف.
    - نظام تتبع الأنف بالمناطق الميتة الصارمة وإيماءات اليد المتقدمة.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("الكيبورد الافتراضي الذكي — Nose Pointer & Gesture Edition v5.0")
        self.root.geometry("1420x920")
        self.root.minsize(1160, 780)
        self.root.configure(bg="#080c14")

        # ----------------------------------------------------------------------
        # 1. آلة الحالات (State Machine)
        # ----------------------------------------------------------------------
        self.state_machine = AppStateMachine(
            on_state_change=self._on_system_state_change,
            on_row_locked=self._on_row_locked_event,
            on_row_unlocked=self._on_row_unlocked_event
        )

        # ----------------------------------------------------------------------
        # 2. إعدادات التثبيت الزمني للكتابة (Dwell Time Typing)
        # ----------------------------------------------------------------------
        self.dwell_threshold = 0.85
        self.cooldown_duration = 0.50
        self.current_hover_key: Optional[Dict[str, Any]] = None
        self.hover_start_time = 0.0
        self.is_cooling_down = False
        self.cooldown_start_time = 0.0
        self.last_typed_key: Optional[Dict[str, Any]] = None
        self.typed_flash_time = 0.0

        # ----------------------------------------------------------------------
        # 3. وضع الماوس والتشخيص
        # ----------------------------------------------------------------------
        self.mouse_mode = False
        self.mouse_pos = [680.0, 460.0]
        self.debug_mode = False
        self.current_layout_name = "AR"  # "AR" أو "EN"

        # إشعارات التنبيه (Toasts)
        self.toast_message = ""
        self.toast_until = 0.0
        self.toast_color = "#10b981"

        # مرشحات تنعيم العرض على الشاشة (Screen Canvas Smoothing)
        self.filter_mode = "OneEuro"
        self.one_euro_filter = OneEuroFilter(min_cutoff=2.0, beta=0.02, deadzone=0.0)
        self.ema_filter = ExponentialFilter(alpha=0.45, deadzone=0.0)
        self.cursor_pos = [680.0, 460.0]

        # مؤشرات الأداء (FPS & Telemetry)
        self.fps = 0.0
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.proc_latency_ms = 0.0

        # ----------------------------------------------------------------------
        # 4. محرك الرؤية وتعدد الخيوط (Multithreading & Concurrency)
        # ----------------------------------------------------------------------
        self.tracker = VisionTrackerEngine()
        self.cap: Optional[cv2.VideoCapture] = None
        self.running = True
        self.camera_ok = False

        # قفل التزامن وحاويات البيانات المشتركة بين الخيوط
        self.data_lock = threading.Lock()
        self.latest_frame: Optional[np.ndarray] = None
        self.latest_tracking: TrackingResult = TrackingResult()

        self._start_camera()
        self._setup_styles()
        self._build_ui()

        # اختصارات لوحة المفاتيح المساعدة
        self.root.bind("<c>", lambda e: self.recalibrate_center())
        self.root.bind("<C>", lambda e: self.recalibrate_center())
        self.root.bind("<m>", lambda e: self.toggle_mouse_mode())
        self.root.bind("<M>", lambda e: self.toggle_mouse_mode())
        self.root.bind("<d>", lambda e: self.toggle_debug_mode())
        self.root.bind("<D>", lambda e: self.toggle_debug_mode())
        self.root.bind("<l>", lambda e: self.toggle_keyboard_layout())
        self.root.bind("<L>", lambda e: self.toggle_keyboard_layout())
        self.root.bind("<r>", lambda e: self.do_reset_calibration())
        self.root.bind("<R>", lambda e: self.do_reset_calibration())
        self.root.bind("<Escape>", lambda e: self.on_close())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # بدء حلقة التحديث الرئيسية لواجهة المستخدم
        self.update_loop()

    # ==========================================================================
    # إعداد النمط البصري وتهيئة الكاميرا في خيط مستقل
    # ==========================================================================
    def _setup_styles(self) -> None:
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#080c14")
        self.style.configure("TLabel", background="#080c14", foreground="#cbd5e1", font=("Segoe UI", 10))

    def _start_camera(self) -> None:
        """تهيئة الكاميرا وتشغيل خيط الالتقاط المنفصل Background Thread."""
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                ret, _ = self.cap.read()
                if ret:
                    self.camera_ok = True
                    print("[OK] Webcam connected successfully.")
                else:
                    self.camera_ok = False
            else:
                self.camera_ok = False
        except Exception as e:
            print(f"[Error] Camera initialization failed: {e}")
            self.camera_ok = False

        if not self.camera_ok:
            print("[Info] Camera unavailable -> Activated Simulated Mouse Mode.")
            self.mouse_mode = True
            self.state_machine.handle_tracking_loss("الكاميرا غير متصلة - وضع الماوس نشط")

        # إطلاق خيط المعالجة الثقيلة المستقل (Anti-Freezing Architecture)
        if self.camera_ok:
            self.video_thread = threading.Thread(target=self._capture_worker, daemon=True)
            self.video_thread.start()

    def _capture_worker(self) -> None:
        """
        خيط المعالجة المستقل (Background Worker Thread):
        - قراءة إطارات الكاميرا ومعالجة الرؤية الحاسوبية دون تجميد واجهة المستخدم مطلقاً.
        - حفظ النتائج داخل كائن TrackingResult محمي بقفل تزامن threading.Lock.
        """
        while self.running:
            if self.cap and self.cap.isOpened():
                t0 = time.time()
                ret, frame = self.cap.read()
                if not ret:
                    with self.data_lock:
                        self.latest_tracking.face_found = False
                    time.sleep(0.02)
                    continue

                # قلب الإطار أفقياً ليكون مرآة طبيعية
                frame = cv2.flip(frame, 1)

                # معالجة الرؤية الحاسوبية (Face + Hands + Nose Algo)
                tracking_res = self.tracker.process_frame(frame, debug=self.debug_mode)
                latency = (time.time() - t0) * 1000.0

                # تحديث آمن للبيانات المشتركة عبر قفل التزامن (Thread-Safe Concurrency)
                with self.data_lock:
                    self.latest_frame = frame
                    self.latest_tracking = tracking_res
                    self.proc_latency_ms = latency

            time.sleep(0.012)

    # ==========================================================================
    # بناء واجهة المستخدم الحديثة (Modern Ergonomic UI Construction)
    # ==========================================================================
    def _build_ui(self) -> None:
        # 1. الشريط العلوي المتطور (Header & Status Badges)
        top_container = tk.Frame(
            self.root, bg="#0f172a", bd=0,
            highlightthickness=1, highlightbackground="#1e293b"
        )
        top_container.pack(side=tk.TOP, fill=tk.X, padx=12, pady=(8, 4))

        # السطر الأول: العنوان وشارات الحالة
        header_row = tk.Frame(top_container, bg="#0f172a")
        header_row.pack(fill=tk.X, padx=12, pady=(6, 4))

        tk.Label(
            header_row,
            text="✨ NOSE-KEYBOARD ENTERPRISE v5.0 | نظام الكيبورد الافتراضي الذكي",
            font=("Segoe UI", 12, "bold"),
            fg="#38bdf8", bg="#0f172a"
        ).pack(side=tk.RIGHT)

        # حاوية شارات الحالة (Status Badges)
        indicators_frame = tk.Frame(header_row, bg="#0f172a")
        indicators_frame.pack(side=tk.LEFT)

        self.badge_state = tk.Label(
            indicators_frame, text="🟢 نشط (ACTIVE)", font=("Segoe UI", 9, "bold"),
            fg="#10b981", bg="#1e293b", padx=9, pady=3
        )
        self.badge_state.pack(side=tk.LEFT, padx=3)

        self.badge_face = tk.Label(
            indicators_frame, text="الأنف: جاري الرصد", font=("Segoe UI", 9, "bold"),
            fg="#f59e0b", bg="#1e293b", padx=9, pady=3
        )
        self.badge_face.pack(side=tk.LEFT, padx=3)

        self.badge_pose = tk.Label(
            indicators_frame, text="الاتجاه: --", font=("Segoe UI", 9, "bold"),
            fg="#94a3b8", bg="#1e293b", padx=9, pady=3
        )
        self.badge_pose.pack(side=tk.LEFT, padx=3)

        self.badge_eyes = tk.Label(
            indicators_frame, text="العين: --", font=("Segoe UI", 9, "bold"),
            fg="#94a3b8", bg="#1e293b", padx=9, pady=3
        )
        self.badge_eyes.pack(side=tk.LEFT, padx=3)

        self.badge_gesture = tk.Label(
            indicators_frame, text="اليد: --", font=("Segoe UI", 9, "bold"),
            fg="#38bdf8", bg="#1e293b", padx=9, pady=3
        )
        self.badge_gesture.pack(side=tk.LEFT, padx=3)

        self.badge_fps = tk.Label(
            indicators_frame, text="-- FPS", font=("Segoe UI", 9, "bold"),
            fg="#cbd5e1", bg="#1e293b", padx=8, pady=3
        )
        self.badge_fps.pack(side=tk.LEFT, padx=3)

        # السطر الثاني: حقل النص والأزرار السريعة
        text_row = tk.Frame(top_container, bg="#0f172a")
        text_row.pack(fill=tk.X, padx=12, pady=(4, 6))

        quick_btns = tk.Frame(text_row, bg="#0f172a")
        quick_btns.pack(side=tk.LEFT, padx=(0, 10))

        # أزرار الإجراءات السريعة بتصميم عصري
        self.btn_top_center = tk.Button(
            quick_btns, text="🎯 ضبط المركز [C]", font=("Segoe UI", 9, "bold"),
            bg="#059669", fg="white", activebackground="#047857", relief=tk.FLAT,
            cursor="hand2", padx=10, pady=5, command=self.recalibrate_center
        )
        self.btn_top_center.pack(side=tk.LEFT, padx=2)

        self.btn_top_mouse = tk.Button(
            quick_btns, text="🖱️ وضع الماوس [M]", font=("Segoe UI", 9, "bold"),
            bg="#334155", fg="white", activebackground="#1e293b", relief=tk.FLAT,
            cursor="hand2", padx=10, pady=5, command=self.toggle_mouse_mode
        )
        self.btn_top_mouse.pack(side=tk.LEFT, padx=2)

        self.btn_top_calib = tk.Button(
            quick_btns, text="🎯 معايرة 9 نقاط", font=("Segoe UI", 9, "bold"),
            bg="#7c3aed", fg="white", activebackground="#6d28d9", relief=tk.FLAT,
            cursor="hand2", padx=10, pady=5, command=self.open_calibration_window
        )
        self.btn_top_calib.pack(side=tk.LEFT, padx=2)

        self.btn_layout_toggle = tk.Button(
            quick_btns, text="🌐 عربي / English [L]", font=("Segoe UI", 9, "bold"),
            bg="#0284c7", fg="white", activebackground="#0369a1", relief=tk.FLAT,
            cursor="hand2", padx=10, pady=5, command=self.toggle_keyboard_layout
        )
        self.btn_layout_toggle.pack(side=tk.LEFT, padx=2)

        self.btn_top_debug = tk.Button(
            quick_btns, text="🐞 تشخيص [D]", font=("Segoe UI", 9, "bold"),
            bg="#475569", fg="white", activebackground="#334155", relief=tk.FLAT,
            cursor="hand2", padx=8, pady=5, command=self.toggle_debug_mode
        )
        self.btn_top_debug.pack(side=tk.LEFT, padx=2)

        tk.Button(
            quick_btns, text="📋 نسخ", font=("Segoe UI", 9, "bold"),
            bg="#2563eb", fg="white", activebackground="#1d4ed8", relief=tk.FLAT,
            cursor="hand2", padx=8, pady=5, command=self.copy_text
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            quick_btns, text="🗑️ مسح", font=("Segoe UI", 9, "bold"),
            bg="#dc2626", fg="white", activebackground="#b91c1c", relief=tk.FLAT,
            cursor="hand2", padx=8, pady=5, command=self.clear_text
        ).pack(side=tk.LEFT, padx=2)

        # حقل النص المكتوب
        self.text_entry = tk.Entry(
            text_row, font=("Segoe UI", 22, "bold"), bg="#090d16", fg="#f8fafc",
            insertbackground="#38bdf8", justify=tk.RIGHT, relief=tk.FLAT, bd=6
        )
        self.text_entry.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # شريط التلميحات السريعة
        tips_bar = tk.Frame(top_container, bg="#0b0f19", padx=8, pady=3)
        tips_bar.pack(fill=tk.X, padx=12, pady=(1, 5))

        tk.Label(
            tips_bar,
            text="💡 الاختصارات: [C] ضبط المركز | [M] الماوس | [L] تبديل اللغة | [D] تشخيص | [Esc] خروج || ✊ قبضة يد للإيقاف | ✋ كف يد للاستئناف | 1-4 أصابع لقفل الصف",
            font=("Segoe UI", 8),
            fg="#94a3b8", bg="#0b0f19"
        ).pack(side=tk.RIGHT)

        # 2. الحاوية الوسطى (مقسمة بين لوحة المفاتيح والشريط الجانبي)
        content_frame = tk.Frame(self.root, bg="#080c14")
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=4)

        # الشريط الجانبي (Sidebar)
        sidebar = tk.Frame(
            content_frame, bg="#0f172a", width=295,
            highlightthickness=1, highlightbackground="#1e293b"
        )
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        sidebar.pack_propagate(False)

        # المعاينة الحية للكاميرا
        cam_box = tk.LabelFrame(
            sidebar, text=" 📹 المعاينة الحية (الأحمر=الأنف، الأخضر=المعالج) ",
            font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#0f172a", padx=4, pady=4
        )
        cam_box.pack(fill=tk.X, padx=6, pady=(4, 3))

        self.cam_label = tk.Label(
            cam_box, bg="#090d16", text="جاري تشغيل الكاميرا...",
            fg="#64748b", height=7
        )
        self.cam_label.pack(fill=tk.BOTH, expand=True)

        # مصغرات الأنف واليد (Minimaps)
        minimap_frame = tk.Frame(sidebar, bg="#0f172a")
        minimap_frame.pack(fill=tk.X, padx=6, pady=2)

        nose_box = tk.LabelFrame(
            minimap_frame, text=" شبكة الأنف 👃 ",
            font=("Segoe UI", 7, "bold"), fg="#ef4444", bg="#0f172a"
        )
        nose_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2, 0))
        self.nose_canvas = tk.Canvas(nose_box, width=110, height=38, bg="#090d16", highlightthickness=0)
        self.nose_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        hand_box = tk.LabelFrame(
            minimap_frame, text=" رادار الأصابع 🖐️ ",
            font=("Segoe UI", 7, "bold"), fg="#10b981", bg="#0f172a"
        )
        hand_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))
        self.hand_canvas = tk.Canvas(hand_box, width=110, height=38, bg="#090d16", highlightthickness=0)
        self.hand_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # صندوق القياسات اللحظية
        stats_box = tk.LabelFrame(
            sidebar, text=" 📊 القياسات اللحظية ",
            font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#0f172a", padx=8, pady=3
        )
        stats_box.pack(fill=tk.X, padx=6, pady=3)

        self.stat_dist_lbl = tk.Label(
            stats_box, text="المسافة: 60cm | الأنف: (0.50, 0.50)",
            font=("Consolas", 8), fg="#cbd5e1", bg="#0f172a"
        )
        self.stat_dist_lbl.pack(anchor=tk.E)

        self.stat_algo_lbl = tk.Label(
            stats_box, text="🎯 الخوارزمية: نشطة ومستقرة",
            font=("Consolas", 8), fg="#10b981", bg="#0f172a"
        )
        self.stat_algo_lbl.pack(anchor=tk.E)

        self.stat_row_lbl = tk.Label(
            stats_box, text="الصف المقفول: لا يوجد (تتبع حر)",
            font=("Segoe UI", 8, "bold"), fg="#38bdf8", bg="#0f172a"
        )
        self.stat_row_lbl.pack(anchor=tk.E)

        self.active_key_lbl = tk.Label(
            stats_box, text="الحرف: خارج الحدود",
            font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#0f172a"
        )
        self.active_key_lbl.pack(anchor=tk.E)

        # إعدادات خوارزمية المؤشر
        settings_box = tk.LabelFrame(
            sidebar, text=" ⚙️ إعدادات التحكم بالمؤشر ",
            font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#0f172a", padx=8, pady=3
        )
        settings_box.pack(fill=tk.BOTH, expand=True, padx=6, pady=3)

        # Deadband Slider (Laser Lock)
        r_db = tk.Frame(settings_box, bg="#0f172a")
        r_db.pack(fill=tk.X, pady=(2, 0))
        tk.Label(r_db, text="المنطقة الميتة (Deadband):", bg="#0f172a", fg="#cbd5e1", font=("Segoe UI", 8)).pack(side=tk.RIGHT)
        self.deadband_val_lbl = tk.Label(r_db, text=f"{self.tracker.nose_algo.head_deadband:.1f}px", bg="#0f172a", fg="#38bdf8", font=("Segoe UI", 8, "bold"))
        self.deadband_val_lbl.pack(side=tk.LEFT)
        self.deadband_scale = tk.Scale(
            settings_box, from_=0.5, to=8.0, resolution=0.1, orient=tk.HORIZONTAL,
            bg="#0f172a", fg="#38bdf8", troughcolor="#090d16", highlightthickness=0,
            showvalue=0, command=self._on_deadband_change, width=8
        )
        self.deadband_scale.set(self.tracker.nose_algo.head_deadband)
        self.deadband_scale.pack(fill=tk.X, pady=(0, 3))

        # حساسية X
        r_sx = tk.Frame(settings_box, bg="#0f172a")
        r_sx.pack(fill=tk.X, pady=(1, 0))
        tk.Label(r_sx, text="الحساسية الأفقية (X):", bg="#0f172a", fg="#cbd5e1", font=("Segoe UI", 8)).pack(side=tk.RIGHT)
        self.sensx_val_lbl = tk.Label(r_sx, text=f"{self.tracker.nose_algo.head_sensitivity_x:.2f}", bg="#0f172a", fg="#38bdf8", font=("Segoe UI", 8, "bold"))
        self.sensx_val_lbl.pack(side=tk.LEFT)
        self.sensx_scale = tk.Scale(
            settings_box, from_=0.4, to=2.5, resolution=0.05, orient=tk.HORIZONTAL,
            bg="#0f172a", fg="#38bdf8", troughcolor="#090d16", highlightthickness=0,
            showvalue=0, command=self._on_sensx_change, width=8
        )
        self.sensx_scale.set(self.tracker.nose_algo.head_sensitivity_x)
        self.sensx_scale.pack(fill=tk.X, pady=(0, 3))

        # حساسية Y
        r_sy = tk.Frame(settings_box, bg="#0f172a")
        r_sy.pack(fill=tk.X, pady=(1, 0))
        tk.Label(r_sy, text="الحساسية الرأسية (Y):", bg="#0f172a", fg="#cbd5e1", font=("Segoe UI", 8)).pack(side=tk.RIGHT)
        self.sensy_val_lbl = tk.Label(r_sy, text=f"{self.tracker.nose_algo.head_sensitivity_y:.2f}", bg="#0f172a", fg="#38bdf8", font=("Segoe UI", 8, "bold"))
        self.sensy_val_lbl.pack(side=tk.LEFT)
        self.sensy_scale = tk.Scale(
            settings_box, from_=0.4, to=2.5, resolution=0.05, orient=tk.HORIZONTAL,
            bg="#0f172a", fg="#38bdf8", troughcolor="#090d16", highlightthickness=0,
            showvalue=0, command=self._on_sensy_change, width=8
        )
        self.sensy_scale.set(self.tracker.nose_algo.head_sensitivity_y)
        self.sensy_scale.pack(fill=tk.X, pady=(0, 3))

        # وقت التثبيت (Dwell Time)
        r_dw = tk.Frame(settings_box, bg="#0f172a")
        r_dw.pack(fill=tk.X, pady=(1, 0))
        tk.Label(r_dw, text="زمن التثبيت (Dwell):", bg="#0f172a", fg="#cbd5e1", font=("Segoe UI", 8)).pack(side=tk.RIGHT)
        self.dwell_val_lbl = tk.Label(r_dw, text=f"{self.dwell_threshold:.2f}s", bg="#0f172a", fg="#38bdf8", font=("Segoe UI", 8, "bold"))
        self.dwell_val_lbl.pack(side=tk.LEFT)
        self.dwell_scale = tk.Scale(
            settings_box, from_=0.5, to=1.5, resolution=0.05, orient=tk.HORIZONTAL,
            bg="#0f172a", fg="#38bdf8", troughcolor="#090d16", highlightthickness=0,
            showvalue=0, command=self._on_dwell_change, width=8
        )
        self.dwell_scale.set(self.dwell_threshold)
        self.dwell_scale.pack(fill=tk.X, pady=(0, 3))

        # زر تبديل المرشح النهائي
        self.btn_filter_mode = tk.Button(
            settings_box, text="⚡ مرشح العرض: One Euro",
            font=("Segoe UI", 8, "bold"),
            bg="#0284c7", fg="white", activebackground="#0369a1", relief=tk.FLAT,
            cursor="hand2", pady=3, command=self.toggle_filter_mode
        )
        self.btn_filter_mode.pack(fill=tk.X, pady=(4, 2))

        # شبكة أزرار التحكم السفلية
        btns_grid = tk.Frame(settings_box, bg="#0f172a")
        btns_grid.pack(fill=tk.X, pady=(3, 2))
        btns_grid.columnconfigure(0, weight=1)
        btns_grid.columnconfigure(1, weight=1)

        tk.Button(
            btns_grid, text="🎯 ضبط المركز", font=("Segoe UI", 8, "bold"),
            bg="#059669", fg="white", relief=tk.FLAT, cursor="hand2", pady=3,
            command=self.recalibrate_center
        ).grid(row=0, column=0, padx=1, pady=1, sticky="ew")

        tk.Button(
            btns_grid, text="🎯 معايرة 9 نقاط", font=("Segoe UI", 8, "bold"),
            bg="#7c3aed", fg="white", relief=tk.FLAT, cursor="hand2", pady=3,
            command=self.open_calibration_window
        ).grid(row=0, column=1, padx=1, pady=1, sticky="ew")

        tk.Button(
            btns_grid, text="🔄 استعادة الضبط الافتراضي", font=("Segoe UI", 8, "bold"),
            bg="#b45309", fg="white", relief=tk.FLAT, cursor="hand2", pady=3,
            command=self.do_reset_calibration
        ).grid(row=1, column=0, columnspan=2, padx=1, pady=2, sticky="ew")

        # 3. لوحة المفاتيح والكانفاس الرئيسي (Main Interactive Canvas)
        keyboard_container = tk.Frame(content_frame, bg="#080c14")
        keyboard_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            keyboard_container, bg="#080c14", highlightthickness=0, cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<Motion>", self._on_mouse_move)

        self.keys: List[Dict[str, Any]] = []
        self._setup_keyboard_layouts()
        self._calculate_key_positions(1000, 600)

    # ==========================================================================
    # تصميم لوحات المفاتيح (Layouts) وحساب الإحداثيات
    # ==========================================================================
    def _setup_keyboard_layouts(self) -> None:
        """تهيئة لوحتي المفاتيح العربية والإنجليزية."""
        self.arabic_layout = [
            ["خ", "ح", "ج", "ث", "ت", "ب", "أ"],
            ["ص", "ش", "س", "ز", "ر", "ذ", "د"],
            ["ق", "ف", "غ", "ع", "ظ", "ط", "ض"],
            ["ي", "و", "هـ", "ن", "م", "ل", "ك"],
            [
                {"label": "🎯 ضبط المركز", "code": "ACTION_CENTER", "span": 1.4},
                {"label": "،", "code": "،", "span": 0.8},
                {"label": "مسافة  ␣", "code": " ", "span": 2.4},
                {"label": ".", "code": ".", "span": 0.8},
                {"label": "⌫ مسح حرف", "code": "ACTION_BACKSPACE", "span": 1.6}
            ]
        ]

        self.english_layout = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"],
            [
                {"label": "🎯 Center", "code": "ACTION_CENTER", "span": 1.4},
                {"label": ",", "code": ",", "span": 0.8},
                {"label": "SPACE  ␣", "code": " ", "span": 2.4},
                {"label": ".", "code": ".", "span": 0.8},
                {"label": "⌫ BACKSPACE", "code": "ACTION_BACKSPACE", "span": 1.6}
            ]
        ]

    def _on_canvas_resize(self, event: tk.Event) -> None:
        self._calculate_key_positions(event.width, event.height)

    def _calculate_key_positions(self, w: int, h: int) -> None:
        """حساب أبعاد المفاتيح هندسياً لملء الكانفاس بمرونة وانسيابية."""
        self.keys.clear()
        active_layout = self.arabic_layout if self.current_layout_name == "AR" else self.english_layout

        rows = len(active_layout)
        pad_x = 9
        pad_y = 9
        margin_x = 12
        margin_y = 12

        available_w = w - (margin_x * 2)
        available_h = h - (margin_y * 2)
        row_h = (available_h - (pad_y * (rows - 1))) / rows

        for r_idx, row in enumerate(active_layout):
            y1 = margin_y + r_idx * (row_h + pad_y)
            y2 = y1 + row_h
            total_spans = sum(item.get("span", 1.0) if isinstance(item, dict) else 1.0 for item in row)
            unit_w = (available_w - (pad_x * (len(row) - 1))) / total_spans

            cur_x = margin_x
            for item in row:
                if isinstance(item, dict):
                    lbl = item["label"]
                    code = item["code"]
                    span = item.get("span", 1.0)
                    is_action = True
                else:
                    lbl = item
                    code = item
                    span = 1.0
                    is_action = False

                k_w = unit_w * span
                x1 = cur_x
                x2 = cur_x + k_w
                cur_x += k_w + pad_x

                self.keys.append({
                    "label": lbl,
                    "code": code,
                    "is_action": is_action,
                    "row_idx": r_idx,
                    "bbox": {
                        "x_min": x1, "y_min": y1, "x_max": x2, "y_max": y2,
                        "center_x": (x1 + x2) / 2.0, "center_y": (y1 + y2) / 2.0
                    }
                })

    # ==========================================================================
    # تفاعلات الإعدادات والمتحكمات (Event Handlers & Callbacks)
    # ==========================================================================
    def _on_mouse_move(self, event: tk.Event) -> None:
        if self.mouse_mode:
            self.mouse_pos = [float(event.x), float(event.y)]

    def _on_deadband_change(self, val: str) -> None:
        v = float(val)
        self.tracker.nose_algo.head_deadband = v
        self.deadband_val_lbl.config(text=f"{v:.1f}px")

    def _on_sensx_change(self, val: str) -> None:
        v = float(val)
        self.tracker.nose_algo.head_sensitivity_x = v
        self.sensx_val_lbl.config(text=f"{v:.2f}")

    def _on_sensy_change(self, val: str) -> None:
        v = float(val)
        self.tracker.nose_algo.head_sensitivity_y = v
        self.sensy_val_lbl.config(text=f"{v:.2f}")

    def _on_dwell_change(self, val: str) -> None:
        v = float(val)
        self.dwell_threshold = v
        self.dwell_val_lbl.config(text=f"{v:.2f}s")

    def toggle_keyboard_layout(self) -> None:
        """تبديل لوحة المفاتيح بين العربية والإنجليزية."""
        self.current_layout_name = "EN" if self.current_layout_name == "AR" else "AR"
        self._calculate_key_positions(self.canvas.winfo_width(), self.canvas.winfo_height())
        lang_str = "الإنجليزية" if self.current_layout_name == "EN" else "العربية"
        self.show_toast(f"🌐 تم التبديل إلى لوحة المفاتيح {lang_str}", duration=1.6)
        self.play_sound(900, 50)

    def toggle_filter_mode(self) -> None:
        if self.filter_mode == "OneEuro":
            self.filter_mode = "EMA"
            self.btn_filter_mode.config(text="⚡ مرشح العرض: Exponential (EMA)", bg="#475569")
        else:
            self.filter_mode = "OneEuro"
            self.btn_filter_mode.config(text="⚡ مرشح العرض: One Euro", bg="#0284c7")

    def toggle_mouse_mode(self) -> None:
        self.mouse_mode = not self.mouse_mode
        if self.mouse_mode:
            self.btn_top_mouse.config(text="🖱️ إلغاء الماوس", bg="#b45309")
            self.show_toast("🖱️ تم تفعيل وضع محاكاة الماوس", duration=1.5)
        else:
            self.btn_top_mouse.config(text="🖱️ وضع الماوس [M]", bg="#334155")
            self.show_toast("👃 تم تفعيل تتبع الأنف الفعلي", duration=1.5)

    def toggle_debug_mode(self) -> None:
        self.debug_mode = not self.debug_mode
        self.btn_top_debug.config(bg="#059669" if self.debug_mode else "#475569")

    def show_toast(self, msg: str, duration: float = 1.8, color: str = "#10b981") -> None:
        self.toast_message = msg
        self.toast_until = time.time() + duration
        self.toast_color = color

    def recalibrate_center(self) -> None:
        """إعادة تعيين نقطة الأنف الحالية كمركز محايد في منتصف الشاشة (0.5, 0.5)."""
        with self.data_lock:
            data = self.latest_tracking

        if data and data.face_found:
            self.tracker.nose_algo.calibrate(
                data.raw_x, data.raw_y,
                data.frame_w, data.frame_h
            )
            # مسح مصفوفة Affine عند إعادة ضبط المركز لتفادي الشذوذ الهندسي
            self.tracker.affine_x = None
            self.tracker.affine_y = None
            self.tracker.is_calibrated = False
            self.tracker.save_calibration()
            self.show_toast("🎯 تم ضبط مركز الأنف في منتصف الشاشة بنجاح!", duration=1.8, color="#10b981")
            self.play_sound(1200, 80)
        else:
            self.show_toast("⚠️ تعذر الضبط: وجه المستخدم غير مرصود حالياً", duration=1.8, color="#ef4444")

    def open_calibration_window(self) -> None:
        """فتح نافذة المعايرة الهندسية 9 نقاط."""
        def get_data_fn():
            with self.data_lock:
                return self.latest_tracking

        CalibrationWindow(
            parent=self.root,
            tracker=self.tracker,
            state_machine=self.state_machine,
            get_tracking_data_fn=get_data_fn,
            on_complete_callback=self._on_calibration_complete
        )

    def _on_calibration_complete(self) -> None:
        self.deadband_scale.set(self.tracker.nose_algo.head_deadband)
        self.sensx_scale.set(self.tracker.nose_algo.head_sensitivity_x)
        self.sensy_scale.set(self.tracker.nose_algo.head_sensitivity_y)
        self.show_toast("✅ تمت المعايرة وتطبيق مصفوفة التحويل الهندسي بنجاح!", duration=2.2)

    def do_reset_calibration(self) -> None:
        if messagebox.askyesno("تأكيد استعادة الضبط", "هل تريد إعادة ضبط جميع إعدادات المعايرة والحساسية للافتراضي؟"):
            self.tracker.reset_calibration()
            self.deadband_scale.set(1.8)
            self.sensx_scale.set(1.0)
            self.sensy_scale.set(1.0)
            self.show_toast("🔄 تمت استعادة جميع الإعدادات الافتراضية بنجاح!", duration=1.8)

    def copy_text(self) -> None:
        txt = self.text_entry.get()
        if txt:
            self.root.clipboard_clear()
            self.root.clipboard_append(txt)
            self.show_toast("📋 تم نسخ النص للحافظة بنجاح!", duration=1.5)
            self.play_sound(1100, 40)

    def clear_text(self) -> None:
        self.text_entry.delete(0, tk.END)
        self.show_toast("🗑️ تم مسح النص بالكامل", duration=1.2)
        self.play_sound(600, 50)

    def play_sound(self, freq: int = 1000, dur: int = 50) -> None:
        if HAS_WINSOUND:
            threading.Thread(target=lambda: winsound.Beep(freq, dur), daemon=True).start()

    def _on_system_state_change(self, old_state: SystemState, new_state: SystemState, reason: str) -> None:
        """معالج أحداث تغيير الحالة في آلة الحالات."""
        if new_state == SystemState.PAUSED:
            if HAS_WINSOUND:
                threading.Thread(target=lambda: (winsound.Beep(900, 80), winsound.Beep(650, 100)), daemon=True).start()
        elif new_state == SystemState.ACTIVE and old_state == SystemState.PAUSED:
            if HAS_WINSOUND:
                threading.Thread(target=lambda: (winsound.Beep(650, 80), winsound.Beep(1000, 100)), daemon=True).start()

    def _on_row_locked_event(self, row_idx: int) -> None:
        self.play_sound(950, 40)

    def _on_row_unlocked_event(self) -> None:
        pass

    def on_key_triggered(self, key_obj: Dict[str, Any]) -> None:
        """تنفيذ الإجراء المرتبط بالمفتاح عند اكتمال التثبيت الزمني (Dwell Complete)."""
        code = key_obj["code"]
        if code == "ACTION_CENTER":
            self.recalibrate_center()
        elif code == "ACTION_BACKSPACE":
            txt = self.text_entry.get()
            if txt:
                self.text_entry.delete(len(txt) - 1, tk.END)
                self.play_sound(750, 60)
        else:
            self.text_entry.insert(tk.END, code)
            self.play_sound(1150, 50)

        self.last_typed_key = key_obj
        self.typed_flash_time = time.time()

    # ==========================================================================
    # حلقة التحديث والرسم الرئيسية (Main Tkinter Loop at ~60 FPS)
    # ==========================================================================
    def update_loop(self) -> None:
        now = time.time()

        # حساب معدل الإطارات (FPS)
        self.frame_count += 1
        if now - self.last_fps_time >= 1.0:
            self.fps = self.frame_count / (now - self.last_fps_time)
            self.frame_count = 0
            self.last_fps_time = now

        # جلب أحدث بيانات التتبع بأمان تام عبر قفل التزامن (Thread Concurrency)
        with self.data_lock:
            data = self.latest_tracking

        cw = max(100, self.canvas.winfo_width())
        ch = max(100, self.canvas.winfo_height())

        # ----------------------------------------------------------------------
        # 1. تحديث آلة الحالات ومعالجة السلامة والإيماءات
        # ----------------------------------------------------------------------
        self.state_machine.update_timers(now)

        if not self.mouse_mode:
            # التحقق من سلامة وجود الوجه (Fail-Safe Handling)
            if not data.face_found:
                self.state_machine.handle_tracking_loss("وجه المستخدم غير مرئي في الإطار ⚠️")
            else:
                self.state_machine.handle_tracking_restored()

                # فحص إغلاق العين (Blink Protection & Drowsiness Safety)
                if not data.eyes_open:
                    if self.state_machine.current_state == SystemState.ACTIVE:
                        # تعليق مؤقت دون تغيير الحالة الكاملة
                        pass

                # معالجة إيماءات اليد (يتم تجاهلها تلقائياً أثناء المعايرة والتجميد الآمن)
                if data.hand_found:
                    self.state_machine.process_hand_gesture(data.gesture_name, now)

        # تحديث شارات الحالة البصرية
        badge_info = self.state_machine.get_badge_info()
        self.badge_state.config(text=badge_info["text"], fg=badge_info["color"])
        self.badge_fps.config(text=f"{self.fps:.0f} FPS | {self.proc_latency_ms:.0f}ms")

        # ----------------------------------------------------------------------
        # 2. حساب موضع المؤشر
        # ----------------------------------------------------------------------
        target_x, target_y = self.cursor_pos[0], self.cursor_pos[1]

        if self.mouse_mode:
            target_x, target_y = self.mouse_pos[0], self.mouse_pos[1]
            self.badge_face.config(text="وضع الماوس 🖱️", fg="#38bdf8")
            self.badge_pose.config(text="محاكاة", fg="#38bdf8")
            self.badge_eyes.config(text="مفتوحة 🟢", fg="#10b981")
            self.badge_gesture.config(text="--", fg="#94a3b8")
        else:
            if not data.face_found:
                self.badge_face.config(text="لا يوجد وجه ⚠️", fg="#ef4444")
                self.badge_pose.config(text="توجه للكاميرا", fg="#94a3b8")
                self.badge_eyes.config(text="--", fg="#94a3b8")
            else:
                self.badge_face.config(text="الأنف: مرصود 👃", fg="#10b981")
                if data.is_frontal:
                    self.badge_pose.config(text="الاتجاه: للأمام 🟢", fg="#10b981")
                else:
                    self.badge_pose.config(text="الاتجاه: ملتفت ⚠️", fg="#f59e0b")

                if data.eyes_open:
                    self.badge_eyes.config(text=f"العين: مفتوحة ({data.avg_ear:.2f}) 🟢", fg="#10b981")
                else:
                    self.badge_eyes.config(text=f"العين: مغلقة ({data.avg_ear:.2f}) 😴", fg="#ef4444")

            if data.hand_found:
                g_map = {
                    "FIST": "✊ قبضة (إيقاف)",
                    "OPEN_PALM": "✋ كف (استئناف)",
                    "FINGER_1": "☝️ صف 1",
                    "FINGER_2": "✌️ صف 2",
                    "FINGER_3": "🤟 صف 3",
                    "FINGER_4": "🖖 صف 4"
                }
                g_str = g_map.get(data.gesture_name, f"أصابع: {data.fingers_count}")
                self.badge_gesture.config(text=f"اليد: {g_str}", fg="#38bdf8")
            else:
                self.badge_gesture.config(text="اليد: لم تُرصد", fg="#64748b")

            # الحصول على الإحداثيات المستهدفة من خوارزمية التحكم
            if data.face_found and self.state_machine.can_move_cursor():
                target_x = data.norm_x * cw
                target_y = data.norm_y * ch

        # تطبيق قفل الصف الأفقي (Row Lock Constraint)
        if self.state_machine.current_state == SystemState.ROW_LOCKED:
            locked_row = self.state_machine.active_locked_row
            if locked_row is not None:
                row_keys = [k for k in self.keys if k["row_idx"] == locked_row]
                if row_keys:
                    row_y_center = (row_keys[0]["bbox"]["y_min"] + row_keys[0]["bbox"]["y_max"]) / 2.0
                    target_y = row_y_center

        # تطبيق مرشح العرض النهائي (Screen Canvas Smoothing Filter)
        if self.filter_mode == "OneEuro":
            smooth_x, smooth_y = self.one_euro_filter.filter(target_x, target_y, now)
        else:
            smooth_x, smooth_y = self.ema_filter.update(target_x, target_y)

        self.cursor_pos = [smooth_x, smooth_y]

        # ----------------------------------------------------------------------
        # 3. فحص التقاطع مع المفاتيح والتثبيت الزمني (Hover & Dwell Logic)
        # ----------------------------------------------------------------------
        hovered_key = None
        for key in self.keys:
            bbox = key["bbox"]
            if (bbox["x_min"] <= smooth_x <= bbox["x_max"] and
                bbox["y_min"] <= smooth_y <= bbox["y_max"]):
                hovered_key = key
                break

        if hovered_key is not None:
            self.active_key_lbl.config(text=f"الحرف: [{hovered_key['label']}]", fg="#38bdf8")
        else:
            self.active_key_lbl.config(text="الحرف: خارج الحدود", fg="#64748b")

        self.stat_dist_lbl.config(
            text=f"المسافة: {data.distance_cm:.0f}cm | الأنف: ({data.nose_norm_x:.2f}, {data.nose_norm_y:.2f})"
        )
        self.stat_algo_lbl.config(
            text=f"🎯 Deadband: {self.tracker.nose_algo.head_deadband:.1f}px | Sens: {self.tracker.nose_algo.head_sensitivity_x:.2f}",
            fg="#10b981"
        )
        if self.state_machine.current_state == SystemState.ROW_LOCKED:
            rem = max(0.0, self.state_machine.row_lock_duration - (now - self.state_machine.row_lock_start_time))
            self.stat_row_lbl.config(
                text=f"🔒 قفل الصف {self.state_machine.active_locked_row + 1} نشط ({rem:.1f}s)", fg="#38bdf8"
            )
        else:
            self.stat_row_lbl.config(text="الصف المقفول: لا يوجد (تتبع حر)", fg="#64748b")

        # معالجة زمن التثبيت Dwell Time
        can_dwell = self.state_machine.can_dwell() and (data.eyes_open or self.mouse_mode)
        dwell_progress = 0.0

        if self.is_cooling_down:
            if now - self.cooldown_start_time >= self.cooldown_duration:
                self.is_cooling_down = False
                self.current_hover_key = None
                self.hover_start_time = now
        elif can_dwell and hovered_key is not None:
            if self.current_hover_key == hovered_key:
                elapsed = now - self.hover_start_time
                dwell_progress = min(1.0, elapsed / max(0.1, self.dwell_threshold))
                if dwell_progress >= 1.0:
                    self.on_key_triggered(hovered_key)
                    self.is_cooling_down = True
                    self.cooldown_start_time = now
                    dwell_progress = 0.0
            else:
                self.current_hover_key = hovered_key
                self.hover_start_time = now
        else:
            self.current_hover_key = None
            dwell_progress = 0.0

        # ----------------------------------------------------------------------
        # 4. رسم الواجهة والمؤشرات وتحديث الكاميرا
        # ----------------------------------------------------------------------
        self._render_canvas(cw, ch, hovered_key, dwell_progress, can_dwell, data)
        self._render_minimaps(data)
        self._update_camera_preview()

        if self.running:
            self.root.after(16, self.update_loop)

    # ==========================================================================
    # محرك الرسم عالي الجودة للكانفاس (Premium Canvas Rendering Engine)
    # ==========================================================================
    def _render_canvas(
        self, w: int, h: int,
        hovered_key: Optional[Dict[str, Any]],
        dwell_progress: float,
        can_dwell: bool,
        data: TrackingResult
    ) -> None:
        self.canvas.delete("all")

        # رسم إضاءة صفية عند تفعيل قفل الصف
        if self.state_machine.current_state == SystemState.ROW_LOCKED:
            locked_row = self.state_machine.active_locked_row
            if locked_row is not None:
                row_keys = [k for k in self.keys if k["row_idx"] == locked_row]
                if row_keys:
                    min_rx = min(k["bbox"]["x_min"] for k in row_keys) - 4
                    max_rx = max(k["bbox"]["x_max"] for k in row_keys) + 4
                    min_ry = min(k["bbox"]["y_min"] for k in row_keys) - 4
                    max_ry = max(k["bbox"]["y_max"] for k in row_keys) + 4
                    self.canvas.create_rectangle(
                        min_rx, min_ry, max_rx, max_ry,
                        outline="#38bdf8", width=3, dash=(8, 4)
                    )

        # رسم أزرار الكيبورد
        for key in self.keys:
            bbox = key["bbox"]
            x1, y1, x2, y2 = bbox["x_min"], bbox["y_min"], bbox["x_max"], bbox["y_max"]
            is_hover = (key == hovered_key)
            is_flash = (key == self.last_typed_key and (time.time() - self.typed_flash_time) < 0.25)

            if is_flash:
                bg_color = "#059669"
                border_color = "#34d399"
                text_color = "#ffffff"
            elif is_hover:
                bg_color = "#1e293b" if can_dwell else "#2a1b24"
                border_color = "#38bdf8" if can_dwell else "#f43f5e"
                text_color = "#ffffff"
            elif key["is_action"]:
                bg_color = "#131b2e"
                border_color = "#24324f"
                text_color = "#93c5fd"
            else:
                bg_color = "#0f172a"
                border_color = "#1e293b"
                text_color = "#f8fafc"

            # رسم كبسولة المفتاح
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=bg_color, outline=border_color,
                width=2 if is_hover else 1
            )

            # ملء شريط التثبيت داخل المفتاح
            if is_hover and dwell_progress > 0.0 and not self.is_cooling_down and can_dwell:
                fill_h = (y2 - y1) * dwell_progress
                self.canvas.create_rectangle(
                    x1 + 2, y2 - fill_h, x2 - 2, y2 - 2,
                    fill="#0284c7", outline=""
                )

            font_size = 18 if key["is_action"] else 26
            cx, cy = bbox["center_x"], bbox["center_y"]
            self.canvas.create_text(
                cx, cy, text=key["label"],
                font=("Segoe UI", font_size, "bold"),
                fill=text_color
            )

        # تراكب الإيقاف المؤقت (Paused Overlay)
        if self.state_machine.current_state == SystemState.PAUSED:
            bw, bh = 520, 120
            bx1 = (w - bw) / 2
            by1 = (h - bh) / 2
            bx2 = bx1 + bw
            by2 = by1 + bh

            self.canvas.create_rectangle(bx1, by1, bx2, by2, fill="#0f172a", outline="#f59e0b", width=3)
            self.canvas.create_text(
                (bx1 + bx2) / 2, by1 + 40,
                text="⏸️ الكيبورد متوقف مؤقتاً (PAUSED)",
                font=("Segoe UI", 16, "bold"), fill="#f59e0b"
            )
            self.canvas.create_text(
                (bx1 + bx2) / 2, by1 + 80,
                text="افتح كف يدك ✋ للاستئناف فوراً",
                font=("Segoe UI", 12), fill="#cbd5e1"
            )

        # تراكب التجميد الآمن (Safe Freeze Overlay)
        elif self.state_machine.current_state == SystemState.SAFE_FREEZE and not self.mouse_mode:
            bw, bh = 540, 110
            bx1 = (w - bw) / 2
            by1 = (h - bh) / 2
            bx2 = bx1 + bw
            by2 = by1 + bh

            self.canvas.create_rectangle(bx1, by1, bx2, by2, fill="#1c1917", outline="#ef4444", width=3)
            self.canvas.create_text(
                (bx1 + bx2) / 2, by1 + 35,
                text="🛡️ تم تفعيل التجميد الآمن للمؤشر (SAFE FREEZE)",
                font=("Segoe UI", 15, "bold"), fill="#ef4444"
            )
            self.canvas.create_text(
                (bx1 + bx2) / 2, by1 + 75,
                text=self.state_machine.freeze_reason or "توجّه نحو الكاميرا لاستعادة التتبع تلقائياً",
                font=("Segoe UI", 11), fill="#fca5a5"
            )

        # ----------------------------------------------------------------------
        # رسم المؤشر الذكي وحلقة التحميل التفاعلية (Interactive Circular Dwell Ring)
        # ----------------------------------------------------------------------
        cx, cy = self.cursor_pos[0], self.cursor_pos[1]

        if self.state_machine.current_state == SystemState.PAUSED:
            reticle_color = "#f59e0b"
            status_text = "متوقف مؤقتاً ⏸️"
        elif self.state_machine.current_state == SystemState.SAFE_FREEZE:
            reticle_color = "#ef4444"
            status_text = "تجميد آمن 🛡️"
        elif not data.eyes_open and not self.mouse_mode:
            reticle_color = "#ef4444"
            status_text = "العيون مغلقة 😴"
        elif not data.is_frontal and not self.mouse_mode:
            reticle_color = "#f59e0b"
            status_text = "الرأس ملتفت ⚠️"
        elif self.is_cooling_down:
            reticle_color = "#94a3b8"
            status_text = "تم الاختيار ✓"
        else:
            reticle_color = "#10b981" if not self.mouse_mode else "#38bdf8"
            status_text = "🎯 Nose Algorithm" if not self.mouse_mode else "🖱️ الماوس"

        # النقطة المركزية للمؤشر
        self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=reticle_color, outline="#ffffff", width=1)

        # الحلقة الخارجية
        ring_r = 25
        self.canvas.create_oval(cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r, outline=reticle_color, width=2)

        # قوس التثبيت الزمني الدائري (Circular Dwell Progress Ring)
        if dwell_progress > 0.0 and not self.is_cooling_down and can_dwell:
            extent_angle = -(dwell_progress * 360.0)
            self.canvas.create_arc(
                cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r,
                start=90, extent=extent_angle, style=tk.ARC,
                outline="#38bdf8", width=5
            )

        if status_text:
            self.canvas.create_text(
                cx, cy + ring_r + 15,
                text=status_text,
                font=("Segoe UI", 9, "bold"),
                fill=reticle_color
            )

        # عرض التنبيهات المنبثقة (Toast Notification)
        now = time.time()
        if now < self.toast_until and self.toast_message:
            tw, th = 520, 38
            tx1 = (w - tw) / 2
            ty1 = 14
            tx2 = tx1 + tw
            ty2 = ty1 + th
            self.canvas.create_rectangle(tx1, ty1, tx2, ty2, fill="#064e3b", outline="#10b981", width=2)
            self.canvas.create_text(
                (tx1 + tx2) / 2, (ty1 + ty2) / 2,
                text=self.toast_message,
                font=("Segoe UI", 11, "bold"), fill="#a7f3d0"
            )

    def _render_minimaps(self, data: TrackingResult) -> None:
        """رسم المصغرات الجانبية لموقع الأنف ورادار الأصابع."""
        # مصغر الأنف
        self.nose_canvas.delete("all")
        nw = self.nose_canvas.winfo_width()
        nh = self.nose_canvas.winfo_height()
        if nw > 20 and nh > 20:
            self.nose_canvas.create_rectangle(4, 4, nw - 4, nh - 4, outline="#1e293b", width=1)
            # خطوط الشبكة
            cx, cy = nw / 2.0, nh / 2.0
            self.nose_canvas.create_line(cx, 4, cx, nh - 4, fill="#1e293b")
            self.nose_canvas.create_line(4, cy, nw - 4, cy, fill="#1e293b")

            if data.face_found:
                px = 4 + (nw - 8) * data.nose_norm_x
                py = 4 + (nh - 8) * data.nose_norm_y
                self.nose_canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="#ef4444", outline="#ffffff")

                sx = 4 + (nw - 8) * data.smooth_norm_x
                sy = 4 + (nh - 8) * data.smooth_norm_y
                self.nose_canvas.create_oval(sx - 3, sy - 3, sx + 3, sy + 3, fill="#10b981", outline="")
            else:
                self.nose_canvas.create_text(cx, cy, text="لا يوجد أنف", font=("Segoe UI", 7), fill="#64748b")

        # مصغر الأصابع
        self.hand_canvas.delete("all")
        hw = self.hand_canvas.winfo_width()
        hh = self.hand_canvas.winfo_height()
        if hw > 20 and hh > 20:
            finger_labels = ["Th", "In", "Mi", "Ri", "Pi"]
            bar_w = 14
            gap = 5
            total_w = (bar_w * 5) + (gap * 4)
            start_x = (hw - total_w) / 2.0

            for i in range(5):
                fx1 = start_x + i * (bar_w + gap)
                fx2 = fx1 + bar_w
                is_up = data.finger_states[i] if i < len(data.finger_states) else False
                bar_h = 24 if is_up else 8
                fy2 = hh - 12
                fy1 = fy2 - bar_h

                col = "#10b981" if is_up else "#1e293b"
                self.hand_canvas.create_rectangle(fx1, fy1, fx2, fy2, fill=col, outline="")
                self.hand_canvas.create_text(
                    (fx1 + fx2) / 2, hh - 6,
                    text=finger_labels[i],
                    font=("Consolas", 7), fill="#94a3b8"
                )

    def _update_camera_preview(self) -> None:
        """تحديث صورة الكاميرا المصغرة في الشريط الجانبي."""
        with self.data_lock:
            frame = self.latest_frame

        if frame is not None and self.camera_ok:
            try:
                preview_w = 245
                h, w = frame.shape[:2]
                preview_h = int(h * (preview_w / w))

                resized = cv2.resize(frame, (preview_w, preview_h))
                rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                img_tk = ImageTk.PhotoImage(image=img)

                self.cam_label.img_tk = img_tk
                self.cam_label.configure(image=img_tk, text="")
            except Exception:
                pass
        else:
            if self.mouse_mode:
                self.cam_label.configure(text="وضع الماوس التجريبي نشط 🖱️", fg="#38bdf8")

    def on_close(self) -> None:
        """إغلاق التطبيق بأمان وتحرير الموارد والخيوط."""
        self.running = False
        time.sleep(0.06)
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.tracker.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = GazeVirtualKeyboardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
