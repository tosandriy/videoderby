from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_lte_10(value):
    if value > 10:
        raise ValidationError(
            _('%(value)s is greater then 5'),
            params={'value': value},
        )