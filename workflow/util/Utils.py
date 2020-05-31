from ckeditor_uploader.widgets import CKEditorUploadingWidget
import os



class Util (object):
    # FIELD_TYPE_STR = 5  # 字符串类型
    # FIELD_TYPE_INT = 10  # 整形类型
    # FIELD_TYPE_FLOAT = 15  # 浮点类型
    # FIELD_TYPE_BOOL = 20  # 布尔类型
    # FIELD_TYPE_DATE = 25  # 日期类型
    # FIELD_TYPE_DATETIME = 30  # 日期时间类型
    # FIELD_TYPE_RADIO = 35  # 单选框
    # FIELD_TYPE_CHECKBOX = 40  # 多选框
    # FIELD_TYPE_SELECT = 45  # 下拉列表
    # FIELD_TYPE_MULTI_SELECT = 50  # 多选下拉列表
    # FIELD_TYPE_TEXT = 55  # 文本域
    # FIELD_TYPE_USERNAME = 60  # 用户名，前端展现时需要调用方系统获取用户列表。loonflow只保存用户名
    # FIELD_TYPE_MULTI_USERNAME = 70  # 多选用户名,多人情况逗号隔开，前端展现时需要调用方系统获取用户列表。loonflow只保存用户名  by  kf
    # FIELD_TYPE_ATTACHMENT = 80  # 附件，多个附件使用逗号隔开。调用方自己实现上传功能，loonflow只保存文件路径   by  kf
    @classmethod
    def createWebDirex(self,field,forms,form_fields,User):
        if field['field_type_id'] == 5:
            form_fields[field['field_key']] = forms.CharField(help_text=field['description'],
                                                              label=field['field_name'],
                                                              required=True if field[
                                                                                   'field_attribute'] == 2 else False,
                                                              initial=field['default_value'],
                                                              error_messages={
                                                                  'required': field['description']},
                                                              widget=forms.TextInput(
                                                                  attrs={'placeholder': field['field_name']}))
        elif field['field_type_id'] in [10, 15]:
            form_fields[field['field_key']] = forms.IntegerField(help_text=field['description'],
                                                                 label=field['field_name'],
                                                                 required=True if field[
                                                                                      'field_attribute'] == 2 else False,
                                                                 initial=field['default_value'],
                                                                 error_messages={
                                                                     'required': field['description']},
                                                                 widget=forms.NumberInput(attrs={
                                                                     'placeholder': field['field_name']}))
        elif field['field_type_id'] == 20:
            form_fields[field['field_key']] = forms.BooleanField(help_text=field['description'],
                                                                 label=field['field_name'],
                                                                 required=True if field[
                                                                                      'field_attribute'] == 2 else False,
                                                                 initial=field['default_value'],
                                                                 error_messages={
                                                                     'required': field['description']})
        elif field['field_type_id'] == 25:
            form_fields[field['field_key']] = forms.DateField(help_text=field['description'],
                                                              label=field['field_name'],
                                                              required=True if field[
                                                                                   'field_attribute'] == 2 else False,
                                                              initial=field['default_value'],
                                                              error_messages={
                                                                  'required': field['description']},
                                                              widget=forms.DateInput(
                                                                  attrs={'placeholder': field['field_name'],
                                                                         'class': 'dateinput'}))
        elif field['field_type_id'] == 30:
            form_fields[field['field_key']] = forms.DateTimeField(help_text=field['description'],
                                                                  label=field['field_name'],
                                                                  required=True if field[
                                                                                       'field_attribute'] == 2 else False,
                                                                  initial=field['default_value'],
                                                                  error_messages={
                                                                      'required': field['description']},
                                                                  widget=forms.DateTimeInput(
                                                                      attrs={'placeholder': field['field_name'],
                                                                             'class': 'datetimeinput'}))
        elif field['field_type_id'] in [35, 45]:
            form_fields[field['field_key']] = forms.ChoiceField(help_text=field['description'],
                                                                label=field['field_name'],
                                                                required=True if field[
                                                                                     'field_attribute'] == 2 else False,
                                                                initial=field['default_value'],
                                                                error_messages={
                                                                    'required': field['description']},
                                                                choices=[(k, v) for k, v in
                                                                         field['field_choice'].items()])
        elif field['field_type_id'] in [40, 50]:
            form_fields[field['field_key']] = forms.MultipleChoiceField(help_text=field['description'],
                                                                        label=field['field_name'],
                                                                        required=True if field[
                                                                                             'field_attribute'] == 2 else False,
                                                                        initial=field['default_value'],
                                                                        error_messages={
                                                                            'required': field['description']},
                                                                        choices=[(k, v) for k, v in
                                                                                 field['field_choice'].items()])
        elif field['field_type_id'] == 55:
            form_fields[field['field_key']] = forms.CharField(help_text=field['description'],
                                                              label=field['field_name'],
                                                              required=True if field[
                                                                                   'field_attribute'] == 2 else False,
                                                              initial=field['default_value'],
                                                              error_messages={
                                                                  'required': field['description']},
                                                               widget=forms.Textarea(
                                                                   attrs={'placeholder': field['field_name'],
                                                                          'cols': 20, 'rows': 10})
                                                              )
        elif field['field_type_id'] == 60:
            form_fields[field['field_key']] = forms.ChoiceField(help_text=field['description'],
                                                                label=field['field_name'],
                                                                required=True if field[
                                                                                     'field_attribute'] == 2 else False,
                                                                initial=field['default_value'],
                                                                error_messages={
                                                                    'required': field['description']},
                                                                choices=[(i.username, i.username) for i in
                                                                         User.objects.all()])
        elif field['field_type_id'] == 80:
            form_fields[field['field_key']] = forms.FileField(help_text=field['description'],
                                                              label=field['field_name'],
                                                              required=True if field[
                                                                                   'field_attribute'] == 2 else False,
                                                              initial=field['default_value'],
                                                              error_messages={
                                                                  'required': field['description']},
                                                              widget=forms.ClearableFileInput(
                                                                  attrs={'multiple': True,'placeholder': field['field_name']}))


    @classmethod
    def saveFile(self,datab, path):
        '''
        以文件形式保存数据
        :param html: 要保存的数据
        :param path: 要保存数据的路径
        :return:

        '''
        # 判断目录是否存在
        file_path = os.path.abspath(os.curdir)+'/media/'+path
        if not os.path.exists(os.path.split(file_path)[0]):
            # 目录不存在创建，makedirs可以创建多级目录
            os.makedirs(os.path.split(file_path)[0])
        try:
            # 保存数据到文件
            with open(file_path, 'wb') as f:
                data = datab.read()
                f.write(data)
            print('保存成功')
        except Exception as e:
            print('保存失败', e)
