#!/usr/bin/env python3
# ==================================================================
# COMBINED FILE FROM MULTIPLE SIMILAR FILES
# Date: 2025-03-22 08:45:54
# Combined files:
# - tools\utilities\timezone_patch_2.py (kept)
# - tools\utilities\timezone_patch.py (moved to quarantine)
# ==================================================================

python
# Patch for timezone configuration in python-telegram-bot
import os
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Monkey patch to fix timezone issues
original_init = AsyncIOScheduler.__init__


def patched_init(self, *args, **kwargs):
    if "timezone" not in kwargs:
        kwargs["timezone"] = pytz.UTC
    return original_init(self, *args, **kwargs)


AsyncIOScheduler.__init__ = patched_init

print("✅ Timezone patch applied successfully")
