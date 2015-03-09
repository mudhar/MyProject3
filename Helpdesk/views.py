
from django.template import *
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError, transaction
from django.db.models import Q
from Helpdesk.models import Users, Ticket, DocNumber, AssignTo, TicketHistory, Response
from Helpdesk.forms import changePasswordForm, UserCreationForm, UserSearchForm, TicketCreationForm, TicketSearchForm, TicketAssignForm, TicketResponseForm, TicketResponseFormUser, TicketResponseFormHelpdesk
from datetime import datetime
import json
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta
#from django.core.mail import EmailMessage
#import smtplib
from django.conf import settings                                
import uuid
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from MyProject3.settings import EMAIL_HOST_USER, STATIC_URL
from django.utils.dateparse import parse_date

def index(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    data = {}
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            # Redirect to a success page.
            auth_login(request, user)
            request.session['username'] = user.username
            request.session['userid'] = user.id
            data['success'] = True
            data['message'] = ''
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data['success'] = False
            data['message'] = 'The password is valid, but the account has been disabled!'
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data['success'] = False
        data['message'] = 'The username and password were incorrect.'
        return HttpResponse(json.dumps(data), content_type="application/json")

def logout(request):
    del request.session['username']
    del request.session['userid']
    auth_logout(request)
    return index(request)

def changePassword(request):
    data = {}
    user = Users.objects.get(username=request.session['username'])
    if request.method == 'POST':
        form = PasswordChangeForm(user, data=request.POST)
        if form.is_valid():
            new_password = form.data['new_password1']
            confirm_password = form.data['new_password2']
            if new_password and confirm_password and new_password == confirm_password:
                form.save()
                update_session_auth_hash(request, user)
                data['success'] = True
                data['message'] = ""
            else:
                data['success'] = False
                data['message'] = "Password did not match."            
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data['success'] = False
            data['message'] = 'Invalid data.'
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        form = changePasswordForm(label_suffix='')
        return render(request, 'Form.html', {'form': form.as_table()})

def user(request):
    data = {}
    if request.method == 'POST':
        user = Users.objects.filter(username=request.POST.get("username", ""))
        if user.count() != 0:
            if request.POST.get("status", "") == 'delete':
                try:
                    user.delete()
                    data['success'] = True
                    data['message'] = ''
                    return HttpResponse(json.dumps(data), content_type="application/json")
                except Exception as e:
                    data['success'] = False
                    data['message'] = 'Delete Failed. ' + e.message
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                dataUser = Users.objects.get(username=request.POST.get("username", ""))
                try:
                    form = UserCreationForm(request.POST, instance=dataUser)
                    if form.is_valid():
                        form.save(True)
                        data['success'] = True
                        data['message'] = ''
                        return HttpResponse(json.dumps(data), content_type="application/json")
                    else:
                        data['success'] = False
                        data['message'] = 'Update Failed. Invalid Input.'
                        return HttpResponse(json.dumps(data), content_type="application/json")
                except Exception as e:
                    data['success'] = False
                    data['message'] = 'Update Failed. ' + e.message
                    return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            try:
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    form.save(True)
                    data['success'] = True
                    data['message'] = ''
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data['success'] = False
                    data['message'] = 'Create Failed. Invalid Input.'
                    return HttpResponse(json.dumps(data), content_type="application/json")
            except Exception as e:
                data['success'] = False
                data['message'] = 'Create Failed. ' + e.message
                return HttpResponse(json.dumps(data), content_type="application/json")
                
    else:
        columns = [field.column for field in Users._meta.fields]
        field_name = {
            "id": "Id",
            "username": "Username",
            "password": "Password",
            "last_login": "Last Login",
            "name": "Name",
            "telpNo": "Telp No",
            "address": "Address",
            "email": "Email",
            "gender": "Gender",
            "position": "Position",
            "is_active": "Is Active",
            "is_admin": "Is Admin",
        }
        formCU = UserCreationForm(label_suffix='')
        formSearch = UserSearchForm(label_suffix='')
        hiddenField = ['id', 'password', 'last_login']
        return render(request, 'UserTemp.html', {'form': columns, 'url':'ListUserData', 'Dialog':formCU, 'DialogSearch':formSearch, 'hiddenField':hiddenField, 'field_name':field_name})
    
def listUserData(request):
    pUsername = request.POST.get("username", "")
    pName = request.POST.get("name", "")
    pTelpNo = request.POST.get("telpNo", "")
    pAddress = request.POST.get("address", "")
    pGender = request.POST.get("gender", "")
    pEmail = request.POST.get("email", "")
    pPosition = request.POST.get("position", "")
    user = Users.objects.filter(
                                Q(username__loe=pUsername),
                                Q(name__loe=pName),
                                Q(telpNo__loe=pTelpNo),
                                Q(address__loe=pAddress),
                                Q(gender__loe=pGender),
                                Q(email__loe=pEmail),
                                Q(position__loe=pPosition)
                                )
    dictionaries = [ obj.as_dict() for obj in user ]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')

def ticket(request):
    data = {}
    if request.method == 'POST':
        ticket = Ticket.objects.filter(ticketNo=request.POST.get("ticketNo", ""))
        if ticket.count() != 0:
            if request.POST.get("status", "") == 'delete':
                try:
                    with transaction.atomic():
                        history = TicketHistory(
                                status='Canceled',
                                desc='',
                                remark='',
                                historyBy_id=request.user.id,
                                ticketId=ticket
                            )
                        history.save()
                        ticket.status = 'Canceled'
                        ticket.save()
                        data['success'] = True
                        data['message'] = ''
                        return HttpResponse(json.dumps(data), content_type="application/json")
                except IntegrityError:
                    handle_exception()
                    data['success'] = False
                    data['message'] = 'Delete Failed.'
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                dataTicket = Ticket.objects.get(ticketNo=request.POST.get("ticketNo", ""))
                try:
                    with transaction.atomic():
                        if request.FILES:
                            file = request.FILES['attachment']
                            if file:
                                form = TicketCreationForm(request.POST, request.FILES, instance=dataTicket)
                        else:
                            form = TicketCreationForm(request.POST, instance=dataTicket)
                        if form.is_valid():
                            form.save(True)
                            ticketSaved = Ticket.objects.get(ticketNo=dataTicket.ticketNo)
                            if request.FILES:
                                file = request.FILES['attachment']
                                if file:
                                    destination = open('C:/xampp/htdocs/MyProject3/Helpdesk/'+ticketSaved.attachment.__str__(), 'wb+')
                                    for chunk in file.chunks():
                                        destination.write(chunk)
                                    destination.close()
                            history = TicketHistory(
                                    status='Open',
                                    desc=
                                        '<table class="detail_grid">' +
                                        '<tr><td style="width:100px;" valign="top">Title</td><td valign="top">:</td><td valign="top">' + ticketSaved.problemTitle + '</td></tr>' +
                                        '<tr><td style="width:100px;" valign="top">Type</td><td valign="top">:</td><td valign="top">' + ticketSaved.problemType + '</td></tr>' +
                                        '<tr><td style="width:100px;" valign="top">Priority</td><td valign="top">:</td><td valign="top">' + ticketSaved.priority + '</td></tr>' +
                                        '<tr><td style="width:100px;" valign="top">Description</td><td valign="top">:</td><td valign="top">' + ticketSaved.problemDesc + '</td></tr>' +
                                        '<tr><td style="width:100px;" valign="top">Step To Reproduce</td><td valign="top">:</td><td valign="top">' + ticketSaved.stepToReproduce + '</td></tr>' +
                                        '<tr><td style="width:100px;" valign="top">Phone</td><td valign="top">:</td><td valign="top">' + ticketSaved.telephone + '</td></tr>' +
                                        '<tr><td style="width:100px;" valign="top">Email</td><td valign="top">:</td><td valign="top">' + ticketSaved.email + '</td></tr>' +
                                        '<tr><td style="width:100px;" valign="top">Reported By</td><td valign="top">:</td><td valign="top">' + ticketSaved.reportedBy.name + '</td></tr>' +
                                        '<tr><td style="width:100px;" valign="top">Attachment</td><td valign="top">:</td><td valign="top"><a href="' + ticketSaved.attachment.__str__() + '" download>'+ticketSaved.attachment.__str__().replace('Static/Upload/', '')+'</a></td></tr>' +
                                         '</table>',
                                    remark='',
                                    historyBy_id=request.user.id,
                                    ticketId=ticketSaved
                            )
                            history.save()
                            data['success'] = True
                            data['message'] = ''
                            return HttpResponse(json.dumps(data), content_type="application/json")
                except IntegrityError:
                    handle_exception()
                    data['success'] = False
                    data['message'] = 'Update Failed.'
                    return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            try:
                with transaction.atomic():
                    docNumber = DocNumber.objects.filter(docType='TCK', year=datetime.now().year, month=datetime.now().month)
                    if docNumber.count() == 0:
                        docNumber = DocNumber(
                            docType='TCK',
                            year=datetime.now().year,
                            month=datetime.now().month,
                            lastNumber=1
                        )
                    else:
                        docNumber = DocNumber.objects.get(docType='TCK', year=datetime.now().year, month=datetime.now().month)
                        docNumber.lastNumber = docNumber.lastNumber + 1
                    docNumber.save()
                    ticketNo = docNumber.docType + "" + docNumber.year.__str__() + "" + docNumber.month.__str__() + "%05d" % docNumber.lastNumber;
                    post_mutable = request.POST.copy()
                    post_mutable["ticketNo"] = ticketNo
                    post_mutable["reportedBy"] = request.user.id
                    
                    if request.FILES:
                        file = request.FILES['attachment']
                        if file:
                            form = TicketCreationForm(post_mutable, request.FILES)
                    else:
                        form = TicketCreationForm(post_mutable)
                    if form.is_valid():
                        form.save(True)
                        ticketSaved = Ticket.objects.get(ticketNo=ticketNo)
                        if request.FILES:
                            file = request.FILES['attachment']
                            if file:
                                destination = open('C:/xampp/htdocs/MyProject3/Helpdesk/'+ticketSaved.attachment.__str__(), 'wb+')
                                for chunk in file.chunks():
                                    destination.write(chunk)
                                destination.close()
                        history = TicketHistory(
                                status='Open',
                                desc=
                                    '<table class="detail_grid">' +
                                    '<tr><td style="width:100px;" valign="top">Title</td><td valign="top">:</td><td valign="top">' + ticketSaved.problemTitle + '</td></tr>' +
                                    '<tr><td style="width:100px;" valign="top">Type</td><td valign="top">:</td><td valign="top">' + ticketSaved.problemType + '</td></tr>' +
                                    '<tr><td style="width:100px;" valign="top">Priority</td><td valign="top">:</td><td valign="top">' + ticketSaved.priority + '</td></tr>' +
                                    '<tr><td style="width:100px;" valign="top">Description</td><td valign="top">:</td><td valign="top">' + ticketSaved.problemDesc + '</td></tr>' +
                                    '<tr><td style="width:100px;" valign="top">Step To Reproduce</td><td valign="top">:</td><td valign="top">' + ticketSaved.stepToReproduce + '</td></tr>' +
                                    '<tr><td style="width:100px;" valign="top">Phone</td><td valign="top">:</td><td valign="top">' + ticketSaved.telephone + '</td></tr>' +
                                    '<tr><td style="width:100px;" valign="top">Email</td><td valign="top">:</td><td valign="top">' + ticketSaved.email + '</td></tr>' +
                                    '<tr><td style="width:100px;" valign="top">Reported By</td><td valign="top">:</td><td valign="top">' + ticketSaved.reportedBy.name + '</td></tr>' +
                                    '<tr><td style="width:100px;" valign="top">Attachment</td><td valign="top">:</td><td valign="top"><a href="' + ticketSaved.attachment.__str__() + '" download>'+ticketSaved.attachment.__str__().replace('Static/Upload/', '')+'</a></td></tr>' +
                                    '</table>',
                                remark='',
                                historyBy_id=request.user.id,
                                ticketId=ticketSaved
                        )
                        history.save()
                        data['success'] = True
                        data['message'] = ''
                        data['number'] = ticketNo
                        return HttpResponse(json.dumps(data), content_type="application/json")
                    else:
                        data['success'] = False
                        data['message'] = 'Invalid Form'
                        data['number'] = ''
                        return HttpResponse(json.dumps(data), content_type="application/json")
            except IntegrityError:
                handle_exception()
                data['success'] = False
                data['message'] = 'Create Failed.'
                return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        if request.GET.get('param', ''):
            tick = Ticket.objects.get(ticketNo=request.GET.get('param', ''))
            form = TicketCreationForm(label_suffix='', instance=tick)
        else:
            form = TicketCreationForm(label_suffix='')
        return render(request, 'Form.html', {'form': form.as_table(), 'upload':True})
    
    
def listTicket(request):
    field_name = {
                  "ticketId": "Ticket Id",
                  "ticketNo": "Ticket No",
                  "status": "Status",
                  "priority": "Priority",
                  "reportedBy_id": "Reported By",
                  "reportedDateTime": "Reported Time",
                  "problemType": "Problem Type",
                  "problemTitle": "Problem Title",
                  "problemDesc": "ProblemDesc",
                  "stepToReproduce": "Step To Reproduce",
                  "solutionDesc": "Solution Desc",
                  "telephone": "Telephone",
                  "email": "Email",
                  "attachment": "Attachment",
                }
    columns = [field.column for field in Ticket._meta.fields]
    formSearch = TicketSearchForm()
    formAssign = TicketAssignForm()
    formResponse = TicketResponseForm()
    
    position = request.user.get_position()
    if(position=='User'):
        #status_choices = (('Reopen', 'Reopen'),('Closed', 'Closed'),('Canceled', 'Canceled'))
        formResponse = TicketResponseFormUser()
    elif(position=='Helpdesk'):
        #status_choices = (('Responded', 'Responded'),('Fixed', 'Fixed'),('Reopen', 'Reopen'))
        formResponse = TicketResponseFormHelpdesk()
        
    formSearch.fields['reportedDateTime'].initial = ''
    formSearch.fields['priority'].initial = ''
    formSearch.fields['assignTo'].initial = ''
    formSearch.fields['problemType'].initial = ''
    formSearch.fields['status'].initial = ''
    #formSearch.fields['reportedBy'].initial = ''
    
    if request.GET.get('reportedBy', ''):
        reportedBy = request.GET.get('reportedBy', '')
    else:
        reportedBy = ''
        
    if request.GET.get('assignTo', ''):
        assignTo = request.GET.get('assignTo', '')
    else:
        assignTo = ''
    
    if request.GET.get('status', ''):
        status = request.GET.get('status', '')
    else:
        status = ''
    
    if request.GET.get('solvedBy', ''):
        solvedBy = request.GET.get('solvedBy', '')
    else:
        solvedBy = ''
        
    return render(request, 'TicketTemp.html', {'form': columns, 'field_name':field_name, 'DialogAssign':formAssign, 'DialogResponse':formResponse, 'DialogSearch':formSearch, 'url':'LTD', 'reportedBy':reportedBy, 'assignTo':assignTo, 'status':status, 'solvedBy':solvedBy})
    
def lTD(request):
    page = int('0' + request.POST['page'])
    rows = int('0' + request.POST['rows'])
    start = ((page-1) * rows)
    end = start + rows
    
    pTicketNo = request.POST.get("ticketNo", "")
    pReportedDateTime = request.POST.get("reportedDateTime", "")
    pPriority = request.POST.get("priority", "")
    pProblemType = request.POST.get("problemType", "")
    pProblemTitle = request.POST.get("problemTitle", "")
    pProblemDesc = request.POST.get("problemDesc", "")
    pStepToReproduce = request.POST.get("stepToReproduce", "")
    pTelephone = request.POST.get("telephone", "")
    pEmail = request.POST.get("email", "")
    pStatus = request.POST.get("status", "")
    pStatusBy = request.POST.get("statusBy", "")
    pStatusBy = int('0' + pStatusBy)
    pStatusBefore = request.POST.get("statusBefore", "")
    pAssignTo = request.POST.get("assignTo", "")
    pAssignTo = int('0' + pAssignTo)
    
    history = TicketHistory.objects.values_list('ticketId','status','historyBy').order_by('ticketId').distinct()
    ticket = Ticket.objects.all()
    
    #my ticket and my assignment
    if pStatusBefore != '':
        history = history.filter(status=pStatus, historyBy_id=pStatusBy)
    
    if pStatus != '' and pStatusBefore == '':
        ticket = ticket.filter(status=pStatus)
        
    if pStatus == 'Open' and pStatusBy != 0 and pStatusBefore == '':
        ticket = ticket.filter(status=pStatus,reportedBy_id=pStatusBy)
    
    listIn = []
    for x in history:
        listIn.append(x[0])
    ticket = ticket.filter(ticketId__in=listIn)
    
    if pAssignTo != 0:
        ticket = ticket.filter(assignto__assignTo_id=pAssignTo)
        
    ticket = ticket.order_by('ticketId').filter(
                           Q(ticketNo__loe=pTicketNo),
                           Q(priority__eoe=pPriority),
                           Q(problemType__eoe=pProblemType),
                           Q(problemTitle__loe=pProblemTitle),
                           Q(problemDesc__loe=pProblemDesc),
                           Q(stepToReproduce__loe=pStepToReproduce),
                           Q(telephone__loe=pTelephone),
                           Q(email__loe=pEmail),
                           )
    if pReportedDateTime != '':
        startDate = parse_date(pReportedDateTime)
        endDate = startDate + timedelta( days=1 ) 
        ticket = ticket.filter(reportedDateTime__range=(startDate,endDate))
    
    ticketCount = ticket.count()
    ticket = ticket[start:end]
    dictionaries = [ obj.as_dict() for obj in ticket ]
    data = {}
    data['total'] = ticketCount
    data['rows'] = dictionaries
    return HttpResponse(json.dumps(data), content_type='application/json')
    
def assignTo(request):
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                strTo = ''
                emailTo = []
                listData = request.POST.getlist('assignTo')
                ticket = Ticket.objects.get(ticketNo=request.POST.get("ticketNo", ""))
                allAssignTo = AssignTo.objects.filter(ticketId=ticket)
                if allAssignTo.count() != 0:
                    allAssignTo.delete()
                for ldata in listData:
                    assignTo = AssignTo(
                                assignBy_id=request.user.id,
                                assignTo_id=ldata,
                                assignDateTime=datetime.now(),
                                ticketId=ticket
                            )
                    assignTo.save()
                    userTo = Users.objects.get(id=ldata)
                    strTo = strTo + assignTo.assignTo.name +', '
                    emailTo.append(userTo.email)
                    
                ticket.status = 'Assigned'
                ticket.save()
                history = TicketHistory(
                                        status='Assigned',
                                        desc=
                                            '<table class="detail_grid">' +
                                            '<tr><td style="width:100px;" valign="top">Assign To</td><td valign="top">:</td><td valign="top">' + strTo + '</td></tr>' +
                                            '<tr><td style="width:100px;" valign="top">Assign By</td><td valign="top">:</td><td valign="top">' + request.user.name + '</td></tr>' +
                                             '</table>',                                         
                                        remark='',
                                        historyBy_id=request.user.id,
                                        ticketId=ticket
                        )
                history.save()
                historyOpen = TicketHistory.objects.filter(ticketId=history.ticketId, status='Open').order_by('historyDateTime')[0:1].get()
                if(ticket.priority=='Critical'):
                    subject = 'Critical Ticket'
                    sender = EMAIL_HOST_USER
                    recipients = emailTo
                    body = historyOpen.desc
                    msg = EmailMultiAlternatives(subject, '', sender, recipients)
                    msg.attach_alternative(body, "text/html")
                    msg.send()
                            
                data['success'] = True
                data['message'] = 'Success'
                return HttpResponse(json.dumps(data), content_type="application/json")
        except IntegrityError:
            handle_exception()
            data['success'] = False
            data['message'] = 'Failed.'
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        if request.GET.get('param', ''):
            ticket = Ticket.objects.get(ticketNo=request.GET.get('param', ''))
            assignToData = AssignTo.objects.filter(ticketId=ticket).values_list('assignTo_id')
            choices = [] 
            for x in assignToData:
                choices.append(x[0])
            form = TicketAssignForm(label_suffix='')
            form.fields['ticketNo'].initial = request.GET.get('param', '')
            form.fields['assignTo'].initial = choices
            return render(request, 'Form.html', {'form': form.as_table()})

def response(request):
    data = {}
    if request.method == 'POST':
        try:
            with transaction.atomic():
                by = Users.objects.get(id=request.user.id)
                ticket = Ticket.objects.get(ticketNo=request.POST.get("ticketNo", ""))
                response = Response(
                                    responseDesc = request.POST.get("responseDesc", ""),
                                    remark = request.POST.get("remark", ""),
                                    status = request.POST.get("status", ""),
                                    responseBy = by,
                                    ticketId = ticket,
                                    )
                response.save()
                
                if request.FILES:
                    file = request.FILES['attachment']
                    fileName = file._name
                    ext = fileName.split('.')[-1]
                    fileName = "%s.%s" % (uuid.uuid4(), ext)
                    response.attachment = 'Static/Upload/'+fileName
                    response.save()
                    if file:
                        destination = open('C:/xampp/htdocs/MyProject3/Helpdesk/'+response.attachment.__str__(), 'wb+')
                        for chunk in file.chunks():
                            destination.write(chunk)
                        destination.close()
                    
                ticket.status = request.POST.get("status", "")
                if request.POST.get("status", "") == 'Fixed':
                    ticket.solutionDesc = request.POST.get("responseDesc", "")
                ticket.save()
                history = TicketHistory(
                                        status=request.POST.get("status", ""),
                                        desc=
                                            '<table class="detail_grid">' +
                                            '<tr><td style="width:100px;" valign="top">Description</td><td valign="top">:</td><td valign="top">' + request.POST.get("responseDesc", "") + '</td></tr>' +
                                            '<tr><td style="width:100px;" valign="top">Remark</td><td valign="top">:</td><td valign="top">' + request.POST.get("remark", "") + '</td></tr>' +
                                            '<tr><td style="width:100px;" valign="top">Attachment</td><td valign="top">:</td><td valign="top"><a href="' + response.attachment.__str__() + '" download>'+response.attachment.__str__().replace('Static/Upload/', '')+'</a></td></tr>' +
                                            '</table>',                                         
                                        remark='Response Id : ' + response.responseId.__str__(),
                                        historyBy_id=request.user.id,
                                        ticketId=ticket
                        )
                history.save()
                data['success'] = True
                data['message'] = 'Success'
                return HttpResponse(json.dumps(data), content_type="application/json")
        except IntegrityError:
            handle_exception()
            data['success'] = False
            data['message'] = 'Failed.'
            return HttpResponse(json.dumps(data), content_type="application/json")
    
           
def listTicketHistory(request):
    ticketId = request.GET.get("param", "")
    return render(request, 'TicketHistoryTemp.html', {'ticketId': ticketId}, context_instance=RequestContext(request))
    
def lTHD(request):
    page = int('0' + request.POST['page'])
    rows = int('0' + request.POST['rows'])
    start = ((page-1) * rows)
    end = start + rows
    pTicketId = request.POST.get("ticketId", "")
    ticketHistory = TicketHistory.objects.order_by('ticketHistoryId').filter(ticketId_id=pTicketId)[start:end]
    ticketHistoryCount = TicketHistory.objects.filter(ticketId_id=pTicketId).count()
    dictionaries = [ obj.as_dict() for obj in ticketHistory ]
    data = {}
    data['total'] = ticketHistoryCount
    data['rows'] = dictionaries
    return HttpResponse(json.dumps(data), content_type='application/json')

width, height = 46.5*cm, 24*cm
def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

def reportClosed(self):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=closed_tickets.pdf'
    
    elements = []
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_JUSTIFY

    tickets = Ticket.objects.filter(status='Closed')

    h1 = Paragraph('''<b>Ticket No</b>''', styleBH)
    h2 = Paragraph('''<b>Problem Desc</b>''', styleBH)
    h3 = Paragraph('''<b>Step To Reproduce</b>''', styleBH)
    h4 = Paragraph('''<b>Reported Time</b>''', styleBH)
    h5 = Paragraph('''<b>Reported By</b>''', styleBH)
    h6 = Paragraph('''<b>Priority</b>''', styleBH)
    h7 = Paragraph('''<b>Problem Title</b>''', styleBH)
    h8 = Paragraph('''<b>Problem Type</b>''', styleBH)
    h9 = Paragraph('''<b>Solution Desc</b>''', styleBH)
    
    table_data = []
    table_data.append([h1,h2,h3,h4,h5,h6,h7,h8,h9])
    for i, ticket in enumerate(tickets):
        c1 = Paragraph(ticket.ticketNo, styleN)
        c2 = Paragraph(ticket.problemDesc, styleN)
        c3 = Paragraph(ticket.stepToReproduce, styleN)
        c4 = Paragraph(ticket.reportedDateTime.__str__()[0:19], styleN)
        c5 = Paragraph(ticket.reportedBy.name, styleN)
        c6 = Paragraph(ticket.priority, styleN)
        c7 = Paragraph(ticket.problemTitle, styleN)
        c8 = Paragraph(ticket.problemType, styleN)
        c9 = Paragraph(ticket.solutionDesc, styleN)
        table_data.append([c1,c2,c3,c4,c5,c6,c7,c8,c9])
        
    user_table = Table(table_data, colWidths=[3.5 * cm, 8 * cm, 8 * cm, 3 * cm, 3 * cm, 2 * cm, 5 * cm, 3 * cm, 8 * cm])
    user_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),('BOX', (0,0), (-1,-1), 0.25, colors.black),]))
    elements.append(user_table)
    
    c = canvas.Canvas(response)
    c.setPageSize((width, height)) 
    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_CENTER
    p.fontSize = 20
    
    para = Paragraph("Laporan Ticket Helpdesk SMK Saradan", p)
    para.wrapOn(c, width, height)
    para.drawOn(c, *coord(1.2, 2, cm))

    user_table.wrapOn(c, width, height)
    user_table.drawOn(c, *coord(1.2, 9, cm))
    c.showPage()
    c.save()
    
    return response

def redirect_to_static(request):
    url = request.path
    filename = url.split('/')[-1]
    filename = STATIC_URL+'Upload/'+filename
    return redirect(filename)


    
    