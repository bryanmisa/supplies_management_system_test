from django_select2 import forms as s2forms


# Select2Widgets


class SupplyItemSelect2Widget(s2forms.ModelSelect2Widget):
    search_fields = ['item_name__icontains']
                     
    def build_attrs(self, base_attrs, extra_attrs=None):
        """Add custom attributes to the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-minimum-input-length'] = 2   # Set minimum input length
        attrs['style'] = 'width: 100%;'  # Set width to 100%
      
        return attrs
    

class SupplierItemSelect2Widget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']
                     
    def build_attrs(self, base_attrs, extra_attrs=None):
        """Add custom attributes to the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-minimum-input-length'] = 2   # Set minimum input length
        attrs['style'] = 'width: 100%;'  # Set width to 100%
      
        return attrs

class CategorySelect2Widget(s2forms.ModelSelect2Widget):
    search_fields = ['name__icontains']
                     
    def build_attrs(self, base_attrs, extra_attrs=None):
        """Add custom attributes to the widget."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-minimum-input-length'] = 2   # Set minimum input length
        attrs['style'] = 'width: 100%;'  # Set width to 100%
      
        return attrs
