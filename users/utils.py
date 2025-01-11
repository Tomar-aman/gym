from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from gym import settings

def send_otp_email(user, otp_code):
    subject = "Verify Your Email Address"
    user_name = user.full_name or "User"

    # Render the HTML template
    html_message = render_to_string(
        'mail/otp.html', 
        {
            'user_name': user_name,  # Pass user name to template
            'otp_code': otp_code,    # Pass OTP code to template
        }
    )

    # Send email
    email = EmailMessage(
        subject,
        html_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.content_subtype = "html"  # Set email content type to HTML
    email.send()
