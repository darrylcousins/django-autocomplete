(function($) {

  window.AutocompleteMultipleSelect = function(source, field_id, field_name, field_title) {
    // in getting inheritance to work I didn't manage to proto the constructor
    // TODO maybe some kind of `super` method?
    this.source = source;
    this.field_id = field_id;
    this.field_name = field_name;
    this.field_title = field_title;
  }
  AutocompleteMultipleSelect.prototype = new AutocompleteBase();
  AutocompleteMultipleSelect.prototype.constructor = AutocompleteMultipleSelect;

  AutocompleteMultipleSelect.prototype.init = function() {

    if (this.field_id.match(/__prefix__/)){
      // Don't intialize on empty forms.
      return;
    }

    this.initBase();

    // a button to trigger the autocomplete search
    this.add_button = $('#add_' + this.field_name);
    this.setTrigger(this.add_button, 'click');
    //
    // the select field that is targeted.
    this.select_field = $('select#' + this.field_id)

    // a button to remove elements from selected field
    this.remove_button = $('#remove_' + this.field_name);
    $(this.remove_button).click(
      {obj: this},
      function(event) {
        var obj = event.data.obj;
        obj.select_field.find('option').each(
          function(idx, opt){
            if (opt.selected) {
              $(opt).remove();
            }
          }
        )
        obj.remove_button.removeClass('btn-primary');
        obj.remove_button.addClass('disabled');
      event.preventDefault();
      return false;
    });

    // add action on each item when selected
    $(this.select_field).change(
      {obj: this},
      function(event) {
        var obj = event.data.obj;
        obj.remove_button.removeClass('disabled');
        obj.remove_button.addClass('btn-primary');
      }
    )

    // add form submit action which marks all items in select box as selected
    if (this.field_id.indexOf('__prefix__') == -1) {
      var form = $(this.add_button).closest('form');
      form.submit(
        {obj: this},
        function(event) {
          var obj = event.data.obj;
          obj.select_field.find('option').each(
            function(idx, opt){
              $(opt).attr('selected', 'selected');
            }
          )
        }
      )
    }

    // create the autocomplete
    this.initAutocomplete()

    // bind the select method
    this.bindAutocomplete()
  }

  AutocompleteMultipleSelect.prototype.bindAutocomplete = function() {

    $(this.input).bind( "autocompleteselect",
      {obj: this},
      function(event, ui) {
        var obj = event.data.obj;
        if (ui.item) {
          var existing = $(obj.select_field).find('option[value=' + ui.item.id + ']')
          if (!existing.length) {
            var option = quickElement('option', obj.select_field.get(0), ui.item.label,
                             'value', ui.item.id);
          }
          $(obj.modal).modal('hide');
        } else {
          alert("Nothing selected, input was " + this.value );
        }
        event.preventDefault();
        return false;
    });
  }
}(jQuery));
