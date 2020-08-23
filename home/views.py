from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib import messages
from home.models import ContactUser, Profile, SigningUser, Newsletter, AnswerQuestion, Twelve_rashi, Videoblog_video

#FOR EMAILING KUNDALI INFORMATION.
import os
import smtplib
import imghdr
from email.message import EmailMessage



def delete_edit_videopost(request):
    if request.method == 'POST':
        if 'delete_video' in request.POST:
            id = request.POST['deleteid']
            delete_v = Videoblog_video.objects.get(id=id)
            delete_v.delete()
            messages.success(request, 'Video was successfully deleted from the blog.')
            return redirect('videoblog')

        if 'edit_video' in request.POST:
            editid = request.POST['editid']
            link = request.POST['link']
            tag = request.POST['tag']
            title = request.POST['title']
            description = request.POST['description']

            v = str(link)
            if '/embed/' not in v:
                if '/watch?v=' not in v:
                    vv = v.replace('https://www.youtube.com/', 'https://www.youtube.com/embed/')
                else:
                    vv = v.replace('https://www.youtube.com/watch?v=', 'https://www.youtube.com/embed/')
                link = vv

            get_obj = Videoblog_video.objects.get(id=editid)
            prev_title = get_obj.title
            get_obj.link = link
            get_obj.tag = tag
            get_obj.title = title
            get_obj.description = description
            get_obj.save()

            emails = Newsletter.objects.all().values()
            for email in emails:
                name = email['name']
                subject = 'Video edited in Bhanu-Astrology'
                to = email['email']

                message = f"""
                            <div style="color:black; padding:2%; border-radius:6px; background-color: #D9AFD9; background-image: linear-gradient(0deg, #D9AFD9 0%, #97D9E1 100%);">
                            <h2>Message from www.bhanuastrology.com</h2>
                            <p style='color:black;'>Dear {name}, 
                            <br>This is to inform you that www.bhanuastrology.com has just edited 
                            a videopost titled: <strong>{prev_title}</strong>. 
                            To see the video, 
                            <a href="https://www.bhanuastrology.com/videoblog" style="padding:10px; border-radius:7px; text-align:center;background-color: #FBAB7E; background-image: linear-gradient(62deg, #FBAB7E 0%, #F7CE68 100%);">See video</a><br><br>
                            You have receive this mail because you were subscribed to our newsletter.<br>
                            Ask astrology related queries from our astrologer.
                            <ul>
                            <li>Dosh mukti</li>
                            <li>Questions related to your kundali</li>
                            <li>Having rough weekends or anxieties.</li>
                            <li>Negetive feeling, unhappy moods, or mood swings.</li>
                            </ul>
                            Thanks and Regrads<br>Team Bhanu-Astrology.
                            </div>"""

                send_mail(subject, to, message)


            messages.success(request, 'Video post was successfully modified and an email was sent to all the subscribers.')
            return redirect('videoblog')



def twelve_rashi(request):

    if request.method == 'POST':
        maish = request.POST['maish']
        vrish = request.POST['vrish']
        mithun = request.POST['mithun']
        kark = request.POST['kark']
        singh = request.POST['singh']
        kanya = request.POST['kanya']
        tula = request.POST['tula']
        vrishchik = request.POST['vrishchik']
        dhanu = request.POST['dhanu']
        makar = request.POST['makar']
        kumbh = request.POST['kumbh']
        meen = request.POST['meen']

        tv_rashi = Twelve_rashi.objects.all()

        if len(tv_rashi) == 0:
            new_obj = Twelve_rashi()
            new_obj.save()
        Twelve_rashi.objects.all()[:1].get()

        all_rashi = Twelve_rashi.objects.all()[:1].get()
        # for x in asd:
        #     print(x,'dd')
        all_rashi.maish = maish
        all_rashi.vrish = vrish
        all_rashi.mithun = mithun
        all_rashi.kark = kark
        all_rashi.singh = singh
        all_rashi.kanya = kanya
        all_rashi.tula = tula
        all_rashi.vrishchik = vrishchik
        all_rashi.dhanu = dhanu
        all_rashi.makar = makar
        all_rashi.kumbh = kumbh
        all_rashi.meen = meen

        all_rashi.save()
        messages.success(request, 'All rashis have been saved (राशि को अपडेट कर दिया गया है! )')
        return redirect('dashboard')
    return HttpResponse("Not working")



