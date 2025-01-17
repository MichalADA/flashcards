from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

# Klasa odpowiedzialna za zarządzanie polami tekstowymi z możliwością przejścia między nimi
class FocusTextInput(TextInput):
    def __init__(self, next_field=None, **kwargs):
        super().__init__(**kwargs)
        self.next_field = next_field  # Referencja do kolejnego pola tekstowego
        self.background_color = [0.95, 0.95, 0.95, 1]  # Kolor tła pola tekstowego
        self.foreground_color = [0.2, 0.2, 0.2, 1]  # Kolor tekstu
        self.cursor_color = [0.2, 0.2, 0.2, 1]  # Kolor kursora
        self.hint_text_color = [0.5, 0.5, 0.5, 1]  # Kolor tekstu podpowiedzi

    # Obsługa naciśnięcia klawisza TAB
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'tab' and self.next_field:  # Jeśli TAB i jest kolejne pole
            self.next_field.focus = True  # Przeniesienie focusa na kolejne pole
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

# Klasa bazowa dla wszystkich ekranów w aplikacji
class BaseScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # Ustawienie orientacji na pionową
        self.spacing = dp(20)  # Odstępy między elementami
        self.padding = dp(30)  # Marginesy

        # Ustawienie tła dla ekranu
        with self.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Jasnoszary kolor tła
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)  # Aktualizacja prostokąta

    # Aktualizacja tła w przypadku zmiany rozmiaru lub pozycji
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    # Tworzenie tytułu ekranu
    def create_title(self, text):
        return Label(
            text=text,
            font_size=dp(32),  # Rozmiar czcionki
            color=[0.2, 0.2, 0.2, 1],  # Kolor tekstu
            size_hint_y=None,
            height=dp(60),  # Wysokość
            bold=True  # Wyróżnienie
        )

    # Tworzenie pola tekstowego
    def create_text_input(self, hint_text, password=False):
        return FocusTextInput(
            hint_text=hint_text,  # Tekst podpowiedzi
            password=password,  # Czy pole ma ukrywać tekst (np. hasła)
            multiline=False,  # Brak możliwości wpisywania wielu linii
            size_hint_y=None,
            height=dp(45),  # Wysokość pola
            font_size=dp(16),
            padding=[dp(15), dp(10)],  # Marginesy wewnętrzne
            write_tab=False  # Wyłączenie obsługi TAB w polu
        )

    # Tworzenie przycisku
    def create_button(self, text, color, **kwargs):
        return Button(
            text=text,  # Tekst przycisku
            size_hint_y=None,
            height=dp(50),  # Wysokość przycisku
            background_normal='',  # Usunięcie domyślnego tła
            background_color=color,  # Ustawienie koloru tła
            font_size=dp(18),
            bold=True,  # Wyróżnienie
            **kwargs
        )

    # Tworzenie kontenera na elementy
    def create_container(self):
        container = BoxLayout(
            orientation='vertical',  # Ustawienie orientacji na pionową
            spacing=dp(15),  # Odstępy między elementami
            size_hint_y=None,
            padding=[dp(20), dp(20)]  # Marginesy wewnętrzne
        )
        container.bind(minimum_height=container.setter('height'))
        return container

    # Tworzenie etykiety dla komunikatów błędów
    def create_error_label(self):
        return Label(
            text="",  # Domyślnie brak tekstu
            font_size=dp(14),  # Rozmiar czcionki
            color=[0.8, 0.2, 0.2, 1],  # Czerwony kolor dla błędów
            size_hint_y=None,
            height=dp(30)  # Wysokość etykiety
        )

    # Kolor dla głównych przycisków
    @staticmethod
    def get_primary_color():
        return [0.2, 0.6, 0.9, 1]  # Niebieski

    # Kolor dla drugorzędnych przycisków
    @staticmethod
    def get_secondary_color():
        return [0.9, 0.3, 0.3, 1]  # Czerwony
