"""
==================================================================================
وحدة إدارة الحالة للنظام (Latching State Machine Management)
System State Machine with Strict Latching and Collision Prevention
==================================================================================
تطبيق معايير هندسة البرمجيات المتقدمة لإدارة الحالات والتنقل الآمن بينها:
- حالات واضحة لمنع التداخل والتعارض (Latching States).
- عزل كامل للإيماءات أثناء المعايرة لمنع أي تعارض تشغيلي.
- انتقال فوري لحالة التجميد الآمن (SAFE_FREEZE) عند غياب الوجه أو الكاميرا.
==================================================================================
"""

from enum import Enum, auto
import time
from typing import Optional, Callable, Dict, Any


class SystemState(Enum):
    """حالات النظام التشغيلية المعيارية."""
    ACTIVE = auto()          # التشغيل الكامل والتتبع الطبيعي
    PAUSED = auto()          # إيقاف مؤقت بإيماءة القبضة أو إغلاق العين
    CALIBRATING = auto()     # جلسة المعايرة التفاعلية (تجاهل مطلق للإيماءات)
    ROW_LOCKED = auto()      # قفل أفقي على صف محدد لتسهيل الكتابة السريعة
    SAFE_FREEZE = auto()     # تجميد آمن للمؤشر لحماية المستخدم عند فقدان الرصد


