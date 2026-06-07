from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Pastor, PastorWife, GalleryImage, Event, Booking


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

        # Send emails in background thread to avoid worker timeout
        import threading

        def send_emails():
            # Email to the person who booked
            if email:
                subject_user = "Booking Confirmation - Christ's New Life Solution & Healing Church"
                message_user = f"""
Dear {full_name},

Thank you for booking a session with Prophet. Dairo Olayemi Jeremiah at Christ's New Life Solution & Healing Church Worldwide.

We have received your booking request with the following details:

  Consultation Type : {consultation_type}
  Preferred Date    : {preferred_date}
  Preferred Time    : {preferred_time}

Our team will contact you within 24 hours to confirm your appointment.

Please arrive 10 minutes before your scheduled time at:
Christ's New Life, Fayegbami Street, Surulere Area, Ikirun, Osun State.

God bless you!

- Christ's New Life Solution & Healing Church Worldwide
"""
                try:
                    send_mail(
                        subject_user,
                        message_user,
                        settings.EMAIL_HOST_USER,
                        [f4b098@gmail.com],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            # Admin notification email
            subject_admin = f'New Booking Request from {full_name}'
            message_admin = f"""
New session booking received on the church website.

BOOKING DETAILS:
Full Name         : {full_name}
Phone Number      : {phone}
Email             : {email or 'Not provided'}
Consultation Type : {consultation_type}
Preferred Date    : {preferred_date}
Preferred Time    : {preferred_time}

Message / Description:
{description or 'No description provided'}

Log in to the admin panel to confirm or manage this booking:
https://christnewlife-church-1.onrender.com/admin/
"""
            try:
                send_mail(
                    subject_admin,
                    message_admin,
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

        # Start email thread — won't block the response
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
