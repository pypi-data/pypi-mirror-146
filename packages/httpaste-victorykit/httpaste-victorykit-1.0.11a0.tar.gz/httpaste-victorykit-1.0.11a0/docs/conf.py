import os
import sys


# -- Project information -------------------------------------------------------

project = 'httpaste'
copyright = '2022 - Tiara Rodney (victoryk.it)'
author = 'Tiara Rodney <t.rodney@victoryk.it'

# The full version, including alpha/beta/rc tags
release = '1b'


# -- General configuration -----------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme',
    'sphinxcontrib.plantuml',
    'sphinxarg.ext',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']

exclude_patterns = [
    '_build',
    '_templates'
    'Thumbs.db',
    '.DS_Store',
    '.gitignore',
]


# -- Options for HTML output ---------------------------------------------------

html_theme = 'sphinx_rtd_theme'

#html_static_path = ['_static']


# -- Options for autodoc & autosummary -----------------------------------------


autosummary_generate = True

autosummary_mock_imports = [
    'httpaste.cgi',
    'httpaste.wsgi',
    'httpaste.fcgi'
]

if tags.has('readme'):
    autosummary_generate = False
    master_doc = 'README'
    exclude_patterns.append('index.rst')
    exclude_patterns.append('_stubs')
    exclude_patterns.append('guide')
