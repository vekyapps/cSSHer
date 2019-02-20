
$(document).ready(function(){

    function fetchProcesses(host, username, password){
        $('#processes-loading').addClass('d-block');

        $('#processes-grid').removeClass('d-block');
        $('#processes-grid').addClass('d-none');
        $.ajax({
            type: "POST",
            url: 'http://localhost:5000/processes/fetch',
            data: {
                'host': host,
                'username': username,
                'password': password
            },
            success: function(response){
                $('#processes-loading').addClass('d-none');
                $('#processes-loading').removeClass('d-block');
                if (!response || !response.data || !response.success) {
                    var msg;
                    if (response.msg) {
                        msg = response.msg;
                    } else {
                        msg = 'Server-side error!';
                    }
                    alert('Error: ' + msg);
                    return;
                }

                if (response.data.constructor !== Array) {
                    alert('Error: Invalid data received (data is not serialized into JSON)!');
                    return;
                }

                var tableBody = '';
                for (var i=0; i < response.data.length; i++) {
                    var item = response.data[i];
                    tableBody += '<tr>';
    
                    tableBody += '<td>'+item.command+'</td>';
                    tableBody += '<td>'+item.pid+'</td>';
                    tableBody += '<td>'+item.cpu+'</td>';
    
                    tableBody += '</tr>';
                }
                $('#processes-grid > tbody').html(tableBody);

                $('#processes-grid').removeClass('d-none');
                $('#processes-grid').addClass('d-block');
            },
            error:function() {
                $('#processes-grid').removeClass('d-block');
                $('#processes-loading').removeClass('d-block');
                $('#processes-grid').addClass('d-none');
                $('#processes-loading').addClass('d-none'); 
                alert("Server-side error! Please contact system administrator."); 
            },
            dataType: 'json'
          });
    }

    $("#fetchBtn").click(function(){
        var hostField = $('#hostField');
        var usernameField = $('#usernameField');
        if (!hostField || !hostField.val()) {
            alert('Host field cannot be empty');
            return;
        }

        if (!usernameField || !usernameField.val()) {
            alert('Username field cannot be empty');
            return;
        }

        var passwordField = $('#passwordField');
        fetchProcesses(hostField.val(), usernameField.val(), passwordField.val());
    });
});