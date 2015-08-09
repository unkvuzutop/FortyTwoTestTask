$(':file').change(function(){
    var file = this.files[0];
    var type = file.type;
    //validation image types
    if (CheckFileType(type) != true) {
        $('#status').html("<span class='error'>We currently only support the following formats .jpg, .png, .bmp, .jpeg</span>");
    }
    else {
        UploadPhoto();
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

function UploadPhoto() {
    var formData = new FormData($('#contactform')[0]);

    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            closeForm();
            statusString.empty();
            statusString.prepend('<span>Loading Image...</span>');
        },
        url: jQuery("#contactform").attr('action'),
        type: 'POST',
        enctype: 'multipart/form-data',
        success: function(res) {
            document.getElementById('photo-preview').setAttribute('src',  res.photo_preview);
            $(".id_photo_preview").html(res.message);
            openForm();
            statusString.empty();
            statusString.prepend('<span id="success">Image uploaded</span>');
        },
        // Form data .
        data: formData,
        //Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false
    });
}