def send_mail(subject, to, body_html):
    # SENDING EMAIL TO VIKAS AND THE ONE WHO HAS SIGNED IN.
    EMAIL_ADDRESS = 'bhanuastrology@gmail.com'
    EMAIL_PASSWORD = 'Bhanu@astrology'

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg.add_alternative(body_html, subtype='html')

    # # image = ['mailimage.jpg']
    # image = ''
    # for file in image:
    #     with open(file, 'rb') as f:  # here rb is read byte mode in which the file will open.
    #         file_data = f.read()
    #         file_type = imghdr.what(f.name)
    #         filename = f.name
    #     msg.add_attachment(file_data, maintype='doc', subtype=file_type, filename=filename)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)



def delete_answered_question(request):
    if request.user.is_superuser or request.user.is_superuser:
        try:
            for_user = AnswerQuestion.objects.filter(user=request.user)
            for_user.delete()
            messages.success(request, "Your previous query was sucessfully removed from our database. You can now ask more related questions.")
        except AnswerQuestion.DoesNotExist:
            messages.success(request, "Sorry your question does not exists. It may have occured due to some technical issue.")
    return redirect('homepage')



def answer_questions(request):
    if request.method == 'POST':
        kundali_answer = request.POST['kundali_answer']
        messages.success(request, "Thankyou for answering people. They will receive your suggestions when they will come back.")
    return redirect('dashboard')



def dashboard(request):
    if request.method == 'POST':
        kundali_answer = request.POST['kundali_answer']
        user = request.POST['user']

        if AnswerQuestion.objects.filter(user=user).exists():
            pq = AnswerQuestion.objects.filter(user=user).first()
        all = AnswerQuestion.objects.filter(user=pq.user,status='not-seen')

        for x in all:
            x.status = 'seen'
            x.kundali_answer = kundali_answer
            x.save()

    kundali = AnswerQuestion.objects.filter(status='not-seen').order_by('-timestamp')

    new_obj_for_twelve = Twelve_rashi.objects.all()
    if len(new_obj_for_twelve) == 0:
        obj_new = Twelve_rashi()
        obj_new.save()
    new_obj_for_twelve = Twelve_rashi.objects.all()
    context = {
        'kundali':kundali,
        '12_rashi' : new_obj_for_twelve,
    }


    all = AnswerQuestion.objects.filter(user=request.user, status='seen')
    for_expert = AnswerQuestion.objects.filter(status='not-seen')
    context.update({
        'size_badge': len(all),
        'for_expert_badge': len(for_expert),
        'mem_len': len(SigningUser.objects.all())
    })

    return render(request, 'home/dashboard.html', context)



def shared_kundali(request):
    if request.user.is_authenticated or request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST['name']
            dob = request.POST['dob']
            number = request.POST['number']
            reason = request.POST['reason']
            user = request.POST['user']
            status = request.POST['status']
            kundali_answer = ''
            if len(request.FILES):
                kundaliphoto = request.FILES['kundaliphoto']
            else:
                kundaliphoto = ''


            if AnswerQuestion.objects.filter(user=user).exists():
                print("Question already exist bastard>!!!")
                question_record = AnswerQuestion.objects.get(user=user)
                question_record.name = name
                question_record.dob = dob
                question_record.number = number
                question_record.reason = reason
                question_record.kundali_answer = kundali_answer
                question_record.status = status
                question_record.kundaliphoto = kundaliphoto

                question_record.save()

            elif not AnswerQuestion.objects.filter(user=user).exists():
                print("Question does not exist>!!!")
                kn_obj = AnswerQuestion(name=name, dob=dob, number=number, reason=reason , status=status, user=user, kundaliphoto=kundaliphoto)
                kn_obj.save()

            subject = name + ' asked a question'
            to = 'vikasedu10@gmail.com'

            message = f"""
                        <div style="color:black; padding:2%; border-radius:6px; background-color: #D9AFD9; background-image: linear-gradient(0deg, #D9AFD9 0%, #97D9E1 100%);">
                        <h2>Someone asked a question,</h2>
                        <p style='color:black;'>Dear Bhanu Prakash, 
                        <br>This is to inform you that <strong>{name}</strong>, has asked a question. Details are refered below:<br><strong>Name:</strong> {name}<br><strong>Date of birth:</strong>{dob}<br><strong>Contact No.:</strong>{number}<br><strong>Reason and Questions:</strong>{reason}<br><br>Answer them at <br><strong>https://www.bhanuastrology.com/dashboard</strong><br> You will receive all questions in your email and you can see the list of questions in the provided link also.<br><br>
                        Go to dashboard to answer questions.<br><br>
                        <a href="www.bhanuastrology.com/dashboard" style="padding:10px; border-radius:7px; text-align:center;background-color: #FBAB7E; background-image: linear-gradient(62deg, #FBAB7E 0%, #F7CE68 100%);">Dashboard</a><br><br>
                        Thankyou!</p>
                        </div>"""

            send_mail(subject, to, message)

            messages.success(request, 'Your details along with your kundali has been sent to our astrologer.')
            messages.success(request, 'If the reply to your question does not appear with in 3-4 working hours (due to more requests), feel free to contact.')

            return redirect('homepage')
        else:
            return HttpResponse("Not a user")
    return render(request, 'home/homepage.html')



