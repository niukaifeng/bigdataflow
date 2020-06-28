from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
try:
    import simplejson as json
except ImportError:
    import json
from django import forms
from django.http import Http404, JsonResponse, FileResponse
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

import datetime
import os
import time
from workflow.apirequest import WorkFlowAPiRequest
from django.contrib.auth.models import User
from workflow.util.Utils import Util
from django.conf import settings
from workflow.models import TempWork

# Create your views here.
# 登录后首页调用的函数，返回的是数据库中workflow_workflow表
class Index(LoginRequiredMixin, TemplateView):
    template_name = 'workflow/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        #context['workflows'] = Workflow.objects.all()
        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status,data = ins.getdata(dict(per_page=20, name=''),method='get',url='/api/v1.0/workflows')
        #print(data['value'])
        if status:
            context['workflows'] = data['data']['value']
        #print(context['workflows'])
        return context

# 用于选择工作流，创建工单的函数  by kf
class TicketCreate(LoginRequiredMixin, FormView):
    template_name = 'workflow/ticketcreate.html'
    success_url = '/'

    def get_form_class(self):
        form_fields = dict()
        workflow_id = self.kwargs.get('workflow_id')

        # get ticket initial data
        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status, state_result = ins.getdata({}, method='get',
                                           url='/api/v1.0/workflows/{0}/init_state'.format(workflow_id))
        # print(1)
        # print(state_result)
        state_result = state_result['data']

        self.kwargs.update({'state_result': state_result})

        #print(state_result.keys())
        if isinstance(state_result, dict) and 'field_list' in state_result.keys():
            class DynamicForm(forms.Form):
                def __init__(self, *args, **kwargs):
                    self.helper = FormHelper()
                    self.helper.form_class = 'form-horizontal'
                    self.helper.label_class = 'col-md-2'
                    self.helper.field_class = 'col-md-8'
                    # DictionaryField bug
                    self.helper.layout = Layout(
                        *[Div(field['field_key'], css_class='form-group') for field in state_result['field_list']])
                    super(DynamicForm, self).__init__(*args, **kwargs)

            for field in state_result['field_list']:
                Util.createWebDirex(field,forms,form_fields,User)
                # handle read only field
                if field['field_attribute'] == 1:
                    form_fields[field['field_key']
                    ].widget.attrs['disabled'] = 'disabled'
        else:
            raise Http404()
        print(form_fields)

        return type('DynamicItemsForm', (DynamicForm,), form_fields)

    def get_context_data(self, **kwargs):
        context = super(TicketCreate, self).get_context_data(**kwargs)
        context['workflow_id'] = self.kwargs.get('workflow_id')
        state_result = self.kwargs.get('state_result', None)
        context['state_result'] = state_result
        # context['msg'] = msg
        if isinstance(state_result, dict) and 'field_list' in state_result.keys() and len(
                state_result['field_list']) == 0:
            context['noform'] = True
        # print(2)
        # print(context)
        if isinstance(state_result, dict) and 'transition' in state_result.keys():
            context['buttons'] = state_result['transition']
        #print(3)
        #print(context)
        return context

    def form_valid(self, form):
        # save ticket
        if 'transition_id' in form.data.keys():

            transition_id = form.data['transition_id']
            form_data = form.cleaned_data
            form_data['transition_id'] = int(transition_id)
            # form_data['username'] = self.request.user.username
            form_data['workflow_id'] = int(self.kwargs.get('workflow_id'))
            file_keys = list(form.files.keys())
            title = form.data["title"]
            for file_key in file_keys:
                #存放
                file = form.files[file_key].file
                file_name  = form.files[file_key].name
                curr_time = datetime.datetime.now()
                form_data[file_key] = os.path.abspath(os.curdir)+ '/media/' + title +"/"  + str(curr_time.date()) + '_' + str(curr_time.hour)+ '-' + str(curr_time.minute) + '-' + str(curr_time.second) + '-' + str(curr_time.microsecond) + '_' + file_name
                Util.saveFile(file,form_data[file_key])

            for key, value in form_data.items():
                #原始代码：if isinstance(value, datetime.datetime):
                # 修改后解决了日期、日期时间的问题
                if isinstance(value, datetime.date):
                    form_data[key] = form.data[key]

            # for test only
            ins = WorkFlowAPiRequest(username=self.request.user.username)
            status, state_result = ins.getdata(data=form_data, method='post', url='/api/v1.0/tickets')
            # if new_ticket_result:
            # code, data = 0, {'ticket_id': new_ticket_result}
            # else:
            # code, data = -1, {}
        return super().form_valid(form)

