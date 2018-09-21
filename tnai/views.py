from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if '132.148.247.155' in self.request.get_host():
            context['base_template'] = "base_instructor.html"
        else:
            context['base_template'] = "base_generic.html"
        return context

class CustomLogoutView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if '132.148.247.155' in self.request.get_host():
            context['base_template'] = "base_instructor.html"
        else:
            context['base_template'] = "base_generic.html"
        return context
