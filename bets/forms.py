from django import forms
from .models import Banca, Aposta


class BancaForm(forms.ModelForm):
    class Meta:
        model = Banca
        fields = ['nome', 'capital_inicial', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Bet365, Pinnacle, Banca Principal',
            }),
            'capital_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_capital_inicial(self):
        valor = self.cleaned_data.get('capital_inicial')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O capital inicial não pode ser negativo.')
        return valor


class ApostaForm(forms.ModelForm):
    class Meta:
        model = Aposta
        fields = ['esporte', 'competicao', 'mercado', 'data', 'odd', 'stake', 'resultado', 'valor_cashout', 'anotacao']
        widgets = {
            'esporte': forms.Select(attrs={'class': 'form-select'}),
            'competicao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Champions League, Brasileirão Série A',
            }),
            'mercado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Over 2.5, 1x2, Moneyline',
            }),
            'data': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'odd': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '1.01',
                'placeholder': '1.50',
            }),
            'stake': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00',
            }),
            'resultado': forms.Select(attrs={'class': 'form-select', 'id': 'id_resultado'}),
            'valor_cashout': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
            'anotacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações opcionais sobre a aposta...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data'].input_formats = ['%Y-%m-%dT%H:%M']
        if self.instance and self.instance.pk and self.instance.data:
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%dT%H:%M')

    def clean_stake(self):
        stake = self.cleaned_data.get('stake')
        if stake is not None and stake <= 0:
            raise forms.ValidationError('O valor apostado deve ser maior que zero.')
        return stake

    def clean_odd(self):
        odd = self.cleaned_data.get('odd')
        if odd is not None and odd <= 1:
            raise forms.ValidationError('A odd deve ser maior que 1.00.')
        return odd

    def clean(self):
        cleaned_data = super().clean()
        resultado = cleaned_data.get('resultado')
        valor_cashout = cleaned_data.get('valor_cashout')
        if resultado == 'CASHOUT' and not valor_cashout:
            self.add_error('valor_cashout', 'Informe o valor recebido no cashout.')
        return cleaned_data
