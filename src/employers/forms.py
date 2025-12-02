from django import forms
from jobs.models import Job

class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'title': 'Enter the job title',
            'company_name': 'Enter the name of your company',
            'description': 'Enter the job description',
            'requirements': 'Enter the requirements for the candidates',
            'location': 'Enter the office location',
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, f'Enter {field_name}')
            })

    class Meta:
        model = Job
        fields = ['title', 'company_name', 'description', 'requirements', 'location', 'category']