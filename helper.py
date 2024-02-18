import os
import random
import string
import csv
from string import digits
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models
from django.http import HttpResponse

from django.core.files.storage import default_storage
from django.db.models import FileField



def file_cleanup(sender, **kwargs):

    for fieldname in sender._meta.get_all_field_names():
        try:
            field = sender._meta.get_field(fieldname)
        except:
            field = None
            if field and isinstance(field, FileField):
                inst = kwargs["instance"]
                f = getattr(inst, fieldname)
                m = inst.__class__._default_manager
                if (
                    hasattr(f, "path")
                    and os.path.exists(f.path)
                    and not m.filter(
                        **{"%s__exact" % fieldname: getattr(inst, fieldname)}
                    ).exclude(pk=inst._get_pk_val())
                ):
                    try:
                        default_storage.delete(f.path)
                    except:
                        pass



class ImageField(models.ImageField):
    def save_form_data(self, instance, data):
        if data is not None:
            file = getattr(instance, self.attname)
            if file.name != '' and data is False:
                file.delete(save=False)
        super(models.ImageField, self).save_form_data(instance, data)


# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
# MAX_UPLOAD_SIZE = getattr(settings, 'MAX_FILE_UPLOAD_SIZE', 5242880)
        
# def check_file(self):
#     content = self.cleaned_data["file"]
#     content_type = content.content_type.split('/')[0]
#     if (content._size > MAX_UPLOAD_SIZE):
#         raise forms.ValidationError(_("Please keep file size under %s. Current file size %s")%(filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content._size)))
#     return content

def file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')

def random_digits_generator(size=5):
    return ''.join([random.choice(digits) for i in range(size)])

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for i in range(size))


def unique_code_generator(instance):
    new_code = random_digits_generator(size=5)
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(code=new_code).exists()
    if qs_exists:
        return unique_code_generator(instance)
    return new_code


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export Selected"




    








