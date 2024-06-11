from django.shortcuts import render


def module(request, module_id):

    context = {}
    return render(request, "module.html", context=context)
