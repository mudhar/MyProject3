from django.conf.urls import patterns, url
from Helpdesk import views
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    url(r'^$', views.index, name='Index1'),
    url(r'^Index', views.index, name='Index2'),
    url(r'^Login', views.login, name='Login'),
    url(r'^Logout', views.logout, name='Logout'),
    url(r'^ChangePassword', views.changePassword, name='Change_Password'),
    url(r'^User', views.user, name='User'),
    url(r'^ListUserData', views.listUserData, name='List_User_Data'),
    url(r'^Ticket', views.ticket, name='Ticket'),
    url(r'^ListTicket/Static/Upload', views.redirect_to_static, name='Static1'),
    url(r'^ListTicketHistory/Static/Upload', views.redirect_to_static, name='Static2'),
    url(r'^ListTicketHistory/LTHD', views.lTHD, name='List_Ticket_History_Data'),
    url(r'^ListTicketHistory', views.listTicketHistory, name='List_Ticket_History'),
    url(r'^ListTicket/LTD', views.lTD, name='List_Ticket'),
    url(r'^ListTicket/LTHD', views.lTHD, name='List_Ticket_History_Data'),
    url(r'^ListTicket/Response', views.response, name='Response'),
    url(r'^LTD', views.lTD, name='List_Ticket_Data'),
    url(r'^LTHD', views.lTHD, name='List_Ticket_History_Data_ORI'),
    url(r'^AssignTo', views.assignTo, name='Assign_To'),
    url(r'^Response', views.response, name='Response'),
    url(r'^ListTicket', views.listTicket, name='List_Ticket'),
    url(r'^ReportClosed', views.reportClosed, name='Report_Closed_Ticket'),
)