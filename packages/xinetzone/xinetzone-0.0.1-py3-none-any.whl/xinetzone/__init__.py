"""Sphinx demo."""
from pathlib import Path

__version__ = '0.0.1'
__version_full__ = __version__


def get_html_theme_path():
    """
    Return path to Sphinx templates folder.
    """
    parent = Path(__file__).parent.resolve()
    theme_path = parent / "themes" / "xinetzone"
    return theme_path


def get_html_template_path():
    theme_dir = get_html_theme_path()
    return theme_dir/"_templates"


def update_context(app, pagename, templatename, context, doctree):
    context["xinetzone_version"] = __version_full__


def setup(app):
    theme_dir = get_html_theme_path()
    app.add_html_theme("xinetzone", str(theme_dir))
    app.connect("html-page-context", update_context)
    template_path = get_html_template_path()
    app.config.templates_path.append(str(template_path))
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
