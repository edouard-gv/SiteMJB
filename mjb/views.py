from django.shortcuts import render

from mjb.models import Theme


def themes(request):
    theme_list = Theme.objects.order_by('mot_cle')
    context = {
        'theme_list': theme_list,
    }
    return render(request, 'themes.html', context)
