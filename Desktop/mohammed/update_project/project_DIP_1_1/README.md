# 🧠 نظام الكيبورد الافتراضي الذكي المتطور (Enterprise Virtual Keyboard v5.0)
## Nose-Tracking & Hand-Gesture Virtual Keyboard with 9-Point Affine Calibration

نظام كيبورد افتراضي ذكي متكامل يعمل بالكامل دون الحاجة لأي عتاد إضافي سوى كاميرا الويب، مصمم وفق معايير هندسة البرمجيات الحديثة (**Modular Object-Oriented Architecture, Multi-threading Concurrency, Latching State Machine, and Fail-Safe Resilience**).

يعتمد النظام على **تتبع طرف الأنف (Nose Tracking)** كمؤشر رئيسي فائق الدقة، و**إيماءات اليد (Hand Gestures)** للتحكم السريع في حالات التطبيق وقفل الصفوف، مع الالتزام الصارم بمعايير الصحة الرقمية والأمان الفسيولوجي (**EAR Eye Closure Detection & Head Pose Ergonomics**).

---

### 🏛️ 1. الهيكلية المعمارية وتنظيم المجلدات (Project Structure)

تم تنظيم المشروع في حزم ومجلدات معيارية مفصولة الاهتمامات (**Frontend / Backend / Models / Config / Tests / Docs / Reports**):

```text
project_DIP_1_1/
│
├── main.py                     # نقطة الانطلاق الرئيسية السريعة (Main Entry Point)
├── requirements.txt            # قائمة التبعيات والمكتبات المطلوبة
├── README.md                   # دليل البدء السريع والهيكلية العامة
│
├── backend/                    # الطبقة الخلفية ومحركات الرؤية والحسابات الرياضية
│   ├── __init__.py
│   ├── core_math.py            # الحسابات الهندسية، EAR، Head Pose، والتنعيم (Pure Math)
│   ├── state_machine.py        # آلة الحالات المستقرة زمنياً (Latching State Machine)
│   ├── tracking_engine.py      # محرك الرؤية وتتبع الملامح (MediaPipe Vision Tracker)
│   └── database_schema.sql     # سكريبت DDL لقاعدة البيانات العلائقية 3NF
│
├── frontend/                   # الطبقة الأمامية وواجهات المستخدم الرسومية
│   ├── __init__.py
│   ├── gaze_keyboard.py        # واجهة الكيبورد المظلمة والمؤشر الليزري (Main GUI)
│   └── calibration_ui.py       # نافذة المعايرة الهندسية 9 نقاط (Calibration Window)
│
├── models/                     # نماذج الذكاء الاصطناعي المدربة مسبقاً (MediaPipe AI Task Models)
│   ├── face_landmarker.task    # نموذج معالم الوجه (478 نقطة ثلاثية الأبعاد)
│   └── hand_landmarker.task    # نموذج معالم اليد (21 مفصلاً ثلاثي الأبعاد)
│
├── config/                     # ملفات الإعدادات والبيانات المحلية
│   └── calibration.json        # المعاملات المحفوظة ومصفوفة التحويل
│
├── tests/                      # حزمة اختبارات ضمان الجودة وضمان الاعتمادية
│   ├── __init__.py
│   └── test_virtual_keyboard.py # 12 اختبار وحدة شاملاً (Unit Tests)
│
├── docs/                       # وثائق النظام والمتطلبات والمواصفات (Technical Documentation)
│   ├── TOOLS.md                # 1. دليل الأدوات والمكتبات والتقنيات البرمجية المستخدمة
│   ├── SYSTEM_DOCUMENTATION.md # 2. الوثيقة الهندسية والمعمارية الشاملة وخط أنابيب المعالجة
│   └── SRS.md                  # 3. وثيقة مواصفات متطلبات البرمجيات (وفق معيار IEEE Std 830)
│
└── reports/                    # التقارير الأكاديمية الفاخرة المنسقة والعروض التقديمية
    ├── scripts/                # سكريبتات التوليد الآلي للتقارير والعروض
    │   ├── build_luxury_pdf_report.py
    │   ├── build_academic_report.py
    │   ├── generate_academic_documentation.py
    │   └── generate_database_specification_pdf.py
    ├── Academic_Engineering_Documentation_Gaze_Keyboard.pdf
    ├── Academic_Presentation_Gaze_Keyboard.pptx
    ├── Academic_Report_Gaze_Keyboard_DIP.pdf
    └── Database_Architecture_And_Engineering_Specification.pdf
```

---

### 🚀 2. التثبيت والتشغيل السريع

#### أ. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

#### ب. تشغيل الكيبورد الافتراضي:
```bash
python main.py
```

#### ج. تشغيل حزمة اختبارات الجودة (Unit Tests):
```bash
python -m unittest discover tests
```

---

### 📚 3. الوثائق والمستندات الهندسية المتاحة (Docs Directory)

يمكنك الاطلاع على التفاصيل المعمقرقة في مجلد `docs/`:
1. **[TOOLS.md](file:///d:/كورسات/مستوى%20رابع%20تقنية%20معلومات/معالجة%20صور/عملي/image_editor_project_ultimate_professional/project_DIP_1_1/docs/TOOLS.md):** تفصيل شامل للأدوات، المكتبات (MediaPipe, OpenCV, NumPy, Tkinter)، ومقارنات الأداء وتبرير الاختيار.
2. **[SYSTEM_DOCUMENTATION.md](file:///d:/كورسات/مستوى%20رابع%20تقنية%20معلومات/معالجة%20صور/عملي/image_editor_project_ultimate_professional/project_DIP_1_1/docs/SYSTEM_DOCUMENTATION.md):** شرح معمارية النظام، خط أنابيب المعالجة (Pipeline)، المعادلات الرياضية (Affine Transform, Strict Deadband, Leash Easing)، والتزامن متعدد الخيوط.
3. **[SRS.md](file:///d:/كورسات/مستوى%20رابع%20تقنية%20معلومات/معالجة%20صور/عملي/image_editor_project_ultimate_professional/project_DIP_1_1/docs/SRS.md):** وثيقة مواصفات متطلبات البرمجيات الرسمية وفق معيار **IEEE 830** متضمنة المتطلبات الوظيفية وغير الوظيفية وحالات الاستخدام ومصفوفة التتبع (RTM).

---

### 🎮 4. إيماءات اليد واختصارات التحكم

| الإيماءة / الاختصار | الوظيفة البرمجية |
| :--- | :--- |
| **✊ قبضة اليد (Fist)** | إيقاف مؤقت للكيبورد (`PAUSED`) وتجميد التثبيت |
| **✋ كف اليد المفتوح (Palm)** | استئناف التتبع الفوري (`ACTIVE`) أو إلغاء قفل الصف |
| **☝️ إصبع واحد** | قفل الصف الأول أفقياً لتسريع الكتابة |
| **✌️ إصبعان** | قفل الصف الثاني أفقياً |
| **🤟 ثلاثة أصابع** | قفل الصف الثالث أفقياً |
| **🖖 أربعة أصابع** | قفل صف المسافة والتحكم |
| **🎯 زر المعايرة (Calibrate)** | فتح نافذة معايرة 9 نقاط الهندسية لتكييف المؤشر مع جلستك |
| **🌐 زر اللغة (Language)** | التبديل الفوري بين لوحة المفاتيح العربية والإنجليزية |
