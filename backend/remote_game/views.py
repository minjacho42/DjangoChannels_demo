from django.shortcuts import render

def index(request):
    return render(request, "remote_game/index.html")

def room(request, match_name):
    return render(request, "remote_game/room.html", {"match_name": match_name})

def lobby(request):
    return render(request, "remote_game/lobby.html")