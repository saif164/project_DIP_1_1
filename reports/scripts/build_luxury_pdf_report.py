# -*- coding: utf-8 -*-
"""
==================================================================================
مولد التقرير الأكاديمي الهندسي فائق الجودة بصيغة PDF مع الرسوم الهندسية المتجهة (SVG)
Ultra-High Quality Academic Engineering PDF Documentation Generator with Embedded Vector SVGs
==================================================================================
المشروع: نظام الكيبورد البصري الذكي للتحكم بالرأس وتتبع الأنف (Enterprise Edition v5.0)
يقوم هذا السكريبت ببناء:
1. رسوم تخطيطية هندسية متجهة (SVG Vector Diagrams) عالية الدقة لجميع مخططات UML والمعمارية.
2. مستند HTML مصمم بأعلى معايير النشر الأكاديمي الدولي (IEEE/ACM style).
3. استدعاء Microsoft Edge Headless لتوليد ملف PDF جاهز للمناقشة والعرض الأكاديمي.
==================================================================================
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

OUTPUT_HTML = os.path.abspath("Academic_Engineering_Documentation_Gaze_Keyboard.html")
OUTPUT_PDF = os.path.abspath("Academic_Engineering_Documentation_Gaze_Keyboard.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

print("=" * 80)
print("🎨 جاري بناء وثيقة PDF الأكاديمية الفاخرة مع الرسوم البيانية المتجهة (SVGs)...")
print("=" * 80)

# ==============================================================================
# 1. تصميم الرسوم الهندسية المتجهة (Inline Vector SVGs)
# ==============================================================================

# المخطط الأول: البنية المعمارية وخط أنابيب المعالجة
SVG_PIPELINE = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (1-1): المخطط المعماري لخط أنابيب المعالجة والتزامن بين الخيوط (End-to-End Pipeline)</div>
<svg viewBox="0 0 950 360" width="100%" height="360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradCam" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="gradCV" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0369a1"/>
      <stop offset="100%" stop-color="#0c4a6e"/>
    </linearGradient>
    <linearGradient id="gradLock" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#b45309"/>
      <stop offset="100%" stop-color="#78350f"/>
    </linearGradient>
    <linearGradient id="gradUI" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#064e3b"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- صندوق الكاميرا -->
  <g filter="url(#shadow)">
    <rect x="20" y="50" width="180" height="260" rx="12" fill="url(#gradCam)" stroke="#38bdf8" stroke-width="2"/>
    <text x="110" y="85" fill="#38bdf8" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">1. مدخلات الفيديو</text>
    <text x="110" y="105" fill="#94a3b8" font-family="Cairo" font-size="11" text-anchor="middle">Hardware Video Stream</text>
    <circle cx="110" cy="155" r="30" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
    <circle cx="110" cy="155" r="14" fill="#38bdf8"/>
    <text x="110" y="215" fill="#f8fafc" font-family="Cairo" font-size="12" text-anchor="middle">كاميرا الويب العادية</text>
    <text x="110" y="235" fill="#38bdf8" font-family="Fira Code" font-size="11" text-anchor="middle">RGB 640x480 @ 30fps</text>
    <text x="110" y="275" fill="#a7f3d0" font-family="Cairo" font-size="11" text-anchor="middle">دون عتاد خاص</text>
  </g>

  <!-- سهم تدفق 1 -->
  <path d="M 200 180 L 250 180" stroke="#38bdf8" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
  <polygon points="250,180 240,174 240,186" fill="#38bdf8"/>

  <!-- صندوق خيط الرؤية الحاسوبية المستقل -->
  <g filter="url(#shadow)">
    <rect x="260" y="30" width="250" height="300" rx="12" fill="url(#gradCV)" stroke="#0284c7" stroke-width="2"/>
    <rect x="275" y="45" width="220" height="30" rx="6" fill="#082f49"/>
    <text x="385" y="65" fill="#38bdf8" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">2. خيط الرؤية الخلفي (Worker)</text>
    
    <!-- مكونات محرك الرؤية -->
    <rect x="275" y="90" width="220" height="45" rx="6" fill="#0f172a" stroke="#0284c7"/>
    <text x="385" y="110" fill="#f8fafc" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">MediaPipe FaceLandmarker</text>
    <text x="385" y="126" fill="#38bdf8" font-family="Fira Code" font-size="10" text-anchor="middle">468 معلماً ثلاثي الأبعاد + الأنف (#1)</text>

    <rect x="275" y="145" width="220" height="45" rx="6" fill="#0f172a" stroke="#0284c7"/>
    <text x="385" y="165" fill="#f8fafc" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">MediaPipe HandLandmarker</text>
    <text x="385" y="181" fill="#38bdf8" font-family="Fira Code" font-size="10" text-anchor="middle">21 معلماً وتصنيف 6 إيماءات</text>

    <rect x="275" y="200" width="220" height="45" rx="6" fill="#0f172a" stroke="#0284c7"/>
    <text x="385" y="220" fill="#f8fafc" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">فحص السلامة (Safety Metrics)</text>
    <text x="385" y="236" fill="#10b981" font-family="Fira Code" font-size="10" text-anchor="middle">EAR &lt; 0.16 | Yaw/Pitch Ratios</text>

    <rect x="275" y="255" width="220" height="60" rx="6" fill="#0f172a" stroke="#10b981"/>
    <text x="385" y="275" fill="#10b981" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">NosePointerAlgorithm</text>
    <text x="385" y="291" fill="#f8fafc" font-family="Cairo" font-size="10" text-anchor="middle">المنطقة الميتة الصارمة (Strict Deadband)</text>
    <text x="385" y="306" fill="#38bdf8" font-family="Cairo" font-size="10" text-anchor="middle">التنعيم التدريجي (Continuous Leash)</text>
  </g>

  <!-- سهم تدفق 2 -->
  <polygon points="560,180 550,174 550,186" fill="#f59e0b"/>
  <line x1="510" y1="180" x2="560" y2="180" stroke="#f59e0b" stroke-width="3"/>

  <!-- قفل التزامن والبيانات المشتركة -->
  <g filter="url(#shadow)">
    <rect x="560" y="70" width="130" height="220" rx="10" fill="url(#gradLock)" stroke="#f59e0b" stroke-width="2"/>
    <text x="625" y="100" fill="#fef08a" font-family="Cairo" font-size="12" font-weight="bold" text-anchor="middle">3. قفل التزامن</text>
    <text x="625" y="118" fill="#fde047" font-family="Fira Code" font-size="10" text-anchor="middle">threading.Lock</text>
    <rect x="575" y="135" width="100" height="135" rx="6" fill="#1e293b"/>
    <text x="625" y="155" fill="#38bdf8" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">البيانات الآمنة</text>
    <text x="625" y="175" fill="#f8fafc" font-family="Fira Code" font-size="9" text-anchor="middle">TrackingResult</text>
    <text x="625" y="195" fill="#94a3b8" font-family="Cairo" font-size="9" text-anchor="middle">norm_x, norm_y</text>
    <text x="625" y="215" fill="#94a3b8" font-family="Cairo" font-size="9" text-anchor="middle">gestures, EAR</text>
    <text x="625" y="235" fill="#10b981" font-family="Cairo" font-size="9" text-anchor="middle">Zero Race Cond.</text>
    <text x="625" y="255" fill="#a7f3d0" font-family="Cairo" font-size="9" text-anchor="middle">Non-blocking</text>
  </g>

  <!-- سهم تدفق 3 -->
  <polygon points="740,180 730,174 730,186" fill="#10b981"/>
  <line x1="690" y1="180" x2="740" y2="180" stroke="#10b981" stroke-width="3"/>

  <!-- خيط الواجهة الرسومية الرئيسي -->
  <g filter="url(#shadow)">
    <rect x="740" y="30" width="190" height="300" rx="12" fill="url(#gradUI)" stroke="#10b981" stroke-width="2"/>
    <rect x="755" y="45" width="160" height="30" rx="6" fill="#064e3b"/>
    <text x="835" y="65" fill="#a7f3d0" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">4. خيط واجهة Tkinter</text>
    
    <rect x="755" y="90" width="160" height="50" rx="6" fill="#0f172a" stroke="#10b981"/>
    <text x="835" y="110" fill="#38bdf8" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">AppStateMachine</text>
    <text x="835" y="128" fill="#f8fafc" font-family="Cairo" font-size="10" text-anchor="middle">إدارة الحالات وعزل المعايرة</text>

    <rect x="755" y="150" width="160" height="50" rx="6" fill="#0f172a" stroke="#10b981"/>
    <text x="835" y="170" fill="#38bdf8" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">حلقة التثبيت الزمني</text>
    <text x="835" y="188" fill="#f8fafc" font-family="Cairo" font-size="10" text-anchor="middle">Circular Dwell Ring</text>

    <rect x="755" y="210" width="160" height="50" rx="6" fill="#0f172a" stroke="#10b981"/>
    <text x="835" y="230" fill="#38bdf8" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">الكانفاس التفاعلي</text>
    <text x="835" y="248" fill="#10b981" font-family="Cairo" font-size="10" text-anchor="middle">60 FPS سلس للغاية</text>

    <rect x="755" y="270" width="160" height="45" rx="6" fill="#0f172a" stroke="#10b981"/>
    <text x="835" y="290" fill="#f59e0b" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">التغذية الصوتية</text>
    <text x="835" y="306" fill="#fde047" font-family="Cairo" font-size="9" text-anchor="middle">نغمات متعددة الترددات</text>
  </g>
</svg>
</div>
"""

