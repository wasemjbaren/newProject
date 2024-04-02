#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParentsNetworkProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

def addParent(request):
    user = User.objects.filter(is_superuser=False)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, 'Parent Added Successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Please Fill the Form Correctly')
    else:
        form = UserForm()
    context = {'user':user, 'form': form}
    return render(request, 'addParent.html', context)


def deleteParent(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('addParent')
