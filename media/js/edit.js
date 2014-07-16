/**
 * Treatments for edit page ajax request.
 */


$("a.formset-ref").live("click",
    function(event) {

        event.preventDefault();
        loader.show();

        $.getJSON($(event.target).attr("href"), function(data) {
            $("#formset-container").html(_.template($("#formset-templ").html(), data));
            loader.hide();
        });

    }
);


$("#formset-form").live("submit",
    function(event) {

        event.preventDefault();
        loader.show();

        var form = $(event.target)
        $.post(form.attr("action"), form.serialize(), function(data) {
            $("#formset-container").html(_.template($("#formset-templ").html(), data));
            loader.hide();
        });

    }
);
