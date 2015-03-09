from django.db import models
from django.conf import settings 
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import datetime
from Helpdesk import lookup
from urllib.request import unquote

class MyUserManager(BaseUserManager):
    def create_user(self, username, name, telpno, address, email, gender, position, password=None):
        errorMessage = ""; 
        isError = False
        if not username:
            errorMessage = errorMessage + 'Username can not be empty \n'
            isError = True
        
        if(isError):
            raise ValueError(errorMessage)
        
        user = self.model(
            username = username,
            name = name,
            telpNo = telpno,
            address = address,
            email = self.normalize_email(email),
            gender = gender,
            position = position
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, telpno, address, email, gender, position, password):
        user = self.create_user(username,
            name = name,
            password = password,
            telpNo = telpno,
            address = address,
            email = self.normalize_email(email),
            gender = gender,
            position = position
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class Users(AbstractBaseUser):
    gender_choices = (('', ''),('Male', 'Male'),('Female', 'Female'),)
    position_choices = (('', ''),('Superadmin', 'Superadmin'),('Helpdesk', 'Helpdesk'),('User', 'User'),)
    is_active_choices = ((True, 'Active'),(False, 'Not Active'),)
    is_admin_choices = (('', ''),(True, 'Active'),(False, 'Not Active'),)
    
    username = models.CharField(max_length=255,unique = True)
    name = models.CharField(max_length=255)
    telpNo = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    gender = models.CharField(max_length=255, choices=gender_choices, default='')
    position = models.CharField(max_length=255, choices=position_choices, default='', blank=False)
    is_active = models.BooleanField(default=True, choices=is_active_choices)
    is_admin = models.BooleanField(default=False, choices=is_admin_choices)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['position']
    
    class Meta:
        db_table = 'Users'
    
    objects = MyUserManager()

    def get_full_name(self):
        return self.name

    def get_position(self):
        return self.position
    
    def get_id(self):
        return self.id
    
    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "last_login": self.last_login.__str__()[0:19],
            "name": self.name,
            "telpNo": self.telpNo,
            "address": self.address,
            "email": self.email,
            "gender": self.gender,
            "position": self.position,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
        }
        
class Ticket(models.Model):
    priority_choices = (('', ''),('Critical', 'Critical'),('High', 'High'),('Medium', 'Medium'),('Low', 'Low'),)
    problemType_choices = (('', ''),('Hardware', 'Hardware'),('Software', 'Software'),)
    status_choices = (('', ''),('Open', 'Open'),('Assigned', 'Assigned'),('Responded', 'Responded'),('Fixed', 'Fixed'),('Reopen', 'Reopen'),('Closed', 'Closed'),('Canceled', 'Canceled'),)
    
    ticketId = models.AutoField(primary_key=True)
    ticketNo = models.CharField(max_length=255,unique = True,)
    reportedDateTime = models.DateTimeField(default=datetime.now)
    reportedBy = models.ForeignKey(settings.AUTH_USER_MODEL)
    priority = models.CharField(max_length=255, choices=priority_choices, default='Medium')
    status = models.CharField(max_length=255, choices=status_choices, default='Open')
    problemType = models.CharField(max_length=255, choices=problemType_choices, default='Hardware')
    problemTitle = models.CharField(max_length=999, blank=False)
    problemDesc = models.TextField(max_length=999, blank=False)
    stepToReproduce = models.TextField(max_length=999, blank=False)
    solutionDesc = models.TextField(max_length=999, blank=True, default='')
    telephone = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255)
    attachment = models.FileField(upload_to='Static/Upload/', default='', blank=True, null=True)
    
    class Meta:
        db_table = 'Ticket'
        
    def as_dict(self):
        return {
            "ticketId": self.ticketId,
            "ticketNo": self.ticketNo,
            "reportedDateTime": self.reportedDateTime.__str__()[0:19],
            "reportedBy_id": self.reportedBy.name,
            "priority": self.priority,
            "problemType": self.problemType,
            "problemTitle": self.problemTitle,
            "status": self.status,
            "problemDesc": self.problemDesc,
            "stepToReproduce": self.stepToReproduce,
            "solutionDesc": self.solutionDesc,
            "telephone": self.telephone,
            "email": self.email,
            "attachment": self.attachment.__str__(),
        }
        
class AssignTo(models.Model):
    assignToId = models.AutoField(primary_key=True)
    ticketId = models.ForeignKey('Helpdesk.Ticket')
    assignBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fk_assign_by')
    assignTo = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fk_assign_to')
    assignDateTime = models.DateTimeField(default=datetime.now)
    
    class Meta:
        db_table = 'AssignTo'
        
    def as_dict(self):
        return {
            "assignToId": self.assignToId,
            "ticketId": self.ticketId.ticketId,
            "assignBy": self.assignBy.name,
            "assignTo": self.assignTo.name,
            "assignDateTime": self.assignDateTime.__str__()[0:19],
        }
        
class Response(models.Model):
    status_choices = (('Responded', 'Responded'),('Fixed', 'Fixed'),('Reopen', 'Reopen'),('Closed', 'Closed'),('Canceled', 'Canceled'))
    
    responseId = models.AutoField(primary_key=True)
    ticketId = models.ForeignKey('Helpdesk.Ticket')
    responseBy = models.ForeignKey(settings.AUTH_USER_MODEL)
    responseDesc = models.TextField(blank=False)
    remark = models.TextField(blank=False, default='')
    responseDateTime = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=255, choices=status_choices, default='Open')
    attachment = models.FileField(upload_to='Static/Upload/', default='', blank=True, null=True)
    
    class Meta:
        db_table = 'Response'
        
    def as_dict(self):
        return {
            "ticketId": self.ticketId.ticketNo,
            "responseBy": self.responseBy.name,
            "responseDesc": self.responseDesc,
            "remark": self.remark,
            "responseDateTime": self.responseDateTime.__str__()[0:19],
            "attachment": self.attachment,
        }
        
class TicketHistory(models.Model):
    ticketHistoryId = models.AutoField(primary_key=True)
    ticketId = models.ForeignKey('Helpdesk.Ticket')
    historyBy =  models.ForeignKey(settings.AUTH_USER_MODEL) 
    status = models.CharField(max_length=999, blank=False)
    desc = models.TextField()
    remark = models.TextField()
    historyDateTime = models.DateTimeField(default=datetime.now)
    
    class Meta:
        db_table = 'TicketHistory'
        
    def as_dict(self):
        return {
            "status": self.status,
            "desc": unquote(self.desc),
            "historyDateTime": self.historyDateTime.__str__()[0:19],
        }
        
class DocNumber(models.Model):
    docType = models.CharField(max_length=3, blank=False)
    year = models.IntegerField()
    month = models.IntegerField()
    lastNumber = models.IntegerField()
       
    class Meta:
        db_table = 'DocNumber'
        
    def as_dict(self):
        return {
            "docType": self.docType,
            "year": self.year,
            "month": self.month,
            "lastNumber": self.lastNumber,
        }