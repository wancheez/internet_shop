from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin

from .models import *

from PIL import Image


class NotebookAdminForm(ModelForm):

    MIN_RESOLUTION = (400, 400)

    def __init__(self, *args, **kwargs):
        super(NotebookAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].help_text = f'Загружайте изображения с минимальным разрешением {self.MIN_RESOLUTION}'

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Загруженное изображение меньше мин. разрешения')
        return image


class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
