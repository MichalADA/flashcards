from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

class PasswordRequirementsPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(
            title='Wymagania hasła',
            size_hint=(None, None),
            size=(dp(300), dp(400)),
            auto_dismiss=True,
            **kwargs
        )
        
        # Główny layout
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Style dla etykiet
        label_style = {
            'color': [0, 0, 0, 1],  # Czarny tekst
            'size_hint_y': None,
            'height': dp(30),
            'text_size': (dp(280), None),
            'halign': 'left'
        }
        
        # Tytuł
        title_label = Label(
            text='Twoje hasło musi spełniać następujące wymagania:',
            bold=True,
            **label_style
        )
        layout.add_widget(title_label)
        
        # Lista wymagań
        requirements = [
            '• Minimum 8 znaków',
            '• Przynajmniej 1 wielka litera',
            '• Przynajmniej 1 mała litera',
            '• Przynajmniej 1 cyfra',
            '• Przynajmniej 1 znak specjalny (np. !@#$%^&*)'
        ]
        
        for req in requirements:
            req_label = Label(
                text=req,
                **label_style
            )
            layout.add_widget(req_label)
        
        # Przycisk zamknięcia
        close_button = Button(
            text='Rozumiem',
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={'center_x': 0.5}
        )
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)
        
        self.content = layout