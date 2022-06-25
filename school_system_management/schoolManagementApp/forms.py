from django import forms

from schoolManagementApp.models import Course, SessionYears, Staff


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
    
    courses = Course.objects.all()
    courses_list = []
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
    
    courses = Course.objects.all()
    courses_list = []
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
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))


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


# FORMULARUL PENTRU ADAUGARE CURS
class AddCourse(forms.Form):
    courseName = forms.CharField(label="Course Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))


# FORMULARUL PENTRU EDITARE CURS
class EditCourse(forms.Form):
    courseName = forms.CharField(label="Course Name", max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control"}))
