from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 1024
    if file.size > max_size_kb * 1024:
        raise ValidationError('فایل اپلود شده نمی تواند بیشتر از یک مگ باشد')