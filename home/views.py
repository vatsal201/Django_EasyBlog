from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,  login, logout
from blog.models import Post
# Create your views here.
def home(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, "home/home.html", context)

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message =request.POST['message']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(message)<4:
            message.s.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, "Your response has been submitted sucessfully!")
    return render(request, "home/contact.html")

def search(request):
    query=request.GET['query']
    if len(query)>50:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

def handleSignUp(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already registered. Please try with another username")
            return redirect('home')

        if len(username)>10:
            messages.error(request, " Your username must be under 10 characters")
            return redirect('home')
        
        if len(username)<2 or len(fname)<2 or len(lname)<2:
            messages.error(request, "Please fill the form correctly")
            return redirect('home')

        if len(pass1)<5:
            messages.error(request, " Your password must contain minimum 5 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " Username should only contain letters and numbers")
            return redirect('home')

        if (pass1!= pass2):
             messages.error(request, " Passwords did not match")
             return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")

def handeLogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged out")
    return redirect('home')