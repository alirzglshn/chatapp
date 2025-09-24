from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def chat_view(request, chatroom_name='visca-barca'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.htmx:  # message submit
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return render(
                request,
                "nameh/partials/chat_message_p.html",
                {"message": message, "user": request.user}
            )

    # normal GET
    context = {
        "chat_group": chat_group,
        "chat_messages": chat_messages,
        "form": form,
        "chatroom_name": chatroom_name,
    }
    return render(request, "nameh/chat.html", context)
