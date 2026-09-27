# -*- coding: utf-8 -*-
"""
==================================================================================
نقطة الانطلاق الرئيسية لتطبيق الكيبورد البصري الذكي (Main Entry Point)
Smart Visual & Gaze Keyboard System - Enterprise Edition v5.0
==================================================================================
تشغيل التطبيق:
    python main.py
==================================================================================
"""

import os
import sys
import tkinter as tk

# ضبط ترميز الإخراج للغة العربية على أنظمة ويندوز
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# إضافة المجلدات الفرعية إلى مسار بايثون
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

for p in [BASE_DIR, BACKEND_DIR, FRONTEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from frontend.gaze_keyboard import GazeVirtualKeyboardApp
except ImportError:
    from gaze_keyboard import GazeVirtualKeyboardApp


def main():
    print("=" * 80)
    print("🧠 تشغيل نظام الكيبورد البصري الذكي المتطور (Enterprise v5.0)...")
    print("=" * 80)
    
    root = tk.Tk()
    app = GazeVirtualKeyboardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
