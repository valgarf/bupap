from __future__ import annotations

from typing import Dict, Union

from nicegui import optional_features, ui

try:
    import plotly.graph_objects as go

    optional_features.register("plotly")
except ImportError:
    pass


class CPlotly(ui.plotly, component="custom_plotly_sfc.vue"):
    pass