#该类用于调用“我创建的”工单页面   by kf
class MyTicket(LoginRequiredMixin, TemplateView):
    template_name = 'workflow/my.html'

    def get_context_data(self, **kwargs):
        context = super(MyTicket, self).get_context_data(**kwargs)
        request_data = self.request.GET
        sn = request_data.get('sn', '')
        title = request_data.get('title', '')
        username = request_data.get('username', '')
        create_start = request_data.get('create_start', '')
        create_end = request_data.get('create_end', '')
        workflow_ids = request_data.get('workflow_ids', '')
        reverse = int(request_data.get('reverse', 1))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        # 待办,关联的,创建
        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status,state_result = ins.getdata(parameters=dict(category='owner'),method='get',url='/api/v1.0/tickets')
        if status:
            if len(state_result) > 0 and isinstance(state_result,dict) and 'data' in state_result.keys() and 'value' in state_result['data'].keys():
                context['ticket_result_restful_list'] = state_result['data']['value']
        context['msg'] = state_result['msg']
        #print(context)
        return context

# 在我创建的页面中点击“详情”，显示工单的详情页面  by kf
#LoginRequiredMixin,TemplateView  FormView
class TicketDetail(LoginRequiredMixin, FormView):
    template_name = 'workflow/ticketdetail.html'
    success_url="/"

    def get_form_class(self):
        form_fields = dict()
        ticket_id = self.kwargs.get('ticket_id')

        ins = WorkFlowAPiRequest(username=self.request.user.username)

        #获取组建
        status, state_result = ins.getdata(parameters={}, method='get',
                                           url='/api/v1.0/tickets/{0}'.format(ticket_id))
        #获取提交按钮
        status2, state_result2 = ins.getdata(parameters={}, method='get',
                                           url='/api/v1.0/tickets/{0}/transitions'.format(self.kwargs.get('ticket_id')))

        state_result = state_result['data']['value']
        state_result2 = state_result2['data']['value']

        out_list = list()

        if isinstance(state_result, dict) and 'field_list' in state_result.keys():
            class DynamicForm(forms.Form):
                def __init__(self, *args, **kwargs):
                    self.helper = FormHelper()
                    self.helper.form_class = 'form-horizontal'
                    self.helper.form_action = " "
                    self.helper.label_class = 'col-md-label'
                    self.helper.field_class = 'col-md-field'
                    # DictionaryField bug
                    self.helper.layout = Layout(
                        *[Div(field['field_key'], css_class='form-table-group') for field in state_result['field_list']])
                    super(DynamicForm, self).__init__(*args, **kwargs)

            find_is_null = False
            j_shigongjindu_float_zonghengzumaosuo  = ""
            j_shigongjindu_float_zongqiefengzhuankong = ""
            j_shigongjindu_float_zongbaopoliefeng = ""
            j_shigongjindu_float_muqianhengzumaosuo = ""
            j_shigongjindu_float_muqianqiefengzhuankong = ""
            j_shigongjindu_float_muqianbaopoliefeng = ""
            try:
                temWork = TempWork.objects.get(ticket_id=ticket_id)

                recode = eval(temWork.process_recod)

                j_shigongjindu_float_zonghengzumaosuo = recode["j_shigongjindu_float_zonghengzumaosuo"]
                j_shigongjindu_float_zongqiefengzhuankong = recode["j_shigongjindu_float_zongqiefengzhuankong"]
                j_shigongjindu_float_zongbaopoliefeng = recode["j_shigongjindu_float_zongbaopoliefeng"]

                j_shigongjindu_float_muqianhengzumaosuo = recode["j_shigongjindu_float_muqianhengzumaosuo"]
                j_shigongjindu_float_muqianqiefengzhuankong= recode["j_shigongjindu_float_muqianqiefengzhuankong"]
                j_shigongjindu_float_muqianbaopoliefeng = recode["j_shigongjindu_float_muqianbaopoliefeng"]

                find_is_null = True
            except TempWork.DoesNotExist:
                pass

            for field in state_result['field_list']:

                attributeFlag = field["field_attribute"]
                # 1只读，2必填，3选填
                #创建时候，只有是必须填写或者选填的才进行渲染  'field_key' (140598713991728) 'b_guanliyuanshenpi_char_xiangmubianhao'
                if  attributeFlag != 1 :
                    if field['field_key']  == 'b_guanliyuanshenpi_char_xiangmubianhao':
                        field['field_attribute'] =  3

                    if field['field_key']  == 'j_shigongjindu_float_zonghengzumaosuo':
                        field['default_value'] = j_shigongjindu_float_zonghengzumaosuo

                    if field['field_key'] == 'j_shigongjindu_float_zongqiefengzhuankong':
                            field['default_value'] = j_shigongjindu_float_zongqiefengzhuankong

                    if field['field_key'] == 'j_shigongjindu_float_zongbaopoliefeng':
                        field['default_value'] = j_shigongjindu_float_zongbaopoliefeng

                    if field['field_key'] == 'j_shigongjindu_float_muqianhengzumaosuo':
                        field['default_value'] = j_shigongjindu_float_muqianhengzumaosuo

                    if field['field_key']  == 'j_shigongjindu_float_muqianqiefengzhuankong':
                        field['default_value'] = j_shigongjindu_float_muqianqiefengzhuankong

                    if field['field_key']  == 'j_shigongjindu_float_muqianbaopoliefeng':
                        field['default_value'] = j_shigongjindu_float_muqianbaopoliefeng

                    out_list.append(field)
                    Util.createWebDirex(field, forms, form_fields, User)
                # handle read only field
                # if field['field_attribute'] == 1:
                #     form_fields[field['field_key']
                #     ].widget.attrs['disabled'] = 'disabled'
        else:
            raise Http404()

        state_result['field_list'] = out_list
        self.kwargs.update({'state_result': state_result})
        self.kwargs.update({'title': state_result["title"]})
        self.kwargs.update({'state_result2': state_result2})
        if (len(state_result['field_list']) != 0):
            self.kwargs.update({'showSuggestion': 'true'})
        return type('DynamicItemsForm', (DynamicForm,), form_fields)

    def get_context_data(self, **kwargs):
        context = super(TicketDetail, self).get_context_data(**kwargs)

        state_result = self.kwargs.get('state_result', None)
        state_result2 = self.kwargs.get('state_result2', None)

        if not state_result2 == None:
            for result in state_result2:
                if settings.WORKTEMPSAVEBUTTONNAME == result['transition_name']:
                    context['show_stpe'] = True
                    context['temp_savebutton'] = settings.FLOWINPUTSTR
                    break
        workflow_name = ""
        if 'workflow_name' in self.request.GET.keys() :
            workflow_name = str(self.request.GET['workflow_name']).strip()

        flow_code = state_result['sn']

        flow_code = flow_code[flow_code.find("_")+1::]

        #为了组建显示
        context['state_result'] = state_result
        context['workflow_name'] = workflow_name
        context['flow_code'] = flow_code
        #查找日志
        context['ticket_id'] = self.kwargs.get('ticket_id')
        # 画面显示“处理意见”控件
        context['showSuggestion'] = self.kwargs.get('showSuggestion')

        # title 文件存储的路径
        context['title'] = self.kwargs.get('title')

        #按钮显示
        context['buttons'] = state_result2

        return context

    # 点击确认后，提交表单
    def form_valid(self, form):
        # save ticket
        if 'transition_id' in form.data.keys():
            transition_id = form.data['transition_id']
            form_data = form.cleaned_data
            form_data['transition_id'] = int(transition_id)
            # suggestion
            ticket_id = int(self.kwargs.get('ticket_id'))
            file_keys = list(form.files.keys())
            suggestion = form.data['suggestion']
            form_data['suggestion'] = suggestion
            title = form.data["title"]

            for file_key in file_keys:
                # 存放
                file = form.files[file_key].file
                file_name = form.files[file_key].name
                curr_time = datetime.datetime.now()
                # form_data[file_key] = os.path.abspath(os.curdir) + '/media/' + title + '/' + str(int(time.time())) + file_name
                form_data[file_key] = os.path.abspath(os.curdir) + '/media/' + title +"/"  + str(curr_time.date()) + '_' + str(curr_time.hour)+ '-' + str(curr_time.minute) + '-' + str(curr_time.second) + '-' + str(curr_time.microsecond) + '_' + file_name
                Util.saveFile(file, form_data[file_key])

            for key, value in form_data.items():
                # 原始代码：if isinstance(value, datetime.datetime):
                # 修改后解决了日期、日期时间的问题
                if isinstance(value, datetime.date):
                    form_data[key] = form.data[key]

            ins = WorkFlowAPiRequest(username=self.request.user.username)
            status, state_result = ins.getdata(data=form_data, method='patch',
                                               url='/api/v1.0/tickets/{0}'.format(ticket_id))

        return super().form_valid(form)


