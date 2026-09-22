import os
import sys

import django

sys.path.insert(0, os.path.abspath(".."))
os.environ["DJANGO_SETTINGS_MODULE"] = "job_tracker.settings"
django.setup()

project = "CareerTrack"
copyright = "2026, Jonah Ngubeni"
author = "Jonah Ngubeni"
release = "1.0.0"

extensions = ["sphinx.ext.autodoc"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
autodoc_member_order = "bysource"
