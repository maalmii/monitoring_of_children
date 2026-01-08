# your_app_name/forms.py
from django import forms
from .models import Ditina
import re

class DitinaForm(forms.ModelForm):
    class Meta:
        model = Ditina

        # ВОССТАНОВЛЕНЫ vik и zrist
        fields = ['imya', 'prizvische', 'plec', 'region', 'vik', 'zrist', 'pryimaie_gormony']

        labels = {
            'imya': "Imię dziecka",
            'prizvische': "Nazwisko dziecka",
            'plec': "Płeć",
            'vik': "Wiek (ukończone lata)",
            'zrist': "Wzrost (w centymetrach)",
            'pryimaie_gormony': "Czy dziecko przyjmuje hormon wzrostu?"
        }
        widgets = {
            'imya': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Wprowadź imię"}),
            'prizvische': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź nazwisko'}),
            'plec': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'vik': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Np.: 5'}),
            'zrist': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Np.: 110'}),
            'pryimaie_gormony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'vik': 'Podaj pełną liczbę lat.',
        }
        error_messages = {
            'imya': {
                'max_length': "Imię jest za długie.",
            },
        }

    def clean_imya(self):
        imya = self.cleaned_data.get('imya')
        if imya:
            if not re.match(r"^[А-Яа-яЇїІіЄєҐґA-Za-z\s'-]+$", imya):
                raise forms.ValidationError("Imię może zawierać tylko litery, spacje, apostrof lub łącznik.")
        return imya

    def clean_prizvische(self):
        prizvische = self.cleaned_data.get('prizvische')
        if prizvische:
            if not re.match(r"^[А-Яа-яЇїІіЄєҐґA-Za-z\s'-]+$", prizvische):
                raise forms.ValidationError("Nazwisko może zawierać tylko litery, spacje, apostrof lub łącznik.")
        return prizvische

    def clean_vik(self):
        vik = self.cleaned_data.get('vik')
        if vik is not None:
            if vik > 18:
                raise forms.ValidationError("Wiek nie może być większy niż 18 lat dla tego formularza.")
            if vik < 0:
                raise forms.ValidationError("Wiek nie może być ujemny.")
        return vik

    def clean_zrist(self):
        zrist = self.cleaned_data.get('zrist')
        max_reasonable_height_for_18_yo = 220
        min_reasonable_height = 20

        if zrist is not None:
            if zrist > max_reasonable_height_for_18_yo:
                raise forms.ValidationError(f"Wzrost nie może przekraczać {max_reasonable_height_for_18_yo} cm.")
            if zrist != 0 and zrist < min_reasonable_height:
                raise forms.ValidationError(f"Wzrost wydaje się być za mały. Minimalny dopuszczalny wzrost to {min_reasonable_height} cm (или 0, если не поддано).")
        return zrist