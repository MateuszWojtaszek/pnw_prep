"""Konfiguracja Sphinksa — konwencja scientific Python (NumPy docstrings)."""

from importlib.metadata import version as _pkg_version

# -- Projekt -----------------------------------------------------------------

project = "pnw-prep"
author = "Mateusz Wojtaszek"
copyright = "2026, Mateusz Wojtaszek"  # noqa: A001
release = _pkg_version("pnw-prep")
version = ".".join(release.split(".")[:2])

# -- Rozszerzenia ------------------------------------------------------------
# autodoc/autosummary/napoleon/intersphinx/viewcode są wbudowane w Sphinksa.

extensions = [
    "sphinx.ext.autodoc",            # czyta docstringi z zaimportowanego pakietu
    "sphinx.ext.autosummary",        # generuje tabele-skróty i strony per obiekt
    "sphinx.ext.napoleon",           # rozumie docstringi NumPy/Google
    "sphinx.ext.intersphinx",        # linki do dokumentacji innych projektów
    "sphinx.ext.viewcode",           # link "source" przy każdym obiekcie
    "sphinx.ext.mathjax",            # wzory LaTeX-owe w docstringach
    "sphinx_autodoc_typehints",      # adnotacje typów -> opisy parametrów
    "sphinx_copybutton",             # przycisk kopiowania na blokach kodu
    "myst_parser",                   # strony pisane w Markdownie zamiast rST
]

# -- Źródła: Markdown obok reStructuredText ----------------------------------

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
myst_enable_extensions = ["dollarmath", "amsmath", "deflist", "colon_fence"]

# -- autodoc / autosummary ---------------------------------------------------

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": False,     # obiekty bez docstringa nie trafiają do docs
    "show-inheritance": True,
    "member-order": "bysource",
}
# Typy trafiają do opisu parametrów zamiast puchnąć w sygnaturze.
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented_params"
typehints_defaults = "comma"

# -- napoleon: konwencja NumPy -----------------------------------------------

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_rtype = False          # typ zwracany w linii "Returns", nie osobno
napoleon_preprocess_types = True

# -- intersphinx -------------------------------------------------------------
# Dzięki temu `np.ndarray` w docstringu staje się linkiem do docs NumPy.

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

# -- HTML --------------------------------------------------------------------

html_theme = "furo"
html_title = f"{project} {release}"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
