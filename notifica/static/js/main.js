$('document').ready(function() {
    // set elements behaviors
    $('.dropdown-menu').on('click', function(event) {
        event.stopPropagation();
        event.preventDefault();
    });

    // $('.form-group').formset({
    // create add form and remove form links
    // });

    $('.close').click(function() {
        $(this).closest('li').remove();
    });
})
