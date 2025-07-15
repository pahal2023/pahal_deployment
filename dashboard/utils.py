from random import randint, choice
import string
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group


def register(name, email):
    username = name.split()[0] + str(randint(100, 999))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(choice(characters) for _ in range(8))  # slightly stronger password

    # Prevent duplicate username
    if User.objects.filter(username=username).exists():
        username += '4'

    # Safely split name
    name_parts = name.split()
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''

    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)
    user.save()

    # Add to group
    group = Group.objects.get(name='teacher')
    user.groups.add(group)

    # Send mail
    mail_credentials(name, email, username, password)

    # ✅ Return the values needed in approve_applicant
    return user


# message follows indentation. It should be written like this.
def mail_credentials(name, email_to, username, password):
    from_email = "pahalfoundationvitb@gmail.com"
    recipient_list = [email_to,]
    subject = "Welcome to Pahal Foundation – Approval Letter & Login Credentials"
    message = (f'''
Dear {name},
Congratulations! We are delighted to inform you that you have been selected as a official volunteer for Pahal Foundation. Your dedication to making a difference is truly appreciated, and we are excited to have you on board.
To get started, you can log in to your volunteer dashboard using the credentials below:

Username: {username}
Password: {password}

Dashboard Link: https://admin.pahalkids.in/

Please ensure you log in and explore the dashboard for important updates and resources. If you face any issues accessing your account, feel free to reach out.
Thank you for joining us in our mission to empower underprivileged students. Looking forward to working together!

Best regards,
AkshatChourey & Krishnashish
Pahal Foundation Team
''')

    send_mail(subject, message, from_email, recipient_list)


def mail_suspension(volunteer_name, email_to):
    from_email = "pahalfoundationvitb@gmail.com"
    recipient_list = [email_to,]
    subject = "Temporary Suspension of Volunteer Account"
    message = (f'''
Dear {volunteer_name},
We hope you are doing well.

We wanted to inform you that your volunteer account has been temporarily suspended due to [reason—e.g., prolonged inactivity or other relevant issue]. At Pahal Foundation, we deeply value the commitment of our volunteers, and we encourage you to reach out if you’d like to resume your contributions.

If you believe this suspension was in error or wish to reactivate your account, please contact the Pahal Foundation coordinators at pahalkids@gmail.com. They will guide you on the next steps.

Thank you for your understanding, and we appreciate your support in our mission to empower underprivileged students.

Best regards,
Pahal Foundation Team

''')
    send_mail(subject, message, from_email, recipient_list)

def mail_removing_suspension(volunteer_name, email_to):
    from_email = "pahalfoundationvitb@gmail.com"
    recipient_list = [email_to,]
    subject = "Volunteer Account Reactivation"
    message = (f'''
Dear {volunteer_name},
We hope you are doing well.

We are happy to inform you that your volunteer account has been reinstated and is now active again. You can resume accessing the dashboard and contributing to Pahal Foundation’s mission.
Dashboard Link: https://admin.pahalkids.in/

If you face any issues logging in or need any assistance, please feel free to reach out to the Pahal Foundation coordinators at pahalkids@gmail.com.

Thank you for your commitment, and we look forward to working together again!

Best regards,
Pahal Foundation Team
''')
    send_mail(subject, message, from_email, recipient_list)

def mail_assign_task(volunteer_name, email_to, deadline):
    from_email = "pahalfoundationvitb@gmail.com"
    recipient_list = [email_to, ]
    subject = "New Task Assigned To You"
    message = (f'''
Dear {volunteer_name},
We hope you're doing well.
    
You’ve just been assigned a new task:
Please check your dashboard for full details regarding this task.
🗓️ Deadline: {deadline}
    
Your contribution plays a vital role in supporting Pahal Foundation’s mission, and we truly appreciate your efforts. For any questions, feel free to reach out to the coordinators.
    
Warm regards,
Pahal Foundation Team  
    ''')
    send_mail(subject, message, from_email, recipient_list)
