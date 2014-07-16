(function($) {

  window.AutocompleteCTSelect = function(source, field_id, field_name, field_title) {
    // in getting inheritance to work I didn't manage to proto the constructor
    // TODO maybe some kind of `super` method?
    this.source = source;
    this.field_id = field_id;
    this.field_name = field_name;
    this.field_title = field_title;
  }
  AutocompleteCTSelect.prototype = new AutocompleteBase();
  AutocompleteCTSelect.prototype.constructor = AutocompleteCTSelect;

  AutocompleteCTSelect.prototype.init = function() {

    if (this.field_id.match(/__prefix__/)){
      // Don't intialize on empty forms.
      return;
    }

    // we want a change in the select to create a new autocomplete on the object_id field
    this.initBase();

    // actual pk field for model forms, shows modal on focus
    this.pk_input = $('#' + this.field_id);

    // displays name of fk value, shows modal on focus
    this.info = $('#' + this.field_name + '_info');

    // set trigger for modal
    this.setTrigger(this.pk_input, 'focus');

    // create the autocomplete
    this.initAutocomplete()

    // bind the select method
    this.bindAutocomplete()
  }

  AutocompleteCTSelect.prototype.bindAutocomplete = function() {

    // and add the action on select of item
    $(this.input).bind( "autocompleteselect",
      {obj: this},
      function(event, ui) {
        var obj = event.data.obj;
        if (ui.item) {
          $(obj.pk_input).attr('value', ui.item.id);
          $(obj.info).html(ui.item.label);
          $(obj.modal).modal('hide');
        } else {
          alert("Nothing selected, input was " + this.value );
        }
        event.preventDefault();
        return false;
      })
    }

}(jQuery));

