from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp

class FocusTextInput(TextInput):
    def __init__(self, next_field=None, **kwargs):
        super().__init__(**kwargs)
        self.next_field = next_field
        self.background_color = [0.95, 0.95, 0.95, 1]
        self.foreground_color = [0.2, 0.2, 0.2, 1]
        self.cursor_color = [0.2, 0.2, 0.2, 1]
        self.hint_text_color = [0.5, 0.5, 0.5, 1]
        
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'tab' and self.next_field:
            self.next_field.focus = True
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

class BaseScreen(BoxLayout):
    """
    Klasa bazowa dla wszystkich ekranów w aplikacji.
    Zapewnia spójny wygląd i podstawowe funkcjonalności.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(20)
        self.padding = dp(30)
        
        # Tło
        with self.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Jasne tło
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def create_title(self, text):
        """Tworzy standardowy tytuł dla ekranu"""
        return Label(
            text=text,
            font_size=dp(32),
            color=[0.2, 0.2, 0.2, 1],
            size_hint_y=None,
            height=dp(60),
            bold=True
        )

    def create_text_input(self, hint_text, password=False):
        """Tworzy standardowe pole tekstowe"""
        return FocusTextInput(
            hint_text=hint_text,
            password=password,
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=dp(16),
            padding=[dp(15), dp(10)],
            write_tab=False
        )

    def create_button(self, text, color, **kwargs):
        """Tworzy standardowy przycisk"""
        return Button(
            text=text,
            size_hint_y=None,
            height=dp(50),
            background_normal='',
            background_color=color,
            font_size=dp(18),
            bold=True,
            **kwargs
        )

    def create_container(self):
        """Tworzy standardowy kontener na elementy"""
        container = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            padding=[dp(20), dp(20)]
        )
        container.bind(minimum_height=container.setter('height'))
        return container

    def create_error_label(self):
        """Tworzy label do wyświetlania błędów"""
        return Label(
            text="",
            font_size=dp(14),
            color=[0.8, 0.2, 0.2, 1],
            size_hint_y=None,
            height=dp(30)
        )

    @staticmethod
    def get_primary_color():
        """Kolor dla głównych przycisków"""
        return [0.2, 0.6, 0.9, 1]

    @staticmethod
    def get_secondary_color():
        """Kolor dla drugorzędnych przycisków"""
        return [0.9, 0.3, 0.3, 1]