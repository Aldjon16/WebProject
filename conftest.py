"""
pytest-django configuration.

Adds the parent directory of the repo to sys.path so that the symlink
``edukimi_femijeve -> WebProject`` makes the app importable under its
declared Django app name.
"""

import os
import sys

_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

# Re-export for pytest-django
django_settings = "edukimi_femijeve.test_settings"