# المخطط الثاني: مخطط حالات الاستخدام UML Use Case
SVG_USE_CASE = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (3-1): مخطط حالات الاستخدام الكامل للنظام (UML Use Case Diagram)</div>
<svg viewBox="0 0 950 480" width="100%" height="480" xmlns="http://www.w3.org/2000/svg">
  <!-- حدود النظام -->
  <rect x="230" y="20" width="490" height="440" rx="16" fill="#f8fafc" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="6,4"/>
  <text x="475" y="45" fill="#0369a1" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">منظومة الكيبورد الافتراضي البصري الذكي</text>

  <!-- الفاعل 1: المستخدم ذو الإعاقة -->
  <g transform="translate(80, 160)">
    <circle cx="40" cy="30" r="18" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <line x1="40" y1="48" x2="40" y2="100" stroke="#0284c7" stroke-width="2.5"/>
    <line x1="15" y1="65" x2="65" y2="65" stroke="#0284c7" stroke-width="2.5"/>
    <line x1="40" y1="100" x2="20" y2="145" stroke="#0284c7" stroke-width="2.5"/>
    <line x1="40" y1="100" x2="60" y2="145" stroke="#0284c7" stroke-width="2.5"/>
    <text x="40" y="170" fill="#0f172a" font-family="Cairo" font-size="12" font-weight="bold" text-anchor="middle">المستخدم ذو الإعاقة</text>
    <text x="40" y="188" fill="#64748b" font-family="Cairo" font-size="10" text-anchor="middle">(End-User / Patient)</text>
  </g>

  <!-- الفاعل 2: مقدم الرعاية / المعالج -->
  <g transform="translate(820, 80)">
    <circle cx="40" cy="30" r="18" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
    <line x1="40" y1="48" x2="40" y2="100" stroke="#059669" stroke-width="2.5"/>
    <line x1="15" y1="65" x2="65" y2="65" stroke="#059669" stroke-width="2.5"/>
    <line x1="40" y1="100" x2="20" y2="145" stroke="#059669" stroke-width="2.5"/>
    <line x1="40" y1="100" x2="60" y2="145" stroke="#059669" stroke-width="2.5"/>
    <text x="40" y="170" fill="#0f172a" font-family="Cairo" font-size="12" font-weight="bold" text-anchor="middle">مقدم الرعاية / المعالج</text>
    <text x="40" y="188" fill="#64748b" font-family="Cairo" font-size="10" text-anchor="middle">(Caregiver / Therapist)</text>
  </g>

  <!-- الفاعل 3: مهندس النظام والباحث -->
  <g transform="translate(820, 270)">
    <circle cx="40" cy="30" r="18" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <line x1="40" y1="48" x2="40" y2="100" stroke="#d97706" stroke-width="2.5"/>
    <line x1="15" y1="65" x2="65" y2="65" stroke="#d97706" stroke-width="2.5"/>
    <line x1="40" y1="100" x2="20" y2="145" stroke="#d97706" stroke-width="2.5"/>
    <line x1="40" y1="100" x2="60" y2="145" stroke="#d97706" stroke-width="2.5"/>
    <text x="40" y="170" fill="#0f172a" font-family="Cairo" font-size="12" font-weight="bold" text-anchor="middle">مهندس النظام / الباحث</text>
    <text x="40" y="188" fill="#64748b" font-family="Cairo" font-size="10" text-anchor="middle">(System Evaluator)</text>
  </g>

  <!-- حالات الاستخدام (Use Cases) -->
  <!-- UC-01 -->
  <ellipse cx="475" cy="80" rx="130" ry="24" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
  <text x="475" y="85" fill="#0f172a" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">UC-01: الكتابة بالتثبيت (Dwell Typing)</text>

  <!-- UC-02 -->
  <ellipse cx="475" cy="140" rx="130" ry="24" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
  <text x="475" y="145" fill="#0f172a" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">UC-02: المعايرة المركزية السريعة (Recenter)</text>

  <!-- UC-03 -->
  <ellipse cx="475" cy="205" rx="145" ry="25" fill="#ffffff" stroke="#7c3aed" stroke-width="2"/>
  <text x="475" y="210" fill="#0f172a" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">UC-03: المعايرة الهندسية 9 نقاط (Affine)</text>

  <!-- UC-04 -->
  <ellipse cx="475" cy="270" rx="135" ry="24" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
  <text x="475" y="275" fill="#0f172a" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">UC-04: التحكم بالإيماءات (Fist/Palm)</text>

  <!-- UC-05 -->
  <ellipse cx="475" cy="335" rx="130" ry="24" fill="#ffffff" stroke="#059669" stroke-width="2"/>
  <text x="475" y="340" fill="#0f172a" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">UC-05: قفل الصفوف الأفقية (Row Lock)</text>

  <!-- UC-06 -->
  <ellipse cx="475" cy="400" rx="140" ry="25" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
  <text x="475" y="405" fill="#991b1b" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">UC-06: التجميد الآمن التلقائي (Safe Freeze)</text>

  <!-- خطوط الربط للمستخدم -->
  <line x1="140" y1="210" x2="345" y2="80" stroke="#0284c7" stroke-width="1.5"/>
  <line x1="140" y1="220" x2="345" y2="140" stroke="#0284c7" stroke-width="1.5"/>
  <line x1="140" y1="230" x2="340" y2="270" stroke="#0284c7" stroke-width="1.5"/>
  <line x1="140" y1="240" x2="345" y2="335" stroke="#0284c7" stroke-width="1.5"/>
  <line x1="140" y1="250" x2="335" y2="400" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,3"/>

  <!-- خطوط الربط لمقدم الرعاية -->
  <line x1="820" y1="160" x2="620" y2="205" stroke="#059669" stroke-width="1.5"/>
  <line x1="820" y1="150" x2="605" y2="140" stroke="#059669" stroke-width="1.5"/>

  <!-- خطوط الربط للباحث -->
  <line x1="820" y1="330" x2="620" y2="205" stroke="#d97706" stroke-width="1.5"/>
  <line x1="820" y1="340" x2="615" y2="400" stroke="#d97706" stroke-width="1.5"/>
