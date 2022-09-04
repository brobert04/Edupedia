from django import forms
from django.forms import ChoiceField

from schoolManagementApp.models import Course, SessionYears, Staff, Subject
from school_system_management import settings


class NotValidatingChoice(ChoiceField):
    def validate(self, value):
        pass

class CustomDateInput(forms.DateInput):
    input_type = "date"


# FORMULARUL PENTRU ADAUGARE STUDENT
class AddStudent(forms.Form):
    firstName = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control", "autocomplete:": "off"}))
    lastName = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    profilePic = forms.FileField(label="Profile Picture", max_length=50)
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Rather Not Say", "Rather Not Say")
    )

    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(
        attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control", "autocomplete:": "off"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))

    # PRELUAM TOATE CURSURILE DIN BAZA DE DATE, CREEM O LISTA CU ELE SI ITERAM PESTE ACESTEA ADAUGANDU-LE IN LISTA SI ULTERIOR LA ADAUGAM IN FORMULAR
    
    
    courses_list = []
    courses = Course.objects.all()
    for c in courses:
            list = (c.id, c.name)
            courses_list.append(list)

    
    sessions_list = []
    sessions = SessionYears.object.all()
    for s in sessions:
            sess = (s.id, f" From {s.startYear}   To   {s.endYear}")
            sessions_list.append(sess)


    course = forms.ChoiceField(label="Course", choices=courses_list, widget=forms.Select(
        attrs={"class": "form-control"}))
    session_id = forms.ChoiceField(
        label="Course Duration", choices=sessions_list, widget=forms.Select(attrs={"class": "form-control"}))


# FORMULARUL PENTRU EDITARE STUDENT
class EditStudent(forms.Form):
    firstName = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    lastName = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    profilePic = forms.FileField(
        label="Profile Picture", max_length=50, required=False)
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Rather Not Say", "Rather Not Say")
    )

    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(
        attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))

    # PRELUAM TOATE CURSURILE DIN BAZA DE DATE, CREEM O LISTA CU ELE SI ITERAM PESTE ACESTEA ADAUGANDU-LE IN LISTA SI ULTERIOR LA ADAUGAM IN FORMULAR
    
    
    courses_list = []
    courses = Course.objects.all()
    for c in courses:
            courses = Course.objects.all()
            list = (c.id, c.name)
            courses_list.append(list)


    sessions_list = []
    sessions = SessionYears.object.all()
    for s in sessions:
            sess = (s.id, f" From {s.startYear}   To   {s.endYear}")
            sessions_list.append(sess)
    
        
        
    course = forms.ChoiceField(label="Course", choices=courses_list, widget=forms.Select(
        attrs={"class": "form-control"}))
    session_id = forms.ChoiceField(
        label="Course Duration", choices=sessions_list, widget=forms.Select(attrs={"class": "form-control"}))


# FORMULARUL PENTRU ADAUGARE STAFF
class AddStaff(forms.Form):
    firstName = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    lastName = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    phoneNumber = forms.CharField(label="Phone Number(wihout +)", max_length=20, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))    
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Rather Not Say", "Rather Not Say")
    )

    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(
        attrs={"class": "form-control"}))
    profilePicture = forms.FileField(label = "Profile Picture", max_length = 50)
    
# FORMULARUL PENTRU EDITARE STAFF
class EditStaff(forms.Form):
    firstName = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    lastName = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    phoneNumber = forms.CharField(label="Phone Number", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control","autocomplete:": "off"}))
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Rather Not Say", "Rather Not Say")
    )

    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(
        attrs={"class": "form-control"}))
    profilePic = forms.FileField(
        label="Profile Picture", max_length=50, required=False)

# FORMULARUL PENTRU ADAUGARE CURS
class AddCourse(forms.Form):
    courseName = forms.CharField(label="Course Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))


# FORMULARUL PENTRU EDITARE CURS
class EditCourse(forms.Form):
    courseName = forms.CharField(label="Course Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))

# FORMULARUL PRIN CARE STAFF-UL ISI POATE EDITA SINGUR CATEVA DIN INFORMATIILE CONTULUI SAU
class StaffOwnProfileEdit(forms.Form):
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off",}))
    email = forms.EmailField(label="Email", max_length=50,required=False, widget=forms.EmailInput(attrs={"class": "form-control", "autocmplete": "off", "disabled": "disabled"}))
    firstName = forms.CharField(label="First Name", max_length=50, required=False, widget=forms.TextInput(attrs={"class": "form-control", "autocmplete": "off", "disabled": "disabled"}))
    lastName = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "autocmplete": "off", }))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "autocmplete": "off"}))
    phoneNumber = forms.CharField(label="Phone Number", max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "autocmplete": "off"}))
    profilePicture = forms.FileField(label="Profile Picture", max_length=50, required=False)
    
    
# FORMULARUL PENTRU EDITAREA REZULATULUI ELEVLUI
class EditResult(forms.Form):
    def __init__(self, *args, **kwargs):
        self.staffId = kwargs.pop("staffId")
        super(EditResult, self).__init__(*args, **kwargs)
        subject_list = []
        try:
            subjects = Subject.objects.filter(staffId=self.staffId)
            for s in subjects:
                subject = (s.id, s.name)
                subject_list.append(subject)
        except:
            subjects = []
        self.fields["subject_id"].choices = subject_list
        
        
    years_list = []
    try:
        years = SessionYears.object.all()
        for y in years:
             year = (y.id, "From " + str(y.startYear) + " to " + str(y.endYear))
             years_list.append(year)
    except:
             years_list = []


    students = NotValidatingChoice(label="Student", widget=forms.Select(attrs={"class": "form-control custom-select form-control-border"}))
    session = forms.ChoiceField(label="Session", choices=years_list,
                                widget=forms.Select(attrs={"class": "form-control custom-select form-control-border"}))
    date = forms.DateField(label="Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    subject_id = forms.ChoiceField(label="Subject", widget=forms.Select(attrs={"class":"form-control custom-select form-control-border "}))
    assignment_mark = forms.CharField(label="Homework Mark", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    exam_mark = forms.CharField(label="Exam Mark", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
        
              