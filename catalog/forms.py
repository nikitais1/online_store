from django import forms

from catalog.models import Product, Version, Category


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CategoryForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner',)

    def clean_product_name(self):
        cleaned_data = self.cleaned_data['product_name']
        f = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
             'радар',)
        if cleaned_data in f:
            raise forms.ValidationError('Недопустимое имя для продукта')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        f = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
             'радар',)
        if cleaned_data in f:
            raise forms.ValidationError('Недопустимое слова для описания продукта')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class ModeratorProductForm(ProductForm):
    """
    Класс создания формы для редактирования модератором
    """

    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')
