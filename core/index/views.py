from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from .forms import ContactUsForm
from .models import Developer, Guide, SubGuide


def index_view(request):
    developers = Developer.objects.all()
    return render(request, 'index.html', {'developers': developers})


def guide_view(request):
    sub_guides = SubGuide.objects.all()
    guides = Guide.objects.all()

    sub_guide_dict = {}

    for i in sub_guides:
        sub_guide_dict[i] = guides.filter(sub_guide=i)

    return render(request, 'guide.html', {'guides_dict': sub_guide_dict})


def contact_view(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('contact'))
        else:
            return HttpResponse('Something went wrong')
    else:
        form = ContactUsForm()

        developers = Developer.objects.all()
        return render(request, 'contact.html', {'developers': developers, 'form': form})
