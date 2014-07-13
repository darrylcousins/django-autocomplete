(function($) {

  window.AutocompleteSelect = function(source, field_id, field_name, field_title) {
    // in getting inheritance to work I didn't manage to proto the constructor
    // TODO maybe some kind of `super` method?
    this.source = source;
    this.field_id = field_id;
    this.field_name = field_name;
    this.field_title = field_title;
  }
  AutocompleteSelect.prototype = new AutocompleteBase();
  AutocompleteSelect.prototype.constructor = AutocompleteSelect;

  AutocompleteSelect.prototype.init = function() {

    if (this.field_id.match(/__prefix__/)){
      // Don't intialize on empty forms.
      return;
    }

    this.initBase();

    // displays name of fk value, shows modal on focus
    this.key_input = $('#' + this.field_id);
    // actual pk field for model forms
    this.pk_input = $('#' + this.field_name + '_select');

    // set trigger for modal
    this.setTrigger(this.key_input, 'focus');

    // create the autocomplete
    this.initAutocomplete()

    // bind the select method
    this.bindAutocomplete()
  }

  AutocompleteSelect.prototype.bindAutocomplete = function() {

    // and add the action on select of item
    $(this.input).bind( "autocompleteselect",
      {obj: this},
      function(event, ui) {
        var obj = event.data.obj;
        if (ui.item) {
          $(obj.pk_input).attr('value', ui.item.id);
          $(obj.key_input).attr('value', ui.item.label);
          var form = $(obj.key_input).parents('fieldset').get(0);
          var inputs = $(form).find(':input:visible:not(.offscreen)');
          var idx = inputs.index(obj.key_input);
          var inp = inputs.get(idx+1);
          if (typeof inp != 'undefined') {
             inp.focus();
          }
          $(obj.modal).modal('hide');
        } else {
          alert("Nothing selected, input was " + this.value );
        }
        event.preventDefault();
        return false;
      })
    }

}(jQuery));
