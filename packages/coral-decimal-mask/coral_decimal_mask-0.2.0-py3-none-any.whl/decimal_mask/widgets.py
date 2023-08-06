import json

from django import forms
from django.core.serializers.json import DjangoJSONEncoder

_json_script_escapes = {
    ord(">"): "\\u003E",
    ord("<"): "\\u003C",
    ord("&"): "\\u0026",
}


class DecimalMaskBaseWidget(forms.TextInput):
    input_type = "tel"
    decimal_attrs = {}

    def __init__(self, decimal_attrs=None, attrs=None):
        default_attrs = {
            "locales": "en-US",
            "decimalPlaces": 2,
        }
        decimal_attrs = (
            self.decimal_attrs
            if decimal_attrs is None
            else decimal_attrs.copy()
        )
        default_attrs.update(decimal_attrs)

        self.decimal_attrs = default_attrs
        super().__init__(attrs=attrs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs["data-decimal-mask"] = ""
        attrs["data-decimal-options"] = json.dumps(
            self.decimal_attrs, cls=DjangoJSONEncoder
        ).translate(_json_script_escapes)
        return attrs

    class Media:
        js = ["decimal_mask/DecimalMask.js", "decimal_mask/init.js"]


class DecimalMaskWidget(DecimalMaskBaseWidget):
    ...


class MoneyMaskWidget(DecimalMaskBaseWidget):
    decimal_attrs = {
        "format": {
            "style": "currency",
            "currency": "USD",
        },
    }


class PercentMaskWidget(DecimalMaskBaseWidget):
    decimal_attrs = {
        "format": {"style": "percent"},
    }
