from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login



# Create your views here.
def home(request):
    return render(request,'carousel.html')
def About(request):
    return render(request,'about.html')

def signup(request):
    error=False
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        u=request.POST['uname']
        p=request.POST['pwd']
        ad=request.POST['add']
        m=request.POST['mobile']
        g=request.POST['male']
        d=request.POST['birth']
        e=request.POST['email']
        i=request.FILES['img']
        user = User.objects.create_user(first_name=f,last_name=l,username=u,password=p,email=e)
        Register.objects.create(user=user,gen=g,add=ad,mobile=m,birth=d,image=i)
        error=True
    d={'error':error}
    return render(request,'signup.html',d)

def signin(request):
    error = ""
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            elif user:
                login(request, user)
                error = "no"
        except:
            error = "yes"
    d={'error':error}
    return render(request,'signin.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def Search(request):
    room=Owner_Detail.objects.all()
    state1=State.objects.all()
    if request.method=='POST':
        s=request.POST['state']
        state=State.objects.filter(state=s).first()
        return redirect('dist',state.id)
    d = {'state': state1,'room':room}
    return render(request,'serach.html',d)
def dist(request,dist):
    state=State.objects.get(id=dist)
    room=Owner_Detail.objects.filter(state=state).all()
    dist=District.objects.filter(state=dist)
    if request.method=='POST':
        s=request.POST['dist']
        dist1=District.objects.filter(dist=s).first()
        return redirect('room',dist1.id)
    d={'dist':dist,'state':state,'room':room}
    return render(request,'dist.html',d)

def room(request,dist):
    dist1 = District.objects.get(id=dist)
    room = Owner_Detail.objects.filter(dist=dist1)
    d={'room':room,'dist':dist1}
    return render(request,'room.html',d)

def detail(request,dist):
    own=Owner_Detail.objects.get(id=dist)
    img = Image.objects.filter(owner=own)
    d={'img':img,'dist':own}
    return render(request,'detail.html',d)

def detail1(request,dist):
    if not request.user.is_authenticated:
        return redirect('home')
    own=Owner_Detail.objects.get(id=dist)
    img = Image.objects.filter(owner=own)
    d={'img':img,'dist':own}
    return render(request,'detail1.html',d)


def Contact(request):
    return render(request,'contact.html')

def rent1(request):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    st=State.objects.all()
    if request.method=="POST":
        try:
            s=request.POST['state']
            state=State.objects.filter(state=s).first()
            return redirect('rent',state.id)

        except:
            pass

    d={'state':st,'error':error}
    return render(request,'rent.html',d)

def rent(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    st2=State.objects.all()
    st=State.objects.get(id=pid)
    dist2=District.objects.filter(state=st)
    if request.method=="POST":
        try:
            s=request.POST['state']
        except:
            pass
        try:
            d=request.POST['dist']
            l=request.POST['local']
            t=request.POST['title']
            de=request.POST['desc']
            r=request.POST['rent']
            i=request.FILES['img']
            dist1=District.objects.filter(dist=d).first()
            req=User.objects.filter(username=request.user.username).first()
            re=Register.objects.filter(user=req).first()
            status=Status.objects.get(status="pending")
            Owner_Detail.objects.create(status=status,register=re,state=st,dist=dist1,title=t,local_add=l,desc=de,rent=r,img=i)
            error=True
        except:
            pass
    d={'dist':dist2,'state':st2,'st':st,'error':error}
    return render(request,'rent.html',d)

def Room_Img(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user=User.objects.get(id=request.user.id)
    reg=Register.objects.filter(user=user).first()
    room=Owner_Detail.objects.filter(register=reg).all()
    d={'room':room}
    return render(request,'room_image.html',d)

def Add_Room_Img(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    room=Owner_Detail.objects.get(id=pid)
    if request.method=="POST":
        r=request.POST['name']
        i=request.FILES['img']
        Image.objects.create(owner=room,room_name=r,img=i)
        error=True
    d={'error':error,'pid':pid}
    return render(request,'add_room_img.html',d)

def Owner_detail(request,pid):
    own=Owner_Detail.objects.get(id=pid)
    d={'own':own}
    return render(request,'owner_detail.html',d)

def User_detail(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user=User.objects.filter(id=request.user.id).first()
    register=Register.objects.filter(user=user).first()
    d={'register':register}
    return render(request,'user_detail.html',d)


def edit_detail1(request,data):
    if not request.user.is_authenticated:
        return redirect('home')
    error = False
    st = State.objects.all()
    if request.method == "POST":
        try:
            s = request.POST['state']
            state = State.objects.filter(state=s).first()
            return redirect('edit_detail', state.id,data)

        except:
            pass

    d = {'state': st, 'error': error}
    return render(request, 'edit_detail.html', d)


def Edit_detail(request,data1,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    data=Owner_Detail.objects.get(id=pid)
    state=State.objects.all()
    st = State.objects.get(id=data1)
    dist2 = District.objects.filter(state=st)
    if request.method=="POST":
        try:
            s = request.POST['state']
        except:
            pass
        d = request.POST['dist']
        l = request.POST['local']
        t = request.POST['title']
        de = request.POST['desc']
        r = request.POST['rent']
        try:
            i = request.FILES['img']
            data.img = i
            data.save()
        except:
            pass

        dist1 = District.objects.filter(dist=d).first()
        data.state = st
        data.dist = dist1
        data.desc = de
        data.rent = r
        data.local_add = l
        data.title = t
        data.save()
        error=True
    d={'data':data,'dist':dist2,'state':state,'st':st,'error':error}
    return render(request,'edit_detail.html',d)

def delete_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    Own=Owner_Detail.objects.get(id=pid)
    Own.delete()
    return redirect('img')


def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    Own=Register.objects.get(id=pid)
    Own.delete()
    return redirect('view_user')

def delete_dist(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    Own=District.objects.get(id=pid)
    Own.delete()
    return redirect('view_dist')

def delete_state(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    Own=State.objects.get(id=pid)
    Own.delete()
    return redirect('view_state')

def View_User(request):
    if not request.user.is_staff:
        return redirect('home')
    data=Register.objects.all()
    d={'data':data}
    return render(request,'view_user.html',d)

def Edit_User(request,pid):
    if not request.user.is_staff:
        return redirect('home')
    error = False
    data=Register.objects.get(id=pid)
    if request.method=="POST":
        u=request.POST['uname']
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        m=request.POST['mobile']
        a=request.POST['add']
        data.user.username=u
        data.user.first_name=f
        data.user.last_name=l
        data.user.email=e
        data.add=a
        data.mobile=m
        data.save()
        error=True
    d={'data':data,'error':error}
    return render(request,'edit_user.html',d)

def Edit_State(request,pid):
    if not request.user.is_staff:
        return redirect('home')
    error = False
    data=State.objects.get(id=pid)
    if request.method=="POST":
        u=request.POST['state']
        data.state=u
        data.save()
        error=True
    d={'data':data,'error':error}
    return render(request,'edit_state.html',d)
def Add_State(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method=="POST":
        s=request.POST['state']
        State.objects.create(state=s)
        return redirect('view_state')
    return render(request,'add_state.html')
def Add_District(request):
    if not request.user.is_staff:
        return redirect('home')
    state=State.objects.all()
    if request.method=="POST":
        s=request.POST['state']
        d=request.POST['dist']
        st=State.objects.get(state=s)
        District.objects.create(state=st,dist=d)
        return redirect('view_dist')
    d={'state':state}
    return render(request,'add_dist.html',d)
def View_State(request):
    if not request.user.is_staff:
        return redirect('home')
    state=State.objects.all()
    d={'state':state}
    return render(request,'view_state.html',d)

def View_District(request):
    if not request.user.is_staff:
        return redirect('home')
    dist=District.objects.all()
    d={'dist':dist}
    return render(request,'view_dist.html',d)

def View_Request(request):
    if not request.user.is_staff:
        return redirect('home')
    error=True
    own=Owner_Detail.objects.all()
    d={'data':own}
    return render(request,"request.html",d)

def Change(request,data,pid):
    if not request.user.is_staff:
        return redirect('home')
    own=Owner_Detail.objects.get(id=pid)
    if int(data) == 1:
        st1=Status.objects.get(status="accepted")
        own.status=st1
        own.save()
    elif int(data) == 2:
        st2 = Status.objects.get(status="rejected")
        own.status = st2
        own.save()
    return redirect('request')

def All_Ads(request):
    if not request.user.is_staff:
        return redirect('home')
    data=Owner_Detail.objects.all()
    d={'data':data}
    return render(request,'all_ads.html',d)

def Change_Img(request,pid):
    if not request.user.is_authenticated:
        return redirect('home')
    error=False
    img=Image.objects.get(id=pid)
    if request.method=="POST":
        i=request.FILES['img']
        n=request.POST['name']
        img.room_name=n
        img.img=i
        img.save()
        error=True
    d={'error':error,'img':img}
    return render(request,'changeimg.html',d)

