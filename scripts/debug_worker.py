#!/usr/bin/env python3
"""
Debug worker that logs detailed message information
"""

import json
import logging
from celery.signals import task_prerun, task_postrun, task_failure

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s: %(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Log task details before execution."""
    logger.info(f"🚀 TASK STARTING")
    logger.info(f"   Task ID: {task_id}")
    logger.info(f"   Task Name: {task}")
    logger.info(f"   Args: {args}")
    logger.info(f"   Kwargs: {kwargs}")
    
    # If it's our tool execution task, log details
    if args and len(args) > 0:
        try:
            message_data = args[0]
            if isinstance(message_data, dict):
                logger.info(f"📧 MESSAGE DETAILS:")
                logger.info(f"   Tool: {message_data.get('tool_name')}")
                logger.info(f"   Module: {message_data.get('tool_module')}")
                logger.info(f"   Class: {message_data.get('tool_class')}")
                logger.info(f"   Agent: {message_data.get('agent_id')}")
                logger.info(f"   Session: {message_data.get('session_id')}")
                logger.info(f"   Created: {message_data.get('created_at')}")
                
                # Log tool arguments
                tool_args = message_data.get('tool_args')
                if tool_args:
                    try:
                        parsed_args = json.loads(tool_args)
                        logger.info(f"   Tool Args: {json.dumps(parsed_args, indent=2)}")
                    except:
                        logger.info(f"   Tool Args (raw): {tool_args}")
        except Exception as e:
            logger.warning(f"Failed to parse message details: {e}")

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **kwds):
    """Log task completion."""
    logger.info(f"✅ TASK COMPLETED")
    logger.info(f"   Task ID: {task_id}")
    logger.info(f"   State: {state}")
    logger.info(f"   Return Value: {str(retval)[:200]}...")

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwds):
    """Log task failures."""
    logger.error(f"❌ TASK FAILED")
    logger.error(f"   Task ID: {task_id}")
    logger.error(f"   Exception: {exception}")
    logger.error(f"   Traceback: {traceback}")

if __name__ == "__main__":
    from gnosari.queue.app import celery_app
    
    logger.info("🔧 Starting debug worker with detailed message logging...")
    
    # Start worker with detailed logging
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--concurrency=1',
        '--queues=gnosari_queue'
    ])