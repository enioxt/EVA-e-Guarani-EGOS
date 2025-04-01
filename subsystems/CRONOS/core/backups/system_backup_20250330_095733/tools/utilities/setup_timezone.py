#!/usr/bin/env python3
python

import os
import sys
import time
import platform
import importlib.util

# Check if pytz is installed
if importlib.util.find_spec("pytz") is None:
    print("Installing pytz...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytz"])

# Now import pytz
import pytz

# Set timezone
os.environ['TZ'] = 'UTC'
if platform.system() != 'Windows' and hasattr(time, 'tzset'):
    time.tzset()

# Patch for APScheduler
def patch_apscheduler():
    from telegram.ext import JobQueue
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    import inspect
    
    # Store original reference of AsyncIOScheduler constructor
    original_asyncio_init = AsyncIOScheduler.__init__
    
    # Replace the constructor to always use UTC
    def patched_asyncio_init(self, *args, **kwargs):
        if 'timezone' not in kwargs:
            kwargs['timezone'] = pytz.UTC
        return original_asyncio_init(self, *args, **kwargs)
    
    # Apply the patch
    AsyncIOScheduler.__init__ = patched_asyncio_init
    
    # Patch for ApplicationBuilder
    from telegram.ext import ApplicationBuilder
    original_build = ApplicationBuilder.build
    
    def patched_build(self):
        app = original_build(self)
        # Ensure the job_queue's scheduler uses UTC
        if hasattr(app, 'job_queue') and app.job_queue is not None:
            if hasattr(app.job_queue, '_scheduler'):
                app.job_queue._scheduler.timezone = pytz.UTC
        return app
    
    ApplicationBuilder.build = patched_build
    
    # Patch for the _create_scheduler method if it exists
    if hasattr(JobQueue, '_create_scheduler'):
        original_create_scheduler = JobQueue._create_scheduler
        
        def patched_create_scheduler(self):
            scheduler = original_create_scheduler(self)
            scheduler.timezone = pytz.UTC
            return scheduler
        
        JobQueue._create_scheduler = patched_create_scheduler
    
    print("APScheduler patched successfully to use UTC timezone")

# Execute the patch
patch_apscheduler()