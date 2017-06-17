$('document').ready(function() {
    // set elements behaviors
    $('.dropdown-menu').on('click.bs.dropdown', function(event) {
        event.stopPropagation();
        event.preventDefault();
    });

    $('ul.dropdown-menu > li > button.close').on('click', function(event) {
        $(this).parent().remove();
    });
})
