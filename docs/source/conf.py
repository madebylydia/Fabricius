# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import fabricius

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "Fabricius"
copyright = "2022-present, Julien Mauroy"
author = "Julien Mauroy"

# The full version, including alpha/beta/rc tags
release = fabricius.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: "list[str]" = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
html_sidebars = {
    "/": [],
    "/index": [],
    "**": ["sidebar-nav-bs", "sidebar-ethical-ads"],
}

# -- Extension configuration -------------------------------------------------
coverage_show_missing_items = True

# -- Options for Pydata theme ------------------------------------------------
announcement = "⚠️ The documentation is not ready and much work is still needed. Please consider the documentation as a draft only. See the home page for more information."
html_theme_options = {
    "logo": {
        "image_light": "logo-dark.png",
        "image_dark": "logo-white.png",
        "text": "Fabricius",
    },
    "announcement": announcement,
    "icon_links": [
        {
            "name": "Go to Fabricius repo",
            "url": "https://github.com/madebylydia/Fabricius",
            "icon": "fa-brands fa-github-alt",
            "type": "fontawesome",
        },
        {
            "name": "Join the Discord",
            "url": "https://discord.gg/FFpHbSbNj5",
            "icon": "fa-brands fa-discord",
            "type": "fontawesome",
        },
    ],
}


# -- Options for autodoc extension ------------------------------------------
autodoc_default_options = {
    "member-order": "bysource",
}
autoclass_content = "both"


# -- Options for coverage extension ------------------------------------------
coverage_show_missing_items = True

# -- Options for intersphinx extension ---------------------------------------
intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
    "rich": ("https://rich.readthedocs.io/en/stable", None),
}
