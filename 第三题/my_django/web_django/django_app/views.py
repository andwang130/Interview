from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django_app.models import *
import datetime
def index(request):
    article=Article.objects.all()[0:3]
    contenx={'user':request.session.get('user_name'),'article':article}
    return render(request,'index.html',contenx)
def login(request):
    if request.method=='POST':
        password=request.POST.get('paswd')
        usname=request.POST.get('name')
        user=AdminU.objects.filter(paswd=password,name=usname).first()

        if user:
            request.session['name']=user.name
            request.session['admin_id']=user.id
            data_json = {'eercode': 0, 'eermegs': '登陆成功'}
            return JsonResponse(data_json)
        else:
            data_json = {'eercode': 110, 'eermegs': '账号密码错误'}
            return JsonResponse(data_json)
    elif request.method=='GET':
        return  render(request,'login.html')
def user_login(request):
    if request.method == 'POST':
        password = request.POST.get('paswd')
        usname = request.POST.get('name')
        user = User.objects.filter(paswd=password, name=usname).first()
        Referer = request.META['HTTP_REFERER']
        if user:
            request.session['user_name'] = user.name
            request.session['used_id'] = user.id
            data_json = {'eercode': 0, 'eermegs': '登陆成功'}
            return JsonResponse(data_json)
        else:
            data_json = {'eercode': 110, 'eermegs': '账号密码错误'}
            return JsonResponse(data_json)
    elif request.method == 'GET':
        return render(request, 'user_login.html')
# Create your views here.
def register(request):
    if request.method=='POST':
        password = request.POST.get('paswd')
        usname = request.POST.get('name')
        if not  AdminU.objects.filter(name=usname).first():
            user=AdminU(paswd=password,name=usname)
            user.save()
            data_json = {'eercode': 0, 'eermegs': '注册成功'}
            return JsonResponse(data_json)
        else:
            data_json = {'eercode': 110, 'eermegs': '用户已经存在'}
            return JsonResponse(data_json)

    elif request.method=='GET':
        return render(request,'register.html')
def user_register(request):
    if request.method == 'POST':
        password = request.POST.get('paswd')
        usname = request.POST.get('name')
        if not User.objects.filter(name=usname).first():
            user = User(paswd=password, name=usname)
            user.save()
            data_json={'eercode':0,'eermegs':'注册成功'}
            return JsonResponse(data_json)
        else:
            data_json = {'eercode': 110, 'eermegs': '用户已经存在'}
            return JsonResponse(data_json)

    elif request.method == 'GET':
        return render(request, 'user_register.html')
def user_cancel(request):
    del request.session['user_name']
    del request.session['used_id']
    Referer=request.META['HTTP_REFERER']
    return redirect(Referer)
def addArtcle(requests):
    if requests.method=='POST':
        title=requests.POST.get('title')
        conten=requests.POST.get('title')
        admin_id=requests.session.get('admin_id')
        print(admin_id)
        if not  Article.objects.filter(title=title).first():
            article=Article(title=title,conten=conten,authon_id=admin_id)
            article.save()
            response_json = {'eercode': 0, 'eermegs': '添加成功'}
            return JsonResponse(response_json)
        else:
            response_json={'eercode':110,'eermegs':'该文章已经存在'}
            return JsonResponse(response_json)
    elif requests.method=='GET':
        return render(requests,'form_Artcle.html')
def news(request):
    if request.method=='GET':
        index=int(request.GET.get('index',1))
        news_articles=Article.objects.filter(type_id=1)
        p=Paginator(news_articles,20)
        pages=p.page_range
        news_article=p.page(index)
        contenx={'pages':pages[-1],'index':index,'article':news_article,'conut':len(news_articles),
                 'page_list':fenye(index,10,pages[-1]),
                 'user':request.session.get('user_name')}
        return render(request,'news.html',contenx)
def compan(request):
    if request.method=='GET':
        index=int(request.GET.get('index',1))
        news_articles=Article.objects.filter(type_id=2)
        p=Paginator(news_articles,20)
        pages=p.page_range
        news_article=p.page(index)
        contenx={'pages':pages[-1],'index':index,'article':news_article,'conut':len(news_articles),'page_list':fenye(index,10,pages[-1]),
                 'user':request.session.get('user_name')}
        return render(request,'companynotices.html',contenx)
def news_conten(request,tyep_id,id):
    if request.method=='GET':
        print(tyep_id,id)
        article=Article.objects.filter(id=id,type_id=tyep_id).first()
        next=Article.objects.filter(type_id=tyep_id,id__gt=id).values('id','title').first()
        up=Article.objects.filter(type_id=tyep_id,id__lt=id).order_by('-id').values('id','title').first()
        contenx={'article':article,'next':next,'up':up,'type':tyep_id,'user':request.session.get('user_name')}
        return render(request,'conten.html',contenx)
def fenye(index,num,pages):
    page_list=[]
    if index<num:
        page_list=[i for i in range(1,num+1) if i<=pages]
    else:
        page_list=[i for i in range(index-(num-2),index+2) if i<=pages ]
    print(page_list)
    return page_list
def addcomment(request):
    if request.method=='POST':
        articel_id=request.POST.get('id')
        user_id=request.session.get('used_id')
        conten=request.POST.get('conten')
        comment=Comment(article_id=articel_id,publisher_id=user_id,conten=conten)
        comment.save()
        data_json={'eercode':0,'eermegs':'留言成功'}
        return JsonResponse(data_json)
def get_comment(request):
    if request.method=='GET':
        article_id=request.GET.get('article_id')
        index=int(request.GET.get('index',1))
        print(article_id)
        comments=Comment.objects.filter(article_id=article_id)
        p=Paginator(comments,10)
        pages=p.page_range[-1]
        page_list=fenye(index,10,pages)
        comment=p.page(index)
        print(type(comment[0].set_time))
        data={'count':len(comments),'pages':pages,'page_list':page_list,'index':index,'comment':[{'id':i.id,'conten':i.conten,'set_time':i.set_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                      'publisher':User.objects.filter(id=i.publisher_id).first().name} for i in comment]}
        data_json={'eercode':0,'eermegs':'留言成功','data':data}
        return JsonResponse(data_json)

