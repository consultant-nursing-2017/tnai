from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'custom_clearable_file_input.html'

    def render(self, name, value, attrs=None, renderer=None):
        """
        Returns this Widget rendered as HTML, as a Unicode string.
        """
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, renderer)
