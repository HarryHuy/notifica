$('document').ready(function() {
    // set elements behaviors
    $('.dropdown-menu').on('click', function(event) {
        event.stopPropagation();
        event.preventDefault();
    });

    $('.form-group').formset({
    // add add form and remove form links
    });

    $('.close').click(function() {
        console.log('close button clicked');
        $(this).closest('li').remove();
    });
})