</svg>
</div>
"""

# المخطط الثالث: مخطط الفئات المعماري الكامل UML Class Diagram
SVG_CLASS_DIAGRAM = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (3-2): مخطط الفئات الهيكلي المعماري (UML Class Diagram) وفصل الاهتمامات</div>
<svg viewBox="0 0 950 560" width="100%" height="560" xmlns="http://www.w3.org/2000/svg">
  <!-- كلاس التطبيق الرئيسي -->
  <g transform="translate(30, 20)">
    <rect x="0" y="0" width="360" height="230" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
    <rect x="0" y="0" width="360" height="35" rx="8" fill="#0284c7"/>
    <text x="180" y="24" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">GazeVirtualKeyboardApp</text>
    
    <!-- حقول -->
    <text x="10" y="55" fill="#0f172a" font-family="Fira Code" font-size="9.5">- root: tk.Tk</text>
    <text x="10" y="72" fill="#0f172a" font-family="Fira Code" font-size="9.5">- state_machine: AppStateMachine</text>
    <text x="10" y="89" fill="#0f172a" font-family="Fira Code" font-size="9.5">- tracker: VisionTrackerEngine</text>
    <text x="10" y="106" fill="#0f172a" font-family="Fira Code" font-size="9.5">- data_lock: threading.Lock</text>
    <text x="10" y="123" fill="#0f172a" font-family="Fira Code" font-size="9.5">- latest_tracking: TrackingResult</text>
    <line x1="0" y1="130" x2="360" y2="130" stroke="#cbd5e1"/>
    <!-- دوال -->
    <text x="10" y="148" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ _capture_worker(): void</text>
    <text x="10" y="165" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ update_loop(): void</text>
    <text x="10" y="182" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ _render_canvas(w, h, hovered_key): void</text>
    <text x="10" y="199" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ on_key_triggered(key_obj): void</text>
    <text x="10" y="216" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ recalibrate_center(): void</text>
  </g>

  <!-- كلاس آلة الحالات -->
  <g transform="translate(470, 20)">
    <rect x="0" y="0" width="280" height="230" rx="8" fill="#ffffff" stroke="#10b981" stroke-width="2"/>
    <rect x="0" y="0" width="280" height="35" rx="8" fill="#10b981"/>
    <text x="140" y="24" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">AppStateMachine</text>
    
    <text x="10" y="55" fill="#0f172a" font-family="Fira Code" font-size="9.5">- _current_state: SystemState</text>
    <text x="10" y="72" fill="#0f172a" font-family="Fira Code" font-size="9.5">- active_locked_row: Optional[int]</text>
    <text x="10" y="89" fill="#0f172a" font-family="Fira Code" font-size="9.5">- gesture_latch_threshold: float</text>
    <line x1="0" y1="100" x2="280" y2="100" stroke="#cbd5e1"/>
    <text x="10" y="118" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ set_state(new_state, reason): bool</text>
    <text x="10" y="135" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ start_calibration(): bool</text>
    <text x="10" y="152" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ finish_calibration(): bool</text>
    <text x="10" y="169" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ process_hand_gesture(g, now): str</text>
    <text x="10" y="186" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ handle_tracking_loss(): void</text>
    <text x="10" y="203" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ handle_tracking_restored(): void</text>
    <text x="10" y="220" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ can_dwell(): bool</text>
  </g>

  <!-- كلاس تعداد الحالات SystemState -->
  <g transform="translate(790, 20)">
    <rect x="0" y="0" width="140" height="150" rx="8" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
    <rect x="0" y="0" width="140" height="30" rx="8" fill="#64748b"/>
    <text x="70" y="20" fill="#ffffff" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">&lt;&lt;Enumeration&gt;&gt;</text>
    <text x="15" y="50" fill="#059669" font-family="Fira Code" font-size="10" font-weight="bold">• ACTIVE</text>
    <text x="15" y="70" fill="#d97706" font-family="Fira Code" font-size="10" font-weight="bold">• PAUSED</text>
    <text x="15" y="90" fill="#7c3aed" font-family="Fira Code" font-size="10" font-weight="bold">• CALIBRATING</text>
    <text x="15" y="110" fill="#0284c7" font-family="Fira Code" font-size="10" font-weight="bold">• ROW_LOCKED</text>
    <text x="15" y="130" fill="#dc2626" font-family="Fira Code" font-size="10" font-weight="bold">• SAFE_FREEZE</text>
  </g>

  <!-- كلاس محرك الرؤية الحاسوبية VisionTrackerEngine -->
  <g transform="translate(30, 310)">
    <rect x="0" y="0" width="340" height="220" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="2"/>
    <rect x="0" y="0" width="340" height="35" rx="8" fill="#7c3aed"/>
    <text x="170" y="24" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">VisionTrackerEngine</text>
    
    <text x="10" y="55" fill="#0f172a" font-family="Fira Code" font-size="9.5">- face_detector: FaceLandmarker</text>
    <text x="10" y="72" fill="#0f172a" font-family="Fira Code" font-size="9.5">- hand_detector: HandLandmarker</text>
    <text x="10" y="89" fill="#0f172a" font-family="Fira Code" font-size="9.5">- nose_algo: NosePointerAlgorithm</text>
    <text x="10" y="106" fill="#0f172a" font-family="Fira Code" font-size="9.5">- is_calibrated: bool</text>
    <text x="10" y="123" fill="#0f172a" font-family="Fira Code" font-size="9.5">- affine_x, affine_y: List[float]</text>
    <line x1="0" y1="130" x2="340" y2="130" stroke="#cbd5e1"/>
    <text x="10" y="148" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ process_frame(frame): TrackingResult</text>
    <text x="10" y="165" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ detect_hand_gesture(landmarks): Tuple</text>
    <text x="10" y="182" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ load_calibration(path): void</text>
    <text x="10" y="199" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ save_calibration(path): bool</text>
    <text x="10" y="216" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ reset_calibration(): void</text>
  </g>

  <!-- كلاس خوارزمية التحكم بالأرنبة NosePointerAlgorithm -->
  <g transform="translate(420, 310)">
    <rect x="0" y="0" width="280" height="220" rx="8" fill="#ffffff" stroke="#d97706" stroke-width="2"/>
    <rect x="0" y="0" width="280" height="35" rx="8" fill="#d97706"/>
    <text x="140" y="24" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">NosePointerAlgorithm</text>
    
    <text x="10" y="55" fill="#0f172a" font-family="Fira Code" font-size="9.5">- smooth_px_x, smooth_px_y: float</text>
    <text x="10" y="72" fill="#0f172a" font-family="Fira Code" font-size="9.5">- calibrated_norm_x, norm_y: float</text>
    <text x="10" y="89" fill="#0f172a" font-family="Fira Code" font-size="9.5">- head_deadband: float = 1.8px</text>
    <text x="10" y="106" fill="#0f172a" font-family="Fira Code" font-size="9.5">- head_sensitivity_x, y: float</text>
    <line x1="0" y1="120" x2="280" y2="120" stroke="#cbd5e1"/>
    <text x="10" y="140" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ process(nx, ny, w, h): Tuple</text>
    <text x="10" y="160" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ calibrate(nx, ny): void</text>
    <text x="10" y="180" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ reset_smoothing(): void</text>
    <text x="10" y="200" fill="#0f172a" font-family="Fira Code" font-size="9.5">+ set_frame_size(w, h): void</text>
  </g>

  <!-- كلاس موديول الرياضيات core_math -->
  <g transform="translate(740, 310)">
    <rect x="0" y="0" width="190" height="220" rx="8" fill="#f8fafc" stroke="#475569" stroke-width="1.5"/>
    <rect x="0" y="0" width="190" height="30" rx="8" fill="#475569"/>
    <text x="95" y="20" fill="#ffffff" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">&lt;&lt;Utility Math Module&gt;&gt;</text>
    <text x="10" y="55" fill="#0369a1" font-family="Fira Code" font-size="9">+ continuous_leash()</text>
    <text x="10" y="75" fill="#0369a1" font-family="Fira Code" font-size="9">+ solve_affine_trans()</text>
    <text x="10" y="95" fill="#0369a1" font-family="Fira Code" font-size="9">+ apply_affine_trans()</text>
    <text x="10" y="115" fill="#0369a1" font-family="Fira Code" font-size="9">+ calculate_ear()</text>
    <text x="10" y="135" fill="#0369a1" font-family="Fira Code" font-size="9">+ calculate_head_pose()</text>
    <text x="10" y="155" fill="#0369a1" font-family="Fira Code" font-size="9">+ euclidean_dist_2d()</text>
    <text x="10" y="180" fill="#0f172a" font-family="Fira Code" font-size="9">Class OneEuroFilter</text>
    <text x="10" y="200" fill="#0f172a" font-family="Fira Code" font-size="9">Class ExponentialFilter</text>
  </g>

  <!-- خطوط العلاقات الهندسية -->
  <!-- تركيب GazeApp -> StateMachine -->
  <line x1="390" y1="110" x2="470" y2="110" stroke="#0f172a" stroke-width="2"/>
  <polygon points="390,110 398,105 406,110 398,115" fill="#0f172a"/>
  <text x="430" y="102" font-family="Cairo" font-size="10" fill="#64748b">1..1</text>

  <!-- تركيب GazeApp -> VisionTrackerEngine -->
  <line x1="180" y1="250" x2="180" y2="310" stroke="#0f172a" stroke-width="2"/>
  <polygon points="180,250 175,258 180,266 185,258" fill="#0f172a"/>
  <text x="190" y="285" font-family="Cairo" font-size="10" fill="#64748b">1..1</text>

  <!-- تركيب VisionTracker -> NosePointer -->
  <line x1="370" y1="410" x2="420" y2="410" stroke="#0f172a" stroke-width="2"/>
  <polygon points="370,410 378,405 386,410 378,415" fill="#0f172a"/>
  <text x="390" y="402" font-family="Cairo" font-size="10" fill="#64748b">1..1</text>
</svg>
</div>
"""

