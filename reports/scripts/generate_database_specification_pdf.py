# -*- coding: utf-8 -*-
"""
==================================================================================
مولد وثيقة وتقرير المخططات الهندسية لقاعدة البيانات بصيغة PDF فائقة الجمال
Comprehensive Database Architecture, ERD & Data Engineering PDF Report Generator
==================================================================================
المشروع: نظام الكيبورد البصري الذكي للتحكم بالرأس وتتبع الأنف (Enterprise Edition v5.0)
==================================================================================
"""

import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

OUTPUT_HTML = os.path.abspath("Database_Architecture_And_Engineering_Specification.html")
OUTPUT_PDF = os.path.abspath("Database_Architecture_And_Engineering_Specification.pdf")
OUTPUT_MD = os.path.abspath("Database_Architecture_And_Engineering_Specification.md")

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

print("=" * 80)
print("🎨 جاري بناء وثيقة ومخططات قاعدة البيانات الأكاديمية الفاخرة (PDF + HTML + MD)...")
print("=" * 80)

# ==============================================================================
# 1. تصميم الرسوم البيانية المتجهة المضمنة عالية الدقة (Inline Vector SVGs)
# ==============================================================================

# المخطط الأول: ERD مخطط الكيانات والعلاقات
SVG_ERD = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (1-1): المخطط الهيكلي للكيانات والعلاقات (Entity-Relationship Diagram - ERD)</div>
<svg viewBox="0 0 1000 680" width="100%" height="680" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradUser" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e3a8a"/><stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="gradCalib" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#065f46"/><stop offset="100%" stop-color="#022c22"/>
    </linearGradient>
    <linearGradient id="gradSession" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#831843"/><stop offset="100%" stop-color="#4c0519"/>
    </linearGradient>
    <linearGradient id="gradErgo" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#92400e"/><stop offset="100%" stop-color="#451a03"/>
    </linearGradient>
    <linearGradient id="gradLayout" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4c1d95"/><stop offset="100%" stop-color="#2e1065"/>
    </linearGradient>
    <linearGradient id="gradPoints" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#115e59"/><stop offset="100%" stop-color="#042f2e"/>
    </linearGradient>
    <filter id="shadowBox" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="3" dy="4" stdDeviation="3" flood-color="#000000" flood-opacity="0.3"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="oneMany" viewBox="0 0 12 12" refX="6" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <circle cx="6" cy="6" r="3" fill="#38bdf8"/>
    </marker>
  </defs>

  <!-- خطوط الربط بين الكيانات -->
  <!-- Users to CalibrationProfiles -->
  <path d="M 320 120 L 460 120" stroke="#38bdf8" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="390" y="110" fill="#38bdf8" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">1 : N (owns)</text>

  <!-- Users to UserSettings -->
  <path d="M 210 230 L 210 320" stroke="#38bdf8" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="255" y="275" fill="#38bdf8" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">1 : 1 (configures)</text>

  <!-- Users to ErgonomicLogs -->
  <path d="M 120 230 L 120 480" stroke="#38bdf8" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="160" y="445" fill="#f59e0b" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">1 : N (logs)</text>

  <!-- Users to TypingSessions -->
  <path d="M 320 180 L 460 380" stroke="#38bdf8" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="360" y="290" fill="#f43f5e" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">1 : N (performs)</text>

  <!-- CalibrationProfiles to CalibrationPoints -->
  <path d="M 680 120 L 760 120" stroke="#34d399" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="720" y="110" fill="#34d399" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">1 : 9 (points)</text>

  <!-- KeyboardLayouts to TypingSessions -->
  <path d="M 760 480 L 680 430" stroke="#a78bfa" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="735" y="440" fill="#a78bfa" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">1 : N (uses)</text>

  <!-- TypingSessions to SessionMetrics -->
  <path d="M 570 510 L 570 560" stroke="#f43f5e" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>
  <text x="615" y="540" fill="#f43f5e" font-family="Cairo" font-size="11" font-weight="bold" text-anchor="middle">1 : 1 (metrics)</text>

  <!-- 1. كيان المستخدمين USERS -->
  <g filter="url(#shadowBox)">
    <rect x="100" y="40" width="220" height="190" rx="10" fill="url(#gradUser)" stroke="#38bdf8" stroke-width="2"/>
    <rect x="100" y="40" width="220" height="35" rx="10" fill="#1e40af"/>
    <text x="210" y="64" fill="#ffffff" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">USERS (المستخدمين)</text>
    <text x="115" y="100" fill="#fbbf24" font-family="Consolas" font-size="12" font-weight="bold">🔑 PK  user_id (INT)</text>
    <text x="115" y="125" fill="#f8fafc" font-family="Consolas" font-size="12">• full_name (VARCHAR)</text>
    <text x="115" y="150" fill="#f8fafc" font-family="Consolas" font-size="12">• username (VARCHAR)</text>
    <text x="115" y="175" fill="#94a3b8" font-family="Consolas" font-size="12">• disability_type (VARCHAR)</text>
    <text x="115" y="200" fill="#94a3b8" font-family="Consolas" font-size="12">• created_at (TIMESTAMP)</text>
  </g>

  <!-- 2. كيان المعايرة CALIBRATION_PROFILES -->
  <g filter="url(#shadowBox)">
    <rect x="460" y="40" width="220" height="210" rx="10" fill="url(#gradCalib)" stroke="#34d399" stroke-width="2"/>
    <rect x="460" y="40" width="220" height="35" rx="10" fill="#047857"/>
    <text x="570" y="64" fill="#ffffff" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">CALIBRATION_PROFILES</text>
    <text x="475" y="100" fill="#fbbf24" font-family="Consolas" font-size="12" font-weight="bold">🔑 PK  profile_id (INT)</text>
    <text x="475" y="122" fill="#38bdf8" font-family="Consolas" font-size="12" font-weight="bold">🔗 FK  user_id (INT)</text>
    <text x="475" y="144" fill="#f8fafc" font-family="Consolas" font-size="12">• deadband_px (REAL)</text>
    <text x="475" y="166" fill="#f8fafc" font-family="Consolas" font-size="12">• sens_x, sens_y (REAL)</text>
    <text x="475" y="188" fill="#a7f3d0" font-family="Consolas" font-size="12">• affine_matrix_x (JSON)</text>
    <text x="475" y="210" fill="#a7f3d0" font-family="Consolas" font-size="12">• affine_matrix_y (JSON)</text>
    <text x="475" y="232" fill="#94a3b8" font-family="Consolas" font-size="12">• is_active (BOOL)</text>
  </g>

  <!-- 3. كيان نقاط المعايرة التسع CALIBRATION_POINTS -->
  <g filter="url(#shadowBox)">
    <rect x="760" y="40" width="210" height="190" rx="10" fill="url(#gradPoints)" stroke="#2dd4bf" stroke-width="2"/>
    <rect x="760" y="40" width="210" height="35" rx="10" fill="#0f766e"/>
    <text x="865" y="64" fill="#ffffff" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">CALIBRATION_POINTS</text>
    <text x="775" y="100" fill="#fbbf24" font-family="Consolas" font-size="12" font-weight="bold">🔑 PK  point_id (INT)</text>
    <text x="775" y="125" fill="#38bdf8" font-family="Consolas" font-size="12" font-weight="bold">🔗 FK  profile_id (INT)</text>
    <text x="775" y="150" fill="#f8fafc" font-family="Consolas" font-size="12">• point_index (1..9)</text>
    <text x="775" y="175" fill="#f8fafc" font-family="Consolas" font-size="12">• target_x, target_y</text>
    <text x="775" y="200" fill="#a7f3d0" font-family="Consolas" font-size="12">• residual_error (REAL)</text>
  </g>

  <!-- 4. كيان إعدادات المستخدم USER_SETTINGS -->
  <g filter="url(#shadowBox)">
    <rect x="100" y="320" width="220" height="140" rx="10" fill="url(#gradUser)" stroke="#60a5fa" stroke-width="2"/>
    <rect x="100" y="320" width="220" height="30" rx="10" fill="#2563eb"/>
    <text x="210" y="342" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">USER_SETTINGS (الإعدادات)</text>
    <text x="115" y="375" fill="#fbbf24" font-family="Consolas" font-size="12" font-weight="bold">🔑 PK  setting_id (INT)</text>
    <text x="115" y="398" fill="#38bdf8" font-family="Consolas" font-size="12" font-weight="bold">🔗 FK  user_id (INT)</text>
    <text x="115" y="420" fill="#f8fafc" font-family="Consolas" font-size="12">• ear_threshold (REAL)</text>
    <text x="115" y="442" fill="#f8fafc" font-family="Consolas" font-size="12">• dwell_time_sec (REAL)</text>
  </g>

  <!-- 5. كيان سجلات الإجهاد والصحة ERGONOMIC_LOGS -->
  <g filter="url(#shadowBox)">
    <rect x="60" y="480" width="240" height="160" rx="10" fill="url(#gradErgo)" stroke="#f59e0b" stroke-width="2"/>
    <rect x="60" y="480" width="240" height="30" rx="10" fill="#b45309"/>
    <text x="180" y="502" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">ERGONOMIC_LOGS (الصحة)</text>
    <text x="75" y="535" fill="#fbbf24" font-family="Consolas" font-size="12" font-weight="bold">🔑 PK  log_id (INT)</text>
    <text x="75" y="558" fill="#38bdf8" font-family="Consolas" font-size="12" font-weight="bold">🔗 FK  user_id (INT)</text>
    <text x="75" y="580" fill="#f8fafc" font-family="Consolas" font-size="12">• avg_ear_value (REAL)</text>
    <text x="75" y="602" fill="#fde68a" font-family="Consolas" font-size="12">• head_pitch, head_yaw</text>
    <text x="75" y="624" fill="#ef4444" font-family="Consolas" font-size="12">• alert_type (VARCHAR)</text>
  </g>

  <!-- 6. كيان جلسات الكتابة TYPING_SESSIONS -->
  <g filter="url(#shadowBox)">
    <rect x="460" y="330" width="220" height="180" rx="10" fill="url(#gradSession)" stroke="#f43f5e" stroke-width="2"/>
    <rect x="460" y="330" width="220" height="35" rx="10" fill="#be123c"/>
    <text x="570" y="354" fill="#ffffff" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">TYPING_SESSIONS (الجلسات)</text>
    <text x="475" y="390" fill="#fbbf24" font-family="Consolas" font-size="12" font-weight="bold">🔑 PK  session_id (INT)</text>
    <text x="475" y="412" fill="#38bdf8" font-family="Consolas" font-size="12" font-weight="bold">🔗 FK  user_id (INT)</text>
    <text x="475" y="434" fill="#a78bfa" font-family="Consolas" font-size="12" font-weight="bold">🔗 FK  layout_id (INT)</text>
    <text x="475" y="456" fill="#34d399" font-family="Consolas" font-size="12" font-weight="bold">🔗 FK  profile_id (INT)</text>
    <text x="475" y="478" fill="#fbcfe8" font-family="Consolas" font-size="12">• words_per_minute (REAL)</text>
    <text x="475" y="500" fill="#fbcfe8" font-family="Consolas" font-size="12">• accuracy_pct (REAL)</text>
  </g>

  <!-- 7. كيان مقاييس الجلسة SESSION_METRICS -->
  <g filter="url(#shadowBox)">
    <rect x="460" y="560" width="220" height="110" rx="10" fill="url(#gradSession)" stroke="#fb7185" stroke-width="1.5"/>
    <rect x="460" y="560" width="220" height="25" rx="10" fill="#9f1239"/>
    <text x="570" y="578" fill="#ffffff" font-family="Cairo" font-size="12" font-weight="bold" text-anchor="middle">SESSION_METRICS (المقاييس)</text>
    <text x="475" y="605" fill="#fbbf24" font-family="Consolas" font-size="11" font-weight="bold">🔑 PK  metric_id</text>
    <text x="475" y="625" fill="#f43f5e" font-family="Consolas" font-size="11" font-weight="bold">🔗 FK  session_id</text>
    <text x="475" y="645" fill="#fbcfe8" font-family="Consolas" font-size="11">• avg_dwell_time, backspaces</text>
  </g>

  <!-- 8. كيان تخطيطات الكيبورد KEYBOARD_LAYOUTS -->
  <g filter="url(#shadowBox)">
    <rect x="760" y="380" width="210" height="160" rx="10" fill="url(#gradLayout)" stroke="#a78bfa" stroke-width="2"/>
    <rect x="760" y="380" width="210" height="30" rx="10" fill="#6d28d9"/>
    <text x="865" y="402" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">KEYBOARD_LAYOUTS</text>
    <text x="775" y="435" fill="#fbbf24" font-family="Consolas" font-size="12" font-weight="bold">🔑 PK  layout_id (INT)</text>
    <text x="775" y="460" fill="#f8fafc" font-family="Consolas" font-size="12">• layout_name (VARCHAR)</text>
    <text x="775" y="485" fill="#ddd6fe" font-family="Consolas" font-size="12">• language_code (AR/EN)</text>
    <text x="775" y="510" fill="#ddd6fe" font-family="Consolas" font-size="12">• total_rows, cols (INT)</text>
  </g>