def videoblog_video(request):
    if request.method == 'POST':
        link = request.POST['link']
        tag = request.POST['tag']
        title = request.POST['title']
        description = request.POST['description']

        v = str(link)
        if '/embed/' not in v:
            if '/watch?v=' not in v:
                vv = v.replace('https://www.youtube.com/', 'https://www.youtube.com/embed/')
            else:
                vv = v.replace('https://www.youtube.com/watch?v=', 'https://www.youtube.com/embed/')
            link = vv

        upload_video = Videoblog_video(videolink=link, tag=tag, title=title, description=description)
        upload_video.save()

        emails = Newsletter.objects.all()
        for email in emails:
            subject = 'New video posted in www.bhanuastrology.com'
            to = email

            message = f"""
                        <div style="color:black; padding:2%; border-radius:6px; background-color: #D9AFD9; background-image: linear-gradient(0deg, #D9AFD9 0%, #97D9E1 100%);">
                        <h2>Message from www.bhanuastrology.com</h2>
                        <p style='color:black;'>Dear {email.name}, 
                        <br>This is to inform you that Bhanu-Astrology has just created a videopost titled: <strong>{title}</strong>. To see the video, go to the following link:<br>https://bhanuastrology.com/videoblog<br> You have receive this mail because you were subscribed to our newsletter.
                        <a href="www.bhanuastrology.com/login" style="padding:10px; border-radius:7px; text-align:center;background-color: #FBAB7E; background-image: linear-gradient(62deg, #FBAB7E 0%, #F7CE68 100%);">Login</a><br><br>
                        Ask astrology related queries from our astrologer.
                        <ul>
                        <li>Dosh mukti</li>
                        <li>Questions related to your kundali</li>
                        <li>Having rough weekends or anxieties.</li>
                        <li>Negetive feeling, unhappy moods, or mood swings.</li>
                        </ul>
                        Thanks and Regrads<br>Team Bhanu-Astrology.</p>
                        </div>"""


            send_mail(subject, to, message)

        messages.success(request, 'Your video has been successfully posted and sent to all your subscribers. Happy journey!')
        return redirect('videoblog')



