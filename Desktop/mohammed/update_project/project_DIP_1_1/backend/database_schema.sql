-- =====================================================================
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. جدول ملفات المعايرة الرياضية (9-Point Affine Calibration Profiles)
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

-- 3. جدول نقاط المعايرة التفصيلية (Calibration Points & Residual Errors)
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

-- 4. جدول إعدادات واجهة المستخدم (User Preferences & Thresholds)
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

-- 5. جدول تخطيطات لوحات المفاتيح (Keyboard Layouts)
CREATE TABLE IF NOT EXISTS keyboard_layouts (
    layout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    layout_name VARCHAR(50) NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    total_rows INTEGER DEFAULT 4,
    total_columns INTEGER DEFAULT 11,
    is_default BOOLEAN DEFAULT 0
);

-- 6. جدول جلسات الكتابة ومقاييس الأداء (Typing Sessions & Analytics)
CREATE TABLE IF NOT EXISTS typing_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    layout_id INTEGER,
    profile_id INTEGER,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    total_characters INTEGER DEFAULT 0,
    words_per_minute REAL DEFAULT 0.0,
    accuracy_percentage REAL DEFAULT 100.0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (layout_id) REFERENCES keyboard_layouts(layout_id),
    FOREIGN KEY (profile_id) REFERENCES calibration_profiles(profile_id)
);

-- 7. جدول سجلات الصحة ووضعية الرأس وإجهاد العين (Ergonomic & Fatigue Logs)
CREATE TABLE IF NOT EXISTS ergonomic_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    avg_ear_value REAL NOT NULL,
    head_pitch REAL,
    head_yaw REAL,
    head_roll REAL,
    alert_type VARCHAR(50) DEFAULT 'NORMAL',
    alert_triggered BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- الفهارس لتسريع الاستعلامات والتقارير الفورية
CREATE INDEX IF NOT EXISTS idx_calib_user ON calibration_profiles(user_id, is_active);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON typing_sessions(user_id, started_at);
CREATE INDEX IF NOT EXISTS idx_ergo_user_time ON ergonomic_logs(user_id, event_time);
