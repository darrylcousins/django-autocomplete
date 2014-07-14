Javascript
==========

The module has a base javascript file ``autocomplete_base`` and each widget then extends that in the following files::

    django_autocomplete/static/js/autocomplete_select.js
    django_autocomplete/static/js/autocomplete_multipleselect.js
    django_autocomplete/static/js/autocomplete_search.js

The base describes a javascript object: ``AutocompleteBase``. This can be extended by prototypal inheritance.

Lets say we want to make our own search widget. The html required will have a
button as a trigger and some javascript to initialize the search::

          <input id="find" placeholder="find something">
          <script type="text/javascript">
            (function($) {
              if (window.AutocompleteExt != undefined) {
                new AutocompleteExt("path/to/api", id_find", "find", "Find something").init();
              }
            }(jQuery));
          </script>

.. note:: Unlike the widgets the javascript is agnostic to the form, and only
          cares about the url path to the api. Jquery will call this url with the query
          string ``term=<entered>``.

The ``AutocompleteExt`` object needs to be defined, first the constructor::

        window.AutocompleteSearch = function(source, field_id, field_name, field_title) {
          this.source = source;
          this.field_id = field_id;
          this.field_name = field_name;
          this.field_title = field_title;
        }

This just repeats the ``AuotcompleteBase`` constructor. We then declare the new
object prototype to be that of ``AutocompleteBase`` so it inherits the methods of
the base::

        AutocompleteSearch.prototype = new AutocompleteBase();

But it needs to use its own constructor (otherwise we get a base object)::

        AutocompleteSearch.prototype.constructor = AutocompleteSearch;

Then we must declare its ``init`` method, this is described line by line below::

        AutocompleteSearch.prototype.init = function() {

Init the base object, this adds the modal to the ``dom`` and initializes some attributes::

        this.initBase();

Locate the dom object that will be the trigger to open the modal::

        this.trigger = $('#' + this.field_id);

And set this as the trigger on the event ``focus``, not this could be any event, e.g. ``click`` on a button::

        this.setTrigger(this.trigger, 'focus');

.. note:: Any other setup could take place here - see as an example ``autocomplete_multipleselect.js``.

The next command declares the jqueryui autocomplete plugin on the input field of the modal.

.. note:: The input field in the modal is available as ``this.input``.

::

      this.initAutocomplete()

Then bind the select action of the autocomplete.

.. note:: This method is not declared in ``AutocompleteBase`` and gives the
          developer freedom to declare what happens when a result is returned from the server.

Call the method that we declare below::

      this.bindAutocomplete() // end init

In this example all that happens is that the input field receives the value of the label.

.. note:: The AutocompleteExt is passed with the event and is available as ``obj``.

::

      AutocompleteExt.prototype.bindAutocomplete = function() {

        // and add the action on select of item
        $(this.input).bind( "autocompleteselect",
          {obj: this},
          function(event, ui) {
            var obj = event.data.obj;
            if (ui.item) {
              // do something
              $(obj.trigger).attr('value', ui.item.label )
              $(obj.modal).modal('hide');
            } else {
              alert("Nothing selected, input was " + this.value );
            }
            event.preventDefault();
            return false;
          })
        }

Hope that helps.

