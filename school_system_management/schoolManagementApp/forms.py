from django import forms

from schoolManagementApp.models import Course

class CustomDateInput(forms.DateInput):
    input_type = "date"
    
class AddStudent(forms.Form):
    firstName = forms.CharField(label="First Name", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    lastName = forms.CharField(label="Last Name", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    profilePic = forms.FileField(label="Profile Picutre", max_length=50)
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Rather Not Say", "Rather Not Say")
    )
    
    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    
    # PRELUAM TOATE CURSURILE DIN BAZA DE DATE, CREEM O LISTA CU ELE SI ITERAM PESTE ACESTEA ADAUGANDU-LE IN LISTA SI ULTERIOR LA ADAUGAM IN FORMULAR
    courses = Course.objects.all()
    courses_list = []
    for c in courses:
        list = (c.id, c.name)
        courses_list.append(list)
    course = forms.ChoiceField(label="Course", choices=courses_list, widget=forms.Select(attrs={"class": "form-control"}))  
    startDate = forms.DateField(label="Start Year", widget=CustomDateInput(attrs={"class": "form-control"}))
    endDate = forms.DateField(label="End Year", widget=CustomDateInput( attrs={"class": "form-control"}))


class EditStudent(forms.Form):
    firstName = forms.CharField(label="First Name", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    lastName = forms.CharField(label="Last Name", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    profilePic = forms.FileField(label="Profile Picutre", max_length=50, required=False)
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Rather Not Say", "Rather Not Say")
    )
    
    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50,widget=forms.TextInput(attrs={"class": "form-control"}))
    
    # PRELUAM TOATE CURSURILE DIN BAZA DE DATE, CREEM O LISTA CU ELE SI ITERAM PESTE ACESTEA ADAUGANDU-LE IN LISTA SI ULTERIOR LA ADAUGAM IN FORMULAR
    courses = Course.objects.all()
    courses_list = []
    for c in courses:
        list = (c.id, c.name)
        courses_list.append(list)
    course = forms.ChoiceField(label="Course", choices=courses_list, widget=forms.Select(attrs={"class": "form-control"}))  
    startDate = forms.DateField(label="Start Year", widget=CustomDateInput(attrs={"class": "form-control"}))
    endDate = forms.DateField(label="End Year", widget=CustomDateInput( attrs={"class": "form-control"}))
   