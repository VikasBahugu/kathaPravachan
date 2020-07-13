from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib import messages
from django.core.paginator import Paginator
from home.models import ContactUser, Profile, SigningUser, Newsletter, AnswerQuestions
from next_prev import next_in_order, prev_in_order

#FOR EMAILING KUNDALI INFORMATION.
import os
import smtplib
import imghdr
from email.message import EmailMessage



def answer_questions(request):
    if request.method == 'POST':
        kundali_answer = request.POST['kundali_answer']
    return redirect('dashboard')

def dashboard(request):
    if request.method == 'POST':
        kundali_answer = request.POST['kundali_answer']
        user = request.POST.get('user')
        print("DDDDDDDDDDDDDDDDDDD", user)

        if AnswerQuestions.objects.filter(user=user).exists():
            pq = AnswerQuestions.objects.filter(user=user)


    kundali = AnswerQuestions.objects.filter(status='not-seen')


    context = {
        'kundali':kundali,
    }
    return render(request, 'home/dashboard.html', context)


def shared_kundali(request):
    if request.method == 'POST':
        name = request.POST['name']
        dob = request.POST['dob']
        number = request.POST['number']
        reason = request.POST['reason']
        user = request.POST['user']
        status = request.POST['status']
        kundaliphoto = request.FILES['kundaliphoto']

        kn_obj = AnswerQuestions(name=name, dob=dob, number=number, reason=reason , status=status, user=user, kundaliphoto=kundaliphoto)
        kn_obj.save()
        messages.success(request, 'Your details along with your kundali has been sent to our astrologer. Now he may soon contact you. If there is no call with in 1-2 working hours, you may feel free to call.')
        messages.success(request, 'You will get all messages and replies here.')
        messages.success(request, 'In case you close it from the bar header, you can refresh it to see that again.')

        return redirect('homepage')
    return render(request, 'home/homepage.html')

# Create your views here.
def homepage(request):
    return render(request, 'home/homepage.html')

def singlepost(request):
    return render(request, 'home/singlepost.html')

def about(request):
    return render(request, 'home/about.html')

def videoblog(request):
    return render(request, 'home/videoblog.html')

def newsletter(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']

        newsletter = Newsletter(name=name, email=email)
        newsletter.save()
        messages.success(request, "Thankyou for subscribing to our newsletter. Now you will receive all our updates!")
        return redirect('homepage')
    return redirect('homepage')

def members(request):
    forlen = Profile.objects.all()
    context = {
        'profiles': [Profile.objects.all()],
        'prosize': len(forlen),
    }
    # print(context[0].photo,"********************************")
    return render(request, 'home/members.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        matter = request.POST['matter']

        contactuser = ContactUser(name=name, email=email, subject=subject, matter=matter)
        contactuser.save()
        messages.success(request, "Thankyou for contacting us. Our team will reach out to you soon.")
        return redirect('homepage')
    return render(request, 'home/contact.html')


def error_404_view(request, exception):
    return render(request, 'home/404.html')

def logout(request):
    if request.method == "GET":
        logout_auth(request)
        request.session.flush()
        messages.warning(request, "You have sucessfully been logged out of your account.")
        return redirect('homepage')
    return render(request, 'home/homepage.html')


def login(request):
    # user = request.user
    if request.user.is_authenticated:
    # do something if the user is authenticated
        return redirect('homepage')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            pass1 = request.POST['pass1']

            curr_user = authenticate(username=username, password=pass1)
            if curr_user is not None:
                login_auth(request, curr_user)

                messages.success(request, "Welcome back to Bhanu-Astrology. Now you may send your kundali to our astrologer to know more about it.")
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')

        users = User.objects.all()
        params = {
            'users': users,
        }
        return render(request, 'home/login.html', params)

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        fullname = request.POST['fullname']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        admin_key = request.POST['admin-key']
        gender = request.POST['gender']
        if pass1 == pass2:
            try:
                user = User.objects.get(username=username)
                return HttpResponse("User already exist with the username you enetered.")
            except User.DoesNotExist:
                if admin_key == 'QkfcXBlMishnF7ee1J1VzzBxMtcudkxX':
                    new_user = User.objects.create_superuser(username, email, pass1)
                else:
                    new_user = User.objects.create_user(username, email, pass1)
                if ' ' in fullname:
                    fname, lname = fullname.split(' ')
                    new_user.first_name = fname
                    new_user.last_name = lname
                else:
                    new_user.first_name = fullname


                # Updating signin model as well
                new_signin = SigningUser(fullname=fullname, passw=pass1, username=username, gender=gender)

                # updating to Profile as well
                name = fullname
                new_profile = Profile(fullname=name, gender=gender, email=email, username=username)

                new_user.save()
                new_signin.save()
                new_profile.save()

                curr_user = authenticate(username=username, password=pass1)
                if curr_user is not None:
                    login_auth(request, curr_user)



                    # SENDING EMAIL TO VIKAS AND THE ONE WHO HAS SIGNED IN.
                    EMAIL_ADDRESS = 'vikasedu10@gmail.com'
                    EMAIL_PASSWORD = 'Vivek@14vikas'

                    msg = EmailMessage()
                    msg['Subject'] = 'Welcome to Bhanu-Astrology'
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = email
                    msg.add_alternative("""
                    <html>
                        <body>
                            <h1>Welcome to Bhanu-Astrology.</h1>
                            <h4>Here you will find about your astrology, which means what is currently with your 'rashi' and you can even call our expert for free. </h4>
                            <h4 style="color:red">Note: We take no charge from anybody. So if anyone claims to take any fee regarding the same, please report to us.</h4>
                        </body>
                    </html>
                    """, subtype='html')

                    # image = ['mailimage.jpg']
                    image = ''
                    for file in image:
                        with open(file, 'rb') as f:  # here rb is read byte mode in which the file will open.
                            file_data = f.read()
                            file_type = imghdr.what(f.name)
                            filename = f.name
                        msg.add_attachment(file_data, maintype='doc', subtype=file_type, filename=filename)

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)

                    # SENDING EMAIL TO VIKAS AND THE ONE WHO HAS SIGNED IN.
                    EMAIL_ADDRESS = 'vikasedu10@gmail.com'
                    EMAIL_PASSWORD = 'Vivek@14vikas'

                    msg = EmailMessage()
                    msg['Subject'] = 'Welcome to Bhanu-Astrology'
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = 'vikasedu10@gmail.com'
                    msg.add_alternative("""
                                    <html>
                                        <body>
                                            <h1>Greetings from Bhanu-Astrology.</h1>
                                            <h4>Hello Bhanu and team. You have a new user just signed in. Please make sure that he gets benefit about comming in our platform. </h4>
                                            <h4 style="color:red">Note: Stay alert about false use of this platform.</h4>
                                        </body>
                                    </html>
                                    """, subtype='html')

                    # image = ['mailimage.jpg']
                    image = ''
                    for file in image:
                        with open(file, 'rb') as f:  # here rb is read byte mode in which the file will open.
                            file_data = f.read()
                            file_type = imghdr.what(f.name)
                            filename = f.name
                        msg.add_attachment(file_data, maintype='doc', subtype=file_type, filename=filename)

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)


                    messages.success(request, "Welcome to Bhanu-Astrogogy, your account has been created sucessfully.")
                    return redirect('homepage')


        else:
            return HttpResponse("Invalid password")

    users = User.objects.all()
    params = {
        'users' : users,
    }
    return render(request, 'home/signup.html', params)


