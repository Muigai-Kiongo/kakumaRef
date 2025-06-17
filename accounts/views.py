from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Import the custom form
from django.views import View

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()  # Use the custom form
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)  # Use the custom form
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
        return render(request, 'registration/register.html', {'form': form})
