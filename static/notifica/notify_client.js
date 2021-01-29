socket.onmessage = function(event) {
//    load_msg(event.text);
    console.log(event.data);
}

//var load_msg = function(msg) {
//    var type = msg['type'];
//    var creator = msg['creator'];
//    var url = msg['url'];
//    $('.dropdown-menu').prepend('<li><a href="'+ url +'">'+ type + ', '+ creator +'</a></li>');
//}
//
//var delete_msg = function(msg) {
//    socket.send('delete'+ msg);
//}

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
