#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Patch to fix timezone issues in APScheduler
"""

import os
import sys
import pytz
import time
from importlib import import_module

# Ensure pytz is in the Python path
pytz_spec = sys.modules.get('pytz')
if not pytz_spec:
    raise ImportError("The pytz module is not installed or was not imported correctly")

# Set timezone globally
os.environ['TZ'] = 'UTC'
if hasattr(time, 'tzset'):
    time.tzset()

# Create UTC timezone object explicitly for verification
utc = pytz.timezone('UTC')
print(f"✅ UTC Timezone configured correctly: {utc}")

# Monkey patch for AsyncIOScheduler from APScheduler
try:
    # Try to import APScheduler dynamically
    apscheduler_module = import_module('apscheduler.schedulers.asyncio')
    AsyncIOScheduler = apscheduler_module.AsyncIOScheduler
    
    # Store original constructor
    original_init = AsyncIOScheduler.__init__
    
    # Define new constructor with pytz timezone
    def patched_init(self, *args, **kwargs):
        # Ensure the timezone is from pytz
        if 'timezone' not in kwargs:
            kwargs['timezone'] = pytz.UTC
        return original_init(self, *args, **kwargs)
    
    # Apply the patch
    AsyncIOScheduler.__init__ = patched_init
    print("✅ Patch applied to AsyncIOScheduler successfully")
    
except (ImportError, AttributeError) as e:
    print(f"❌ Error applying patch to APScheduler: {e}")
    # Continue even with error - the patch will just be a backup

# Patch for JobQueue from python-telegram-bot
try:
    # Try to import JobQueue dynamically
    ptr_module = import_module('telegram.ext._jobqueue')
    JobQueue = ptr_module.JobQueue
    
    # Store original constructor
    original_jobqueue_init = JobQueue.__init__
    
    # Define new constructor with pytz timezone
    def patched_jobqueue_init(self, *args, **kwargs):
        # Force use of pytz timezone in JobQueue
        self._tzinfo = pytz.UTC
        return original_jobqueue_init(self, *args, **kwargs)
    
    # Apply the patch
    JobQueue.__init__ = patched_jobqueue_init
    print("✅ Patch applied to JobQueue successfully")
    
except (ImportError, AttributeError) as e:
    print(f"❌ Error applying patch to JobQueue: {e}")
    # Continue even with error