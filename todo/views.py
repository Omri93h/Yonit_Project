# from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import  NancyForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Nancy
from django.utils import timezone

################################## LOGIN & REGISTER #################################
def registerForm(request):
    if (request.method == 'GET'):
        return render(request, 'nancy/registerForm.html', {'form': UserCreationForm() })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('nancy')
            except IntegrityError:
                return render(request, 'nancy/registerForm.html', {'form': UserCreationForm(), "errMsg": "User exists. Choose a different one" })
        else:
            return render(request, 'nancy/registerForm.html', {'form': UserCreationForm(), "errMsg": "Password didn't match" })

def logoutuser(request):
    logout(request)
    return redirect('login') 

def loginuser(request):
    if (request.method == 'GET'):
        return render(request, 'nancy/loginform.html', {'form': AuthenticationForm() })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'nancy/loginform.html', {'form': AuthenticationForm(), "errMsg": "User doesn't exist" })
        else:
            login(request, user)
            return redirect('nancy')

################################## end of LOGIN & REGISTER #################################

################################## HOMEPAGE #################################

def nancy(request):
    if request.user.is_authenticated:
        return render(request, 'nancy/index1.html')
    else:
       return redirect('login')
        
def homepage(request):
    return render(request, 'nancy/index.html')

################################## end of HOMEPAGE #################################

################################## MEALS ###########################################
check='checked="checked"'
uncheck=""
class radioCheck :
    def __init__(self):
        self.UP = uncheck
        self.DOWN = check
        
        self.YES = uncheck
        self.NO = uncheck
        self.ALL = check

    def UPchecked(self):
        self.UP = check
        self.DOWN = uncheck

    def DOWNchecked(self):
        self.UP = uncheck
        self.DOWN = check  

    def YESchecked(self):
        self.YES = check
        self.NO = uncheck
        self.ALL = uncheck

    def NOchecked(self):
        self.YES = uncheck
        self.NO = check
        self.ALL = uncheck

    def ALLchecked(self):
        self.YES = uncheck
        self.NO = uncheck
        self.ALL = check

select = 'selected'
unselect =  ""
class ShowSelectInput:
    def __init__(self):
        self.MYmeals = unselect
        self.ALLusersMeals = select   

    def selectMYmeals(self):
        self.MYmeals = select
        self.ALLusersMeals = unselect 

    def selectALLusersMeals(self):     
        self.MYmeals = unselect


@login_required
def meals(request):
    checkingControl = radioCheck()
    selectcontrol = ShowSelectInput()
    mealsSort=request.GET.get("sort")
    if (mealsSort == "UP"):
        checkingControl.UPchecked()
        order = '-dateCreated' 
    else:
        order = 'dateCreated'
        checkingControl.DOWNchecked()
    mealsfilter=request.GET.get("filter")   
    if (mealsfilter=="YES"):
        checkingControl.YESchecked()
        meal = Nancy.objects.filter(HasItamarTasted = 1,).order_by(order)
    elif (mealsfilter=="NO"):
        checkingControl.NOchecked()
        meal = Nancy.objects.filter(HasItamarTasted = 0).order_by(order)  
    else : 
        checkingControl.ALLchecked()
        meal= Nancy.objects.all().order_by(order)    
    selectMealCreator=request.GET.get("userMeals") 
    selectcontrol.selectALLusersMeals()
    if (selectMealCreator=="myMeals"):
        selectcontrol.selectMYmeals()
        meal=meal.filter(user_id = request.user)
    #filter(user_id = request.user)
  
    return render(request, 'nancy/meals.html',{'allmeals':meal ,'checked':checkingControl , 'select':selectcontrol })


@login_required
def mealData(request, meal_pk):
    meal = get_object_or_404(Nancy, pk=meal_pk)
    form = NancyForm(instance=meal)
    # creator=get_object_or_404(User,pk=meal.user_id)
    if (request.method == 'GET'):
        return render(request, 'nancy/meal-data.html', {'meal': meal, 'form': form , 'creator':meal.user_id})
    else:
        # meal = get_object_or_404(Nancy, pk=meal_pk) #, user_id=request.user
        try:
            # form = NancyForm(request.POST, instance=meal)
            form.save()
            return redirect('meals')
        except ValueError:
            return render(request, 'nancy/meal-data.html', {'form': form, 'errMsg': "Data mismatch"})



def updateMeal(request, meal_pk):
    meal = get_object_or_404(Nancy, pk=meal_pk)

    if (request.method == 'GET'):
        form = NancyForm(instance=meal)
        act=2
        return render(request, 'nancy/create-meal.html', {'meal': meal, 'form': form ,'act':act})
    else:
        try:
            form = NancyForm(request.POST, instance=meal)
            form.save()
            return redirect('meals')
        except ValueError:
            return render(request, 'nancy/create-meal.html', {'form': form, 'errMsg': "Data mismatch"})



def createNewMeal(request):
    if request.method == 'GET':
        act=1
        return render(request, 'nancy/create-meal.html', {'form': NancyForm(),'act':act})
    else:
        try:
            form = NancyForm(request.POST,request.FILES)
            newMeal = form.save(commit=False) #commit=False
            newMeal.user_id = request.user
            newMeal.save()
            return redirect('meals')
        except ValueError:
            return render(request, 'nancy/create-meal.html', {'form': NancyForm(), 'errMsg': 'Data mismatch'})

@login_required
def deleteMeal(request, meal_pk):
    meal = get_object_or_404(Nancy, pk=meal_pk, user_id=request.user)

    if (request.method == 'POST'):
        meal.delete()
        return redirect('meals') 
    
################################## end of MEALS #################################