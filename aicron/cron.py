# Copyright (c) 2025 dev-droid. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

from croniter import croniter
from datetime import datetime
from crontab import CronTab
import platform
import shutil
import os

def validate_expression(expression: str) -> bool:
    """
    Validates if a cron expression is valid using croniter.
    """
    try:
        return croniter.is_valid(expression)
    except Exception:
        return False

def get_next_schedule(expression: str, count: int = 5) -> list[str]:
    """
    Returns the next 'count' run times for verification.
    """
    if not validate_expression(expression):
        return []
        
    try:
        iter = croniter(expression, datetime.now())
        return [str(iter.get_next(datetime)) for _ in range(count)]
    except Exception:
        return []

def add_job(expression: str, command: str, comment: str, user: bool = True) -> bool:
    """
    Adds a new job to the user's crontab.
    On Windows, if no 'crontab' command is found, falls back to a local file 'cron.tab'.
    """
    try:
        if platform.system() == "Windows":
             # Check if crontab executable exists
             if not shutil.which("crontab"):
                 print(" [System] 'crontab' executable not found. Falling back to local 'cron.tab' file.")
                 # Use absolute path for safety
                 tab_file = os.path.abspath('cron.tab')
                 # Create file if not exists
                 if not os.path.exists(tab_file):
                     with open(tab_file, 'w') as f:
                         f.write("# Local crontab file for ai-cron testing\n")
                 
                 cron = CronTab(tabfile=tab_file)
             else:
                 cron = CronTab(user=user)
        else:
            cron = CronTab(user=user)

        job = cron.new(command=command, comment=comment)
        job.setall(expression)
        
        if not job.is_valid():
            print("Job invalid.")
            return False
            
        cron.write()
        return True
    except Exception as e:
        print(f"Error writing to crontab: {e}")
        return False

if __name__ == "__main__":
    # Test
    expr = "0 8 * * *"
    print(f"Validating '{expr}': {validate_expression(expr)}")
    print(f"Next runs: {get_next_schedule(expr)}")

