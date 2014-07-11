# -*- coding: utf-8 -*-
from itertools import chain

from django import forms
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils import formats
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict, MergeDict
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
    <form class="navbar-form navbar-right" role="search" id="changelist-search" action="" method="get">
      <div class="form-group">
        <input type="text" class="form-control search-query" placeholder="{% trans 'Search' %}" size="40"
               name="{{ search_var }}" value="{{ cl.query }}" id="searchbar" />
      </div>
    </form>

    """
    class Media:
        js = (
            settings.STATIC_URL + 'js/autocomplete_base.js',
            settings.STATIC_URL + 'js/autocomplete_search.js',
            )
        css = {
            'screen': (settings.STATIC_URL + 'css/autocomplete.css', )
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
        final_attrs['size'] = '40'

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

        >>> print(dir(autocomplete))

    Renders with input field and bootstrap modal

        >>> from django.forms import ModelChoiceField
        >>> queryset = TestModel.fkm.field.model.objects.all()
        >>> field = ModelChoiceField(queryset=queryset,
        ...     widget=AutocompleteSelectWidget)
        >>> result = field.widget.render('fkm', None, attrs=dict(id='id_fkm'))
        >>> for line in result.split('\\n'):
        ...     print(line)
        <input id="fkm_select" type="hidden" name="fkm_select" value="">
        <input class="autocomplete-select form-control" id="id_fkm" name="fkm"\
               placeholder="Search test models ..." style="display:inline-block" type="text" />
        <script type="text/javascript">
          (function($) {
            if (window.AutocompleteSelect != undefined) {
              new AutocompleteSelect("id_fkm", "fkm", "test models").init();
            }
          }(jQuery));
        </script>

    """
    allow_multiple_selected = False
    input_type = 'text'

    class Media:
        js = (
            settings.STATIC_URL + 'js/autocomplete_base.js',
            settings.STATIC_URL + 'js/autocomplete_select.js',
            )
        css = {
            'screen': (settings.STATIC_URL + 'css/autocomplete.css', )
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
        <select multiple="multiple" class="autocomplete-multipleselect form-control" id="id_fkm" name="fkm">
        </select>
          <script type="text/javascript">
          (function($) {
          if (window.AutocompleteMultipleSelect != undefined) {
          new AutocompleteMultipleSelect("id_fkm", "fkm", "test models").init();
          }
          }(jQuery));
        </script>

    """
    allow_multiple_selected = True

    class Media:
        js = (
            settings.STATIC_URL + 'js/autocomplete_base.js',
            settings.STATIC_URL + 'js/autocomplete_multipleselect.js',
            )
        css = {
            'screen': (settings.STATIC_URL + 'css/autocomplete.css', )
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