#“我的代办”，页面处理函数   by kf
class MyToDoTicket(LoginRequiredMixin, TemplateView):
    template_name = 'workflow/mytodo.html'

    def get_context_data(self, **kwargs):
        context = super(MyToDoTicket, self).get_context_data(**kwargs)
        request_data = self.request.GET
        sn = request_data.get('sn', '')
        title = request_data.get('title', '')
        username = request_data.get('username', '')
        create_start = request_data.get('create_start', '')
        create_end = request_data.get('create_end', '')
        workflow_ids = request_data.get('workflow_ids', '')
        reverse = int(request_data.get('reverse', 1))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        # 待办,关联的,创建
        category = request_data.get('category')
        #因为需要对应不同username，所以接口返回的数据也不同
        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status,state_result = ins.getdata(parameters=dict(category='duty'),method='get',url='/api/v1.0/tickets')
        #print(state_result)
        if status:
            if len(state_result) > 0 and isinstance(state_result,dict) and 'data' in state_result.keys() and isinstance(state_result['data'],dict) and 'value' in state_result['data'].keys():
                context['ticket_result_restful_list'] = state_result['data']['value']
        context['msg'] = state_result['msg']
        #print(context)
        return context

#左侧菜单栏中“我相关的”页面处理函数  by kf
class MyRelatedTicket(LoginRequiredMixin, TemplateView):
    template_name = 'workflow/myrelated.html'

    def get_context_data(self, **kwargs):
        context = super(MyRelatedTicket, self).get_context_data(**kwargs)
        request_data = self.request.GET
        sn = request_data.get('sn', '')
        title = request_data.get('title', '')
        username = request_data.get('username', '')
        create_start = request_data.get('create_start', '')
        create_end = request_data.get('create_end', '')
        workflow_ids = request_data.get('workflow_ids', '')
        reverse = int(request_data.get('reverse', 1))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        # 待办,关联的,创建
        category = request_data.get('category')
        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status,state_result = ins.getdata(parameters=dict(category='relation'),method='get',url='/api/v1.0/tickets')
        if status:
            if len(state_result) > 0 and isinstance(state_result,dict) and 'data' in state_result.keys() and 'value' in state_result['data'].keys():
                context['ticket_result_restful_list'] = state_result['data']['value']
        context['msg'] = state_result['msg']
        return context

