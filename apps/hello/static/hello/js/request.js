// use jQuery
var csrftoken = $.cookie('csrftoken');
var titleString = '| 42-unkvuzutop-test';

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.table').on('click', function () {
    var newRequests = [];

    var newRows = $("#requests-table").find("tr");
    $.each(newRows, function (key, row) {
        row.classList.remove('unreaded');
        row.classList.remove('readed');
        if (row.getAttribute('data-id')){
            newRequests.push(row.getAttribute('data-id'));
        }
    });

    $.ajax({
        dataType: "json",
        url: '/api/v1/update',
        method: 'POST',
        data: {'viewed': newRequests.join()},
        success: function() {
             document.title = titleString;
        }
    });
});

function getNewRequests() {
    var lastLoadedId = document.getElementById('requests-table').getAttribute('data-last-id');
    $.ajax({
        dataType: "json",
        url: '/api/v1/count',
        method: 'POST',
        data: {last_loaded_id: lastLoadedId},
        success: function(response) {
            renderResponse(response);
        }
    });
}

function renderResponse(response) {
    var title = document.title;
    title = title.slice(' ', 10);
    if (title[0] == '|') {
        document.title = response.count;
        document.title +=  ' New Requests ' + titleString;
    } else {
        document.title = response.count + $('.unreaded').length;
        document.title +=  ' New Requests ' + titleString;
    }
    $.each(response.requests, function(key,requestObj) {
        var tableRow = '';
        tableRow += '<tr class="request  unreaded" id="request_'+ requestObj.id + '" data-id="' + requestObj.id + '">';
        tableRow += '<td>'+requestObj.method+'</td>';
        tableRow += '<td>' + requestObj.path + '</td>';
        tableRow += '<td>'+ requestObj.date + '</td>';
        tableRow += '<td>' + requestObj.ip + '</td>';
        tableRow += '<td>' + requestObj.host + '</td>';
        $('#requests-table > tbody').prepend(tableRow);
    });

    document.getElementById('requests-table').setAttribute('data-last-id', response.last_request);

}

//getNewRequests();
setInterval(getNewRequests, 10000);
