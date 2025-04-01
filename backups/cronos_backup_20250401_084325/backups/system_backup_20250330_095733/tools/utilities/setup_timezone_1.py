#!/usr/bin/env python3
python

# Set timezone before running the bot
import os
import sys
import time
import importlib
import logging

logger = logging.getLogger("setup_timezone")

# Apply patch directly to APScheduler before anything else
def patch_apscheduler():
    try:
        # Check if APScheduler is installed
        import apscheduler
        
        # Patch the astimezone function of APScheduler
        try:
            from apscheduler import util
            
            # Store the original function
            original_astimezone = util.astimezone
            
            # Redefine the astimezone function
            def patched_astimezone(obj):
                import pytz
                
                # If None, return None
                if obj is None:
                    return None
                
                # If already a pytz timezone, return directly
                if hasattr(obj, 'localize') and callable(obj.localize):
                    return obj
                
                # If it's a string, convert to pytz timezone
                if isinstance(obj, str):
                    return pytz.timezone(obj)
                
                # For other timezone objects, convert to pytz
                if hasattr(obj, 'tzname') and callable(obj.tzname):
                    try:
                        return pytz.timezone(obj.tzname(None))
                    except:
                        return pytz.UTC
                
                # If nothing works, return UTC
                return pytz.UTC
            
            # Apply the patch
            util.astimezone = patched_astimezone
            print("✅ Patch applied to the astimezone function of APScheduler")
        except Exception as e:
            print(f"❌ Error applying patch to the astimezone function: {e}")
        
        # Modify the behavior of JobQueue without altering read-only methods
        try:
            # Import python-telegram-bot
            import telegram
            import inspect
            
            # Patch the Application builder to ensure the JobQueue uses the correct timezone
            try:
                from telegram.ext import ApplicationBuilder
                import pytz
                
                # Store the original build method
                original_build = ApplicationBuilder.build
                
                # Define a new build method that applies the timezone afterward
                def patched_build(self):
                    # Use the original build
                    app = original_build(self)
                    
                    # If the app has a job_queue, modify its scheduler when created
                    if hasattr(app, 'job_queue') and app.job_queue is not None:
                        # The scheduler will be created during start, so we cannot modify it now
                        # Instead, we'll monitor when Application.start is called
                        original_app_start = app.start
                        
                        # Wrapper for the start method
                        def app_start_wrapper():
                            # Call the original start
                            result = original_app_start()
                            
                            # Now try to configure the scheduler in the job_queue
                            try:
                                # If the scheduler has been created, set its timezone
                                if hasattr(app.job_queue, '_scheduler') and app.job_queue._scheduler is not None:
                                    app.job_queue._scheduler.timezone = pytz.UTC
                                    print("✅ Scheduler timezone set to pytz.UTC after initialization")
                            except Exception as e:
                                print(f"⚠️ Could not set scheduler timezone: {e}")
                            
                            return result
                        
                        # Replace the start method only in the app object, not in the class
                        app.start = app_start_wrapper
                        
                    return app
                
                # Apply the patch
                ApplicationBuilder.build = patched_build
                print("✅ Patch applied to ApplicationBuilder.build to fix JobQueue timezone")
            except Exception as e:
                print(f"❌ Error applying patch to ApplicationBuilder: {e}")
            
            # Alternative patch: monkeypatch the _AsyncIOScheduler class to ensure it always uses pytz.UTC
            try:
                from apscheduler.schedulers.asyncio import AsyncIOScheduler
                import pytz
                
                # Store the original constructor
                original_init = AsyncIOScheduler.__init__
                
                # New constructor that always uses pytz.UTC
                def patched_init(self, *args, **kwargs):
                    # Ensure timezone is pytz.UTC
                    kwargs['timezone'] = pytz.UTC
                    
                    # Call the original constructor
                    return original_init(self, *args, **kwargs)
                
                # Apply the patch
                AsyncIOScheduler.__init__ = patched_init
                print("✅ Patch applied to AsyncIOScheduler.__init__ to ensure use of pytz.UTC")
            except Exception as e:
                print(f"⚠️ Alternative patch not applied: {e}")
                
        except ImportError:
            print("⚠️ Python-telegram-bot not found, skipping JobQueue patches")
    except ImportError:
        print("⚠️ APScheduler not found, cannot apply patch")

# Apply the patch
patch_apscheduler()

# Try to import pytz first
try:
    import pytz
    print(f"✅ Pytz imported correctly: version {getattr(pytz, '__version__', 'unknown')}")
    utc = pytz.timezone('UTC')
    print(f"✅ UTC timezone created: {utc}")
    
    # Set up environment
    os.environ['TZ'] = 'UTC'
    if hasattr(time, 'tzset'):
        time.tzset()
    
    # Direct patch on internal classes of python-telegram-bot to avoid read-only attributes
    try:
        import telegram.ext._jobqueue as jobqueue_module
        import pytz
        
        # Check if the module has the JobQueue attribute
        if hasattr(jobqueue_module, 'JobQueue'):
            JobQueue = jobqueue_module.JobQueue
            
            # Get reference to the AsyncIOScheduler class
            import apscheduler.schedulers.asyncio
            AsyncIOScheduler = apscheduler.schedulers.asyncio.AsyncIOScheduler
            
            # Wrapper function for _create_scheduler (if it exists)
            if hasattr(JobQueue, '_create_scheduler'):
                original_create_scheduler = JobQueue._create_scheduler
                
                def patched_create_scheduler(self):
                    scheduler = original_create_scheduler(self)
                    if scheduler is not None:
                        # Modify the scheduler after creation
                        scheduler.timezone = pytz.UTC
                        print(f"✅ Scheduler timezone modified to {scheduler.timezone}")
                    return scheduler
                
                # Replace the method
                JobQueue._create_scheduler = patched_create_scheduler
                print("✅ Patch applied to the _create_scheduler method of JobQueue")
                
            # If we cannot modify _create_scheduler, try another entry point
            if hasattr(AsyncIOScheduler, '__init__'):
                print("ℹ️ Applying patch to AsyncIOScheduler constructor")
                
                # Store original constructor
                original_init = AsyncIOScheduler.__init__
                
                # Replace with version that always uses pytz.UTC
                def ensure_pytz_timezone(func):
                    def wrapper(self, *args, **kwargs):
                        # Ensure timezone is from pytz
                        if 'timezone' not in kwargs:
                            kwargs['timezone'] = pytz.UTC
                        elif kwargs['timezone'] is None:
                            kwargs['timezone'] = pytz.UTC
                        return func(self, *args, **kwargs)
                    return wrapper
                
                # Apply the decorator
                AsyncIOScheduler.__init__ = ensure_pytz_timezone(original_init)
                print("✅ Applied decorator to ensure pytz timezone in AsyncIOScheduler")
        
    except Exception as e:
        print(f"⚠️ Error applying direct patch: {e}")
    
except ImportError as e:
    print(f"❌ Error importing pytz: {e}")
    sys.exit(1)

# Run the original bot (removing BOM if present)
bot_script = sys.argv[1]
print(f"Running bot at: {bot_script}")

# Read the file content and remove BOM (U+FEFF) if present
with open(bot_script, 'r', encoding='utf-8') as f:
    content = f.read()
    # Check if the first character is BOM (U+FEFF)
    if content and ord(content[0]) == 0xFEFF:
        print("⚠️ Detected and removed BOM character (U+FEFF) from the start of the file")
        content = content[1:]  # Remove the first character (BOM)

# Execute the bot code without BOM
exec(compile(content, bot_script, 'exec'))