def homepage(request):
    # SENDING msg TO VIKAS AND THE ONE WHO HAS SIGNED IN.
    # Your new Phone Number is +12029725928

    # # Your Account Sid and Auth Token from twilio.com/console
    # # DANGER! This is insecure. See http://twil.io/secure
    # account_sid = 'AC57821e6c47ff3f067f2dd8249cd49232'
    # auth_token = 'bb6a71d0e2627a265bf9d52f074747cd'
    # client = Client(account_sid, auth_token)
    #
    # message = client.messages \
    #     .create(
    #     body="Someone have entered to your website.",
    #     from_='+12029725928',
    #     to='+917895579330'
    # )
    #
    # print(message.sid)

    emails = User.objects.filter(is_active=True).exclude(email='').values_list('email', flat=True)
    params = {}

    if request.user.is_authenticated or request.user.is_superuser:
        try:
            answers = AnswerQuestion.objects.get(user=request.user)
            params = {
                'seen_msgs': answers,
            }
        except AnswerQuestion.DoesNotExist:
            pass

        if AnswerQuestion.objects.filter(user=request.user).exists():
            pq = AnswerQuestion.objects.filter(user=request.user).first()
        all = AnswerQuestion.objects.filter(user=request.user, status='seen')
        for_expert = AnswerQuestion.objects.filter(status='not-seen')
        params.update( {
            'size_badge':len(all),
            'for_expert_badge': len(for_expert),
        } )

    tv_rashi =  Twelve_rashi.objects.all()
    if len(tv_rashi) == 0:
        new_obj = Twelve_rashi()
        new_obj.save()
    tv_rashi = Twelve_rashi.objects.all()
    params.update({'12_rashi': tv_rashi})
    params.update({'mem_len': len(SigningUser.objects.all())})

    return render(request, 'home/homepage.html', params)



def singlepost(request):
    return render(request, 'home/singlepost.html')



def about(request):
    params = {}

    # about page me badge me pending messages honge (kundli ke rpy)
    all = AnswerQuestion.objects.filter(user=request.user, status='seen')
    for_expert = AnswerQuestion.objects.filter(status='not-seen')
    params.update({
        'size_badge': len(all),
        'for_expert_badge': len(for_expert),
        'mem_len': len(SigningUser.objects.all())
    })
    return render(request, 'home/about.html', params)



