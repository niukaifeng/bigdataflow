from django.conf.urls import url, include,re_path

from workflow.views import Index,TicketCreate,MyTicket,TicketDetail,MyToDoTicket,MyRelatedTicket,AllTicket,TicketFlowStep,TicketTransition,TicketFlowlog,GetUserName,TicketBeforeFlowStep# , TicketDetail, TicketCreate


urlpatterns = [
    re_path(r'^$', Index.as_view(), name='workflow-index'),
    re_path(r'^my/$', MyTicket.as_view(), name='ticket-my'),
    re_path(r'^mytodo/$', MyToDoTicket.as_view(), name='ticket-my-todo'),
    re_path(r'^myrelated/$', MyRelatedTicket.as_view(), name='ticket-my-related'),
    re_path(r'^all/$', AllTicket.as_view(), name='ticket-all'),

    re_path(r'^ticket/(?P<ticket_id>[0-9]+)/$',
        TicketDetail.as_view(), name='ticketdetailtable'),

    re_path(r'(?P<ticket_id>[0-9]+)/flowsteps',
        TicketFlowStep.as_view(), name='ticketflowsteps'),
    re_path(r'(?P<ticket_id>[0-9]+)/flowlogs',
        TicketFlowlog.as_view(), name='ticketflowlogs'),
    re_path(r'(?P<ticket_id>[0-9]+)/transitions',
        TicketTransition.as_view(), name='tickettranstion'),
    re_path(r'^ticket/(?P<workflow_id>[0-9]+)/new/$',
        TicketCreate.as_view(), name='ticketcreate'),
    re_path(r'^getusername/$',
        GetUserName.as_view(), name='getusername'),

    re_path(r'(?P<ticket_id>[0-9]+)/beforeflowsteps',
        TicketBeforeFlowStep.as_view(), name='ticketbeforeflowsteps'),
]