</svg>
</div>
"""

# المخطط الثاني: DFD مخطط تدفق البيانات للمنظومة
SVG_DFD = """
<div class="diagram-wrapper">
<div class="diagram-title">الشكل (1-2): مخطط تدفق البيانات (DFD Level 1 - Data Storage & Engine Pipeline)</div>
<svg viewBox="0 0 950 420" width="100%" height="420" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="dfdProc" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
    <linearGradient id="dfdStore" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d9488"/><stop offset="100%" stop-color="#115e59"/>
    </linearGradient>
    <linearGradient id="dfdExt" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <filter id="dfdShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
    <marker id="dfdArrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
  </defs>

  <!-- الكيان الخارجي 1: الكاميرا -->
  <g filter="url(#dfdShadow)">
    <rect x="20" y="60" width="150" height="80" rx="8" fill="url(#dfdExt)" stroke="#38bdf8" stroke-width="2"/>
    <text x="95" y="95" fill="#38bdf8" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">📷 كاميرا الويب</text>
    <text x="95" y="118" fill="#94a3b8" font-family="Cairo" font-size="11" text-anchor="middle">Webcam Frames</text>
  </g>

  <!-- العملية 1.0: محرك الرؤية -->
  <g filter="url(#dfdShadow)">
    <rect x="230" y="50" width="180" height="100" rx="15" fill="url(#dfdProc)" stroke="#bae6fd" stroke-width="2"/>
    <text x="320" y="80" fill="#ffffff" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">1.0 محرك الرؤية وتتبع الملامح</text>
    <text x="320" y="105" fill="#e0f2fe" font-family="Cairo" font-size="11" text-anchor="middle">MediaPipe Face & Hands</text>
    <text x="320" y="125" fill="#bae6fd" font-family="Consolas" font-size="11" text-anchor="middle">Nose Tip / EAR / Gestures</text>
  </g>

  <!-- العملية 2.0: التحويل التآلفي والتثبيت -->
  <g filter="url(#dfdShadow)">
    <rect x="480" y="50" width="190" height="100" rx="15" fill="url(#dfdProc)" stroke="#bae6fd" stroke-width="2"/>
    <text x="575" y="80" fill="#ffffff" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">2.0 التحويل التآلفي والتنعيم</text>
    <text x="575" y="105" fill="#e0f2fe" font-family="Cairo" font-size="11" text-anchor="middle">Affine Transform & Leash</text>
    <text x="575" y="125" fill="#bae6fd" font-family="Consolas" font-size="11" text-anchor="middle">Laser Lock & Deadband</text>
  </g>

  <!-- العملية 3.0: واجهة الكيبورد والكتابة -->
  <g filter="url(#dfdShadow)">
    <rect x="740" y="50" width="180" height="100" rx="15" fill="url(#dfdProc)" stroke="#bae6fd" stroke-width="2"/>
    <text x="830" y="80" fill="#ffffff" font-family="Cairo" font-size="14" font-weight="bold" text-anchor="middle">3.0 محرك الكيبورد والتثبيت</text>
    <text x="830" y="105" fill="#e0f2fe" font-family="Cairo" font-size="11" text-anchor="middle">Virtual Keyboard Engine</text>
    <text x="830" y="125" fill="#bae6fd" font-family="Consolas" font-size="11" text-anchor="middle">Dwell Typing & WPM</text>
  </g>

  <!-- مخازن البيانات Data Stores -->
  <!-- D1: ملفات المعايرة -->
  <g filter="url(#dfdShadow)">
    <path d="M 470 250 L 680 250 M 470 310 L 680 310" stroke="#2dd4bf" stroke-width="3"/>
    <rect x="470" y="250" width="210" height="60" fill="url(#dfdStore)" rx="6"/>
    <text x="495" y="285" fill="#fbbf24" font-family="Consolas" font-size="14" font-weight="bold">D1</text>
    <text x="585" y="278" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">ملفات المعايرة (9-Points)</text>
    <text x="585" y="298" fill="#99f6e4" font-family="Cairo" font-size="11" text-anchor="middle">Calibration Profiles & Matrices</text>
  </g>

  <!-- D2: إحصائيات الأداء والجلسات -->
  <g filter="url(#dfdShadow)">
    <path d="M 730 250 L 930 250 M 730 310 L 930 310" stroke="#f43f5e" stroke-width="3"/>
    <rect x="730" y="250" width="200" height="60" fill="#881337" rx="6"/>
    <text x="755" y="285" fill="#fbbf24" font-family="Consolas" font-size="14" font-weight="bold">D2</text>
    <text x="840" y="278" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">جلسات الكتابة والسرعة</text>
    <text x="840" y="298" fill="#fecdd3" font-family="Cairo" font-size="11" text-anchor="middle">Typing Analytics & WPM Logs</text>
  </g>

  <!-- D3: سجلات الصحة والإجهاد -->
  <g filter="url(#dfdShadow)">
    <path d="M 220 250 L 420 250 M 220 310 L 420 310" stroke="#f59e0b" stroke-width="3"/>
    <rect x="220" y="250" width="200" height="60" fill="#78350f" rx="6"/>
    <text x="245" y="285" fill="#fbbf24" font-family="Consolas" font-size="14" font-weight="bold">D3</text>
    <text x="330" y="278" fill="#ffffff" font-family="Cairo" font-size="13" font-weight="bold" text-anchor="middle">سجلات الإجهاد البصري</text>
    <text x="330" y="298" fill="#fef3c7" font-family="Cairo" font-size="11" text-anchor="middle">EAR Blink & Head Pose Logs</text>
  </g>

  <!-- خطوط التدفق -->
  <!-- كاميرا إلى 1.0 -->
  <path d="M 170 100 L 225 100" stroke="#38bdf8" stroke-width="2" marker-end="url(#dfdArrow)"/>
  <text x="200" y="90" fill="#bae6fd" font-family="Cairo" font-size="10" text-anchor="middle">Frames</text>

  <!-- 1.0 إلى 2.0 -->
  <path d="M 410 100 L 475 100" stroke="#38bdf8" stroke-width="2" marker-end="url(#dfdArrow)"/>
  <text x="445" y="90" fill="#bae6fd" font-family="Cairo" font-size="10" text-anchor="middle">Nose Coords</text>

  <!-- 2.0 إلى 3.0 -->
  <path d="M 670 100 L 735 100" stroke="#38bdf8" stroke-width="2" marker-end="url(#dfdArrow)"/>
  <text x="705" y="90" fill="#bae6fd" font-family="Cairo" font-size="10" text-anchor="middle">Screen (X, Y)</text>

  <!-- D1 إلى 2.0 (تحميل المعايرة) -->
  <path d="M 545 250 L 545 155" stroke="#2dd4bf" stroke-width="2" marker-end="url(#dfdArrow)"/>
  <text x="515" y="200" fill="#2dd4bf" font-family="Cairo" font-size="10">قراءة المصفوفة</text>

  <!-- 2.0 إلى D1 (حفظ المعايرة) -->
  <path d="M 605 155 L 605 250" stroke="#34d399" stroke-width="2" stroke-dasharray="4" marker-end="url(#dfdArrow)"/>
  <text x="615" y="200" fill="#34d399" font-family="Cairo" font-size="10">حفظ 9-Points</text>

  <!-- 3.0 إلى D2 (حفظ إحصائيات الكتابة) -->
  <path d="M 830 155 L 830 250" stroke="#f43f5e" stroke-width="2" marker-end="url(#dfdArrow)"/>
  <text x="840" y="200" fill="#f43f5e" font-family="Cairo" font-size="10">سجلات WPM</text>

  <!-- 1.0 إلى D3 (سجلات EAR) -->
  <path d="M 320 155 L 320 250" stroke="#f59e0b" stroke-width="2" marker-end="url(#dfdArrow)"/>
  <text x="330" y="200" fill="#f59e0b" font-family="Cairo" font-size="10">إجهاد العين EAR</text>

