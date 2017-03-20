        google.charts.load('visualization', '1.0', {'packages':['corechart'], 'callback': drawChart});
        //google.charts.setOnLoadCallback(drawChart);
        function drawChart(webdata) {                   
                    
                    var data = new google.visualization.DataTable();  
                    var options = {
                        title: 'Current Temperature',
                        curveType: 'function',
                        legend: {position: 'bottom'},
                        'backgroundColor': 'transparent',
                        vAxis: {
                            gridlines: {
                                color: 'transparent'
                            },
                            textStyle: {
                                color: 'black'
                            }                            
                        },
                        hAxis: {
                            textStyle: {
                                color: 'black'
                            },
                            gridlines: {
                                color: 'transparent'
                            }
                        }
                    };
                    data.addColumn('number', 'Time');
                    data.addColumn('number', 'Celsius');
                    temp = webdata.split(" ");
                    //console.log(temp);
                    for (var i = 0; i < temp.length; i++) {
                        //console.log(temp[i]);
                        data.addRow([i - 10, Number(temp[i])]);
                    }
                    //console.log(0);
                    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
                    chart.draw(data, options);
                    $('#curTemp').text(temp[temp.length - 1] + " Degree Celsius");         
        }   

        setInterval(reload, 3000);    
        function reload(){
            //console.log(tempVar);
            $(document).ready(function(){
                $.ajax({
                    url: "{% static 'temp.txt' %}",
                    async: true,
                    success: function(data){
                            drawChart(data);
                    },
                });
            });
        }