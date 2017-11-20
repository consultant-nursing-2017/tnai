import os
import pdb
from django.core.exceptions import ValidationError

class ValidateFileExtension(object):
    def validate_file(value):
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        valid_extensions = ['.pdf']
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension. Must be: ' + ','.join(valid_extensions) + '.')

    def validate_image(value):
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.gif', '.png']
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension for image. Must be: ' + ','.join(valid_extensions) + '.')
