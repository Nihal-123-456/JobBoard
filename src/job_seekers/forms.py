from django import forms
from .models import Education, WorkExperience
from jobs.models import JobApplication

class JobApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'full_name': 'Enter your full name',
            'email': 'Enter your email address',
            'cover_letter': 'Write a professional cover letter',
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, f'Enter {field_name}')
            })

    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'resume', 'cover_letter']

class EducationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'institution': 'Enter the name of your Institution',
            'degree': 'Enter the name of your Degree',
            'major': 'Enter the subject you majored in',
            'passing_year': 'Enter your passing year',
            'result': 'Enter you result (e.g. GPA, CGPA)'
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, f'Enter {field_name}')
            })

    class Meta:
        model = Education
        fields = ['institution', 'degree', 'major', 'passing_year', 'result']

class WorkExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'institution': 'Enter the name of your Institution',
            'position': 'Enter your designation',
            'responsibilities': 'Enter the responsibilities you had to carry out',
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, f'Enter {field_name}')
            })

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = WorkExperience
        fields = ['institution', 'position', 'start_date', 'end_date', 'is_currently_there', 'responsibilities']
    
    def clean(self):
        cleaned_data = super().clean()
        end_date = cleaned_data.get("end_date")
        is_currently_there = cleaned_data.get("is_currently_there")

        if end_date and is_currently_there:
            raise forms.ValidationError(
                "You cannot set both an end date and mark as currently working."
            )
        if not end_date and not is_currently_there:
            raise forms.ValidationError(
                "Please either provide an end date or mark as currently working."
            )

        return cleaned_data