from django import forms
from django.forms.widgets import PasswordInput, TextInput, Select, HiddenInput, Textarea, SelectMultiple,\
    FileInput
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from Helpdesk.models import Users, Ticket, AssignTo, Response
        
class changePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', max_length=100, widget=PasswordInput(attrs={'class':'easyui-validatebox','required':'true'}))
    new_password1 = forms.CharField(label='New Password', max_length=100, widget=PasswordInput(attrs={'class':'easyui-validatebox','required':'true'}))
    new_password2 = forms.CharField(label='Confirm Password', max_length=100, widget=PasswordInput(attrs={'class':'easyui-validatebox','required':'true'}))   


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', max_length=100, widget=PasswordInput(attrs={'class':'easyui-validatebox','required':'true'}))
    password2 = forms.CharField(label='Password conf', max_length=100, widget=PasswordInput(attrs={'class':'easyui-validatebox','required':'true'}))   

    class Meta:
        model = Users
        fields = ('id','username', 'name', 'telpNo', 'address', 'email', 'gender', 'position')
        widgets = {
            'id': HiddenInput,
            'username': TextInput(attrs={'class':'easyui-validatebox','required':'true'}),
            'name': TextInput(attrs={'class':'easyui-validatebox','required':'true'}),
            'telpNo': TextInput(attrs={'class':'easyui-validatebox','required':'true'}),
            'address': TextInput(attrs={'class':'easyui-validatebox','required':'true'}),
            'gender': Select(attrs={'class':'easyui-validatebox','data-options':'required:true'}),
            'email': TextInput(attrs={'class':'easyui-validatebox','data-options':'required:true,validType:"email"'}),
            'position': Select(attrs={'class':'easyui-validatebox','data-options':'required:true'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Users
        fields = ('username', 'name', 'password', 'telpNo', 'address', 'email', 'gender', 'position', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
    
class UserSearchForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username', 'name', 'telpNo', 'address', 'email', 'gender', 'position')


class TicketCreationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('solutionDesc',)
        fields = ('ticketId','ticketNo', 'reportedDateTime', 'priority', 'problemType', 'problemTitle', 'problemDesc', 
                  'stepToReproduce', 'telephone', 'email', 'reportedBy', 'attachment')
        labels = {
            'ticketId': 'Ticket Id',
            'ticketNo': 'Ticket No', 
            'reportedDateTime': 'Reported Time', 
            'priority': 'Priority', 
            'problemType': 'Problem Type', 
            'problemTitle': 'Problem Title', 
            'problemDesc': 'Problem Desc', 
            'stepToReproduce': 'Step To Reproduce', 
            'telephone': 'Telp No', 
            'email': 'Email',
            'attachment': 'Attachment'
        }
        widgets = {
            'ticketId': HiddenInput,
            'ticketNo': TextInput(attrs={'title':'Ticket No','readonly':'readonly'}),
            'reportedDateTime': HiddenInput,
            'priority': Select(attrs={'title':'Priority','class':'easyui-validatebox'}),
            'problemType': Select(attrs={'title':'Problem Type','class':'easyui-validatebox'}),
            'problemTitle': TextInput(attrs={'title':'Problem Title','class':'easyui-validatebox','required':'true'}),
            'problemDesc': Textarea(attrs={'title':'Problem Desc','class':'easyui-validatebox','required':'true','cols': 80, 'rows': 5}),
            'stepToReproduce': Textarea(attrs={'title':'Step To Reproduce','class':'easyui-validatebox','required':'true','cols': 80, 'rows': 5}),
            'telephone': TextInput(attrs={'title':'Telp No','class':'easyui-validatebox','required':'true'}),
            'email': TextInput(attrs={'class':'easyui-validatebox','data-options':'required:true,validType:"email"'}),
            'reportedBy': HiddenInput,
            'attachment': FileInput,
        }
        
class TicketChangeForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('solutionDesc',)
        fields = ('ticketNo', 'reportedDateTime', 'priority', 'problemType', 'problemTitle', 'problemDesc', 
                  'stepToReproduce', 'telephone', 'email', 'status', 'reportedBy','attachment')

class TicketSearchForm(forms.ModelForm):
    assignTo = forms.ModelChoiceField(label='Assign To', required=False, widget=forms.Select(attrs={'style':'width:173px'}), queryset=Users.objects.exclude(position='User'))
    statusBy = forms.ModelChoiceField(label='Status By', required=False, widget=forms.Select(attrs={'style':'width:173px'}), queryset=Users.objects.all())
    class Meta:
        model = Ticket
        labels = {'ticketNo':'Ticket No', 'reportedDateTime':'Reported Time', 'priority':'Priority', 'problemType':'Problem Type', 
                 'problemTitle':'Problem Title', 'problemDesc':'Problem Desc', 'stepToReproduce':'Step To Reproduce', 
                 'telephone':'Telephone', 'email':'Email', 'status':'Status'}
        fields = ('ticketNo', 'reportedDateTime', 'priority', 'assignTo', 'problemType', 'problemTitle', 'problemDesc', 
                  'stepToReproduce', 'telephone', 'email', 'status', 'statusBy')
        widgets = {
            'problemDesc': Textarea(attrs={'cols': 80, 'rows': 3}),
            'stepToReproduce': Textarea(attrs={'cols': 80, 'rows': 3}),
            'reportedDateTime': TextInput(attrs={'class':'easyui-datebox','data-options':'formatter:myformatter,parser:myparser','style':'width:150px'}),
            'status': Select(attrs={'onchange':'changeStatusBy(this.value)'})
        }
        
        
class TicketAssignForm(forms.Form):
    fields = ('ticketNo','assignTo')
    ticketNo = forms.CharField(label='Ticket No', max_length=100)
    assignTo = forms.ModelMultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'style':'width:173px'}), queryset=Users.objects.exclude(position='User'))
 
   
class TicketResponseForm(forms.ModelForm):
    status_choices = (('Responded', 'Responded'),('Fixed', 'Fixed'),('Reopen', 'Reopen'),('Closed', 'Closed'),('Canceled', 'Canceled'))
    
    ticketNo = forms.CharField(label='Ticket No', max_length=100)
    status = forms.ChoiceField(label='Status', required=False, widget=forms.Select(attrs={'style':'width:173px'}), choices=status_choices)
 
    class Meta:
        model = Response
        fields = ('ticketNo', 'status', 'responseDesc', 'remark','attachment','ticketId')
        exclude = ('responseBy','responseId')
        labels = {
            'responseDesc': 'Response Desc',
            'remark': 'Remark',
            'attachment': 'Attachment'
        }
        widgets = {
            'responseDesc': Textarea(attrs={'cols': 80, 'rows': 3}),
            'remark': Textarea(attrs={'cols': 80, 'rows': 3}),
            'attachment': FileInput,
            'ticketId': HiddenInput,
        }
        
class TicketResponseFormUser(forms.ModelForm):
    status_choices = (('Reopen', 'Reopen'),('Closed', 'Closed'),('Canceled', 'Canceled'))
    
    ticketNo = forms.CharField(label='Ticket No', max_length=100)
    status = forms.ChoiceField(label='Status', required=False, widget=forms.Select(attrs={'style':'width:173px'}), choices=status_choices)
 
    class Meta:
        model = Response
        fields = ('ticketNo', 'status', 'responseDesc', 'remark','attachment')
        labels = {
            'responseDesc': 'Response Desc',
            'remark': 'Remark',
            'attachment': 'Attachment'
        }
        widgets = {
            'responseDesc': Textarea(attrs={'cols': 80, 'rows': 3}),
            'remark': Textarea(attrs={'cols': 80, 'rows': 3}),
            'attachment': FileInput,
        }
        
class TicketResponseFormHelpdesk(forms.ModelForm):
    status_choices = (('Responded', 'Responded'),('Fixed', 'Fixed'),('Reopen', 'Reopen'))
    
    ticketNo = forms.CharField(label='Ticket No', max_length=100)
    status = forms.ChoiceField(label='Status', required=False, widget=forms.Select(attrs={'style':'width:173px'}), choices=status_choices)
 
    class Meta:
        model = Response
        fields = ('ticketNo', 'status', 'responseDesc', 'remark','attachment')
        exclude = ('responseBy','responseId')
        labels = {
            'responseDesc': 'Response Desc',
            'remark': 'Remark',
            'attachment': 'Attachment'
        }
        widgets = {
            'responseDesc': Textarea(attrs={'cols': 80, 'rows': 3}),
            'remark': Textarea(attrs={'cols': 80, 'rows': 3}),
            'attachment': FileInput,
        }