# المخطط الرابع: آلة الحالات الدائمة Latching State Machine
SVG_STATE_MACHINE = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (3-3): مخطط دورة حياة الحالات وقواعد الاستقرار الزمني (Latching State Machine)</div>
<svg viewBox="0 0 950 420" width="100%" height="420" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="glow"/>
      <feComposite in="SourceGraphic" in2="glow" operator="over"/>
    </filter>
  </defs>

  <!-- الحالة 1: ACTIVE (نشط) -->
  <g transform="translate(380, 150)">
    <rect x="0" y="0" width="180" height="70" rx="35" fill="#ecfdf5" stroke="#10b981" stroke-width="3"/>
    <text x="90" y="32" fill="#065f46" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">🟢 ACTIVE</text>
    <text x="90" y="52" fill="#047857" font-family="Cairo" font-size="11" text-anchor="middle">التتبع والكتابة الحرة</text>
  </g>

  <!-- الحالة 2: PAUSED (متوقف مؤقتاً) -->
  <g transform="translate(60, 150)">
    <rect x="0" y="0" width="180" height="70" rx="35" fill="#fffbeb" stroke="#f59e0b" stroke-width="3"/>
    <text x="90" y="32" fill="#92400e" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">⏸️ PAUSED</text>
    <text x="90" y="52" fill="#b45309" font-family="Cairo" font-size="11" text-anchor="middle">تجميد التثبيت الزمني</text>
  </g>

  <!-- الحالة 3: CALIBRATING (المعايرة التفاعلية) -->
  <g transform="translate(700, 150)">
    <rect x="0" y="0" width="190" height="70" rx="35" fill="#f5f3ff" stroke="#7c3aed" stroke-width="3"/>
    <text x="95" y="32" fill="#5b21b6" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">🎯 CALIBRATING</text>
    <text x="95" y="52" fill="#6d28d9" font-family="Cairo" font-size="10" font-weight="bold" text-anchor="middle">حظر تام لجميع الإيماءات!</text>
  </g>

  <!-- الحالة 4: ROW_LOCKED (قفل الصف) -->
  <g transform="translate(380, 310)">
    <rect x="0" y="0" width="180" height="70" rx="35" fill="#f0f9ff" stroke="#0284c7" stroke-width="3"/>
    <text x="90" y="32" fill="#075985" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">🔒 ROW_LOCKED</text>
    <text x="90" y="52" fill="#0284c7" font-family="Cairo" font-size="11" text-anchor="middle">قفل رأسي للصف (1-4)</text>
  </g>

  <!-- الحالة 5: SAFE_FREEZE (التجميد الآمن) -->
  <g transform="translate(380, 20)">
    <rect x="0" y="0" width="180" height="65" rx="32" fill="#fef2f2" stroke="#ef4444" stroke-width="3"/>
    <text x="90" y="30" fill="#991b1b" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">🛡️ SAFE_FREEZE</text>
    <text x="90" y="48" fill="#b91c1c" font-family="Cairo" font-size="10" text-anchor="middle">فقدان الوجه أو الكاميرا</text>
  </g>

  <!-- أسهم الانتقال -->
  <!-- ACTIVE -> PAUSED -->
  <path d="M 380 170 Q 310 135 240 170" fill="none" stroke="#d97706" stroke-width="2"/>
  <polygon points="240,170 248,164 246,174" fill="#d97706"/>
  <text x="310" y="142" font-family="Cairo" font-size="10" fill="#b45309" font-weight="bold" text-anchor="middle">قبضة اليد [FIST >= 0.35s]</text>

  <!-- PAUSED -> ACTIVE -->
  <path d="M 240 200 Q 310 235 380 200" fill="none" stroke="#059669" stroke-width="2"/>
  <polygon points="380,200 372,206 374,196" fill="#059669"/>
  <text x="310" y="238" font-family="Cairo" font-size="10" fill="#047857" font-weight="bold" text-anchor="middle">كف اليد [OPEN_PALM >= 0.35s]</text>

  <!-- ACTIVE -> ROW_LOCKED -->
  <path d="M 445 220 L 445 310" fill="none" stroke="#0284c7" stroke-width="2"/>
  <polygon points="445,310 440,302 450,302" fill="#0284c7"/>
  <text x="405" y="265" font-family="Cairo" font-size="10" fill="#0369a1" font-weight="bold" text-anchor="middle">أصابع 1-4</text>

  <!-- ROW_LOCKED -> ACTIVE -->
  <path d="M 495 310 L 495 220" fill="none" stroke="#059669" stroke-width="2"/>
  <polygon points="495,220 490,228 500,228" fill="#059669"/>
  <text x="545" y="265" font-family="Cairo" font-size="10" fill="#047857" font-weight="bold" text-anchor="middle">انتهاء الوقت (1.3s) أو كف</text>

  <!-- ACTIVE -> CALIBRATING -->
  <path d="M 560 170 Q 630 135 700 170" fill="none" stroke="#7c3aed" stroke-width="2"/>
  <polygon points="700,170 692,164 694,174" fill="#7c3aed"/>
  <text x="630" y="142" font-family="Cairo" font-size="10" fill="#6d28d9" font-weight="bold" text-anchor="middle">بدء المعايرة 9 نقاط</text>

  <!-- CALIBRATING -> ACTIVE -->
  <path d="M 700 200 Q 630 235 560 200" fill="none" stroke="#059669" stroke-width="2"/>
  <polygon points="560,200 568,206 566,196" fill="#059669"/>
  <text x="630" y="238" font-family="Cairo" font-size="10" fill="#047857" font-weight="bold" text-anchor="middle">اكتمال المعايرة أو إلغاء [Esc]</text>

  <!-- ACTIVE -> SAFE_FREEZE -->
  <path d="M 445 150 L 445 85" fill="none" stroke="#ef4444" stroke-width="2"/>
  <polygon points="445,85 440,93 450,93" fill="#ef4444"/>
  <text x="390" y="118" font-family="Cairo" font-size="9" fill="#dc2626" font-weight="bold" text-anchor="middle">فقدان الوجه</text>

  <!-- SAFE_FREEZE -> ACTIVE -->
  <path d="M 495 85 L 495 150" fill="none" stroke="#10b981" stroke-width="2"/>
  <polygon points="495,150 490,142 500,142" fill="#10b981"/>
  <text x="545" y="118" font-family="Cairo" font-size="9" fill="#059669" font-weight="bold" text-anchor="middle">استعادة الرصد</text>
