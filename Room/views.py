from django.shortcuts import render, redirect
from .models import Room
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
def post(room, player, move, result, turn):
    if player == 1:
        room.move1 = move
        room.result = result
        room.turn = turn
    else:
        room.move2 = move
        room.result = result
        room.turn = turn
    return room

def index(request, ports, player_id1, player_id2):
    room = Room.objects.get(port=ports)
    if request.method == "GET":
        return render(request,'room/index.html',{ "room": room})

    elif request.method == 'POST':
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is None or (user.id != player_id1 and user.id != player_id2):
            return redirect('/home/')
        if room.player1.id != player_id1 or room.player2.id != player_id2:
            return redirect('/home/')

        if user.id == room.player1.id:
            player = 1
        else:
            player = 2
        rooms = post(room, player, request.POST['move'], request.POST['result'][0], request.POST['turn'][0])
        rooms.save()
        return render(request,'room/index.html',{ "room": rooms})

def wait(request, ports):
    if request.method != 'POST':
        return redirect('/home/')
    user = authenticate(username=request.POST['username'],password=request.POST['password'])
    if user is None:
        return redirect('/home/')
    #join exist room
    try:
        room = Room.objects.get(port=ports)
        #when player refresh
        if room.player2.id != 0:
            if room.player1.id == user.id or room.player2.id == user.id:
                return render(request,'room/wait.html',{'player1':room.player1.id,'player2':room.player2.id})
            else:
                return redirect('/home/')
        else:
            #when player2 join
            if room.player1.id != user.id:
                room.player2 = user
                room.save()
            return render(request,'room/wait.html',{'player1':room.player1.id,'player2':room.player2.id})
    #create new room
    except:
        r = Room()
        r.port = ports
        r.player1=user
        r.player2=User.objects.get(id=0)
        r.save()
        return render(request,'room/wait.html',{'player1':r.player1.id,'player2':r.player2.id})
