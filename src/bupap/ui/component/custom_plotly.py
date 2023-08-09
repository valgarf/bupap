from __future__ import annotations

from typing import Dict, Union

from nicegui import globals, ui

try:
    import plotly.graph_objects as go
    globals.optional_features.add('plotly')
except ImportError:
    pass


class CPlotly(ui.plotly, component='custom_plotly.vue'):
    pass
