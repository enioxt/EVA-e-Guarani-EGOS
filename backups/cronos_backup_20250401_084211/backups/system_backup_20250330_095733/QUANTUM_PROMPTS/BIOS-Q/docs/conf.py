#!/usr/bin/env python3
"""
EVA & GUARANI - Documentation Configuration
----------------------------------------
This module provides the Sphinx configuration for the
EVA & GUARANI BIOS-Q documentation.

Version: 7.5
Created: 2025-03-26
"""

import os
import sys
from datetime import datetime

# Add BIOS-Q to Python path
sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "EVA & GUARANI BIOS-Q"
copyright = f"{datetime.now().year}, EVA & GUARANI Team"
author = "EVA & GUARANI Team"
version = "7.5"
release = "7.5"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "myst_parser",
]

# Source file parsers
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

# The master toctree document
master_doc = "index"

# List of patterns to ignore when looking for source files
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use
pygments_style = "sphinx"

# HTML output options
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Custom sidebar templates
html_sidebars = {
    "**": [
        "about.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
        "donate.html",
    ]
}

# Theme options
html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "style_nav_header_background": "#2980B9",
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# Custom CSS
html_css_files = [
    "custom.css",
]

# LaTeX output options
latex_elements = {
    "papersize": "letterpaper",
    "pointsize": "10pt",
    "preamble": "",
    "figure_align": "htbp",
}

# Grouping the document tree into LaTeX files
latex_documents = [
    (
        master_doc,
        "EVAGuaraniBIOSQ.tex",
        "EVA & GUARANI BIOS-Q Documentation",
        "EVA & GUARANI Team",
        "manual",
    ),
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "torch": ("https://pytorch.org/docs/stable", None),
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Todo settings
todo_include_todos = True

# GitHub links
html_context = {
    "display_github": True,
    "github_user": "evaguarani",
    "github_repo": "bios-q",
    "github_version": "main",
}