</svg>
</div>
"""

# ==============================================================================
# 2. توليد مستند HTML الأكاديمي المنسق
# ==============================================================================

html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>وثيقة التصميم المعماري ومخططات قاعدة البيانات - Enterprise Virtual Keyboard v5.0</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cairo:wght@300;400;600;700;800;900&family=Fira+Code:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --primary: #0284c7;
    --primary-dark: #0369a1;
    --secondary: #0f172a;
    --accent: #38bdf8;
    --bg-light: #f8fafc;
    --card-bg: #ffffff;
    --text-main: #0f172a;
    --text-muted: #475569;
    --border-color: #e2e8f0;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
  }}

  @page {{
    size: A4 portrait;
    margin: 18mm 15mm 20mm 15mm;
    @bottom-right {{
      content: "صفحة " counter(page) " من " counter(pages);
      font-family: 'Cairo', sans-serif;
      font-size: 9pt;
      color: #64748b;
    }}
    @bottom-left {{
      content: "نظام الكيبورد البصري الذكي v5.0 - وثيقة قاعدة البيانات";
      font-family: 'Cairo', sans-serif;
      font-size: 9pt;
      color: #64748b;
    }}
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'Cairo', sans-serif;
    background-color: var(--bg-light);
    color: var(--text-main);
    line-height: 1.7;
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }}

  .cover-page {{
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    min-height: 250mm;
    padding: 30px;
    background: linear-gradient(145deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
    color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
  }}

  .cover-header {{
    text-align: center;
    border-bottom: 2px solid rgba(56, 189, 248, 0.4);
    padding-bottom: 20px;
  }}

  .cover-header h3 {{
    margin: 0;
    font-size: 14pt;
    color: #94a3b8;
    font-weight: 600;
  }}

  .cover-header h4 {{
    margin: 5px 0 0 0;
    font-size: 12pt;
    color: #38bdf8;
    font-weight: 700;
  }}

  .cover-body {{
    text-align: center;
    margin: 40px 0;
  }}

  .cover-title {{
    font-size: 26pt;
    font-weight: 900;
    line-height: 1.4;
    color: #ffffff;
    margin-bottom: 15px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
  }}

  .cover-subtitle {{
    font-size: 14pt;
    color: #38bdf8;
    font-weight: 600;
    line-height: 1.6;
    max-width: 850px;
    margin: 0 auto;
  }}

  .cover-badge {{
    display: inline-block;
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid #38bdf8;
    color: #e0f2fe;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 11pt;
    font-weight: 700;
    margin-top: 25px;
  }}

  .cover-footer {{
    border-top: 1px solid rgba(255,255,255,0.2);
    padding-top: 20px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    font-size: 11pt;
  }}

  .footer-box {{
    background: rgba(15, 23, 42, 0.6);
    padding: 15px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
  }}

  .footer-box strong {{
    color: #38bdf8;
    display: block;
    margin-bottom: 5px;
  }}

  h1, h2, h3, h4 {{
    font-family: 'Cairo', sans-serif;
    color: var(--secondary);
    font-weight: 800;
    page-break-after: avoid;
  }}

  h1 {{
    font-size: 18pt;
    color: var(--primary-dark);
    border-right: 6px solid var(--primary);
    padding-right: 12px;
    margin-top: 30px;
    margin-bottom: 15px;
    background: linear-gradient(to left, rgba(2, 132, 199, 0.08), transparent);
    padding-top: 6px;
    padding-bottom: 6px;
    border-radius: 0 4px 4px 0;
  }}

  h2 {{
    font-size: 14pt;
    color: #1e293b;
    margin-top: 25px;
    margin-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 5px;
  }}

  h3 {{
    font-size: 12pt;
    color: #334155;
    margin-top: 18px;
  }}

  p, li {{
    font-size: 10.5pt;
    color: #334155;
    text-align: justify;
  }}

  .diagram-wrapper {{
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 15px;
    margin: 20px 0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    page-break-inside: avoid;
  }}

  .diagram-title {{
    font-size: 11pt;
    font-weight: 700;
    color: var(--primary-dark);
    text-align: center;
    margin-bottom: 12px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 8px;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 10pt;
    background: #ffffff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    page-break-inside: avoid;
  }}

  th, td {{
    padding: 10px 12px;
    border: 1px solid var(--border-color);
    text-align: right;
  }}

  th {{
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    font-size: 10pt;
  }}

  tr:nth-child(even) {{
    background: #f8fafc;
  }}

  .badge-pk {{
    background: #fef3c7;
    color: #92400e;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8.5pt;
    font-weight: 700;
    border: 1px solid #fde68a;
  }}

  .badge-fk {{
    background: #e0f2fe;
    color: #0369a1;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8.5pt;
    font-weight: 700;
    border: 1px solid #bae6fd;
  }}

  pre {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 14px;
    border-radius: 8px;
    font-family: 'Fira Code', monospace;
    font-size: 9pt;
    direction: ltr;
    text-align: left;
    overflow-x: auto;
    border-left: 4px solid var(--accent);
    page-break-inside: avoid;
    line-height: 1.5;
  }}

  code {{
    font-family: 'Fira Code', monospace;
    font-size: 9pt;
    background: #e2e8f0;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 4px;
  }}

  .card-box {{
    background: #ffffff;
    border-right: 4px solid var(--primary);
    padding: 15px 18px;
    border-radius: 0 8px 8px 0;
    margin: 15px 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    border-top: 1px solid #f1f5f9;
    border-bottom: 1px solid #f1f5f9;
    border-left: 1px solid #f1f5f9;
    page-break-inside: avoid;
  }}

  .page-break {{
    page-break-after: always;
  }}
</style>
</head>
<body>

<!-- 1. غلاف التقرير الأكاديمي -->
<div class="cover-page">
  <div class="cover-header">
    <h3>الجمهورية اليمنية - وزارة التعليم العالي والبحث العلمي</h3>
    <h4>مشروع تخرج / مقرر معالجة الصور الرقمية والرؤية الحاسوبية المتقدمة (DIP / CV)</h4>
  </div>

  <div class="cover-body">
    <div class="cover-title">وثيقة التصميم المعماري لقاعدة البيانات وهندسة تدفق البيانات</div>
    <div class="cover-subtitle">
      Database Architecture, Entity-Relationship Modeling (ERD), Relational Schema (3NF) & Data Flow Specifications
    </div>
    <div class="cover-badge">
      Enterprise Edition v5.0 | Hybrid Real-Time & Clinical Relational Persistence
    </div>
  </div>

  <div class="cover-footer">
    <div class="footer-box">
      <strong>🏢 المنظومة البرمجية:</strong>
      نظام الكيبورد الافتراضي الذكي بتتبع الأنف وإيماءات اليد (Gaze & Gesture Keyboard)
    </div>
    <div class="footer-box">
      <strong>🎯 التخصص الأكاديمي:</strong>
      تقنية المعلومات (Information Technology) - المستوى الرابع
    </div>
  </div>
</div>

<!-- 2. محتوى الوثيقة -->
<h1>1. الرؤية المعمارية وتبرير إدارة البيانات (Architectural Paradigm)</h1>
<p>
في أنظمة التفاعل الإنساني الحاسوبي (HCI) عالية الدقة المعتمدة على الرؤية الحاسوبية اللحظية (Computer Vision)، تبرز الحاجة إلى نموذج هجين لإدارة البيانات يجمع بين متطلبين أساسيين:
</p>
<div class="card-box">
  <strong>1. الوضع الحسابي اللحظي (Zero-Latency Real-Time Pipeline):</strong>
  تخزين محلي فوري لمعاملات مصفوفة التحويل التآلفي (9-Point Affine Transform Matrix) والمنطقة الميتة (Deadband Radius) في ملف <code>calibration.json</code> لضمان استجابة بمعدل <strong>0ms Latency</strong> أثناء رسم المؤشر وتحديث واجهة المستخدم بمعدل 60 إطاراً في الثانية.
</div>
<div class="card-box">
  <strong>2. منظومة البيانات المؤسسية والطبية (Enterprise & Assistive Healthcare DB):</strong>
  قاعدة بيانات علائقية متكاملة تضمن استدامة السجلات، تخصيص الإعدادات لمرضى التصلب الجانبي الضموري (ALS) والشلل الرباعي، تخزين تاريخ المعايرات لكل مريض، وتسجيل مقاييس الأداء (WPM, Error Rates) وبيانات الإرهاق البصري (EAR Blinking & Head Pose Fatigue).
</div>

<div class="page-break"></div>

<h1>2. مخطط الكيانات والعلاقات (Entity-Relationship Diagram - ERD)</h1>
<p>
يوضح المخطط التالي بنية الكيانات والعلاقات والصفات وفق أحدث معايير هندسة البرمجيات وقواعد البيانات:
</p>

{SVG_ERD}

<div class="card-box">
  <strong>تحليل العلاقات الهندسية (Cardinalities & Constraints):</strong>
  <ul>
    <li><strong>علاقة (1 : N) بين USERS و CALIBRATION_PROFILES:</strong> يمتلك كل مستخدم عدة ملفات معايرة تتناسب مع وضعيات الجلوس والإضاءة المختلفة.</li>
    <li><strong>علاقة (1 : 9) بين CALIBRATION_PROFILES و CALIBRATION_POINTS:</strong> يحتوي كل ملف معايرة على 9 نقاط مرجعية موزعة على الشاشة بنظام 3x3 مع حساب الخطأ المتبقي (Residual Error).</li>
    <li><strong>علاقة (1 : 1) بين USERS و USER_SETTINGS:</strong> يمتلك المستخدم ملف إعدادات شخصي فريد يحفظ تفضيلاته (حساسية العين، زمن التثبيت، الصوت).</li>
    <li><strong>علاقة (1 : N) بين USERS و TYPING_SESSIONS:</strong> يسجل النظام كافة جلسات الكتابة ومعدل الكلمات في الدقيقة (WPM) ومعدل الأخطاء.</li>
    <li><strong>علاقة (1 : N) بين USERS و ERGONOMIC_LOGS:</strong> رصد دوري لسلامة المستخدم ونسبة فتحة العين (EAR) وتنبيهات الإجهاد.</li>
  </ul>
</div>

<div class="page-break"></div>

<h1>3. مخطط تدفق البيانات للمنظومة (Data Flow Diagram - DFD)</h1>
<p>
يوضح مخطط DFD Level 1 تدفق إطارات الفيديو الخام من الكاميرا، مروراً بمحرك الرؤية، والتحويل التآلفي، وصولاً إلى التخزين في قواعد البيانات وقراءتها:
</p>

{SVG_DFD}

<div class="page-break"></div>

<h1>4. قاموس البيانات المرجعي (Comprehensive Data Dictionary)</h1>
<p>
يوثق هذا الجدول كافة الحقول والأنواع والقيود في قاعدة البيانات لتحقيق المعيار القياسي الثالث (3NF):
</p>

<table>
  <thead>
    <tr>
      <th>الجدول (Table)</th>
      <th>الحقل (Field)</th>
      <th>نوع البيانات</th>
      <th>القيد (Constraint)</th>
      <th>الوصف الهندسي والوظيفي</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4"><strong>users</strong></td>
      <td><code>user_id</code></td>
      <td>INTEGER</td>
      <td><span class="badge-pk">PRIMARY KEY</span></td>
      <td>المعرف الرقمي الفريد للمستخدم أو المريض</td>
    </tr>
    <tr>
      <td><code>full_name</code></td>
      <td>VARCHAR(100)</td>
      <td>NOT NULL</td>
      <td>الاسم الكامل للمستخدم</td>
    </tr>
    <tr>
      <td><code>username</code></td>
      <td>VARCHAR(50)</td>
      <td>UNIQUE, NOT NULL</td>
      <td>اسم الدخول الفريد للنظام</td>
    </tr>
    <tr>
      <td><code>disability_type</code></td>
      <td>VARCHAR(50)</td>
      <td>NULLABLE</td>
      <td>نوع الإعاقة الحركية (مثل: ALS, Quadriplegia)</td>
    </tr>
    <tr>
      <td rowspan="5"><strong>calibration_profiles</strong></td>
      <td><code>profile_id</code></td>
      <td>INTEGER</td>
      <td><span class="badge-pk">PRIMARY KEY</span></td>
      <td>المعرف الفريد لملف المعايرة</td>
    </tr>
    <tr>
      <td><code>user_id</code></td>
      <td>INTEGER</td>
      <td><span class="badge-fk">FOREIGN KEY</span></td>
      <td>معرف المستخدم المالك للمعايرة (ON DELETE CASCADE)</td>
    </tr>
    <tr>
      <td><code>deadband_px</code></td>
      <td>REAL</td>
      <td>DEFAULT 1.8</td>
      <td>نصف قطر المنطقة الميتة للقفل الليزري المانع للارتعاش</td>
    </tr>
    <tr>
      <td><code>affine_matrix_x</code></td>
      <td>TEXT (JSON)</td>
      <td>NOT NULL</td>
      <td>معاملات مصفوفة التحويل للمحور السيني [a1, a2, a3]</td>
    </tr>
    <tr>
      <td><code>affine_matrix_y</code></td>
      <td>TEXT (JSON)</td>
      <td>NOT NULL</td>
      <td>معاملات مصفوفة التحويل للمحور الصادي [b1, b2, b3]</td>
    </tr>
    <tr>
      <td rowspan="3"><strong>calibration_points</strong></td>
      <td><code>point_id</code></td>
      <td>INTEGER</td>
      <td><span class="badge-pk">PRIMARY KEY</span></td>
      <td>المعرف الفريد لنقطة المعايرة</td>
    </tr>
    <tr>
      <td><code>profile_id</code></td>
      <td>INTEGER</td>
      <td><span class="badge-fk">FOREIGN KEY</span></td>
      <td>معرف ملف المعايرة التابع له</td>
    </tr>
    <tr>
      <td><code>residual_error</code></td>
      <td>REAL</td>
      <td>DEFAULT 0.0</td>
      <td>الخطأ الإقليدي المتبقي بعد حل معادلة المربعات الصغرى</td>
    </tr>
    <tr>
      <td rowspan="4"><strong>typing_sessions</strong></td>
      <td><code>session_id</code></td>
      <td>INTEGER</td>
      <td><span class="badge-pk">PRIMARY KEY</span></td>
      <td>المعرف الفريد لجلسة الكتابة</td>
    </tr>
    <tr>
      <td><code>user_id</code></td>
      <td>INTEGER</td>
      <td><span class="badge-fk">FOREIGN KEY</span></td>
      <td>معرف المستخدم المنفذ للجلسة</td>
    </tr>
    <tr>
      <td><code>words_per_minute</code></td>
      <td>REAL</td>
      <td>CHECK(WPM >= 0)</td>
      <td>سرعة الكتابة الصافية بالكلمات في الدقيقة</td>
    </tr>
    <tr>
      <td><code>accuracy_percentage</code></td>
      <td>REAL</td>
      <td>CHECK(0..100)</td>
      <td>نسبة الدقة وتفادي أخطاء الضغط والمسح</td>
    </tr>
    <tr>
      <td rowspan="3"><strong>ergonomic_logs</strong></td>
      <td><code>log_id</code></td>
      <td>INTEGER</td>
      <td><span class="badge-pk">PRIMARY KEY</span></td>
      <td>معرف سجل المراقبة الفسيولوجية</td>
    </tr>
    <tr>
      <td><code>avg_ear_value</code></td>
      <td>REAL</td>
      <td>NOT NULL</td>
      <td>متوسط مقياس انفتاح العين (Eye Aspect Ratio)</td>
    </tr>
    <tr>
      <td><code>alert_type</code></td>
      <td>VARCHAR(50)</td>
      <td>DEFAULT 'NORMAL'</td>
      <td>نوع التنبيه (مثال: FATIGUE_WARNING, EYE_CLOSURE)</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h1>5. سكريبت الإنشاء التنفيذي لقاعدة البيانات (DDL SQL Script)</h1>
<p>
كود SQL DDL معياري جاهز للتنفيذ الفوري على بيئات SQLite و PostgreSQL و MySQL مع بناء الفهارس الحسابية:
</p>

<pre><code>-- =====================================================================
-- نظام الكيبورد البصري الذكي - Enterprise Database Schema (v5.0)
-- =====================================================================
PRAGMA foreign_keys = ON;

-- 1. جدول المستخدمين (Users Table)
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    disability_type VARCHAR(50),
    hand_preference VARCHAR(10) DEFAULT 'RIGHT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. جدول ملفات المعايرة الرياضية (Calibration Profiles)
CREATE TABLE IF NOT EXISTS calibration_profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    profile_name VARCHAR(50) DEFAULT 'Default Calibration',
    reference_distance_cm REAL DEFAULT 60.0,
    deadband_px REAL DEFAULT 1.8,
    sens_x REAL DEFAULT 1.91,
    sens_y REAL DEFAULT 2.0,
    affine_matrix_x TEXT NOT NULL, -- JSON Array [a1, a2, a3]
    affine_matrix_y TEXT NOT NULL, -- JSON Array [b1, b2, b3]
    is_active BOOLEAN DEFAULT 1,
    calibrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 3. جدول نقاط المعايرة التسع (Calibration Points)
CREATE TABLE IF NOT EXISTS calibration_points (
    point_id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    point_index INTEGER CHECK(point_index BETWEEN 1 AND 9),
    target_screen_x REAL NOT NULL,
    target_screen_y REAL NOT NULL,
    captured_nose_x REAL NOT NULL,
    captured_nose_y REAL NOT NULL,
    residual_error REAL DEFAULT 0.0,
    FOREIGN KEY (profile_id) REFERENCES calibration_profiles(profile_id) ON DELETE CASCADE
);

-- 4. جدول إعدادات المستخدم (User Settings)
CREATE TABLE IF NOT EXISTS user_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    ear_threshold REAL DEFAULT 0.16,
    dwell_time_sec REAL DEFAULT 0.85,
    preferred_language VARCHAR(10) DEFAULT 'AR',
    dark_mode BOOLEAN DEFAULT 1,
    sound_feedback BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 5. جدول جلسات الكتابة ومقاييس الأداء (Typing Sessions)
CREATE TABLE IF NOT EXISTS typing_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    total_characters INTEGER DEFAULT 0,
    words_per_minute REAL DEFAULT 0.0,
    accuracy_percentage REAL DEFAULT 100.0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 6. جدول سجلات الصحة ووضعية الرأس (Ergonomic Health Logs)
CREATE TABLE IF NOT EXISTS ergonomic_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    avg_ear_value REAL NOT NULL,
    head_pitch REAL,
    head_yaw REAL,
    head_roll REAL,
    alert_type VARCHAR(50) DEFAULT 'NORMAL',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- الفهارس لتسريع الاستعلامات والتقارير الفورية
CREATE INDEX IF NOT EXISTS idx_calib_user ON calibration_profiles(user_id, is_active);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON typing_sessions(user_id, started_at);
CREATE INDEX IF NOT EXISTS idx_ergo_user_time ON ergonomic_logs(user_id, event_time);
</code></pre>

<div class="card-box">
  <strong>الخلاصة التوصيفية للأطروحة الأكاديمية:</strong>
  تمنح هذه المعمارية البياناتية المشروع تكاملاً هندسياً شاملاً بين خوارزميات معالجة الصور اللحظية (MediaPipe & OpenCV) وأنظمة تخزين البيانات الطبية الموثوقة، مما يجعله مؤهلاً بقوة للتحول إلى منتج سريري ومجتمعي متكامل لخدمة أصحاب الهمم.
</div>

</body>
</html>
"""