def videoblog(request):
    all_videos = Videoblog_video.objects.all().values().order_by('-timestamp')
    params = {'videos': all_videos}

    # videoblog page me agr koi pending messages honge to vo dikh jaenge.
    all = AnswerQuestion.objects.filter(user=request.user, status='seen')
    for_expert = AnswerQuestion.objects.filter(status='not-seen')
    params.update({
        'size_badge': len(all),
        'for_expert_badge': len(for_expert),
        'mem_len': len(SigningUser.objects.all()),
    })

    return render(request, 'home/videoblog.html', params)



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
    if AnswerQuestion.objects.filter(user=request.user).exists():
        pq = AnswerQuestion.objects.filter(user=request.user).first()
    all = AnswerQuestion.objects.filter(user=request.user, status='seen')
    for_expert = AnswerQuestion.objects.filter(status='not-seen')
    context.update({
        'size_badge': len(all),
        'for_expert_badge': len(for_expert),
        'mem_len': len(SigningUser.objects.all()),
    })

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

        subject = 'Someone want to contact you.'
        to = 'vikasedu10@gmail.com'

        body_html = f"""
                    <div style="color:black; padding:2%; border-radius:6px; background-color: #D9AFD9; background-image: linear-gradient(0deg, #D9AFD9 0%, #97D9E1 100%);">
                    <h2>Message to admin</h2>
                    <p style='color:black;'>Dear Bhanu Prakash, 
                    <br>Dear Admin, <br>This is to inform you that someone want to contact you. Details are shared below: <br>
                    <strong>Name: </strong>{name}<br>
                    <strong>Email: </strong>{email}<br>
                    <strong>Subject: </strong>{subject}<br>
                    <strong>Matter: </strong>{matter}<br>
                    It is therefore a request that you contact back as soon as possible.<br>
                    Thankyou!</p>
                    </div>"""

        send_mail(subject, to, body_html)

        messages.success(request, f'Thankyou for contacting us {name}. Our team will reach out to you at {email}.')
        return redirect('homepage')

    if AnswerQuestion.objects.filter(user=request.user).exists():
        pq = AnswerQuestion.objects.filter(user=request.user).first()
    all = AnswerQuestion.objects.filter(user=request.user, status='seen')
    for_expert = AnswerQuestion.objects.filter(status='not-seen')
    params = {}
    params.update({
        'size_badge': len(all),
        'for_expert_badge': len(for_expert),
        'mem_len': len(SigningUser.objects.all()),
    })

    return render(request, 'home/contact.html', params)


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
                if admin_key == 'AAaaBBccDDeeOTXzSMT1234BB_Z8JzG7JkSVxI':
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
                new_signin = SigningUser(fullname=fullname,  username=username, gender=gender)

                # updating to Profile as well
                name = fullname
                new_profile = Profile(fullname=name, gender=gender, email=email, username=username)

                new_user.save()
                new_signin.save()
                new_profile.save()

                curr_user = authenticate(username=username, password=pass1)
                if curr_user is not None:
                    login_auth(request, curr_user)

                    # To the person who signup
                    subject = "'bhanuastrology' welcomes you"
                    to = email

                    body_html = f"""
                                <div style="color:black; padding:2%; border-radius:6px; background-color: #D9AFD9; background-image: linear-gradient(0deg, #D9AFD9 0%, #97D9E1 100%);">
                                <h2>Welcome to www.bhanuastrology.com,</h2>
                                <p style='color:black;'>Dear {fullname}, 
                                <br>Here you will find about your astrology, which means what is currently with your 'rashi' 
                                and you can even call our expert for free.
                                <br><strong>Username: </strong>{username}
                                <br><strong>Password: </strong>{pass2}<br>
                                Please don't share your password with anyone.<br><br>
                                <a href="www.bhanuastrology.com/profile" style="padding:10px; border-radius:7px; text-align:center;background-color: #FBAB7E; background-image: linear-gradient(62deg, #FBAB7E 0%, #F7CE68 100%);">Update profile</a><br><br>
                                Now you can ask astrology related queries from our astrologer.
                                <ul>
                                <li>Dosh mukti</li>
                                <li>Questions related to your kundali</li>
                                <li>Having rough weekends or anxieties.</li>
                                <li>Negetive feeling, tension related solutions.</li>
                                </ul>
                                Thanks and Regrads<br>Team Bhanu-Astrology.
                                <p style='color:red; font-weight:300'>Note: We take no charge from anybody. So if anyone 
                                claims to take any fee regarding the same, please report to us.</p><br>
                                </div>"""
                    send_mail(subject, to, body_html)

                    # to admin to let them know
                    fullname = fullname
                    email = email
                    username = username
                    subject = fullname + ' just signed up'
                    to = 'bhanuastrology@gmail.com'
                    body_html = f"""
                                <div style="color:black; padding:2%; border-radius:6px; background-color: #D9AFD9; background-image: linear-gradient(0deg, #D9AFD9 0%, #97D9E1 100%);">
                                <h2>Admin panel,</h2>
                                <p style='color:black;'>Dear Bhanu, 
                                <br>Dear Bhanu and team. You have a new user, 
                                <strong>{fullname}</strong> as <strong>{username}</strong>, signed in as <strong>{email}</strong>. Please make sure that he gets benefit
                                about comming in our platform. <br>
                                Please make sure that you stay connected with people.<br><br>
                                <a href="www.bhanuastrology.com/login" style="padding:10px; border-radius:7px; text-align:center;background-color: #FBAB7E; background-image: linear-gradient(62deg, #FBAB7E 0%, #F7CE68 100%);">Home</a><br><br>
                                Thankyou!<br>
                                </div>"""

                    send_mail(subject, to, body_html)

                    # SENDING msg TO VIKAS AND THE ONE WHO HAS SIGNED IN.
                    # Your new Phone Number is +12029725928
                    # Download the helper library from https://www.twilio.com/docs/python/install
                    # from twilio.rest import Client
                    #
                    # # Your Account Sid and Auth Token from twilio.com/console
                    # # DANGER! This is insecure. See http://twil.io/secure
                    # account_sid = 'AC57821e6c47ff3f067f2dd8249cd49232'
                    # auth_token = 'bb6a71d0e2627a265bf9d52f074747cd'
                    # client = Client(account_sid, auth_token)
                    #
                    # message = client.messages \
                    #     .create(
                    #     body="Someone have just created an account.",
                    #     from_='+12029725928',
                    #     to='+917895579330'
                    # )
                    #
                    # print(message.sid)

                    messages.success(request, f"Welcome to 'www.bhanuastrology.com', {fullname} your account has been created sucessfully. To ask queries about your kundali or astrology, go to kundali share option.")
                    return redirect('homepage')


        else:
            return HttpResponse("Invalid password")

    users = User.objects.all()
    params = {
        'users' : users,
    }

    all = AnswerQuestion.objects.filter(user=request.user, status='seen')
    for_expert = AnswerQuestion.objects.filter(status='not-seen')
    params.update({
        'size_badge': len(all),
        'for_expert_badge': len(for_expert),
    })
    return render(request, 'home/signup.html', params)



