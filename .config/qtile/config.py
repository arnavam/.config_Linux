from powerline.bindings.qtile.widget import PowerlineTextBox
from curses.panel import top_panel
import random
import os
import json
import re
import socket
import subprocess
from libqtile.log_utils import logger
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen,ScratchPad,DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras.widget.decorations import BorderDecoration
from newclass import Flybar
from qtile_extras.resources import wallpapers
from qtile_extras.widget.decorations import RectDecoration
mod = "mod4"
terminal = "xterm"

# _  __  _____  __   __
#| |/ / | ____| \ \ / /
#| ' /  |  _|    \ V / 
#| . \  | |___    | |  
#|_|\_\ |_____|   |_|

groups = [
          Group('1', label=" 阿 ",layout='monadtall'),
          Group('2', label=" 尔 ",layout='monadtall'),
          Group('3', label=" 纳 ",layout='monadtall'),
          Group('4', label=" 夫 ",layout='monadtall'),
          Group('5', label=" ? ",layout='monadtall')
         
]  
                     
keys = [
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    # Key([mod], "c", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "v", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "x", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod], "space", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "a", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"],"Return",lazy.layout.toggle_split(),desc="Toggle bw split sides of stack"),
    Key([mod], "m", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
     Key([mod,"shift"], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "w",lazy.window.togroup('5', switch_group=False), desc="Kill focused window"),
    Key([mod],"f",lazy.window.toggle_fullscreen(),
                    desc="Toggle fullscreen on the focused window"),
    Key([mod,"control"], "p", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "s", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    #custom

    Key([mod], "b",lazy.spawn("firefox"),desc="Open browser"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn a commandbro using a prompt widget"),
    #Key([mod, "shift"], "q", lazy.spawn("dm-logout"), desc="Logout menu"),
    Key([mod], "f6", lazy.spawn('''brightnessctl -d "intel_backlight" set 10%+'''), desc='brightness UP'),
    Key([mod], "f5", lazy.spawn('''brightnessctl -d "intel_backlight" set 10%-'''), desc='brightness Down'),
    Key([mod], "f1",lazy.spawn("systemctl suspend"),desc="sleep mode"),

    Key([mod],"n", lazy.spawn("nemo"), desc='file manager'),
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
  
      Key([mod],"return",lazy.window.toggle_minimize(),desc="minimize"),

    Key([mod], "t", lazy.group['note'].dropdown_toggle("notpad")),
    Key([mod], "Tab", lazy.group.focus_back(), desc="Alternate between two most recent windows"), 
    Key([mod], "j", lazy.group.next_window(), desc="[Layout] Focus next window"),

    Key([mod], "k", lazy.group.prev_window(), desc="[Layout] Focus next window"),
]
#  ____   ____     ___    _   _   ____    ____  
# / ___| |  _ \   / _ \  | | | | |  _ \  / ___| 
#| |  _  | |_) | | | | | | | | | | |_) | \___ \ 
#| |_| | |  _ <  | |_| | | |_| | |  __/   ___) |
# \____| |_| \_\  \___/   \___/  |_|     |____/ 

'''
groups = [Group(" 阿 ", layout='monadtall',),
          Group(" 尔 ", layout='monadtall'),
          Group(" 纳 ", layout='monadtall'),
          Group(" 夫 ", layout='monadtall'),
          Group(" ? ", layout='monadtall'), 
  

]
'''
# def load_colors():
#     home = os.path.expanduser("~")
#     with open(f"{home}/.cache/wal/colors.json") as f:
#         colors = json.load(f)
#     return colors

# colors = load_colors()


for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
    
groups.append(
                #=-/ Scratchpad groups /-=#
   ScratchPad("note",[DropDown( "notpad",['/home/arnav/applications/Joplin-3.0.14.AppImage'], x=0.05, y=0.02, width=0.50, height=0.6, on_focus_lost_hide=False)]
    )
)
# _          _     __   __   ___    _   _   _____ 
#| |        / \    \ \ / /  / _ \  | | | | |_   _|
#| |       / _ \    \ V /  | | | | | | | |   | |  
#| |___   / ___ \    | |   | |_| | | |_| |   | |  
#|_____| /_/   \_\   |_|    \___/   \___/    |_|  
                                                 
layouts = [
    layout.MonadTall(  
        border_focus='#f94449',
	    border_normal='4B0082',
        border_width=2,
        margin=7,
        new_client_position='top',
        ratio=0.5
        ),
    layout.Columns( 
        margin= [5,5,5,5], 
        border_focus='#f94Joplin-3.0.14.AppImage449',
	    border_normal='4B0082',
        border_width=2,
        num_columns=2),

    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.Bsp(),
    layout.Matrix(),
    layout.MonadTall(),
    layout.MonadWide(),
    layout.RatioTile(),
    layout.Tile(),
    layout.TreeTab(),
    layout.VerticalTile(),
    layout.Zoomy(),
]

 
 
#    _____   _   _   _   _    ____   ____  
#   |  ___| | | | | | \ | |  / ___| / ___| 
#   | |_    | | | | |  \| | | |     \___ \ 
#   |  _|   | |_| | | |\  | | |___   ___) |
#   |_|      \___/  |_| \_|  \____| |____/ 
#                                     
def longNameParse(text): 
   for string in ["Chromium", "Firefox","config.py","qtile ","Code" ] :
    if string in text:
        text = string

   for string in ["~"] :
    if string in text:
        text = "terminal"
    else: 
        text = text.split('-')[0]
   return text

def no_text(text):
        return ""

def search():
    qtile.cmd_spawn("rofi -show drun")
    
def powermenu():
    qtile.spawn("bash /home/arnav/.config/rofi/powermenu/type-2/powermenu.sh")
#   __     ___    ____  ___    _    ____  _     _____ 
#   \ \   / / \  |  _ \|_ _|  / \  | __ )| |   | ____|
#    \ \ / / _ \ | |_) || |  / _ \ |  _ \| |   |  _|  
#     \ V / ___ \|  _ < | | / ___ \| |_) | |___| |___ 
#      \_/_/   \_\_| \_\___/_/   \_\____/|_____|_____|

pic1= widget.Image( filename='/home/arnav/.config/qtile/Assets/6.png',)

wallpaper_dir = '/home/arnav/Pictures/wallpaper'
def wallpaper():
    wallpapers = [os.path.join(wallpaper_dir, f) for f in os.listdir(wallpaper_dir) if f.endswith(('jpg', 'png'))]
    if wallpapers:
        wallpaper = random.choice(wallpapers)
    else:
        print(f"No wallpapers found in {wallpaper_dir}")
    return wallpaper
w2=wallpaper()

# Load Pywal colors
home = os.path.expanduser('~')
colors_path = os.path.join(home, '.cache', 'wal', 'colors.json')

if os.path.isfile(colors_path):
    with open(colors_path) as f:
        colordict = json.load(f)
else:
    raise FileNotFoundError(f"Colorscheme file not found: {colors_path}")

a0=(colordict['colors']['color0'])#very dark
a1=(colordict['colors']['color1'])#medium

a2=(colordict['colors']['color2'])#medium
a3=(colordict['colors']['color3'])#medium-light
a4=(colordict['colors']['color4'])#medium-light
a5=(colordict['colors']['color5'])#medium-light
a6=(colordict['colors']['color6'])#medium
a7=(colordict['colors']['color8'])#medium
a8=(colordict['colors']['color7'])#light

# b2=(colordict['colors']['color9'])#same as 1

f=(colordict['colors']['color15'])
pr='#282738'
# a1='#ffba08'
# a2='#faa307'
# a3='#e85d04'
# a4='#9d0208'
# a5='#6a040f'
# a6='#370617'
# a7='#03071e'
n='#00000000'
b1='#1E3F66'
b2='#03045e'
b3='000000'
p1='#FFE5B4'
p2='#CAA9E0'
powerline = {
    "decorations": [
        PowerLineDecoration(path='rounded_left',
                            #extrawidth=5,
                            #shift=4,
                            #size=10
                            )
    ]
}

powerline1 = {
    "decorations": [
        PowerLineDecoration(path='rounded_right',
                            #extrawidth=5,
                            #shift=4,
                            #size=10
                            )
    ]
}

rectangle1 = {
    "decorations": [
        RectDecoration(colour="", radius=80, filled=True, padding_y=4, group=True)
    ],
    "padding": 16,
}
#https://unsplash.it/1920/1080?random
w=wallpapers.WALLPAPER_TRIANGLES_ROUNDED
qtile.spawn(f"wal -i {w2}")
#__        __  ___   ____     ____   _____   _____   ____  
#\ \      / / |_ _| |  _ \   / ___| | ____| |_   _| / ___| 
# \ \ /\ / /   | |  | | | | | |  _  |  _|     | |   \___ \ 
#  \ V  V /    | |  | |_| | | |_| | | |___    | |    ___) |
#   \_/\_/    |___| |____/   \____| |_____|   |_|   |____/ 
#

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        #  wallpaper=w2,
        # wallpaper_mode="fill",
        bottom=bar.Bar(
            [   
                 widget.CurrentLayoutIcon(
                    background=a7,
                    # foreground=a1,#'#CAA9E0',
                    #padding = 4,
                    scale = 0.6,
                    **powerline
                ),

                widget.CurrentLayout(
                    background=a8,#'#FFE5B4',
                    foreground=a0,
                    fmt='{}',
                    font="JetBrains Mono Bold",
                    fontsize= 13,
                    **powerline
                ),

               
                widget.Image(
                    filename='/home/arnav/.config/qtile/Assets/search1.svg',
                    margin=5,
                    background=a7,
                    scale=True,
                    mouse_callbacks={"Button1": search},
                    **powerline,
                ),
                widget.Prompt(),
                widget.TaskList(
                   
                    unfocused_border=p1,
                    border='#BFB4E2',
                    font='JetBrains Mono Bold',
                    background='#00000000',
                    foreground='#1f3050',
                    markup_minimized= "._<span>{}</span>",
                    highlight_method='block',
                    rounded=True,
                    parse_text=longNameParse,
                    margin_y=0,
                    **powerline1
                 ),
                 widget.Pomodoro(
                    
                    num_pomodori=4,
                    length_pomodori=25,
                    length_short_break=5,
                    length_long_break=15,
                    color_inactive='#ffff00',
                    color_break='#00A36C',
                    color_active='#ff0000',
                    notification_on=True,
                    prefix_inactive="🍅",
                    prefix_active="🍅 ",
                    prefix_break="☕ ",
                    prefix_long_break="☕ ",
                    prefix_paused="🍅 PAUSED",
                    **powerline1
                ),
                widget.WidgetBox(
                    fmt='>',
                    widgets=[
               widget.QuickExit(),
               widget.Bluetooth(
                   **powerline1
               ),

                    widget.Clipboard(
                     **powerline1
                ),
                 widget.Systray(
                    **powerline1
                    ),
                ],**powerline1),
                # widget.BatteryIcon(
                #     theme_path='/home/arnav/.config/qtile/Assets/Battery/',
                #     background=a8,
                #     scale=1,
                    
                # ),
                widget.UPowerWidget(
                    
                    battery_height=9,
                    battery_width =16,
                    fill_critical='#880808',
                    fill_low='#FFA500',
                    fill_normal=a8,
                    foreground= a0,
                    fill_charge='#5BC236',
                    margin=0,
              border_charge_colour='#FFFFFF',
                    border_colour=a8,
                    background=a4,
             ),
                
                widget.Battery(
                    # font='JetBrains Mono Bold',
                    background=a4,
                    foreground=a8,
                    format='{percent:2.0%}',
                    fontsize=11,
                    **powerline1
                ),
             # widget.BrightnessControl(
                    
                # ),
                # widget.ALSAWidget(),
                # widget.MemoryGraph(
                #     background=a1,
                    
                # ),
                widget.Memory(
                 foreground = a0,
                 background=a1,
                 fontsize=11,
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
                 format = '{MemUsed: .0f}{mm}',
                 fmt = '🖥{} ',
                 **powerline1
               
                 ),

                
                

    
               
                
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.StatusNotifier(),
                
                
                widget.AnalogueClock(
                    adjust_y=2,
                    adjust_x=0,
                    background=a0,
                    face_border_colour=a8,#'#CAA9E0',
                    face_shape = 'circle',
                    hour_length=0.4,
                    hour_size=1,
                    margin=3,
                    minute_length=0.7,
                    minute_size=1
                ),


                widget.Clock(
                    format='%I:%M:%S %p',
                    background=a0,
                    foreground=a8,#'#CAA9E0',
                    # font="JetBrains Mono Bold",
                     fontsize=10,
                )
                
            ],
        24,
        background='#00000000',
        border_width=[0, 6, 0, 0],  # Draw top and bottom borders
        border_color=['#00000000', a0, a1, a5],  # Borders are magenta
        #border_color = '#282738',
        opacity=1
            
        ),
# ____        ,      _____    ___  
#|  _ \      /\     |  __ \  |__ \ 
#| |_) |    /  \    | |__) |    ) |
#|  _ <    / /\ \   |  _  /    / / 
#| |_) |  / ____ \  | | \ \   / /_ 
#|____/  /_/    \_\ |_|  \_\ |____|

    top=Flybar([
        widget.Image(
                    filename='/home/arnav/.config/qtile/Assets/qtile.jpeg',
                     margin=1,
                    padding=3,
                        fontsize=16,
                    background='#265575',
                    # scale=True,
                    mouse_callbacks={"Button1": powermenu},
                   decorations=[

                            PowerLineDecoration(path='arrow_right',
                            # extrawidth=5,
                             shift=0,
                            size=5
                            )
                        ]
                ),
                widget.Spacer(background=n),
                PowerlineTextBox(update_interval=2, side='left'),
                widget.GroupBox(
                    background=n,
                    highlight_method='block',
                    this_current_screen_border="#FF0000",
                    borderwidth=9,
                    
                    decorations =[BorderDecoration(
                        colour= "#FF0000",
                        border_width=[0,0,3,0],
                        # padding_x=5,
                        padding_y=None,)
                        ],
                    ),
                widget.Spacer(background=n)
             
            ], 
            15,background='#00000000', opacity=1),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]


# __  __  ___  _   _ ____  _____ 
#|  \/  |/ _ \| | | / ___|| ____|
#| |\/| | | | | | | \___ \|  _|  
#| |  | | |_| | |_| |___) | |___ 
#|_|  |_|\___/ \___/|____/|_____|
                                
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Click([mod], "Button1", lazy.hide_show_bar()),
]







dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart_once.sh')
    subprocess.Popen([home])
    
# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "QTILE"
