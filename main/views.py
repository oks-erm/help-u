from django.shortcuts import render
from datetime import datetime
from .models import ContactFormMessage


def home_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        msg = request.POST.get('message')
        # date = datetime.now()
        print(name)
        new = ContactFormMessage(
            name=name,
            email=email,
            subject=subject,
            message=msg,
            # date=date,
            )
        new.save()

    return render(request, 'index.html')
