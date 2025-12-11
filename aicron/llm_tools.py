# Copyright (c) 2025 dev-droid. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for details.

import os
import glob
from typing import List

def list_dir(path: str) -> str:
    """
    Safely list directories and files in a given path.
    """
    try:
        # Basic security check: forbid going above root or into sensitive areas if needed
        # For this MVP, we just ensure it exists
        if not os.path.exists(path):
            return f"Error: Path '{path}' does not exist."
        
        items = os.listdir(path)
        # Limit output to prevent context overflow
        if len(items) > 50:
            return "\n".join(items[:50]) + f"\n... (and {len(items)-50} more)"
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

def find_file(pattern: str, path: str = ".") -> str:
    """
    Find files matching a glob pattern in a given path.
    """
    try:
        if not path.endswith(os.path.sep):
            path += os.path.sep
        
        # Recursive search if pattern includes **
        full_pattern = os.path.join(path, pattern)
        matches = glob.glob(full_pattern, recursive="**" in pattern)
        
        if not matches:
            return "No matches found."
        
        # Limit matches
        if len(matches) > 20:
            return "\n".join(matches[:20]) + f"\n... (and {len(matches)-20} more)"
        return "\n".join(matches)
    except Exception as e:
        return f"Error finding file: {str(e)}"