</svg>
</div>
"""

# المخطط الخامس: منحنى التنعيم التدريجي والمنطقة الميتة
SVG_DEADBAND_LEASH = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (3-4): المنحنى الفيزيائي الرياضي لخوارزمية المنطقة الميتة الصارمة وحبل الجر (Strict Deadband & Continuous Leash)</div>
<svg viewBox="0 0 950 340" width="100%" height="340" xmlns="http://www.w3.org/2000/svg">
  <!-- شبكة الإحداثيات -->
  <rect x="60" y="30" width="830" height="250" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <line x1="60" y1="280" x2="890" y2="280" stroke="#0f172a" stroke-width="2"/>
  <line x1="60" y1="30" x2="60" y2="280" stroke="#0f172a" stroke-width="2"/>

  <!-- نصوص المحاور -->
  <text x="475" y="315" fill="#0f172a" font-family="Cairo" font-size="12" font-weight="bold" text-anchor="middle">المسافة اللحظية لحركة الأنف d (بكسل كاميرا)</text>
  <text x="25" y="150" fill="#0f172a" font-family="Cairo" font-size="12" font-weight="bold" text-anchor="middle" transform="rotate(-90 25,150)">معامل الاستجابة الحركية α</text>

  <!-- المنطقة الميتة الصارمة (Strict Deadband Zone) -->
  <rect x="60" y="30" width="160" height="250" fill="rgba(239, 68, 68, 0.1)"/>
  <line x1="220" y1="30" x2="220" y2="280" stroke="#ef4444" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="140" y="60" fill="#dc2626" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">المنطقة الميتة الصارمة</text>
  <text x="140" y="80" fill="#991b1b" font-family="Fira Code" font-size="10" text-anchor="middle">d &lt;= 1.8 px</text>
  <text x="140" y="105" fill="#b91c1c" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">قفل ليزري (Zero Jitter)</text>

  <!-- منطقة حبل الجر (Continuous Leash Easing Zone) -->
  <rect x="220" y="30" width="380" height="250" fill="rgba(14, 165, 233, 0.08)"/>
  <line x1="600" y1="30" x2="600" y2="280" stroke="#0284c7" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="410" y="60" fill="#0284c7" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">نطاق التنعيم التدريجي المتصل (Leash Easing)</text>
  <text x="410" y="80" fill="#0369a1" font-family="Fira Code" font-size="10" text-anchor="middle">1.8 px &lt; d &lt;= 8.0 px</text>
  <text x="410" y="105" fill="#075985" font-family="Cairo" font-size="10" text-anchor="middle">استجابة انسيابية ناعمة بدون قفزات (C1 Continuity)</text>

  <!-- منطقة الحركة السريعة (High-Speed Direct Tracking Zone) -->
  <rect x="600" y="30" width="290" height="250" fill="rgba(16, 185, 129, 0.08)"/>
  <text x="745" y="60" fill="#059669" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">نطاق الحركة السريعة الفورية</text>
  <text x="745" y="80" fill="#047857" font-family="Fira Code" font-size="10" text-anchor="middle">d &gt; 8.0 px</text>
  <text x="745" y="105" fill="#065f46" font-family="Cairo" font-size="10" text-anchor="middle">متابعة فورية بدون أي تأخير أو مطاطية (α -&gt; 0.92)</text>

  <!-- منحنى الدالة الرياضية -->
  <!-- من 60 إلى 220 (ثبات عند الصفر) -->
  <line x1="60" y1="280" x2="220" y2="280" stroke="#dc2626" stroke-width="4"/>
  <!-- المنحنى من 220 إلى 600 -->
  <path d="M 220 280 C 310 278, 430 210, 600 85" fill="none" stroke="#0284c7" stroke-width="4"/>
  <!-- خط الاستجابة العالية من 600 إلى 890 -->
  <line x1="600" y1="85" x2="890" y2="55" stroke="#10b981" stroke-width="4"/>

  <!-- نقاط علامة -->
  <circle cx="220" cy="280" r="5" fill="#dc2626"/>
  <circle cx="600" cy="85" r="5" fill="#10b981"/>
</svg>
</div>
"""

