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

  window.AutocompleteMultipleSearch = {

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

      // set up some actions
      var focusInput = function() {
          // bootstrap event modal.on('shown.bs.modal') is not triggered 
          // (because of way the modal in created??)
          console.log(this);
          $(this).attr('value', '');
          $(this).focus();
      }.bind(input);

      // a button to trigger the autocomplete search
      var add_button = $('#add_' + field_name);

      // add button triggers autocomplete modal
      $(add_button).click(function() {
        $(modal).modal('show');
        // focus input field - see above, bootstrap event missing
        setTimeout(focusInput, 200);
        event.preventDefault();
        return false;
      });

      // a button to remove elements from selected field
      var remove_button = $('#remove_' + field_name);

      // remove button removes items from the select input
      $(remove_button).click(
        function(event) {
          $('select#' + field_id).find('option').each(
            function(idx, opt){
              if (opt.selected) {
                $(opt).remove();
              }
            }
          )
        event.preventDefault();
        return false;
      });

      // hide help block and spinner
      $(spinner).hide();

      // the select field that is targeted.
      var select = $('#' + field_id)
      // add action on each item when selected
      $(select).change(
        function() {
          $('#remove_' + field_name).removeClass('disabled');
        }
      )

      // add form submit action which marks all items in select box as selected
      if (field_id.indexOf('__prefix__') != -1) {
        var form = $(add_button).closest('form');
        form.submit(
          function(event) {
            $(this).find('select#' + field_id).find('option').each(
              function(idx, opt){
                $(opt).attr('selected', 'selected');
              }
            )
          }
        )
      }

      // create actual autocomplete plugin object
      $(input).autocomplete({
        source: '/api/filter/' + short_name + '/',
        minLength: 1,
        delay: 300,
        appendTo: items,
        select: function(event, ui) {
          if (ui.item) {
            var existing = $(select).find('option[value=' + ui.item.id + ']')
            if (!existing.length) {
              var option = quickElement('option', select.get(0), ui.item.label,
                               'value', ui.item.id);
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
