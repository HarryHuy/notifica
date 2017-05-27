$('document').ready(function() {
    recieve = function(msg) {
    $('.dropdown-menu').prepend('<li><a href="#">New message</a></li>')
    }

    load_msg = function() {
    }

    delete_msg = function(msg) {
        $()
    }

    // set elements behaviors
    $('.dropdown-menu').on('click.bs.dropdown', function(event) {
        event.stopPropagation();
        event.preventDefault();
    })
    $('ul.dropdown-menu > li > button.close').on('click', function(event) {
        $(this).parent().remove();
    })
})