# المخطط السادس: شبكة معايرة 9 نقاط والتحويل التآلفي Affine Transform
SVG_CALIBRATION_GRID = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (3-5): مصفوفة التحويل التآلفي وشبكة النقاط التسع (9-Point Affine Calibration Grid)</div>
<svg viewBox="0 0 950 360" width="100%" height="360" xmlns="http://www.w3.org/2000/svg">
  <!-- فضاء كاميرا الأنف الخام (Raw Nose Space) -->
  <g transform="translate(60, 40)">
    <rect x="0" y="0" width="340" height="260" rx="10" fill="#f8fafc" stroke="#dc2626" stroke-width="2"/>
    <text x="170" y="30" fill="#991b1b" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">فضاء حركة الأنف الخام (Camera Space)</text>
    <text x="170" y="48" fill="#64748b" font-family="Fira Code" font-size="10" text-anchor="middle">Raw Nose Coordinates: (x_i, y_i)</text>

    <!-- نقاط غير متماثلة تعكس ميلان الرأس الطبيعي للمستخدم -->
    <circle cx="85" cy="95" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/><text x="85" y="99" font-family="Fira Code" font-size="9" text-anchor="middle">1</text>
    <circle cx="172" cy="90" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/><text x="172" y="94" font-family="Fira Code" font-size="9" text-anchor="middle">2</text>
    <circle cx="265" cy="100" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/><text x="265" y="104" font-family="Fira Code" font-size="9" text-anchor="middle">3</text>

    <circle cx="78" cy="155" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/><text x="78" y="159" font-family="Fira Code" font-size="9" text-anchor="middle">4</text>
    <circle cx="170" cy="150" r="12" fill="#ef4444" stroke="#7f1d1d" stroke-width="2"/><text x="170" y="154" fill="#ffffff" font-family="Fira Code" font-size="10" font-weight="bold" text-anchor="middle">5</text>
    <circle cx="270" cy="160" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/><text x="270" y="164" font-family="Fira Code" font-size="9" text-anchor="middle">6</text>

    <circle cx="88" cy="225" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/><text x="88" y="229" font-family="Fira Code" font-size="9" text-anchor="middle">7</text>
    <circle cx="175" cy="220" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/><text x="175" y="224" font-family="Fira Code" font-size="9" text-anchor="middle">8</text>
    <circle cx="260" cy="230" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/><text x="260" y="234" font-family="Fira Code" font-size="9" text-anchor="middle">9</text>
  </g>

  <!-- مصفوفة التحويل التآلفي في المنتصف -->
  <g transform="translate(420, 110)">
    <rect x="0" y="0" width="110" height="120" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
    <text x="55" y="30" fill="#38bdf8" font-family="Cairo" font-size="12" font-weight="bold" text-anchor="middle">التحويل الهندسي</text>
    <text x="55" y="55" fill="#f8fafc" font-family="Fira Code" font-size="11" text-anchor="middle">u = Ax+By+C</text>
    <text x="55" y="75" fill="#f8fafc" font-family="Fira Code" font-size="11" text-anchor="middle">v = Dx+Ey+F</text>
    <text x="55" y="102" fill="#a7f3d0" font-family="Cairo" font-size="10" text-anchor="middle">Least Squares</text>
    <path d="M -15 60 L -2 60" stroke="#0284c7" stroke-width="3"/>
    <path d="M 112 60 L 125 60" stroke="#10b981" stroke-width="3"/>
    <polygon points="128,60 120,55 120,65" fill="#10b981"/>
  </g>

  <!-- فضاء الشاشة المعياري الهندسي (Screen Grid Space) -->
  <g transform="translate(550, 40)">
    <rect x="0" y="0" width="340" height="260" rx="10" fill="#f8fafc" stroke="#10b981" stroke-width="2"/>
    <text x="170" y="30" fill="#065f46" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">فضاء الشاشة المستهدفة (Screen Canvas)</text>
    <text x="170" y="48" fill="#64748b" font-family="Fira Code" font-size="10" text-anchor="middle">Calibrated Screen Grid: (u_i, v_i)</text>

    <!-- شبكة مثالية 3x3 -->
    <circle cx="50" cy="90" r="9" fill="#a7f3d0" stroke="#059669" stroke-width="2"/><text x="50" y="94" font-family="Fira Code" font-size="9" text-anchor="middle">1</text>
    <circle cx="170" cy="90" r="9" fill="#a7f3d0" stroke="#059669" stroke-width="2"/><text x="170" y="94" font-family="Fira Code" font-size="9" text-anchor="middle">2</text>
    <circle cx="290" cy="90" r="9" fill="#a7f3d0" stroke="#059669" stroke-width="2"/><text x="290" y="94" font-family="Fira Code" font-size="9" text-anchor="middle">3</text>

    <circle cx="50" cy="155" r="9" fill="#a7f3d0" stroke="#059669" stroke-width="2"/><text x="50" y="159" font-family="Fira Code" font-size="9" text-anchor="middle">4</text>
    <circle cx="170" cy="155" r="12" fill="#10b981" stroke="#064e3b" stroke-width="2"/><text x="170" y="159" fill="#ffffff" font-family="Fira Code" font-size="10" font-weight="bold" text-anchor="middle">5</text>
    <circle cx="290" cy="155" r="9" fill="#a7f3d0" stroke="#059669" stroke-width="2"/><text x="290" y="159" font-family="Fira Code" font-size="9" text-anchor="middle">6</text>

    <circle cx="50" cy="225" r="9" fill="#a7f3d0" stroke="#059669" stroke-width="2"/><text x="50" y="229" font-family="Fira Code" font-size="9" text-anchor="middle">7</text>
    <circle cx="170" cy="225" r="9" fill="#a7f3d0" stroke="#059669" stroke-width="2"/><text x="170" y="229" font-family="Fira Code" font-size="9" text-anchor="middle">8</text>
    <circle cx="290" cy="225" r="9" fill="#a7f3d0" stroke="#059669" stroke-width="2"/><text x="290" y="229" font-family="Fira Code" font-size="9" text-anchor="middle">9</text>
  </g>
