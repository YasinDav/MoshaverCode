from django.shortcuts import render

from .models import Developer, Guide, SubGuide


def index(request):
    developers = Developer.objects.all()
    return render(request, 'index.html', {'developers': developers})


def guide(request):
    sub_guides = SubGuide.objects.all()
    guides = Guide.objects.all()

    sub_guide_dict = {}

    for i in sub_guides:
        sub_guide_dict[i] = guides.filter(sub_guide=i)

    return render(request, 'guide.html', {'guides_dict': sub_guide_dict, "guides": guides})
