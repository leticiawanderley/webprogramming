from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from social.models import Member, Profile, Message

appname = 'Facemagazine'

# decorator that tests whether user is logged in
def loggedin(f):
    def test(request):
        if 'username' in request.session:
            return f(request)
        else:
            template = loader.get_template('social/not-logged-in.html')
            context = RequestContext(request, {'appname': appname})
            return HttpResponse(template.render(context))
    return test

def index(request):
    template = loader.get_template('social/index.html')
    context = RequestContext(request, {
    		'appname': appname,
    	})
    return HttpResponse(template.render(context))

def signup(request):
    template = loader.get_template('social/signup.html')
    context = RequestContext(request, {
    		'appname': appname,
    	})
    return HttpResponse(template.render(context))

def register(request):
    u = request.POST['user']
    p = request.POST['pass']
    user = Member(username=u, password=p)
    user.save()
    template = loader.get_template('social/user-registered.html')    
    context = RequestContext(request, {
        'appname': appname,
        'username' : u
        })
    return HttpResponse(template.render(context))

def login(request):
    if 'username' not in request.POST:
        template = loader.get_template('social/login.html')
        context = RequestContext(request, {
                'appname': appname,
            })
        return HttpResponse(template.render(context))
    else:
        u = request.POST['username']
        p = request.POST['password']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            raise Http404("User does not exist")
        if p == member.password:
            request.session['username'] = u;
            request.session['password'] = p;
            return render(request, 'social/login.html', {
                'appname': appname,
                'username': u,
                'loggedin': True}
                )
        else:
            return HttpResponse("Wrong password") 

@loggedin
def friends(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    template = 'social/friends.html'
    if 'remove' in request.POST:
        friend = request.POST['remove']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.friends.remove(friend_obj)
        member_obj.save()
        template = 'social/friends_ajax.html'
    # list of people I'm following
    friends = member_obj.friends.all()
    # list of people that are following me
    followers = Member.objects.filter(friends__username=username)
    # render reponse
    return render(request, template, {
        'appname': appname,
        'username': username,
        'members': members,
        'friends': friends,
        'followers': followers,
        'loggedin': True}
        )

@loggedin
def logout(request):
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()        
        template = loader.get_template('social/logout.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': u
            })
        return HttpResponse(template.render(context))
    else:
        raise Http404("Can't logout, you are not logged in")

def member(request, view_user):
    username = request.session['username']
    member = Member.objects.get(pk=view_user)

    if view_user == username:
        greeting = "Your"
    else:
        greeting = view_user + "'s"

    if member.profile:
        text = member.profile.text
    else:
        text = ""
    return render(request, 'social/member.html', {
        'appname': appname,
        'username': username,
        'view_user': view_user,
        'greeting': greeting,
        'profile': text,
        'loggedin': True}
        )

@loggedin
def members(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    template = 'social/members.html'
    # request a friendship
    if 'add' in request.POST:
        friend = request.POST['add']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.friendship_request.add(friend_obj)
        member_obj.save()
        template = 'social/members_ajax.html'
    # accept a friendship request
    elif 'accept' in request.POST:
        friend = request.POST['accept']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.friends.add(friend_obj)
        friend_obj.friendship_request.remove(member_obj)
        member_obj.save()
        template = 'social/members_ajax.html'
    # deny a friendship request
    elif 'deny' in request.POST:
        friend = request.POST['deny']
        friend_obj = Member.objects.get(pk=friend)
        friend_obj.friendship_request.remove(member_obj)
        friend_obj.save()
        template = 'social/members_ajax.html'
    # cancel a friendship request
    elif 'cancel' in request.POST:
        friend = request.POST['cancel']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.friendship_request.remove(friend_obj)
        member_obj.save()
        template = 'social/members_ajax.html'
    # remove friendship
    elif 'remove' in request.POST:
        friend = request.POST['remove']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.friends.remove(friend_obj)
        member_obj.save()
        template = 'social/members_ajax.html'

    # view user profile
    elif 'view' in request.GET:
        return member(request, request.GET['view']) 
    # list of all other members
    members = Member.objects.exclude(pk=username)
    # list of people I'm following
    friends = member_obj.friends.all()     
    # list of people that requested my friendship
    friendship_request = Member.objects.filter(friendship_request__username=username)
    # list of people that I requested friendship
    my_friendship_request = member_obj.friendship_request.all()
    
    recommendations = member_obj.get_recommendations()
    # render reponse
    return render(request, template, {   
        'appname': appname,
        'username': username,
        'members': members,
        'friends': friends,
        'friendship_request': friendship_request,
        'my_friendship_request': my_friendship_request,
        'recommendations': recommendations,
        'loggedin': True}
        )

@loggedin
def profile(request):
    u = request.session['username']
    member = Member.objects.get(pk=u)
    if 'text' in request.POST:
        text = request.POST['text']
        if member.profile:
            member.profile.text = text
            member.profile.save()
        else:
            profile = Profile(text=text)
            profile.save()
            member.profile = profile
        member.save()
    else:
        if member.profile:
            text = member.profile.text
        else:
            text = ""
    return render(request, 'social/profile.html', {
        'appname': appname,
        'username': u,
        'text' : text,
        'loggedin': True}
        )

@loggedin
def messages(request):
    username = request.session['username']
    user = Member.objects.get(pk=username)
    # Whose message's are we viewing?
    if 'view' in request.GET:
        view = request.GET['view']
    else:
        view = username
    recip = Member.objects.get(pk=view)
    # If message was deleted
    if 'erase' in request.GET:
        msg_id = request.GET['erase']
        Message.objects.get(id=msg_id).delete()
    # If text was posted then save on DB
    if 'text' in request.POST:
        text = request.POST['text']
        pm = request.POST['pm'] == "0"
        message = Message(user=user,recip=recip,pm=pm,time=timezone.now(),text=text)
        message.save()
    messages = Message.objects.filter(recip=recip)
    profile_obj = Member.objects.get(pk=view).profile
    profile = profile_obj.text if profile_obj else ""
    return render(request, 'social/messages.html', {
        'appname': appname,
        'username': username,
        'profile': profile,
        'view': view,
        'messages': messages,
        'loggedin': True}
        )

""" Check if the username inserted is available
"""
def checkusersignup(request):
    if 'user' in request.POST:
        u = request.POST['user']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
            return render(request, "social/username_taken.html", RequestContext(request, locals()))
        else:
            return render(request, "social/username_free.html", RequestContext(request, locals()))

""" Check if the username inserted as login is already registered
"""
def checkuserlogin(request):
    if 'user' in request.POST:
        u = request.POST['user']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
            return render(request, "social/username_registered.html", RequestContext(request, locals()))
        else:
            return render(request, "social/username_unregistered.html", RequestContext(request, locals()))