class AppStateMachine:
    """
    آلة حالات ذات استقرار ثنائي وتأكيد زمني (Latching State Machine):
    - تمنع التقلب العشوائي (Chatter/Bouncing) في الأحداث السريعة.
    - تفرض قواعد أولوية صارمة تمنع تضارب الحالات.
    """
    def __init__(
        self,
        on_state_change: Optional[Callable[[SystemState, SystemState, str], None]] = None,
        on_row_locked: Optional[Callable[[int], None]] = None,
        on_row_unlocked: Optional[Callable[[], None]] = None
    ):
        self._current_state = SystemState.ACTIVE
        self._previous_state = SystemState.ACTIVE
        self._pause_reason = ""
        self._freeze_reason = ""

        # مستمعو الأحداث
        self.on_state_change = on_state_change
        self.on_row_locked = on_row_locked
        self.on_row_unlocked = on_row_unlocked

        # توقيتات التثبيت الزمني للإيماءات لمنع النقر الخاطئ
        self.fist_detect_start = 0.0
        self.palm_detect_start = 0.0
        self.gesture_latch_threshold = 0.35  # ثانية لتأكيد الإيماءة

        # قفل الصفوف
        self.active_locked_row: Optional[int] = None
        self.row_lock_start_time = 0.0
        self.row_lock_duration = 1.30
        self.finger_gesture_candidate: Optional[int] = None
        self.finger_gesture_start = 0.0

    @property
    def current_state(self) -> SystemState:
        return self._current_state

    @property
    def pause_reason(self) -> str:
        return self._pause_reason

    @property
    def freeze_reason(self) -> str:
        return self._freeze_reason

    def can_dwell(self) -> bool:
        """هل يُسمح بتنشيط التثبيت الزمني لكتابة الحروف في الحالة الحالية؟"""
        return self._current_state in (SystemState.ACTIVE, SystemState.ROW_LOCKED)

    def can_move_cursor(self) -> bool:
        """هل يتحرك المؤشر مع حركة الأنف؟"""
        return self._current_state in (SystemState.ACTIVE, SystemState.ROW_LOCKED)

    def set_state(self, new_state: SystemState, reason: str = "") -> bool:
        """الانتقال إلى حالة جديدة مع تطبيق القواعد الهندسية الصارمة."""
        if self._current_state == new_state:
            return False

        old_state = self._current_state

        # قاعدة صارمة: إذا كان النظام في حالة المعايرة CALIBRATING، لا يمكن الانتقال إلا بإلغاء أو إكمال المعايرة
        if old_state == SystemState.CALIBRATING and new_state not in (SystemState.ACTIVE, SystemState.PAUSED):
            return False

        # حفظ الحالة السابقة قبل التجميد الآمن للرجوع إليها بسلاسة
        if new_state == SystemState.SAFE_FREEZE:
            self._previous_state = old_state
            self._freeze_reason = reason
        elif old_state == SystemState.SAFE_FREEZE:
            self._freeze_reason = ""

        if new_state == SystemState.PAUSED:
            self._pause_reason = reason
        elif old_state == SystemState.PAUSED and new_state != SystemState.SAFE_FREEZE:
            self._pause_reason = ""

        # عند الخروج من قفل الصف
        if old_state == SystemState.ROW_LOCKED and new_state != SystemState.ROW_LOCKED:
            self.active_locked_row = None
            if self.on_row_unlocked:
                self.on_row_unlocked()

        self._current_state = new_state

        if self.on_state_change:
            self.on_state_change(old_state, new_state, reason)

        return True

    def start_calibration(self) -> bool:
        """بدء المعايرة: يعزل النظام تماماً عن أي إيماءات أو نقرات."""
        return self.set_state(SystemState.CALIBRATING, "بدء جلسة معايرة 9 نقاط")

    def finish_calibration(self, success: bool = True) -> bool:
        """إنهاء المعايرة والعودة للحالة النشطة."""
        if self._current_state == SystemState.CALIBRATING:
            return self.set_state(SystemState.ACTIVE, "اكتملت المعايرة بنجاح" if success else "إلغاء المعايرة")
        return False

    def handle_tracking_loss(self, reason: str = "فقدان رصد الوجه") -> None:
        """تفعيل التجميد الآمن عند فقدان الإشارة أو الكاميرا."""
        if self._current_state != SystemState.SAFE_FREEZE and self._current_state != SystemState.CALIBRATING:
            self.set_state(SystemState.SAFE_FREEZE, reason)

    def handle_tracking_restored(self) -> None:
        """استعادة الحالة الطبيعية فور عودة رصد الوجه بأمان."""
        if self._current_state == SystemState.SAFE_FREEZE:
            restore_to = self._previous_state if self._previous_state != SystemState.SAFE_FREEZE else SystemState.ACTIVE
            self.set_state(restore_to, "استعادة الرصد بنجاح")

    def lock_row(self, row_idx: int, duration: float = 1.30) -> None:
        """قفل صف أفقي محدد."""
        if self._current_state not in (SystemState.ACTIVE, SystemState.ROW_LOCKED):
            return

        self.active_locked_row = row_idx
        self.row_lock_start_time = time.time()
        self.row_lock_duration = duration

        if self._current_state != SystemState.ROW_LOCKED:
            self.set_state(SystemState.ROW_LOCKED, f"قفل الصف رقم {row_idx + 1}")

        if self.on_row_locked:
            self.on_row_locked(row_idx)

    def unlock_row(self) -> None:
        """إلغاء قفل الصف والرجوع للتتبع الحر."""
        if self._current_state == SystemState.ROW_LOCKED:
            self.set_state(SystemState.ACTIVE, "إلغاء قفل الصف")

    def update_timers(self, now: float) -> None:
        """تحديث المؤقتات الزمنية للحالات المؤقتة مثل انتهاء قفل الصف."""
        if self._current_state == SystemState.ROW_LOCKED and self.active_locked_row is not None:
            if now - self.row_lock_start_time >= self.row_lock_duration:
                self.unlock_row()

    def process_hand_gesture(self, gesture: str, now: float) -> Optional[str]:
        """
        معالجة إيماءات اليد وفق قواعد الاستقرار الزمني:
        
        ⭐ قاعدة هندسية حاسمة:
        إذا كانت الحالة CALIBRATING، يتم تجاهل جميع الإيماءات تماماً لمنع حدوث أي تعارض.
        """
        # 1. التجاهل التام للإيماءات أثناء المعايرة أو التجميد الآمن
        if self._current_state in (SystemState.CALIBRATING, SystemState.SAFE_FREEZE):
            self.fist_detect_start = 0.0
            self.palm_detect_start = 0.0
            self.finger_gesture_candidate = None
            return None

        action_triggered = None

        # 2. إيماءة القبضة FIST (إيقاف مؤقت Latching Pause)
        if gesture == "FIST":
            if self.fist_detect_start == 0.0:
                self.fist_detect_start = now
            elif (now - self.fist_detect_start) >= self.gesture_latch_threshold:
                if self._current_state != SystemState.PAUSED:
                    self.set_state(SystemState.PAUSED, "قبضة اليد ✊")
                    action_triggered = "PAUSED_BY_FIST"
        else:
            self.fist_detect_start = 0.0

        # 3. إيماءة الكف المفتوح OPEN_PALM (استئناف Latching Resume)
        if gesture == "OPEN_PALM":
            if self.palm_detect_start == 0.0:
                self.palm_detect_start = now
            elif (now - self.palm_detect_start) >= self.gesture_latch_threshold:
                if self._current_state == SystemState.PAUSED:
                    self.set_state(SystemState.ACTIVE, "كف اليد ✋")
                    action_triggered = "RESUMED_BY_PALM"
                elif self._current_state == SystemState.ROW_LOCKED:
                    self.unlock_row()
                    action_triggered = "UNLOCKED_BY_PALM"
        else:
            self.palm_detect_start = 0.0

        # 4. إيماءات الأصابع لقفل الصفوف (تُفعل فقط في الحالة النشطة ACTIVE)
        if self._current_state in (SystemState.ACTIVE, SystemState.ROW_LOCKED):
            if gesture in ("FINGER_1", "FINGER_2", "FINGER_3", "FINGER_4"):
                try:
                    f_idx = int(gesture.split("_")[1]) - 1
                    if self.finger_gesture_candidate == f_idx:
                        if (now - self.finger_gesture_start >= 0.22) and (self.active_locked_row != f_idx):
                            self.lock_row(f_idx, self.row_lock_duration)
                            action_triggered = f"LOCKED_ROW_{f_idx + 1}"
                    else:
                        self.finger_gesture_candidate = f_idx
                        self.finger_gesture_start = now
                except Exception:
                    self.finger_gesture_candidate = None
            else:
                self.finger_gesture_candidate = None

        return action_triggered

    def get_badge_info(self) -> Dict[str, str]:
        """الحصول على نصوص وألوان الشارات التوضيحية لواجهة المستخدم."""
        if self._current_state == SystemState.ACTIVE:
            return {"text": "🟢 نشط (ACTIVE)", "color": "#10b981", "desc": "تتبع حر طبيعي"}
        elif self._current_state == SystemState.PAUSED:
            return {"text": f"⏸️ متوقف ({self._pause_reason or 'PAUSED'})", "color": "#f59e0b", "desc": "افتح كف اليد للاستئناف"}
        elif self._current_state == SystemState.CALIBRATING:
            return {"text": "🎯 معايرة (CALIBRATING)", "color": "#a855f7", "desc": "جلسة معايرة نشطة"}
        elif self._current_state == SystemState.ROW_LOCKED:
            row_num = (self.active_locked_row + 1) if self.active_locked_row is not None else 1
            return {"text": f"🔒 قفل الصف {row_num} (ROW_LOCKED)", "color": "#38bdf8", "desc": "تتبع أفقي للصف"}
        elif self._current_state == SystemState.SAFE_FREEZE:
            return {"text": "🛡️ تجميد آمن (SAFE_FREEZE)", "color": "#ef4444", "desc": self._freeze_reason or "فقدان الإشارة"}
        return {"text": "مجهول", "color": "#94a3b8", "desc": ""}
