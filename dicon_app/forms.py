from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer # どのモデルをベースにするか

        # フォームに表示するフィールド
        fields = ('company_name', 'contact_name', 'email', 'phone', 'user', 'tags')

        # 必須項目にしたくない場合など、個別の設定
        # （こんかいは　userとtagsを必須ではない設定にします）
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
