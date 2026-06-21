from django import forms
from jobs.models import Job
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class JobForm(forms.ModelForm):
    def __init__(self, *args, submit_text="Create Job", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title', 'company_name', 'description', 'requirements', 'location', 'category',
            Submit('submit',  submit_text, css_class='btn btn-primary w-100 py-2 mt-3 fw-bold rounded-pill')
        )
        
        placeholders = {
            'title': 'Enter the job title',
            'company_name': 'Enter the name of your company',
            'description': 'Enter the job description',
            'requirements': 'Enter the requirements for the candidates',
            'location': 'Enter the office location',
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(field_name, f'Enter {field_name}'),
                'class': 'form-control'
            })

    class Meta:
        model = Job
        fields = ['title', 'company_name', 'description', 'requirements', 'location', 'category']