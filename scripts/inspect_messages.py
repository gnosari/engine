#!/usr/bin/env python3
"""
Script to inspect Celery queue messages
"""

import redis
import json
import pickle
import base64
from datetime import datetime
from typing import List, Dict, Any

def connect_redis(host='localhost', port=6379, db=0):
    """Connect to Redis broker."""
    try:
        r = redis.Redis(host=host, port=port, db=db, decode_responses=False)
        r.ping()
        return r
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        return None

def inspect_queue_messages(queue_name='gnosari_queue', max_messages=10):
    """Inspect messages in Celery queue."""
    r = connect_redis()
    if not r:
        return
    
    print(f"🔍 Inspecting queue: {queue_name}")
    print("=" * 50)
    
    # Check queue length
    queue_length = r.llen(queue_name)
    print(f"Queue length: {queue_length}")
    
    if queue_length == 0:
        print("Queue is empty")
        return
    
    # Get messages
    messages = r.lrange(queue_name, 0, min(max_messages - 1, queue_length - 1))
    
    for i, message in enumerate(messages):
        print(f"\n📨 Message {i + 1}:")
        print("-" * 30)
        
        try:
            # Celery messages are usually JSON with base64-encoded body
            decoded_message = json.loads(message.decode('utf-8'))
            
            print(f"Task ID: {decoded_message.get('id', 'Unknown')}")
            print(f"Task: {decoded_message.get('task', 'Unknown')}")
            print(f"ETA: {decoded_message.get('eta', 'None')}")
            print(f"Expires: {decoded_message.get('expires', 'None')}")
            
            # Decode the body (task arguments)
            body = decoded_message.get('body')
            if body:
                try:
                    # Body is base64 encoded
                    decoded_body = base64.b64decode(body)
                    # Then pickle decoded
                    task_args = pickle.loads(decoded_body)
                    print(f"Arguments: {task_args}")
                    
                    # If it's our tool execution message, extract details
                    if task_args and len(task_args) > 0:
                        first_arg = task_args[0]
                        if isinstance(first_arg, dict):
                            print("\n🔧 Tool Execution Details:")
                            print(f"  Tool Name: {first_arg.get('tool_name', 'Unknown')}")
                            print(f"  Task ID: {first_arg.get('task_id', 'Unknown')}")
                            print(f"  Agent ID: {first_arg.get('agent_id', 'Unknown')}")
                            print(f"  Session ID: {first_arg.get('session_id', 'Unknown')}")
                            print(f"  Module: {first_arg.get('tool_module', 'Unknown')}")
                            print(f"  Class: {first_arg.get('tool_class', 'Unknown')}")
                            print(f"  Created: {first_arg.get('created_at', 'Unknown')}")
                            
                            # Show tool arguments
                            tool_args = first_arg.get('tool_args')
                            if tool_args:
                                try:
                                    parsed_tool_args = json.loads(tool_args)
                                    print(f"  Tool Args: {json.dumps(parsed_tool_args, indent=4)}")
                                except:
                                    print(f"  Tool Args (raw): {tool_args}")
                
                except Exception as e:
                    print(f"Failed to decode body: {e}")
                    print(f"Raw body: {body[:100]}...")
            
            # Show other properties
            props = decoded_message.get('properties', {})
            if props:
                print(f"Priority: {props.get('priority', 'None')}")
                print(f"Delivery Mode: {props.get('delivery_mode', 'None')}")
        
        except Exception as e:
            print(f"Failed to parse message: {e}")
            print(f"Raw message: {message[:200]}...")

def inspect_all_queues():
    """Inspect all Celery-related queues."""
    r = connect_redis()
    if not r:
        return
    
    # Get all keys
    keys = r.keys('*')
    celery_queues = [key.decode('utf-8') for key in keys if b'queue' in key.lower() or b'celery' in key.lower()]
    
    print("🔍 Found Celery-related queues:")
    for queue in celery_queues:
        length = r.llen(queue)
        print(f"  {queue}: {length} messages")
    
    return celery_queues

def monitor_queue_real_time(queue_name='gnosari_queue', interval=2):
    """Monitor queue in real-time."""
    import time
    
    r = connect_redis()
    if not r:
        return
    
    print(f"📊 Monitoring queue '{queue_name}' in real-time...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            length = r.llen(queue_name)
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Queue length: {length}")
            
            if length > 0:
                # Show latest message
                latest = r.lindex(queue_name, 0)
                try:
                    decoded = json.loads(latest.decode('utf-8'))
                    task_id = decoded.get('id', 'Unknown')[:8]
                    task_name = decoded.get('task', 'Unknown')
                    print(f"  Latest: {task_name} ({task_id}...)")
                except:
                    pass
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "all":
            inspect_all_queues()
        elif command == "monitor":
            queue = sys.argv[2] if len(sys.argv) > 2 else "gnosari_queue"
            monitor_queue_real_time(queue)
        elif command == "inspect":
            queue = sys.argv[2] if len(sys.argv) > 2 else "gnosari_queue"
            max_msgs = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            inspect_queue_messages(queue, max_msgs)
        else:
            print("Usage:")
            print("  python inspect_messages.py all                    # List all queues")
            print("  python inspect_messages.py inspect [queue] [max]  # Inspect messages") 
            print("  python inspect_messages.py monitor [queue]        # Real-time monitoring")
    else:
        # Default: inspect main queue
        inspect_queue_messages()