from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import Http404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync





@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404
        for member in chat_group.members.all():
            if member != request.user :
                other_user = member
                break
    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            # notify other websocket clients
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                chatroom_name,
                {
                    'type': 'message_handler',
                    'message_id': message.id,
                }
            )

            return render(
                request,
                "nameh/partials/chat_message_p.html",
                {"message": message, "user": request.user}
            )


    context = {
        "chat_group": chat_group,
        "chat_messages": chat_messages,
        "form": form,
        "chatroom_name": chatroom_name,
        "online_count": chat_group.users_online.count(),
        "other_user" : other_user
    }

    return render(request, "nameh/chat.html", context)




@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    other_user = User.objects.get(username=username)
    my_private_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_private_chatrooms.exists():
        for chatroom in my_private_chatrooms:
            if other_user in chatroom.members.all():
                return redirect("chatroom" , chatroom.group_name)


    chatroom = ChatGroup.objects.create(is_private=True)
    chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.group_name)