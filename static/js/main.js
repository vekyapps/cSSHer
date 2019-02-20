
$(document).ready(function(){


    function fetchProcesses(host, username, password){
        $('#processes-loading').show();
        $.ajax({
            type: "POST",
            url: 'http://localhost:5000/processes/fetch',
            data: {
                'host': host,
                'username': username,
                'password': password
            },
            success: function(response){
                //$('#processes-loading').hide();
                if (!response || !response.data) {
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
            },
            dataType: 'json'
          });
    }
    fetchProcesses('docker.maidea.internal','vdekovic','Maidea123');
});