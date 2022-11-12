from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from schoolManagementApp.forms import EditResult
from schoolManagementApp.models import Student, StudentResults, Subject
from django.contrib.messages.views import messages

class EditViewClass(View):
    def get(self,request, *args, **kwargs):
        staff_id = request.user.id
        edit_form = EditResult(staffId=staff_id)
        return render(request, 'staff_templates/edit_results.html', {"form":edit_form})

    def post(self,request, *args, **kwargs):
        form = EditResult(request.POST, staffId = request.user.id)
        if form.is_valid():
            student_id = form.cleaned_data["students"]
            exam_mark = form.cleaned_data['exam_mark']
            date = form.cleaned_data['date']
            subject_id = form.cleaned_data['subject_id']

            student = Student.objects.get(admin=student_id)
            subject = Subject.objects.get(id=subject_id)

            res = StudentResults.objects.get(subjectID=subject, studentID=student, date=date)
            res.subject_exam_mark = exam_mark
            res.save()
            messages.success(request, "Succesfully updated marks.")
            return HttpResponseRedirect(reverse('edit_student_result'))
        else:
            messages.error(request, "Failed to update marks.")
            form = EditResult(request.POST, staffId=request.user.id)
            return render(request, 'staff_templates/edit_results.html', {"form":form})