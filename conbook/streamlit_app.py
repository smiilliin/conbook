import importlib.util
import os
import subprocess
import sys
from pathlib import Path


def _ensure_required_packages() -> None:
    packages = {
        "streamlit": "streamlit",
        "plotly": "plotly",
        "pandas": "pandas",
        "openai": "openai",
        "dotenv": "python-dotenv",
    }
    for module_name, package_name in packages.items():
        if importlib.util.find_spec(module_name) is None:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def _bind_project_root() -> None:
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault("CONBOOK_ROOT", str(project_root))


_bind_project_root()
_ensure_required_packages()

import streamlit as st

from conbook.components.book_info import render_book_info
from conbook.components.book_tabs import render_insight_page
from conbook.components.chat import render_chat
from conbook.components.sidebar import render_sidebar
from conbook.components.visualization import render_visualization_page
from conbook.utils.api import create_client
from conbook.utils.session import init_session_state, set_page_config


def main() -> None:
    set_page_config()
    init_session_state()
    render_sidebar()

    client = create_client()
    step = st.session_state.step

    if step == 0:
        render_book_info()
    elif step == 1:
        render_chat(client)
    elif step == 2:
        render_insight_page()
    else:
        render_visualization_page()


if __name__ == "__main__":
    main()
