(function($) {

  if (typeof window.quickElement == 'undefined') {
    // quickElement(tagType, parentReference [, textInChildNode, attribute, attributeValue ...]);
    function quickElement() {
        var obj = document.createElement(arguments[0]);
        if (arguments[2]) {
            var textNode = document.createTextNode(arguments[2]);
            obj.appendChild(textNode);
        }
        var len = arguments.length;
        for (var i = 3; i < len; i += 2) {
            obj.setAttribute(arguments[i], arguments[i+1]);
        }
        arguments[1].appendChild(obj);
        return obj;
    }
  }

  window.AutocompleteSearch = {

    init: function(field_id, field_name, field_title) {

      if (field_id.match(/__prefix__/)){
        // Don't intialize on empty forms.
        return;
      }

      // detect and pick an inline form
      var short_name = '';
      var poss = field_name.lastIndexOf('-');
      if (poss > 1) {
        short_name = field_name.substring(poss + 1, field_name.length);
        var inline_id = field_id.substring(0, poss + 4) + 'id';
      } else {
        short_name = field_name;
      }

      // insert modal at in the dom
      d = $('div#content').get(0);

      // build the modal into the dom
      var modal = quickElement('div', document.body, false,
           'id', field_name + '_modal',
           'class', 'modal fade',
           'style', 'width:560px;margin: 20px auto 0 auto;',
           'tabindex', '-1',
           'role', 'dialog',
           'aria-hidden', 'true');
      var modal_content = quickElement('div', modal, false,
           'class', 'modal-content');
      var modal_header = quickElement('div', modal_content, false,
           'class', 'modal-header');
      var button = quickElement('button', modal_header, false,
           'class', 'close',
           'data-dismiss', 'modal');
      var hide = quickElement('span', button, 'x',
           'aria-hidden', 'true');
      var header = quickElement('h3', modal_header, 'Search in: ' + field_title,
           'class', 'text-center');
      var header_title = quickElement('span', header, '',
           'id', field_name + '_title');
      var modal_body = quickElement('div', modal_content, false,
           'class', 'modal-body');
      var modal_body_group = quickElement('div', modal_body, false,
           'class', 'form-group has-feedback');
      var label = quickElement('label', modal_body_group, 'Search',
           'class', 'hidden sr-only',
           'for', field_name + '_autocomplete');
      var input = quickElement('input', modal_body_group, false,
           'class', 'form-control',
           'id', field_name + '_autocomplete',
           'type', 'text',
           'placeholder', 'Start typing ...');
      var spinner = quickElement('span', modal_body_group, false,
           'class', 'group-addon',
           'id', field_name + '_spinner');
      var spinner_obj = quickElement('i', spinner, false,
           'class', 'glyphicon glyphicon-refresh spin form-control-feedback');
      var items = quickElement('div', modal_body, false,
           'id', field_name + '_items',
           'class', 'filter-items');

      // input fields:

      // displays name of fk value, shows modal on focus
      var key_input = $('#' + field_id);

      // actual pk field for model forms
      var pk_input = $('#' + field_name + '_select');

      // detect the hidden id field of a many to many field
      if (inline_id) {
        inline_input = $('#' + inline_id);
      }

      // set up some actions

      var focusInput = function() {
          // bootstrap event modal.on('shown.bs.modal') is not triggered 
          // (because of way the modal in created??)
          $(this).focus();
      }.bind(input);

      $(spinner).hide();

      $(key_input).focus(function() {
        $(modal).modal('show');
        // focus input field - see above, bootstrap event missing
        setTimeout(focusInput, 200);
      });

      // create actual autocomplete plugin object
      $(input).autocomplete({
        source: '/api/filter/' + short_name + '/',
        minLength: 1,
        delay: 300,
        appendTo: items,
        select: function(event, ui) {
          if (ui.item) {
            $(pk_input).attr('value', ui.item.id);
            $(key_input).attr('value', ui.item.label);
            var form = $(key_input).parents('fieldset').get(0);
            var inputs = $(form).find(':input:visible:not(.offscreen)');
            var idx = inputs.index(key_input);
            var inp = inputs.get(idx+1);
            if (typeof inp != 'undefined') {
               inp.focus();
            }
            $(modal).modal('hide');
          } else {
            alert("Nothing selected, input was " + this.value );
          }
          event.preventDefault();
          return false;
        },
        search: function(event, ui) {
          $(spinner).show();
        },
        response: function(event, ui) {
          $(spinner).hide();
          if (!ui.item) {
            $('#filter-items').html('No results found.');
          }
        },
        change: function(event, ui) {
          $(modal).modal('hide');
          event.preventDefault();
          return false;
        }
      });
    },
  }
}(jQuery));
