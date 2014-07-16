# -*- coding: utf-8 -*-
from itertools import chain

from django import forms
from django.conf import settings
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils import formats
from django.utils.html import format_html
from django.utils.translation import ugettext as _


class SmallTextareaWidget(forms.Textarea):
    """
    Use a smaller text area in the admin views.

        >>> textarea = SmallTextareaWidget()
        >>> textarea
        <django_autocomplete.widgets.SmallTextareaWidget object at ...>

    Renders with cols=20 and rows=4::

        >>> textarea.render('name', 'value')
        '<textarea class="vTextField" cols="20"...rows="4">...value</textarea>'

    """
    def __init__(self, attrs=None):
        final_attrs = {'class': 'vTextField', 'cols': '20', 'rows': '4'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(SmallTextareaWidget, self).__init__(attrs=final_attrs)


class SearchInput(forms.TextInput):
    """
    The SearchInput widget::

        >>> autocomplete = AutocompleteSelectWidget()
        >>> autocomplete
        <django_autocomplete.widgets.AutocompleteSelectWidget object at ...>

    Renders with input field and javascipt initialization::

        >>> from django.forms import CharField
        >>> field = forms.CharField(widget=SearchInput(model=TestModel))
        >>> result = field.widget.render('q', None, attrs=dict(id='id_q'))
        >>> for line in result.split('\\n'):
        ...     print(line)
        <input ... id="id_q" name="q" placeholder="Search Test models ..." size="40" type="text" />
        <script type="text/javascript">
          (function($) {
            if (typeof AutocompleteSearch != "undefined") {
              new AutocompleteSearch("api/filter/silly", "id_q", "q", "Test models").init();
            }
          }(jQuery));
        </script>

    """
    class Media:
        js = (
            settings.STATIC_URL + 'django_autocomplete/js/autocomplete_base.js',
            settings.STATIC_URL + 'django_autocomplete/js/autocomplete_search.js',
            )
        css = {
            'screen': (settings.STATIC_URL + 'django_autocomplete/css/autocomplete.css', )
            }

    def __init__(self, attrs=None, model=None):
        super(SearchInput, self).__init__(attrs)
        self.model = model

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        title = self.model._meta.verbose_name_plural.capitalize()
        final_attrs['placeholder'] = str(_('Search ')) + title + ' ...'
        final_attrs['class'] = 'form-control search-query'
        final_attrs['size'] = '55'

        output = []

        output.append(format_html('<input{0} />', flatatt(final_attrs)))

        output.append('<script type="text/javascript">')
        output.append('(function($) {')
        output.append('if (typeof AutocompleteSearch != "undefined") {')
        output.append('new AutocompleteSearch("%(source)s", "%(id_)s", "%(name)s", "%(title)s").init();' % dict(
            source=self.model.autocomplete.path,
            name=final_attrs['name'],
            title=title,
            id_=final_attrs['id']))
        output.append('}')
        output.append('}(jQuery));')
        output.append('</script>')

        return mark_safe('\n'.join(output))


class AutocompleteSelectWidget(forms.Select):
    """
    A autocomplete select widget to replace dropdown foreign key select widget
    for admin screens.

        >>> autocomplete = AutocompleteSelectWidget()
        >>> autocomplete
        <django_autocomplete.widgets.AutocompleteSelectWidget object at ...>

    Renders with input field and bootstrap modal

        >>> from django.forms import ModelChoiceField
        >>> queryset = TestModel.fkm.field.model.objects.all()
        >>> field = ModelChoiceField(queryset=queryset,
        ...     widget=AutocompleteSelectWidget)
        >>> result = field.widget.render('fkm', None, attrs=dict(id='id_fkm'))
        >>> for line in result.split('\\n'):
        ...     print(line)
        <input id="fkm_select" type="hidden" name="fkm_select" value="">
        <input ... data-source="api/filter/silly" id="id_fkm" name="fkm" ... type="text" />
        <script type="text/javascript">
          (function($) {
            if (typeof AutocompleteSelect != "undefined") {
              new AutocompleteSelect("api/filter/silly", "id_fkm", "fkm", "test models").init();
            }
          }(jQuery));
        </script>

    """
    allow_multiple_selected = False
    input_type = 'text'

    class Media:
        js = (
            settings.STATIC_URL + 'django_autocomplete/js/autocomplete_base.js',
            settings.STATIC_URL + 'django_autocomplete/js/autocomplete_select.js',
            settings.STATIC_URL + 'admin/js/RelatedObjectLookupsNG.js',
            )
        css = {
            'screen': (settings.STATIC_URL + 'django_autocomplete/css/autocomplete.css', )
            }

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of it paired hidden field.
        """
        name = '%(name)s_select' % dict(name=name)
        return data.get(name, None)

    def render(self, name, value, attrs={}, choices=()):
        """
        Renders two input fields along with a modal and javascript.

        The hidden input holds the pk value of the fk and will be collected on
        submission of form.
        """
        model = self.choices.field.queryset.model
        title = model._meta.verbose_name_plural
        if value is None:
            value = ''
            str_value = ''
        else:
            str_value = str(model.objects.get(pk=value))
            str_value = force_text(self._format_value(str_value))
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs['data-relation'] = name
        final_attrs['title'] = title
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(str_value))
        final_attrs['class'] = 'autocomplete-select form-control'
        final_attrs['style'] = 'display:inline-block'
        final_attrs['data-source'] = model.autocomplete.path
        final_attrs['placeholder'] = str(_('Search ')) + str(title) + ' ...'
        final_attrs['id'] = 'id_%s' % final_attrs['name']
        output = []
        output.append(
            '<input id="%(name)s_select" type="hidden" name="%(name)s_select" value="%(value)s">' % dict(
                name=name, value=value))

        output.append(format_html('<input{0} />', flatatt(final_attrs)))
        # only init if not a inline template form
        if '__prefix__' not in name:
            output.append('<script type="text/javascript">')
            output.append('(function($) {')
            output.append('if (typeof AutocompleteSelect != "undefined") {')
            output.append('new AutocompleteSelect("%(source)s", "%(id_)s", "%(name)s", "%(title)s").init();' % dict(
                source=model.autocomplete.path,
                name=name,
                title=title,
                id_=final_attrs['id']))
            output.append('}')
            output.append('}(jQuery));')
            output.append('</script>')

        return mark_safe('\n'.join(output))


class AutocompleteSelectMultipleWidget(forms.SelectMultiple):
    """
    A autocomplete select widget to replace dropdown foreign key select widget
    for admin screens.

        >>> autocomplete = AutocompleteSelectMultipleWidget()
        >>> autocomplete
        <django_autocomplete.widgets.AutocompleteSelectMultipleWidget object at ...>

    Renders with input field and javascript

        >>> from django.forms import ModelChoiceField
        >>> queryset = TestModel.fkm.field.model.objects.all()
        >>> field = ModelChoiceField(queryset=queryset,
        ...     widget=AutocompleteSelectMultipleWidget)
        >>> result = field.widget.render('fkm', None,
        ...   attrs=dict(id='id_fkm', title='M2m'))
        >>> for line in result.split('\\n'):
        ...     print(line)
        <div class="btn-group">
            <button class="btn btn-default" role="button" id="add_fkm">
            Add test model</button>
            <button class="btn btn-default disabled" role="button" id="remove_fkm">
            Remove selected</button>
        </div>
        <div class="control-group">&nbsp;</div>
        <select multiple="multiple" ... data-source="api/filter/silly" id="id_fkm" name="fkm">
        </select>
        <script type="text/javascript">
          (function($) {
            if (window.AutocompleteMultipleSelect != undefined) {
              new AutocompleteMultipleSelect("api/filter/silly", "id_fkm", "fkm", "Test models").init();
            }
          }(jQuery));
        </script>

    """
    allow_multiple_selected = True

    class Media:
        js = (
            settings.STATIC_URL + 'django_autocomplete/js/autocomplete_base.js',
            settings.STATIC_URL + 'django_autocomplete/js/autocomplete_multipleselect.js',
            )
        css = {
            'screen': (settings.STATIC_URL + 'django_autocomplete/css/autocomplete.css', )
            }

    def value_from_datadict(self, data, files, name):
        """
        Shouldn't need to override this - make note if you do!!
        """
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            # only list selected choices in select field
            if str(option_value) in selected_choices:
                if isinstance(option_label, (list, tuple)):
                    output.append(format_html('<optgroup label="{0}">', force_text(option_value)))
                    for option in option_label:
                        # not passing selected values to render
                        output.append(self.render_option([], *option))
                    output.append('</optgroup>')
                else:
                    # not passing selected values to render
                    output.append(self.render_option([], option_value, option_label))
        return '\n'.join(output)

    def render(self, name, value, attrs=None, choices=()):
        model = self.choices.field.queryset.model
        verbose_name_plural = model._meta.verbose_name_plural
        verbose_name = model._meta.verbose_name
        if value is None:
            value = []

        output = ['<div class="btn-group">']
        output.append('<button class="btn btn-default" role="button" id="add_%s">' % name)
        output.append('Add %s</button>' % verbose_name)
        output.append('<button class="btn btn-default disabled" role="button" id="remove_%s">' % name)
        output.append('Remove selected</button>')
        output.append('</div>')
        output.append('<div class="control-group">&nbsp;</div>')

        final_attrs = self.build_attrs(attrs, name=name)
        if 'title' in final_attrs:
            del final_attrs['title']
        final_attrs['class'] = 'autocomplete-multipleselect form-control'
        final_attrs['data-source'] = model.autocomplete.path
        final_attrs['id'] = 'id_%s' % final_attrs['name']
        output.append(format_html('<select multiple="multiple"{0}>', flatatt(final_attrs)))
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')

        # only init if not a inline template form
        if '__prefix__' not in name:
            output.append('<script type="text/javascript">')
            output.append('(function($) {')
            output.append('if (window.AutocompleteMultipleSelect != undefined) {')
            output.append(
                'new AutocompleteMultipleSelect("%(source)s", "%(id_)s", "%(name)s", "%(title)s").init();' % dict(
                    source=model.autocomplete.path,
                    name=name,
                    title=verbose_name_plural.capitalize(),
                    id_=final_attrs['id']))
            output.append('}')
            output.append('}(jQuery));')
            output.append('</script>')

        return mark_safe('\n'.join(output))

        return mark_safe(render_to_string('autocomplete/multipleselect.html', {
            'name': name,
            'id': final_attrs['id'],
            'verbose_name': verbose_name,
            'verbose_name_plural': verbose_name_plural,
            'select': mark_safe('\n'.join(output)),
            'init': '__prefix__' not in name,
        }))


class AutocompleteCTWidget(forms.Select):
    """
    A autocomplete select widget to handle generec content types
    for admin screens.

        >>> autocomplete = AutocompleteCTWidget()
        >>> autocomplete
        <django_autocomplete.widgets.AutocompleteCTWidget object at ...>

    Renders with input field and bootstrap modal

        >>> from django.contrib.contenttypes.models import ContentType
        >>> from django.forms import ModelChoiceField
        >>> queryset = ContentType.objects.all()[:2]
        >>> field = ModelChoiceField(queryset=queryset,
        ...     widget=AutocompleteCTWidget)
        >>> result = field.widget.render('fkm', None, attrs=dict(id='id_fkm'))
        >>> for line in result.split('\\n'):
        ...     print(line)
        <select id="id_fkm" name="fkm">
        <option value="" selected="selected">---------</option>
        <option value="...">...</option>
        <option value="...">...</option>
        </select>

    A simple select is shown as for normal select widget. This is because the
    widget cannot use autocomplete unless all the models have an autocomplete
    attribute.

    Again then with queryset restricted to model with autocomplete::

        >>> queryset = ContentType.objects.filter(name='test model')
        >>> field = ModelChoiceField(queryset=queryset,
        ...     widget=AutocompleteCTWidget)
        >>> result = field.widget.render('fkm', None, attrs=dict(id='id_fkm'))
        >>> for line in result.split('\\n'):
        ...     print(line)
        <select id="id_fkm" name="fkm">
          <option value="" selected="selected">---------</option>
          <option value="...">test model</option>
        </select>
        <script type="text/javascript">
          var SourceDict = {};
          SourceDict["..."] = "api/filter/silly";
          (function($) {
            if (window.AutocompleteCTSelect != undefined) {
              $("#id_fkm").change(
                function() {
                  var ctname = $(this).find("option:selected").html();
                  var ctpk = $(this).val();
                  var source = SourceDict[ctpk];
                  $("#object_id_info").html("Searching " + ctname + " ...");
                  new AutocompleteCTSelect(source, "id_object_id", "object_id", ctname).init();
                })
                $(document).ready(function() {
                  $('<span class="text-muted" id="object_id_info"></span>').insertAfter("#id_object_id")
                })
            }
          }(jQuery));
        </script>

    """
    allow_multiple_selected = False
    object_field = 'object_id'

    class Media:
        js = (
            settings.STATIC_URL + 'django_autocomplete/js/autocomplete_base.js',
            settings.STATIC_URL + 'django_autocomplete/js/autocomplete_ct_select.js',
            )
        css = {
            'screen': (settings.STATIC_URL + 'django_autocomplete/css/autocomplete.css', )
            }

    def render(self, name, value, attrs=None):
        result = super(AutocompleteCTWidget, self).render(name, value, attrs)
        ct = None
        verbose_name_plural = ''
        if value:
            ct = ContentType.objects.get(pk=value)
            if not hasattr(ct.model_class(), 'autocomplete'):
                # abandon the widget
                return result
            verbose_name_plural = ct.model_class()._meta.verbose_name_plural.capitalize()
        output = [result]

        output.append('<script type="text/javascript">')
        output.append('var SourceDict = {};')
        for choice in self.choices:
            if choice[0]:
                content_type = ContentType.objects.get(pk=choice[0])
                if not hasattr(content_type.model_class(), 'autocomplete'):
                    # if no autocomplete on any of these models then abandon the widget
                    return result
                path = content_type.model_class().autocomplete.path
                output.append('SourceDict["%(key)s"] = "%(value)s";' % dict(
                    key=choice[0],
                    value=path))
        output.append('(function($) {')
        output.append('if (window.AutocompleteCTSelect != undefined) {')
        output.append('$("#id_%(name)s").change(' % dict(name=name))
        output.append('function() {')
        output.append('var ctname = $(this).find("option:selected").html();')
        output.append('var ctpk = $(this).val();')
        output.append('var source = SourceDict[ctpk];')
        search = _('Searching')
        output.append('$("#%(name)s_info").html("%(search)s " + ctname + " ...");' % dict(
            name=self.object_field,
            search=search))
        output.append(
            'new AutocompleteCTSelect(source, "id_%(name)s", "%(name)s", ctname).init();' % dict(
                name=self.object_field))
        output.append('})')

        output.append('$(document).ready(function() {')
        output.append(
            """$('<span class="text-muted" id="%(name)s_info"></span>').insertAfter("#id_%(name)s")""" % dict(  # nopep8
                name=self.object_field))
        if ct:
            # with a selected value the autocomplete can be initialised
            model = ct.model_class()
            output.append(
                'new AutocompleteCTSelect("%(source)s", "id_%(name)s", "%(name)s", "%(title)s").init();' % dict(
                    source=model.autocomplete.path,
                    name=self.object_field,
                    title=verbose_name_plural))
        output.append('})')

        output.append('}')
        output.append('}(jQuery));')
        output.append('</script>')

        return mark_safe('\n'.join(output))