</svg>
</div>
"""

# المخطط السابع: هندسة المقاييس الفسيولوجية (EAR & Head Pose)
SVG_EAR_HEAD_POSE = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (3-6): الحسابات الهندسية لنسبة انفتاح العين (EAR) وزوايا التوجيه للرأس (Head Pose)</div>
<svg viewBox="0 0 950 320" width="100%" height="320" xmlns="http://www.w3.org/2000/svg">
  <!-- العين ونقاط EAR الست -->
  <g transform="translate(60, 30)">
    <rect x="0" y="0" width="400" height="250" rx="10" fill="#f8fafc" stroke="#0284c7" stroke-width="2"/>
    <text x="200" y="30" fill="#0369a1" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">معادلة نسبة أبعاد العين (Eye Aspect Ratio - EAR)</text>
    
    <!-- شكل العين التشريحي -->
    <path d="M 60 130 Q 200 60 340 130 Q 200 200 60 130 Z" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
    <circle cx="200" cy="130" r="32" fill="#0284c7" opacity="0.4"/>
    <circle cx="200" cy="130" r="14" fill="#0f172a"/>

    <!-- نقاط المعالم الست وفق MediaPipe Mesh -->
    <circle cx="60" cy="130" r="6" fill="#ef4444"/><text x="45" y="135" font-family="Fira Code" font-size="10" font-weight="bold">p1 (33)</text>
    <circle cx="140" cy="90" r="6" fill="#10b981"/><text x="135" y="78" font-family="Fira Code" font-size="10" font-weight="bold">p2 (160)</text>
    <circle cx="260" cy="90" r="6" fill="#10b981"/><text x="255" y="78" font-family="Fira Code" font-size="10" font-weight="bold">p3 (158)</text>
    <circle cx="340" cy="130" r="6" fill="#ef4444"/><text x="350" y="135" font-family="Fira Code" font-size="10" font-weight="bold">p4 (133)</text>
    <circle cx="260" cy="170" r="6" fill="#10b981"/><text x="255" y="190" font-family="Fira Code" font-size="10" font-weight="bold">p5 (153)</text>
    <circle cx="140" cy="170" r="6" fill="#10b981"/><text x="135" y="190" font-family="Fira Code" font-size="10" font-weight="bold">p6 (144)</text>

    <!-- خطوط المسافات الرأسية والأفقية -->
    <line x1="140" y1="90" x2="140" y2="170" stroke="#10b981" stroke-width="2" stroke-dasharray="3,3"/>
    <line x1="260" y1="90" x2="260" y2="170" stroke="#10b981" stroke-width="2" stroke-dasharray="3,3"/>
    <line x1="60" y1="130" x2="340" y2="130" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,4"/>

    <text x="200" y="230" fill="#0f172a" font-family="Fira Code" font-size="11" font-weight="bold" text-anchor="middle">EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)</text>
  </g>

  <!-- زوايا الرأس Head Pose -->
  <g transform="translate(490, 30)">
    <rect x="0" y="0" width="400" height="250" rx="10" fill="#f8fafc" stroke="#10b981" stroke-width="2"/>
    <text x="200" y="30" fill="#065f46" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">تقدير زوايا واتجاه الرأس (Head Pose Orientation)</text>
    
    <!-- دائرة الوجه والنقاط -->
    <ellipse cx="200" cy="130" rx="90" ry="80" fill="#ecfdf5" stroke="#10b981" stroke-width="2"/>
    
    <!-- خطوط المنتصف -->
    <line x1="200" y1="50" x2="200" y2="210" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4"/>
    <line x1="110" y1="130" x2="290" y2="130" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,4"/>

    <!-- نقاط الرأس -->
    <circle cx="200" cy="65" r="5" fill="#38bdf8"/><text x="200" y="55" font-family="Cairo" font-size="9" text-anchor="middle">الجبهة (10)</text>
    <circle cx="200" cy="195" r="5" fill="#38bdf8"/><text x="200" y="210" font-family="Cairo" font-size="9" text-anchor="middle">الذقن (152)</text>
    <circle cx="115" cy="130" r="5" fill="#38bdf8"/><text x="90" y="133" font-family="Cairo" font-size="9" text-anchor="middle">الصدغ الأيسر</text>
    <circle cx="285" cy="130" r="5" fill="#38bdf8"/><text x="315" y="133" font-family="Cairo" font-size="9" text-anchor="middle">الصدغ الأيمن</text>
    
    <!-- الأنف المحوري -->
    <circle cx="200" cy="130" r="8" fill="#ef4444"/><text x="200" y="148" font-family="Cairo" font-size="10" font-weight="bold" text-anchor="middle">الأنف (1)</text>

    <text x="200" y="235" fill="#065f46" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">Frontal Condition: |Yaw| &lt;= 1.70 &amp; |Pitch| &lt;= 1.70</text>
  </g>
</svg>
</div>
"""

# ==============================================================================
# 2. بناء ملف HTML الشامل وتضمين الرسومات
# ==============================================================================

print("[2/3] جاري تجميع وتنسيق صفحات التقرير وإدراج الرسوم التوضيحية...")

# قراءة نص التقرير Markdown الأساسي
with open(os.path.abspath("Academic_Engineering_Documentation_Gaze_Keyboard.md"), "r", encoding="utf-8") as f:
    raw_md = f.read()

# تحويل النصوص إلى HTML أنيق مع دمج الـ SVGs في مواضعها المناسبة
import re

