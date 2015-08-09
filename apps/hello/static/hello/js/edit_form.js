var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    closeForm();
    }
});

var baseFormObject =document.getElementById('contactform');

function closeForm() {
    document.getElementById('edit-button').style.display = 'block';
    document.getElementById('submit').style.display ='none';
    document.getElementById('cancel').style.display ='none';

    var newRows = $("#contactform").find(".form-control");

    $.each(newRows, function (key, row) {
        row.setAttribute('disabled', 'disabled');
    });
}

function openForm() {
    document.getElementById('edit-button').style.display = 'none';
    document.getElementById('submit').style.display ='block';
    document.getElementById('cancel').style.display ='block';

    var newRows = $("#contactform").find(".form-control");
    $.each(newRows, function (key, row) {
        row.removeAttribute('disabled');
    });
}

function reset(e) {
    $('#contactform').empty();
    jQuery("#status").prepend(baseFormObject.getEinnerHTML);
}

$('#cancel').on('click', function () {
    var newRows = $("#contactform").find(".form-control");
    $.each(newRows, function (key, row) {
        row.setAttribute('disabled', 'disabled');
    });
    document.getElementById('edit-button').style.display = 'block';
    document.getElementById('submit').style.display ='none';
    document.getElementById('cancel').style.display ='none';
});

jQuery(function(ev, da) {
    var form = jQuery("#contactform");
    form.submit(function(e,data) {

    console.log(e);
    console.log(data);
        jQuery("#sendbutton").attr('disabled', true);
        jQuery("#status").prepend('<span>Sending message, please wait... </span>');
        $.ajax({
            type: 'json',
            method: 'POST',
            enctype: 'multipart/form-data',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                //$("#sendwrapper").html(data);
                jQuery("#status").empty();
                jQuery("#status").prepend('<span>Secces</span>');
                baseFormObject =document.getElementById('contactform');
                closeForm();
            },
            error: function(data) {
                var response = JSON.parse(data.responseText);
                $.each(response, function (key, value) {
                    $('#status').html('<span id="form-error" >ERROR:' + key +' : ' + value);
                });
                //$("#ajaxwrapper").html("Something went wrong!");
            }
        });
        e.preventDefault();
    });
});

$('#edit-button').on('click', function () {
    openForm()
});
