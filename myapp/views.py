from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from myapp.models import *

def login(request):
    request.session['lid'] = ''
    return render(request, 'login_index.html')

def login_post(request):
    username = request.POST['textfield']
    password = request.POST['textfield2']
    res = Login.objects.filter(username=username, password=password)
    if res.exists():
        ress = Login.objects.get(username = username, password=password)
        request.session['lid']=ress.id

        if ress.type == 'Doctor':
            return redirect('/myapp/view_doctor/')
        elif ress.type == 'Patient':
            return redirect('/myapp/view_patient/')
        else:
            return HttpResponse('''<script>alert('User not found or Invalid Username or Password');window.location='/myapp/login/'</script>''')

    else:
        return HttpResponse('''<script>alert('User not found or Invalid Username or Password');window.location='/myapp/login/'</script>''')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Login, Doctor, Patient

def signup(request):
    return render(request, 'signup.html')

def signup_post(request):
    fname = request.POST.get('textfield', '')
    lname = request.POST.get('textfield11', '')
    photo = request.FILES.get('textfield99', None)
    user = request.POST.get('textfield8', '')
    username = request.POST.get('textfield16', '')
    password = request.POST.get('textfield10', '')
    confirm_password = request.POST.get('textfield12', '')
    email = request.POST.get('textfield3', '')
    address = request.POST.get('textfield6', '')
    city = request.POST.get('textfield13', '')
    state = request.POST.get('textfield14', '')
    pincode = request.POST.get('textfield15', '')

    # Prepare context data to retain entered data
    context = {
        'fname': fname,
        'lname': lname,
        'user': user,
        'username': username,
        'email': email,
        'address': address,
        'city': city,
        'state': state,
        'pincode': pincode,
    }

    # Check if the passwords match
    if password != confirm_password:
        return HttpResponse('''
            <script>
                alert('Passwords do not match.');
                window.history.back();
            </script>
        ''')

    # Check if the username already exists
    if Login.objects.filter(username=username).exists():
        return HttpResponse('''
            <script>
                alert('Username is already taken. Please choose a different username.');
                window.history.back();
            </script>
        ''')

    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
    fs = FileSystemStorage()
    if photo:
        fs.save(date, photo)
        path = fs.url(date)
    else:
        path = ''

    # Create user based on type
    if user == 'Doctor':
        l = Login(username=username, password=str(password), type=user)
        l.save()

        s = Doctor(LOGIN=l, fname=fname, lname=lname, photo=path, email=email, address=address, city=city,
                   state=state, pincode=pincode)
        s.save()

        return HttpResponse(
            '''<script>alert('Doctor Added Successfully');window.location='/myapp/login/'</script>''')

    else:
        l = Login(username=username, password=str(password), type=user)
        l.save()

        s = Patient(LOGIN=l, fname=fname, lname=lname, photo=path, email=email, address=address, city=city,
                    state=state, pincode=pincode)
        s.save()

        return HttpResponse(
            '''<script>alert('Patient Added Successfully');window.location='/myapp/login/'</script>''')


# def signup(request):
#     return render(request, 'signup.html')
#
# def signup_post(request):
#
#     fname = request.POST['textfield']
#     lname = request.POST['textfield11']
#     photo = request.FILES['textfield99']
#     user = request.POST['textfield8']
#     username = request.POST['textfield16']
#     password = request.POST['textfield10']
#     confirm_password = request.POST['textfield12']
#     email = request.POST['textfield3']
#     address = request.POST['textfield6']
#     city = request.POST['textfield13']
#     state = request.POST['textfield14']
#     pincode = request.POST['textfield15']
#
#     # Check if the password and confirm password is same
#     if password != confirm_password:
#         return HttpResponse('''<script>alert('Passwords do not match.');window.location='/myapp/signup/'</script>''')
#
#     # Check if the username already exists
#     if Login.objects.filter(username=username).exists():
#         return HttpResponse('''<script>alert('Username is already taken. Please choose a different username.');window.location='/myapp/signup/'</script>''')
#
#
#     from datetime import datetime
#     date = datetime.now().strftime('%Y%m%d_%H%M%S')+".jpg"
#     fs = FileSystemStorage()
#     fs.save(date,photo)
#     path = fs.url(date)
#
#
#
#
#
#     if user == 'Doctor':
#
#         l = Login()
#         l.username = username
#         l.password = str(password)
#         l.type = user
#         l.save()
#
#         s = Doctor()
#         s.LOGIN = l
#         s.fname = fname
#         s.lname = lname
#         s.photo = path
#         s.email = email
#         s.address = address
#         s.city = city
#         s.state = state
#         s.pincode = pincode
#
#         s.save()
#
#         return HttpResponse('''<script>alert('Doctor Added Successfully');window.location='/myapp/login/'</script>''')
#
#     else:
#         l = Login()
#         l.username = username
#         l.password = str(password)
#         l.type = user
#         l.save()
#
#         s = Patient()
#         s.LOGIN = l
#         s.fname = fname
#         s.lname = lname
#         s.photo = path
#         s.email = email
#         s.address = address
#         s.city = city
#         s.state = state
#         s.pincode = pincode
#
#         s.save()
#
#         return HttpResponse('''<script>alert('Patient Added Successfully');window.location='/myapp/login/'</script>''')

def view_patient(request):
    if not request.session.get('lid'):
        return redirect('/')

    try:
        # Get the current logged-in patient's details
        patient = Patient.objects.get(LOGIN_id=request.session['lid'])
        context = {'data': [patient]}  # Put patient in a list for consistency with the template
    except Patient.DoesNotExist:
        context = {'data': []}  # No patient found, send empty list

    return render(request, 'patient/view_patient.html', context)
    # if request.session['lid'] == '':
    #     return redirect('/')
    # res=Patient.objects.all()
    # return render(request, 'patient/view_patient.html',{'data':res})

def view_doctor(request):
    if not request.session.get('lid'):
        return redirect('/')

    try:
        # Get the current logged-in doctor's details
        doctor = Doctor.objects.get(LOGIN_id=request.session['lid'])
        context = {'data': [doctor]}  # Put doctor in a list for consistency with the template
    except Doctor.DoesNotExist:
        context = {'data': []}  # No doctor found, send empty list

    return render(request, 'doctor/view_doctor.html', context)