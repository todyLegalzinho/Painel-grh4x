import json
from pathlib import Path

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

BG = (0.035, 0.035, 0.045, 1)
PANEL = (0.085, 0.075, 0.09, 1)
RED = (0.92, 0.055, 0.16, 1)
WHITE = (0.94, 0.93, 0.95, 1)
MUTED = (0.62, 0.60, 0.64, 1)
GREEN = (0.20, 0.85, 0.48, 1)


class PanelCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(14)
        self.spacing = dp(9)
        with self.canvas.before:
            Color(*PANEL)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size


class RedPanelApp(App):
    title = "GRH4X RED PANEL"

    def build(self):
        Window.clearcolor = BG
        self.config_path = Path(self.user_data_dir) / "settings.json"
        self.settings = self.load_settings()
        self.root_box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        self.make_header()
        self.nav = GridLayout(cols=3, size_hint_y=None, height=dp(44), spacing=dp(6))
        for name in ("HOME", "SETTINGS", "HUD LAB"):
            self.nav.add_widget(self.make_button(name, lambda _, n=name: self.show_page(n)))
        self.root_box.add_widget(self.nav)

        self.scroll = ScrollView(do_scroll_x=False)
        self.content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=(0, dp(2)))
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        self.root_box.add_widget(self.scroll)

        self.status = Label(text="● SIMULATOR READY", color=GREEN, font_size=sp(11),
                            size_hint_y=None, height=dp(22), halign="left")
        self.status.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.root_box.add_widget(self.status)
        self.show_page("HOME")
        return self.root_box

    def load_settings(self):
        defaults = {
            "general": 85, "red_dot": 78, "scope_2x": 72, "scope_4x": 65,
            "sniper": 45, "free_look": 80, "hud_enabled": True,
            "crosshair": True, "aim_demo": False, "esp_demo": False
        }
        try:
            if self.config_path.exists():
                defaults.update(json.loads(self.config_path.read_text()))
        except Exception:
            pass
        return defaults

    def make_header(self):
        header = BoxLayout(size_hint_y=None, height=dp(64), spacing=dp(10))
        mark = Label(text="[b]G[/b]", markup=True, color=RED, font_size=sp(34),
                     size_hint_x=None, width=dp(45))
        title_box = BoxLayout(orientation="vertical", spacing=0)
        title_box.add_widget(Label(text="[b]GRH4X RED PANEL[/b]", markup=True,
                                   color=WHITE, font_size=sp(18), halign="left",
                                   valign="bottom"))
        title_box.add_widget(Label(text="ANDROID CONFIGURATION SIMULATOR",
                                   color=MUTED, font_size=sp(9), halign="left",
                                   valign="top"))
        header.add_widget(mark)
        header.add_widget(title_box)
        header.add_widget(Label(text="V1.0", color=RED, font_size=sp(11),
                                size_hint_x=None, width=dp(40)))
        self.root_box.add_widget(header)

    def make_button(self, text, callback):
        b = Button(text=text, size_hint_y=None, height=dp(42),
                   background_normal="", background_color=RED,
                   color=WHITE, font_size=sp(11), bold=True)
        b.bind(on_release=callback)
        return b

    def add_label(self, text, size=13, color=WHITE, height=dp(25), markup=False):
        label = Label(text=text, markup=markup, color=color, font_size=sp(size),
                      size_hint_y=None, height=height, halign="left", valign="middle")
        label.bind(size=lambda w, s: setattr(w, "text_size", (s[0], None)))
        self.content.add_widget(label)
        return label

    def add_card(self):
        card = PanelCard(size_hint_y=None)
        card.bind(minimum_height=card.setter("height"))
        self.content.add_widget(card)
        return card

    def show_page(self, page):
        self.content.clear_widgets()
        if page == "HOME":
            self.add_label("WELCOME BACK", 17, RED, dp(32), True)
            card = self.add_card()
            card.add_widget(Label(text="[b]SYSTEM STATUS[/b]", markup=True,
                                  color=WHITE, font_size=sp(14), size_hint_y=None,
                                  height=dp(25), halign="left"))
            card.add_widget(Label(text="Training simulator is running locally.",
                                  color=MUTED, font_size=sp(11), size_hint_y=None,
                                  height=dp(25), halign="left"))
            card.add_widget(Label(text="No connection to Free Fire • No game modification",
                                  color=GREEN, font_size=sp(10), size_hint_y=None,
                                  height=dp(22), halign="left"))
            self.add_label("QUICK ACCESS", 13, RED)
            for label, target in (("OPEN SENSITIVITY", "SETTINGS"), ("OPEN HUD LAB", "HUD LAB")):
                self.content.add_widget(self.make_button(label, lambda _, p=target: self.show_page(p)))
            self.add_label("This app is a standalone visual simulator. It does not provide cheats or guarantee immunity from bans.", 10, MUTED, dp(55))
        elif page == "SETTINGS":
            self.add_label("SENSITIVITY CONFIGURATION", 16, RED, dp(32), True)
            card = self.add_card()
            for key, title in (
                ("general", "General"), ("red_dot", "Red Dot"),
                ("scope_2x", "2x Scope"), ("scope_4x", "4x Scope"),
                ("sniper", "Sniper Scope"), ("free_look", "Free Look")
            ):
                self.add_slider(card, key, title)
            self.content.add_widget(self.make_button("SAVE CONFIGURATION", self.save_settings))
            self.content.add_widget(self.make_button("RESET DEFAULTS", self.reset_settings))
        elif page == "HUD LAB":
            self.add_label("HUD & TRAINING LAB", 16, RED, dp(32), True)
            card = self.add_card()
            self.add_toggle(card, "hud_enabled", "Custom HUD preview")
            self.add_toggle(card, "crosshair", "Training crosshair preview")
            self.add_toggle(card, "aim_demo", "Aimbot concept demo (visual only)")
            self.add_toggle(card, "esp_demo", "ESP concept demo (visual only)")
            self.add_label("PREVIEW", 13, RED)
            preview = PanelCard(size_hint_y=None, height=dp(180))
            preview.add_widget(Label(
                text="[b]TRAINING AREA[/b]\\n\\n      +\\n\\n[ DEMO TARGET ]",
                markup=True, color=WHITE, font_size=sp(16), halign="center"))
            self.content.add_widget(preview)
            self.content.add_widget(self.make_button("SAVE HUD SETTINGS", self.save_settings))
            self.add_label("The Aimbot/ESP switches only change this local preview; they do not interact with the game.", 10, MUTED, dp(48))

    def add_slider(self, card, key, title):
        row = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(68), spacing=dp(2))
        top = BoxLayout(size_hint_y=None, height=dp(22))
        value_label = Label(text=f"{title}: {int(self.settings[key])}", color=WHITE,
                            font_size=sp(11), halign="left")
        value_label.bind(size=lambda w, s: setattr(w, "text_size", s))
        top.add_widget(value_label)
        row.add_widget(top)
        slider = Slider(min=0, max=200, value=self.settings[key])
        slider.bind(value=lambda _, value: self.update_slider(key, title, value, value_label))
        row.add_widget(slider)
        card.add_widget(row)

    def update_slider(self, key, title, value, label):
        self.settings[key] = int(value)
        label.text = f"{title}: {int(value)}"

    def add_toggle(self, card, key, title):
        row = BoxLayout(size_hint_y=None, height=dp(42))
        row.add_widget(Label(text=title, color=WHITE, font_size=sp(11), halign="left"))
        toggle = CheckBox(active=bool(self.settings[key]), size_hint_x=None, width=dp(48))
        toggle.bind(active=lambda _, value: self.settings.update({key: value}))
        row.add_widget(toggle)
        card.add_widget(row)

    def save_settings(self, *_):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.settings, indent=2))
        self.status.text = "● CONFIGURATION SAVED"
        self.status.color = GREEN

    def reset_settings(self, *_):
        self.settings = {
            "general": 85, "red_dot": 78, "scope_2x": 72, "scope_4x": 65,
            "sniper": 45, "free_look": 80, "hud_enabled": True,
            "crosshair": True, "aim_demo": False, "esp_demo": False
        }
        self.save_settings()
        self.show_page("SETTINGS")


if __name__ == "__main__":
    RedPanelApp().run()
