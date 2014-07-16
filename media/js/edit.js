/**
 * Treatments for "edit" page ajax request.
 */


function filling_formset(data) {
    $("#formset-container").html(_.template($("#formset-templ").html(), data));
    $(".datefield").datepicker({
        "changeMonth": true, 
        "changeYear": true,
        "dateFormat": "yy-mm-dd"
    });
    loader.hide();
}


$("a.formset-ref").live("click",
    function(event) {

        event.preventDefault();
        loader.show();

        $.getJSON($(event.target).attr("href"), filling_formset);

    }
);


$("#formset-form").live("submit",
    function(event) {

        event.preventDefault();
        loader.show();

        var form = $(event.target)
        $.post(form.attr("action"), form.serialize(), filling_formset);

    }
);
