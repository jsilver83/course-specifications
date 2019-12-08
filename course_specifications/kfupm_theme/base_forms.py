from crispy_forms.helper import FormHelper


class BaseCrispyForm:

    def __init__(self, *args, **kwargs):
        super(BaseCrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        # self.helper.form_group_wrapper_class = 'form-group row' NOT WORKING
        self.helper.label_class = 'col-xs-3 mr-4'
        self.helper.field_class = 'col-xs-9'


class BaseCrispySearchForm(BaseCrispyForm):

    def __init__(self, *args, **kwargs):
        super(BaseCrispySearchForm, self).__init__(*args, **kwargs)
        self.helper.form_method = 'get'
