from django import forms
from ..models import Comment
class TicketForm(forms.Form):
    SUBJECT_CHOICES=(
        ("suggestion","suggestion"),
        ("criticism","criticism"),
        ("problem","problem"),
    )
    message=forms.CharField(widget=forms.Textarea,required=True)
    name=forms.CharField(max_length=250,required=True)
    email=forms.EmailField()
    phone=forms.CharField(max_length=11,required=True)
    subject=forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("phone number is not true")
            
            else:
                return phone

# class CommentForms(forms.ModelForm):
#     class Meta:
#         model=Comment                                                 
#         feilds=['name','body']