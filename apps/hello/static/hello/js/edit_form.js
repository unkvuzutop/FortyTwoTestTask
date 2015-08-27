var csrftoken = $.cookie('csrftoken');
var statusString = jQuery("#status");
var baseFormObject =document.getElementById('contactform');

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


function closeForm() {
    document.getElementById('submit').style.display ='none';
    document.getElementById('cancel').style.display ='none';
    document.getElementById('id_photo').style.display = 'none';
    document.getElementById('id_photo').setAttribute('disabled', 'disabled');
    var newRows = $("#contactform").find(".form-control");

    $.each(newRows, function (key, row) {
        row.setAttribute('disabled', 'disabled');
    });
}

function openForm() {
    document.getElementById('id_photo').style.display = 'block';
    document.getElementById('id_photo').removeAttribute('disabled');
    document.getElementById('submit').style.display ='block';
    document.getElementById('cancel').style.display ='block';

    var newRows = $("#contactform").find(".form-control");
    $.each(newRows, function (key, row) {
        row.removeAttribute('disabled');
    });
}

function reset(e) {
    $('#contactform').empty();
    statusString.prepend(baseFormObject.getEinnerHTML);
}

jQuery(function(ev, da) {
    var form = jQuery("#contactform");
    form.submit(function(e,data) {
        $("div[id^='error-']").html('');
        $("input[id^='id_']").removeClass('error-input');
        statusString.empty();
        jQuery("#sendbutton").attr('disabled', true);
        statusString.prepend('<span>Sending message, please wait... </span>');
        $.ajax({
            type: 'json',
            method: 'POST',
            enctype: 'multipart/form-data',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                statusString.empty();
                statusString.prepend('<span id="success">Profile updated seccesfully</span>');
                baseFormObject =document.getElementById('contactform');
                openForm();
            },
            error: function(data) {
                var response = JSON.parse(data.responseText);
                $.each(response, function (key, value) {
                    $('#status').html('<span id="form-error" >Form error');
                    $('#error-'+key).html(value).addClass('error');
                    $('#id_'+key).addClass('error-input');
                });
                openForm();
            }
        });
        e.preventDefault();
    });
});

$( document ).ajaxComplete(function() {
    var submit_status = document.getElementById('submit').style.display;
    if (submit_status == 'none') {
        document.getElementById('edit-button').style.display = 'block';
    }
});

// bootstrap custom upload file button
$('input[type=file]').bootstrapFileInput();
$('.file-inputs').bootstrapFileInput();

// datetimepickrer init
$(function() {
    $( ".datepicker" ).datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: "1900:2012"
    });
});
