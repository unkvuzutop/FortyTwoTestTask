$(document).on('change', '.priority', function() {
    var str ='';
    $(this.children).each(function() {
        if(this.selected) {
            str += $(this).val() + " ";
        }
    });
    $.ajax({
        dataType: "json",
        url: '/api/v1/update/priority',
        method: 'POST',
        data: {'request_id': this.getAttribute('data-request-id'),
               'priority':str},
        success: function() {
             document.title = titleString;
        }
    });
});