#左侧菜单栏中“所有工单”页面处理函数  by kf
class AllTicket(LoginRequiredMixin, TemplateView):
    template_name = 'workflow/allticket.html'

    def get_context_data(self, **kwargs):
        context = super(AllTicket, self).get_context_data(**kwargs)
        request_data = self.request.GET
        #filter ticket in the future if necessary
        sn = request_data.get('sn', '')
        title = request_data.get('title', '')
        username = request_data.get('username', '')
        create_start = request_data.get('create_start', '')
        create_end = request_data.get('create_end', '')
        workflow_ids = request_data.get('workflow_ids', '')
        reverse = int(request_data.get('reverse', 1))
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))
        # 待办,关联的,创建
        category = request_data.get('category')

        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status,state_result = ins.getdata(parameters=dict(category='all'),method='get',url='/api/v1.0/tickets')
        if status:
            if len(state_result) > 0 and isinstance(state_result,dict) and 'data' in state_result.keys() and 'value' in state_result['data'].keys():
                context['ticket_result_restful_list'] = state_result['data']['value']
        context['msg'] = state_result['msg']
        #print(context)
        return context

#工单流转step: 用于显示工单当前状态的step图  by kf
class TicketFlowStep(LoginRequiredMixin,View):
    """
    工单流转step: 用于显示工单当前状态的step图(线形结构，无交叉)
    """

    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request_data.get(
            'username', request.user.username)  # 可用于权限控制
        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status,state_result = ins.getdata(parameters={},method='get',url='/api/v1.0/tickets/{0}/flowsteps'.format(self.kwargs.get('ticket_id')))
        return JsonResponse(data=state_result)

