import random
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

class Flybar(bar.Bar):
    def __init__(self, widgets, size, **config) -> None:
        self.hiding = True
        super().__init__(widgets, size, **config)

    def show_bar_callback(self) -> None:
        if self.hiding:
            _, y = qtile.core.get_mouse_position()
            if y > qtile.current_screen.height - self.initial_size:
                self.show(True)
            qtile.call_later(0.25, self.show_bar_callback)

    def show(self, is_show=True):
        if is_show:
            self.hiding = False
        else:
            self.hiding = True
            qtile.call_later(0.25, self.show_bar_callback)
        super().show(is_show)

    def process_pointer_leave(self, x: int, y: int) -> None:
        super().process_pointer_leave(x, y)
        self.show(False)


flybar = Flybar(
    [
        widget.CurrentLayout(),
        widget.Notify(),
        widget.Prompt(),
        # etc
    ],
    24
)


@hook.subscribe.startup
def start_flybar_timer():
    flybar.show(False)
    qtile.call_later(0.25, flybar.show_bar_callback)


@hook.subscribe.startup_complete
def widget_hover_change_cursor():
    
        for s in qtile.screens:
            bars = []  # get list of bars
            for b in ["top", "bottom", "left", "right"]:  # only the last bar works???
                if getattr(s, b) is not None:
                    bars.append(getattr(s, b))

            for bar in bars:
               for w in bar.widgets:
                    if w.mouse_callbacks:  # widget can be clicked
                       def enter(*args, **kwargs):
                            bar.window.window.set_cursor("hand2")
                            # run original mouse enter code if widget defined it
                            w.mouse_enter(*args, **kwargs)
                       w.mouse_enter = enter

                       def leave(*args, **kwargs):
                            bar.window.window.set_cursor("left_ptr")
                            w.mouse_leave(*args, **kwargs)