function sendUserID(userID, divID){
    $.ajax({
        type: "POST",
        url: "/delete",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            ID: userID
        }),
        success: function (response) {
            if(response.data == "200"){
                update_current_div(divID);
            }
        },
        error: function () {
        }
    });
};

function retrieveData(){
    $.ajax({
        type: "POST",
        url: "/dashboard",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            "data": "send"
        }),
        success: function (response) {
            if(response.status == "200"){
                updateCharts(chart1,[response.daysChart.day1, response.daysChart.day2],"Ilość",[response.dataChart.data1,response.dataChart.data2],"Ilość wyprodukowanych");
                updateCharts(chart2,[response.daysChart.day1, response.daysChart.day2],"Ilość",[response.dataChart.data1,response.dataChart.data2],"Ilość wyprodukowanych");
            }
        },
        error: function () {
        }
    });
};
function updateCharts(chartName, labels, label, data, text){
    chartName.data.labels = labels;
    chartName.data.datasets[0].label = label;
    chartName.data.datasets[0].data = data;
    chartName.options.title.text = text;
    chartName.update();
}
function update_current_div(divID){
    let url = $(location).attr('href');
    let result =  url.concat(" ", divID)
    $(divID).load(result);
};