def profile(request):

#     if request.method == 'POST':
#
#         current_user = request.user.username
#
#         if Profile.objects.filter(username=current_user).exists():
#             from_profile_model = Profile.objects.get(username=current_user)
#             old_photo = from_profile_model.photo
#         else:
#             old_photo = ''
#
#         new_username = request.POST['username']
#         name = request.POST['fullname']
#         bio = request.POST['bio']
#         dob = request.POST['dob']
#         gender = request.POST['gender']
#         marrystatus = request.POST['marrystatus']
#         address = request.POST['address']
#         number = request.POST['number']
#         email = request.POST['email']
#         languagesknown = request.POST['languagesknown']
#
#         if len(request.FILES) != 0:
#             new_photo = request.FILES['profilephoto']
#         else:
#             new_photo = old_photo
#
#
# # USER
#         a = 0
#         if User.objects.filter(username=new_username).exists():
#             a = 1
#             user = User.objects.get(username=new_username)
#             if ' ' in name:
#                 fname, lname = name.split(' ')
#             else:
#                 fname = name
#                 lname = ' '
#             user.username = new_username
#             user.first_name = fname
#             user.last_name = lname
#             user.email = email
#
#         else:
#             # It will update user if username is unique.
#             user = User.objects.get(username=current_user)
#             if ' ' in name:
#                 fname, lname = name.split(' ')
#             else:
#                 fname = name
#                 lname = ' '
#             user.username = new_username
#             user.first_name = fname
#             user.last_name = lname
#             user.email = email
#
# # SIGNUP
#         if SigningUser.objects.filter(username=new_username).exists():
#             signin_info = SigningUser.objects.get(username=new_username)
#             signin_info.fname = fname
#             signin_info.lname = lname
#             signin_info.username = new_username
#             signin_info.email = email
#             signin_info.gender = gender
#
#         else:
#             signin_info = SigningUser.objects.get(username=current_user)
#             signin_info.fname = fname
#             signin_info.lname = lname
#             signin_info.username = new_username
#             signin_info.email = email
#             signin_info.gender = gender
#
# # PROFILE
#         if Profile.objects.filter(username=new_username).exists():
#             new_profile = Profile.objects.get(username=new_username)
#             new_profile.username = new_username
#             new_profile.photo = new_photo
#             new_profile.fullname = name
#             new_profile.bio = bio
#             new_profile.dob = dob
#             new_profile.gender = gender
#             new_profile.marrystatus = marrystatus
#             new_profile.address = address
#             new_profile.number = number
#             new_profile.email = email
#             new_profile.languages = languagesknown
#
#         else:
#             new_profile = Profile.objects.get(username=current_user)
#             new_profile.username = new_username
#             new_profile.photo = new_photo
#             new_profile.fullname = name
#             new_profile.bio = bio
#             new_profile.dob = dob
#             new_profile.gender = gender
#             new_profile.marrystatus = marrystatus
#             new_profile.address = address
#             new_profile.number = number
#             new_profile.email = email
#             new_profile.languages = languagesknown
#
#
#         user_obj = Createpost.objects.filter(author=current_user)
#         for item in user_obj:
#             new_post_author = Createpost.objects.get(title=item)
#             new_post_author.author = new_username
#             new_post_author.save()
#
#         user.save()
#         signin_info.save()
#         new_profile.save()
#         if a == 0:
#             messages.success(request, "Your profile was updated successfully.")
#         else:
#             messages.warning(request, "Username was not updated because it already exists.")
#         return redirect('profile')
#
#
#     updated_username = request.user.username
#     updated_profile = Profile.objects.get(username=updated_username)
#     context = {
#         'from_profile' : updated_profile,
#     }

    return render(request,'home/profile.html')
