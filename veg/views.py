from django.shortcuts import render,redirect
from django.http import HttpResponse
from veg.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def Recipe_view(request):
    if request.method=='POST':
        data=request.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image
        )
        messages.success(request,"Recipe added sucessfully")

        return redirect('/recipe')
    r_obj=Recipe.objects.all()
    if request.GET.get('search'):
        r_obj=Recipe.objects.filter(recipe_name__icontains=request.GET.get('search'))
    context={'r_obj':r_obj}
    return render(request, 'recipe.html',context)
def update_recipe(request,id):
    rupdate=Recipe.objects.get(id=id)
    if request.method == "POST":
        data=request.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
        rupdate.recipe_name=recipe_name
        rupdate.recipe_description=recipe_description
        if recipe_image:
            rupdate.recipe_image=recipe_image
        rupdate.save()
        return redirect('/recipe')
    
    context={'rupdate':rupdate}
    return render (request,'update.html',context)
def delete_Recipe(request,id):
    d=Recipe.objects.get(id = id)
    d.delete()
    return redirect('/recipe')

def register_page(request):
    if request.method == 'POST':
        data = request.POST
        first_name=data.get('fname')
        last_name=data.get('lname')
        username=data.get('uname')
        password=data.get('pwd')

        user=User.objects.filter(username=username)
        if user:
            messages.info(request, "username already exists")
            return redirect('/register')
        user=User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username
        )
        user.set_password(password)
        user.save()
        messages.success(request,"account created ")
        return redirect('/login')

    
    return render(request,'register.html')



def login_page(request):
    if request.method == 'POST':
        data = request.POST
        username=data.get('uname')
        password=data.get('pwd')
        if not User.objects.filter(username=username).exists():
            messages.info(request, "username does not exist")
            return redirect('/login')
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,'login sucessfully')
            return redirect('/recipe')
        else:
            messages.info(request,"invalid username or password")
            return redirect('/login')
        

    return render(request,'login.html')
def logout_page(request):
    logout(request)
    return redirect('/login')