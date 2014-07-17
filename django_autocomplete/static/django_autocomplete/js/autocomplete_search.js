// autocomplete search for admin
(function($) {

  window.AutocompleteSearch = function(source, field_id, field_name, field_title) {
    // in getting inheritance to work I didn't manage to proto the constructor
    // TODO maybe some kind of `super` method?
    this.source = source;
    this.field_id = field_id;
    this.field_name = field_name;
    this.field_title = field_title;
  }
  AutocompleteSearch.prototype = new AutocompleteBase();
  AutocompleteSearch.prototype.constructor = AutocompleteSearch;

  AutocompleteSearch.prototype.init = function() {

    this.initBase();

    // the search field
    this.search_input = $('#' + this.field_id);

    // set trigger for modal on the search
    this.setTrigger(this.search_input, 'focus');

    // nice would be to find the form
    this.search_form = $('form#autocomplete-search');

    // create the autocomplete
    this.initAutocomplete()

    // bind the select method
    this.bindAutocomplete()
  }

  AutocompleteSearch.prototype.bindAutocomplete = function() {

    // and add the action on select of item
    $(this.input).bind( "autocompleteselect",
      {obj: this},
      function(event, ui) {
        var obj = event.data.obj;
        if (ui.item) {
          // do something
          $(obj.search_input).attr('value', ui.item.label )
          var location = document.location.origin + document.location.pathname;
          var url = location + ui.item.id + '/';
          window.document.location = url;
          $(obj.modal).modal('hide');
        } else {
          alert("Nothing selected, input was " + this.value );
        }
        event.preventDefault();
        return false;
      })
    }

}(jQuery));