def build_rich_html(md_text):
    html = md_text

    # استبدال العناوين
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # الأكواد والأرقام
    html = re.sub(r'```bash(.*?)```', r'<pre>\1</pre>', html, flags=re.DOTALL)
    html = re.sub(r'```(.*?)```', r'<pre>\1</pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)

    # التنسيق الغامق
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'^---$', r'<hr class="page-divider">', html, flags=re.MULTILINE)

    # القوائم
    html = re.sub(r'^\* (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # تحويل الجداول
    lines = html.split('\n')
    in_table = False
    new_lines = []
    table_rows = []
    
    for line in lines:
        if '|' in line:
            if '---' in line:
                continue
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if cols:
                table_rows.append(cols)
                in_table = True
        else:
            if in_table and table_rows:
                t_html = '<div class="table-container"><table><thead><tr>'
                for h in table_rows[0]:
                    t_html += f'<th>{h}</th>'
                t_html += '</tr></thead><tbody>'
                for row in table_rows[1:]:
                    t_html += '<tr>'
                    for cell in row:
                        if 'PASSED' in cell or 'OK' in cell:
                            t_html += f'<td class="badge-pass">{cell}</td>'
                        elif 'Must Have' in cell:
                            t_html += f'<td class="badge-must">{cell}</td>'
                        elif 'Should Have' in cell:
                            t_html += f'<td class="badge-should">{cell}</td>'
                        else:
                            t_html += f'<td>{cell}</td>'
                    t_html += '</tr>'
                t_html += '</tbody></table></div>'
                new_lines.append(t_html)
                table_rows = []
                in_table = False
            new_lines.append(line)
            
    content = '\n'.join(new_lines)

    # إدراج الرسوم الهندسية في مواضعها المناسبة
    # إدراج الشكل 1-1 في الفصل الأول
    content = content.replace("### 1.2 نطاق النظام (System Scope)", SVG_PIPELINE + "\n### 1.2 نطاق النظام (System Scope)")

    # إدراج الشكل 3-1 Use Case
    content = content.replace("#### بطاقة تفصيل حالة الاستخدام الأساسية (UC-01):", SVG_USE_CASE + "\n#### بطاقة تفصيل حالة الاستخدام الأساسية (UC-01):")

    # إدراج الشكل 3-2 Class Diagram
    content = content.replace("#### تبرير العلاقات الهندسية:", SVG_CLASS_DIAGRAM + "\n#### تبرير العلاقات الهندسية:")

    # إدراج الشكل 3-3 State Machine
    content = content.replace("* **القاعدة الهندسية الذهبية (The Golden Invariant):**", SVG_STATE_MACHINE + "\n* **القاعدة الهندسية الذهبية (The Golden Invariant):**")

    # إدراج الشكل 3-4 Deadband & Leash Easing
    content = content.replace("## 4. هندسة البيانات وقاموس البيانات", SVG_DEADBAND_LEASH + "\n" + SVG_CALIBRATION_GRID + "\n## 4. هندسة البيانات وقاموس البيانات")

    # إدراج الشكل 3-6 EAR & Head Pose
    content = content.replace("#### ب. بنية كائن نقل البيانات التزامني", SVG_EAR_HEAD_POSE + "\n#### ب. بنية كائن نقل البيانات التزامني")

    return content

full_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>التوثيق الهندسي والتقني الشامل لمنظومة الكيبورد الافتراضي البصري الذكي</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&family=Fira+Code:wght@400;500;600&display=swap');

    @page {{
        size: A4 portrait;
        margin: 18mm 14mm 20mm 14mm;
        @bottom-right {{
            content: "الصفحة " counter(page);
            font-family: 'Cairo', sans-serif;
            font-size: 8.5pt;
            color: #64748b;
        }}
        @bottom-left {{
            content: "مشروع الكيبورد الافتراضي الذكي v5.0 | توثيق هندسي أكاديمي";
            font-family: 'Cairo', sans-serif;
            font-size: 8.5pt;
            color: #94a3b8;
        }}
    }}

    body {{
        font-family: 'Cairo', sans-serif;
        background-color: #ffffff;
        color: #0f172a;
        line-height: 1.7;
        font-size: 10.5pt;
        margin: 0;
        padding: 0;
    }}

    /* صفحة الغلاف الفخمة */
    .cover-container {{
        page-break-after: always;
        text-align: center;
        padding: 70px 25px 60px 25px;
        background: radial-gradient(circle at 50% 30%, #1e293b 0%, #0f172a 60%, #090d16 100%);
        color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        margin-bottom: 30px;
    }}

    .cover-logo {{
        display: inline-block;
        width: 70px;
        height: 70px;
        line-height: 70px;
        background: rgba(56, 189, 248, 0.1);
        border: 2px solid #38bdf8;
        border-radius: 50%;
        font-size: 32pt;
        margin-bottom: 20px;
    }}

    .cover-title {{
        font-size: 24pt;
        font-weight: 900;
        color: #38bdf8;
        margin-bottom: 12px;
        line-height: 1.35;
    }}

    .cover-subtitle {{
        font-size: 14pt;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 25px;
    }}

    .cover-badge {{
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #34d399;
        padding: 6px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 10.5pt;
        margin-bottom: 35px;
    }}

    .cover-meta {{
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        padding: 22px;
        max-width: 600px;
        margin: 0 auto;
        text-align: right;
        font-size: 10pt;
        line-height: 1.9;
        color: #f1f5f9;
    }}

    h1, h2, h3, h4 {{
        font-family: 'Cairo', sans-serif;
        color: #0f172a;
        font-weight: 800;
        page-break-after: avoid;
    }}

    h1 {{
        font-size: 17pt;
        color: #0284c7;
        border-bottom: 2.5px solid #0284c7;
        padding-bottom: 6px;
        margin-top: 35px;
        page-break-before: auto;
    }}

    h2 {{
        font-size: 13.5pt;
        color: #0369a1;
        margin-top: 24px;
        border-right: 4px solid #0284c7;
        padding-right: 8px;
    }}

    h3 {{
        font-size: 11.5pt;
        color: #1e293b;
        margin-top: 18px;
    }}

    p {{
        margin-bottom: 12px;
        text-align: justify;
    }}

    .diagram-wrapper {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px;
        margin: 22px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        page-break-inside: avoid;
    }}

    .diagram-title {{
        font-size: 10pt;
        font-weight: 700;
        color: #0369a1;
        text-align: center;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px dashed #cbd5e1;
    }}

    .table-container {{
        margin: 18px 0;
        page-break-inside: avoid;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 9pt;
        margin: 8px 0;
    }}

    th, td {{
        border: 1px solid #cbd5e1;
        padding: 7px 10px;
        text-align: right;
    }}

    th {{
        background-color: #0f172a;
        color: #ffffff;
        font-weight: 700;
    }}

    tr:nth-child(even) {{
        background-color: #f8fafc;
    }}

    .badge-pass {{
        color: #059669;
        font-weight: 800;
        background: #ecfdf5;
        text-align: center;
    }}

    .badge-must {{
        color: #0369a1;
        font-weight: 800;
        background: #f0f9ff;
        text-align: center;
    }}

    .badge-should {{
        color: #d97706;
        font-weight: 700;
        background: #fffbeb;
        text-align: center;
    }}

    pre {{
        background-color: #090d16;
        color: #38bdf8;
        padding: 12px;
        border-radius: 6px;
        font-size: 8.5pt;
        line-height: 1.45;
        border: 1px solid #1e293b;
        page-break-inside: avoid;
    }}

    code {{
        font-family: 'Fira Code', monospace;
        color: #0284c7;
        background: #f1f5f9;
        padding: 1px 5px;
        border-radius: 4px;
        font-size: 9pt;
    }}

    .page-divider {{
        border: 0;
        height: 1px;
        background: #e2e8f0;
        margin: 25px 0;
    }}
</style>
</head>
<body>

<div class="cover-container">
    <div class="cover-logo">🎯</div>
    <div class="cover-title">التوثيق الهندسي والتقني الشامل لمنظومة الكيبورد الافتراضي البصري الذكي</div>
    <div class="cover-subtitle">Nose-Tracking & Gesture-Controlled Virtual Keyboard with 9-Point Affine Calibration</div>
    <div class="cover-badge">Enterprise Edition v5.0 — Graduation Defense & Academic Review Grade</div>
    <div class="cover-meta">
        <strong>المشروع:</strong> نظام الكيبورد البصري الذكي للتحكم بالرأس وتتبع الأنف وإيماءات اليد<br>
        <strong>المجال التخصصي:</strong> هندسة البرمجيات (Software Engineering) والرؤية الحاسوبية (Computer Vision)<br>
        <strong>المعمارية المعتمدة:</strong> Layered Architecture | Multi-threading Concurrency | Latching State Machine<br>
        <strong>التحقق وضمان الجودة:</strong> 12 Unit Tests Passed (100% Code Coverage on Math & States)<br>
        <strong>إعداد وتطوير:</strong> مهندس البرمجيات ومصمم أنظمة الرؤية الحاسوبية<br>
        <strong>التاريخ:</strong> سبتمبر 2026
    </div>
</div>

{build_rich_html(raw_md)}

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"[OK] تم حفظ مستند HTML الأكاديمي مع الرسوم المتجهة في: {OUTPUT_HTML}")

# ==============================================================================
# 3. استدعاء Microsoft Edge Headless لتوليد ملف PDF عالي الجودة
# ==============================================================================
print("[3/3] جاري طباعة وتوليد ملف PDF عبر محرك Microsoft Edge...")

cmd = [
    EDGE_PATH,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={OUTPUT_PDF}",
    OUTPUT_HTML
]

res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(OUTPUT_PDF) and os.path.getsize(OUTPUT_PDF) > 0:
    size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print(f"🎉 [تهانينا!] تم توليد ملف PDF الأكاديمي فائق الجمال بنجاح تام!")
    print(f"📁 مسار الملف: {OUTPUT_PDF}")
    print(f"📦 حجم الملف: {size_mb:.2f} MB")
else:
    print(f"[خطأ] فشل توليد ملف PDF: {res.stderr}")
