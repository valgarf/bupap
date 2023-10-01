from nicegui import ui


def separator_line():
    return ui.element("hr").classes("h-px my-1 bg-gray-200 border-0 dark:bg-gray-700")
