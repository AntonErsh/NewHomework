from django.shortcuts import render

# Create your views here.


def platform(request):
    return render(request, 'fourth_task/main_page.html')


def shop(request):
    game1 = 'Half-life'
    game2 = 'Resident Evil 2'
    game3 = 'Metal Gear Solid'
    game4 = "Baldur's Gate"
    game5 = 'Вангеры'
    context = {'games': [game1, game2, game3, game4, game5]}
    return render(request, 'fourth_task/shop.html', context)


def basket(request):
    return render(request, 'fourth_task/basket.html')
