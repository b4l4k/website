from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
import requests

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def send_telegram_message(message):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    return requests.post(url, json=payload)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            msg_content = form.cleaned_data['message']
            
            full_message = f"🚀 *New Survey Submission*\n\n*Name:* {name}\n*Email:* {email}\n*Message:*\n{msg_content}"
            
            try:
                response = send_telegram_message(full_message)
                if response.status_code == 200:
                    messages.success(request, 'Thank you! I received your message.')
                else:
                    print(f"Telegram API error: {response.status_code} - {response.text}")
                    messages.error(request, 'Error sending to Telegram.')
            except Exception as e:
                messages.error(request, 'Connection error. Please try again later.')
            
            return redirect('/#contact')