def profile(request):
    context = {}


    if request.method == 'POST':

        current_user = request.user.username

        if Profile.objects.filter(username=current_user).exists():
            from_profile_model = Profile.objects.get(username=current_user)
            old_photo = from_profile_model.profile_photo
        else:
            old_photo = ''

        new_username = request.POST['username']
        name = request.POST['fullname']
        bio = request.POST['bio']
        dob = request.POST['dob']
        gender = request.POST['gender']
        # gender = 'Male'
        number = request.POST['number']
        email = request.POST['email']

        if len(request.FILES) != 0:
            new_photo = request.FILES['profile_photo']
        else:
            new_photo = old_photo


# USER
        a = 0
        if User.objects.filter(username=new_username).exists():
            a = 1
            user = User.objects.get(username=new_username)
            if ' ' in name:
                fname, lname = name.split(' ')
            else:
                fname = name
                lname = ''
            user.username = new_username
            user.first_name = fname
            user.last_name = lname
            user.email = email

        else:
            # It will update user if username is unique.
            user = User.objects.get(username=current_user)
            if ' ' in name:
                fname, lname = name.split(' ')
            else:
                fname = name
                lname = ' '
            user.username = new_username
            user.first_name = fname
            user.last_name = lname
            user.email = email

# SIGNUP
        if SigningUser.objects.filter(username=new_username).exists():
            signin_info = SigningUser.objects.get(username=new_username)
            signin_info.username = new_username

        else:
            signin_info = SigningUser.objects.get(username=current_user)
            signin_info.username = new_username
        signin_info.fname = fname
        signin_info.lname = lname
        signin_info.email = email
        signin_info.gender = gender

# PROFILE
        if Profile.objects.filter(username=new_username).exists():
            new_profile = Profile.objects.get(username=new_username)
            new_profile.username = new_username

        else:
            new_profile = Profile.objects.get(username=current_user)
            new_profile.username = new_username
        new_profile.profile_photo = new_photo
        new_profile.dob = dob
        new_profile.fullname = name
        new_profile.bio = bio
        new_profile.gender = gender
        new_profile.number = number
        new_profile.email = email


        user.save()
        signin_info.save()
        new_profile.save()
        if a == 0:
            messages.success(request, "Your profile was updated successfully.")
        else:
            messages.warning(request, "Username was not updated because it already exists.")

        return redirect('profile')

#
    all = AnswerQuestion.objects.filter(user=request.user, status='seen')
    for_expert = AnswerQuestion.objects.filter(status='not-seen')
    context.update({
        'size_badge': len(all),
        'for_expert_badge': len(for_expert),
    })
    context.update({'mem_len': len(SigningUser.objects.all())})

    updated_username = request.user.username

    try:
        updated_profile = Profile.objects.get(username=updated_username)

        blank = 'm'
        if updated_profile.gender == 'Female':
            blank = 'f'
        elif updated_profile.gender == 'Custom':
            blank = 'c'

        context.update({
            'blank' : blank,
            'from_profile' : updated_profile,
        })
    except Profile.DoesNotExist:
        pass

    return render(request, 'home/profile.html', context)

def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'home/terms_of_services.html')



def horoscope(request, horoscope_name=None):
    obj = Twelve_rashi.objects.first()
    about_that_horoscope = getattr(obj, horoscope_name)
    print(about_that_horoscope,"########")

    print('(',horoscope_name,')')
    new_p = ''
    if horoscope_name == 'mithun':
        new_p = 'gemini'
    if horoscope_name == 'kanya':
        new_p = 'virgo'
    params = {
        'all_horoscope': Twelve_rashi.objects.all(),
        'particular': [horoscope_name, about_that_horoscope, new_p],
    }
    return render(request, 'home/horoscope_page_for_all.html', params)