# حفظ ملف HTML
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"✅ تم إنشاء مستند HTML بنجاح: {OUTPUT_HTML}")

# حفظ نسخة Markdown
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(f"""# وثيقة التصميم المعماري لقاعدة البيانات وهندسة تدفق البيانات
## Enterprise Gaze & Gesture Virtual Keyboard (v5.0)

تم توليد هذه الوثيقة الأكاديمية كمرجع رسمي للمخططات الهندسية لقاعدة البيانات الخاصة بنظام الكيبورد البصري الذكي.

### محتويات الوثيقة:
1. الرؤية المعمارية وتبرير إدارة البيانات (Real-time JSON + Relational Enterprise DB).
2. مخطط الكيانات والعلاقات الكامل (Entity-Relationship Diagram - ERD).
3. مخطط تدفق البيانات (Data Flow Diagram - DFD Level 0 & Level 1).
4. قاموس البيانات المرجعي الشامل (Data Dictionary).
5. سكريبت الإنشاء التنفيذي لقاعدة البيانات (DDL SQL Script).

راجع النسخة المنسقة الجاهزة للطباعة: `{OUTPUT_PDF}`.
""")
print(f"✅ تم إنشاء ملخص Markdown: {OUTPUT_MD}")

# ==============================================================================
# 3. التحويل إلى PDF فائق الدقة عبر Microsoft Edge / Chrome Headless
# ==============================================================================
print("[3/3] جاري تحويل المستند إلى PDF فائق الدقة (A4 Luxury Print)...")

edge_binary = None
for p in EDGE_PATHS:
    if os.path.exists(p):
        edge_binary = p
        break

if edge_binary:
    cmd = [
        edge_binary,
        "--headless",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={OUTPUT_PDF}",
        OUTPUT_HTML
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"🎉 تم توليد ملف الـ PDF بنجاح تام: {OUTPUT_PDF}")
    except Exception as e:
        print(f"⚠️ خطأ أثناء توليد PDF عبر Edge: {e}")
else:
    print("⚠️ لم يتم العثور على متصفح Edge أو Chrome لتوليد PDF تلقائياً.")

print("=" * 80)
print("🚀 اكتملت عملية التوليد بنجاح!")
print("=" * 80)
