from django.shortcuts import render


def sensors_list(request):
    context = {
        "title": "Главная",
    }
    return render(request, "block_list.html", context=context)
