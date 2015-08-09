$(':file').change(function(){
    var file = this.files[0];
    var size = file.size;
    var type = file.type;
    //Your validation
    if (CheckFileType(type) != true) {
        $('.avatarMessage').html("<span class='error'>I'm sorry we do not support this type of file.  We currently only support the following formats .jpg, .png, .bmp, .jpeg</span>");
    }
    else {
        //if (CheckFileSize(size) == false) {
    //console.log(3333);
    //        $('.avatarMessage').html("<span class='error'>I'm sorry the file must be less than 1MB. </span>");
    //    } else {
            console.log(3334);
            UploadAvatar();
        //}
    }
});
// supported file types
function CheckFileType(type) {
    // four default filetypes
    var fileTypes = ["image/jpg", "image/png", "image/gif", "image/bmp", "image/jpeg"];
    var i;
    for (i = 0; i < fileTypes.length; i++) {
        if (fileTypes[i] === type) {
            return true;
        }
    }
    return false;
}
function CheckFileSize(size) {
    if (size < 1048576) {
        return true;
    } else {
        return false;
    }
}
function progressHandlingFunction(e){
        if(e.lengthComputable){
            $('progress').attr({value:e.loaded,max:e.total});
        }
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function UploadAvatar() {
    $('#progress').css('display', 'inherit');
    $('#uploadProgress').css('display', 'inherit');
    // var formDataIndex = $("#avatarForm").index();
    var formData = new FormData($('#contactform')[0]);
    console.log(formData);
    //var formData = jQuery("#contactform")[0];
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: jQuery("#contactform").attr('action'), //Server script to process data
        //type: 'POST',
        //xhr: function() { // Custom XMLHttpRequest
        //    var myXhr = $.ajaxSettings.xhr();
        //    if (myXhr.upload) { // Check if upload property exists
        //        myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // For handling the progress of the upload
        //    }
        //    return myXhr;
                        type: 'POST',
            //method: 'POST',
            // cache: false,
        //contentType: false,
        //processData: false,
            enctype: 'multipart/form-data',
            //url: form.attr('action'),
            //data: form.serialize(),
            xhr: function() {  // Custom XMLHttpRequest
            var myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){ // Check if upload property exists
                myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // For handling the progress of the upload
            }
            return myXhr;
        },
        //Ajax events
        success: function(res) {
            $(".avatarMessage").html(res.message);
            $("#avatarImage").attr("src", res.image_url);
        },
        // Form data
        data: formData,
        //Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false
    });
}