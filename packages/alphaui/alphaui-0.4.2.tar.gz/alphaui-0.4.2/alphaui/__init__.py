import pkg_resources

from alphaui.blocks import Blocks, Column, Row, Tab
from alphaui.flagging import (
    CSVLogger,
    FlaggingCallback,
    HuggingFaceDatasetSaver,
    SimpleCSVLogger,
)
from alphaui.interface import Interface, close_all, reset_all
from alphaui.mix import Parallel, Series
from alphaui.routes import get_state, set_state
from alphaui.static import Button, Markdown

# current_pkg_version = pkg_resources.require("gradio")[0].version
# __version__ = current_pkg_version
