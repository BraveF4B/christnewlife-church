from django.shortcuts import render
from django.conf import settings
from .models import Pastor, PastorWife, GalleryImage, Event, Booking
import requests
import threading


def send_brevo_email(to_email, to_name, subject, content):
    """Send email via Brevo HTTP API — no SMTP ports needed."""
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": settings.BREVO_API_KEY,
    }
    data = {
        "sender": {"name": "Christ's New Life Church", "email": "f4b098@gmail.com"},
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "textContent": content,
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"BREVO RESPONSE: {response.status_code} - {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"BREVO ERROR: {e}")
        return False


def home(request):
    pastor = Pastor.objects.first()
    events = Event.objects.filter(is_active=True, status='upcoming').order_by('date')[:3]
    gallery = GalleryImage.objects.all()[:6]
    return render(request, 'main/home.html', {
        'pastor': pastor,
        'events': events,
        'gallery': gallery,
    })


def about(request):
    pastor = Pastor.objects.first()
    pastor_wife = PastorWife.objects.first()
    return render(request, 'main/about.html', {
        'pastor': pastor,
        'pastor_wife': pastor_wife,
    })


def book_session(request):
    pastor = Pastor.objects.first()
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        consultation_type = request.POST.get('consultation_type')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        description = request.POST.get('description')

        # Save to database
        Booking.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            consultation_type=consultation_type,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            description=description,
        )

        # Send emails via Brevo HTTP API in background thread
        def send_emails():
            # Confirmation to booker
            if email:
                user_content = f"""Dear {full_name},

Thank you for booking a session with Prophet. Dairo Olayemi Jeremiah at Christ's New Life Solution & Healing Church Worldwide.

We have received your booking request with the following details:

  Consultation Type : {consultation_type}
  Preferred Date    : {preferred_date}
  Preferred Time    : {preferred_time}

Our team will contact you within 24 hours to confirm your appointment.

Please arrive 10 minutes before your scheduled time at:
Christ's New Life, Fayegbami Street, Surulere Area, Ikirun, Osun State.

God bless you!

- Christ's New Life Solution & Healing Church Worldwide"""
                send_brevo_email(
                    email, full_name,
                    "Booking Confirmation - Christ's New Life Solution & Healing Church",
                    user_content
                )

            # Admin notification
            admin_content = f"""New session booking received on the church website.

BOOKING DETAILS:
Full Name         : {full_name}
Phone Number      : {phone}
Email             : {email or 'Not provided'}
Consultation Type : {consultation_type}
Preferred Date    : {preferred_date}
Preferred Time    : {preferred_time}

Message / Description:
{description or 'No description provided'}

Log in to the admin panel:
https://christnewlife-church-1.onrender.com/admin/"""
            send_brevo_email(
                settings.ADMIN_EMAIL, "Admin",
                f"New Booking Request from {full_name}",
                admin_content
            )

        email_thread = threading.Thread(target=send_emails)
        email_thread.daemon = True
        email_thread.start()

        return render(request, 'main/book_session.html', {'success': True, 'pastor': pastor})
    return render(request, 'main/book_session.html', {'pastor': pastor})


def gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    categories = GalleryImage.objects.values_list('category', flat=True).distinct()
    return render(request, 'main/gallery.html', {
        'images': images,
        'categories': categories,
    })


def events(request):
    upcoming = Event.objects.filter(is_active=True, status='upcoming').order_by('date')
    past = Event.objects.filter(is_active=True, status='past').order_by('-date')
    return render(request, 'main/events.html', {
        'upcoming': upcoming,
        'past': past,
    })


def give(request):
    return render(request, 'main/give.html')
