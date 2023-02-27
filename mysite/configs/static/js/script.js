function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


$(document).ready(function () {
    $('#my-button3').click(function () {
        $('#spinner').show();
        $.ajax({
            url: '/send_tele/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            // data: {'my_data': 'my_value'},
            success: function (response) {
                $('#spinner').hide();
                alert("Success! \n\n");
            }
        });
    });
    $('#my-button1').click(function () {
        $('#spinner').show();
        $.ajax({
            url: '/get_recs/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            // data: {'my_data': 'my_value'},
            success: function (response) {
                $('#spinner').hide();
                console.log(response.result)

                var headerHTML = '<tr>'
                var isFirstRow = true
                var trHTML = '';
                $.each(response.result, function (i, pos) {
                    trHTML += '<tr>'

                    Object.entries(pos).forEach(entry => {
                        const [key, value] = entry;
                        trHTML += '<td>'
                        trHTML += value
                        trHTML += '</td>'
                        if (isFirstRow) {
                            headerHTML += '<td>'
                            headerHTML += key
                            headerHTML += '</td>'
                        }
                        console.log(key, value);
                    });
                    isFirstRow = false

                    trHTML += '</tr>'
                });
                headerHTML += '</td>'

                $('#tHead').append(headerHTML);
                $('#tBody').append(trHTML);
                alert("Success! \n\n");
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});