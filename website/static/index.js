// FUNCTION TO SEND OBJECT ID TO DELETE IT FROM DATABASE
function sendID(ObjectID, divID){
    if (confirm('Jesteś pewien że chcesz usunąć ?')) {
        $.ajax({
            type: "POST",
            url: window.location.pathname,
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                ID: ObjectID
            }),
            success: function (response) {
                if(response.data == "200"){
                    update_current_div(divID);
                }
            },
            error: function () {
            }
        });
      }
};

// FUNCTION TO RETRIEVE DATA FROM BACKEND
function retrieveData(){
    $.ajax({
        type: "POST",
        url: $(location).attr('href'),
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            "data": "send"
        }),
        success: function (response) {
            if(response.status == "200"){
                console.log(response['productionData']);
                updateCharts(chart1, response['productionData']);
                content = '';
                for(let i=0; i<response['sensorNames'].length; i++){
                    content += '<tr>'
                    content += '<th scope="row" >' + response['sensorNames'][i] +'</th>'
                    content += '<td>' + response['sensorValues'][i] + '</td>'
                    content += '</tr>'
                }
                console.log(content)
                $('#replaceData').html(content)
                
            }
            if(response.status == "404"){
                console.log('Brak połączenia ze sterownikiem!!!')
                $("#pole1").html("<h4 class='h-100 d-flex align-items-center justify-content-center text-white'>Brak danych o sterowniku</h4>");
                $("#pole2").html("<h4 class='h-100 d-flex align-items-center justify-content-center text-white'>Brak danych o sterowniku</h4>");
                $("#pole3").html("<h4 class='h-100 d-flex align-items-center justify-content-center text-white'>Brak danych o sterowniku</h4>");
            }
        },
        error: function () {
        }
    });
};

// FUNCTION TO UDPATE LIVE CHARTS
function updateCharts(chartName, dataList){
    chartName.data.datasets[0].data = dataList;
    chartName.update();
}

// FUNCTION TO UPDATE CURRENT DIV
function update_current_div(divID){
    let url = $(location).attr('href');
    let result =  url.concat(" ", divID)
    $(divID).load(result);
};