# 工单流转时，可以做的操作   by kf
class TicketTransition(LoginRequiredMixin,View):
    """
    工单可以做的操作
    """

    def get(self, request, *args, **kwargs):
        pass

#工单流转的记录日志    by kf
class TicketFlowlog(LoginRequiredMixin,View):
    """
    工单流转记录
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request_data.get(
            'username', request.user.username)  # 可用于权限控制
        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))

        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status,state_result = ins.getdata(parameters={},method='get',url='/api/v1.0/tickets/{0}/flowlogs'.format(self.kwargs.get('ticket_id')))
        return JsonResponse(data=state_result)

class SaveTempFlow(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request_data.get(
            'username', request.user.username)  # 可用于权限控制

        #总恒阻锚索/米
        j_shigongjindu_float_zonghengzumaosuo =  request_data.get('j_shigongjindu_float_zonghengzumaosuo')

        #总切缝钻孔/米
        j_shigongjindu_float_zongqiefengzhuankong = request_data.get('j_shigongjindu_float_zongqiefengzhuankong')

        # 总爆破裂缝/米
        j_shigongjindu_float_zongbaopoliefeng = request_data.get('j_shigongjindu_float_zongbaopoliefeng')

        #当前已完成恒阻锚索/米
        j_shigongjindu_float_muqianhengzumaosuo = request_data.get('j_shigongjindu_float_muqianhengzumaosuo')

        #当前已完成切缝钻孔/米
        j_shigongjindu_float_muqianqiefengzhuankong =  request_data.get('j_shigongjindu_float_muqianqiefengzhuankong')

        #当前已完成爆破裂缝/米
        j_shigongjindu_float_muqianbaopoliefeng = request_data.get('j_shigongjindu_float_muqianbaopoliefeng')

        state_result = dict()
        insertData = dict()
        temWork = TempWork()
        find_is_null = False
        try :
            temWork = TempWork.objects.get(ticket_id = ticket_id)

            recode =  eval(temWork.process_recod)


            insertData['j_shigongjindu_float_muqianhengzumaosuo'] = j_shigongjindu_float_muqianhengzumaosuo
            insertData['j_shigongjindu_float_muqianqiefengzhuankong'] = j_shigongjindu_float_muqianqiefengzhuankong
            insertData['j_shigongjindu_float_muqianbaopoliefeng'] =j_shigongjindu_float_muqianbaopoliefeng
            # insertData['j_shigongjindu_float_muqianhengzumaosuo'] = str(
            #     int(recode["j_shigongjindu_float_muqianhengzumaosuo"]) + int(j_shigongjindu_float_muqianhengzumaosuo))
            # insertData['j_shigongjindu_float_muqianqiefengzhuankong'] = str(
            #     int(recode["j_shigongjindu_float_muqianqiefengzhuankong"]) + int(
            #         j_shigongjindu_float_muqianqiefengzhuankong))
            # insertData['j_shigongjindu_float_muqianbaopoliefeng'] = str(
            #     int(recode["j_shigongjindu_float_muqianbaopoliefeng"]) + int(j_shigongjindu_float_muqianbaopoliefeng))

            find_is_null = True
        except TempWork.DoesNotExist:
            pass

        insertData['j_shigongjindu_float_zonghengzumaosuo'] = j_shigongjindu_float_zonghengzumaosuo
        insertData['j_shigongjindu_float_zongqiefengzhuankong'] = j_shigongjindu_float_zongqiefengzhuankong
        insertData['j_shigongjindu_float_zongbaopoliefeng'] = j_shigongjindu_float_zongbaopoliefeng

        if not find_is_null:
            insertData['j_shigongjindu_float_muqianhengzumaosuo'] = j_shigongjindu_float_muqianhengzumaosuo
            insertData['j_shigongjindu_float_muqianqiefengzhuankong'] = j_shigongjindu_float_muqianqiefengzhuankong
            insertData['j_shigongjindu_float_muqianbaopoliefeng'] = j_shigongjindu_float_muqianbaopoliefeng

        temWork.ticket_id = ticket_id
        temWork.process_recod =str (insertData)
        temWork.save()

        return JsonResponse(data=state_result)


class TicketFlowBack(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')
        username = request_data.get(
            'username', request.user.username)  # 可用于权限控制
        suggestion = request_data.get('suggestion')
        transitionid = request_data.get('transitionid')
        #
        form_data = dict()
        form_data['suggestion'] = suggestion
        form_data['transition_id'] = int(transitionid)
        ins = WorkFlowAPiRequest(username=self.request.user.username)
        status, state_result = ins.getdata(data=form_data, method='patch',
                                           url='/api/v1.0/tickets/{0}'.format(ticket_id))
        return JsonResponse(data=state_result)


# 获取此时登录网页的用户名    by kf
class GetUserName(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        try:
            data = User.objects.all(id=user_id).username
        except:
            data = None
        return JsonResponse(data={'username':data})

    # 获取此时登录网页的用户名    by kf
class downloadFile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        path = request.GET.get('path')

        file = open(path,'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="'+path.split("/")[len(path.split("/"))-1]+'"'
        return response



#查找历史保存数据    by gu
class FlowDataFlap(LoginRequiredMixin,View):
    """
    工单流转记录
    """
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        ticket_id = kwargs.get('ticket_id')

        datadic = dict
        try :
            datadic = eval(TempWork.objects.get(ticket_id=ticket_id).process_recod)
        except:
            pass

        return JsonResponse(data=datadic)


##数据库查询数据，没有数据什么都不显示
class TickeFlowDetail(LoginRequiredMixin, FormView):
    template_name = 'workflow/tickeflowdetail.html'
    success_url = "/"
    def get_form_class(self):
        form_fields = dict()

        class DynamicForm(forms.Form):
            def __init__(self, *args, **kwargs):
                self.helper = FormHelper()
                super(DynamicForm, self).__init__(*args, **kwargs)
        return type('DynamicItemsForm', (DynamicForm,), form_fields)
    def get_context_data(self, **kwargs):
        context = super(TickeFlowDetail, self).get_context_data(**kwargs)
        context['ticket_id'] = self.kwargs.get('ticket_id')
        return context





#在工单详情页面中点击“查看上部工作流操作详情”跳转的页面处理函数
class TicketBeforeFlowStep(LoginRequiredMixin, FormView):
    template_name = 'workflow/ticketbeforeflowsteps.html'
    success_url = "/"

    def get_form_class(self):
        form_fields = dict()
        ticket_id = self.kwargs.get('ticket_id')

        ins = WorkFlowAPiRequest(username=self.request.user.username)

        # 获取组建
        status, state_result = ins.getdata(parameters={}, method='get',
                                           url='/api/v1.0/tickets/{0}'.format(ticket_id))

        state_result = state_result['data']['value']

        out_list = list();
        file_out_list = list();

        if isinstance(state_result, dict) and 'field_list' in state_result.keys():
            class DynamicForm(forms.Form):
                def __init__(self, *args, **kwargs):
                    self.helper = FormHelper()
                    self.helper.form_class = 'form-horizontal'
                    self.helper.form_action = " "
                    self.helper.label_class = 'col-md-label'
                    self.helper.field_class = 'col-md-field'
                    # DictionaryField bug
                    self.helper.layout = Layout(
                        *[Div(field['field_key'], css_class='form-table-group') for field in
                          state_result['field_list']])
                    super(DynamicForm, self).__init__(*args, **kwargs)

            for field in state_result['field_list']:

                attributeFlag = field["field_attribute"]
                # 将控件的值提读出来
                field["default_value"] = field["field_value"]
                # 1只读，2必填，3选填
                # 创建时候，只有是必须填写或者选填的才进行渲染
                if attributeFlag == 1:
                    if  field['field_type_id'] == 80:
                        #控件是文件类型，画面中生成<a>标签就可以
                        item = dict()
                        path = field['field_value']
                        if path == None:
                            continue
                        else:
                            mypath = "."
                            index = 0
                            contineFlag = 0
                            for file_path_part in path.split("/"):
                                if (contineFlag == 1 or file_path_part == "media"):
                                    mypath += "/" + file_path_part
                                    contineFlag = 1
                                else:
                                    index += 1
                                    continue
                            file_orgin = path.split("/")[len(path.split("/"))-1]
                            file_name = file_orgin.split("_")[2]
                            item['field_name'] = field["field_name"]
                            item['download_path'] = "/workflow/"+ticket_id+"/download_file?path="+mypath
                            item['link_name'] = file_name
                            file_out_list.append(item)
                            continue
                    out_list.append(field)
                    Util.createWebDirex(field, forms, form_fields, User)
                # handle read only field
                if field['field_attribute'] == 1:
                    form_fields[field['field_key']
                    ].widget.attrs['disabled'] = 'disabled'
        else:
            raise Http404()

        state_result['field_list'] = out_list
        self.kwargs.update({'state_result': state_result})
        #file_out_list
        self.kwargs.update({'file_out_list': file_out_list})
        self.kwargs.update({'title': state_result["title"]})


        return type('DynamicItemsForm', (DynamicForm,), form_fields)

    def get_context_data(self, **kwargs):
        context = super(TicketBeforeFlowStep, self).get_context_data(**kwargs)

        state_result = self.kwargs.get('state_result', None)

        file_out_list = self.kwargs.get('file_out_list', None)

        # 为了组建显示
        context['state_result'] = state_result

        if len(file_out_list) != 0 :
            context['file_out_list_flag'] = "true"

        # 文件
        context['file_out_list'] = file_out_list

        # 查找日志
        context['ticket_id'] = self.kwargs.get('ticket_id')


        # title 文件存储的路径
        context['title'] = self.kwargs.get('title')

        return context


