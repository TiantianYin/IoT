     
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
           
        var options = {
          title: 'Company Performance',
          curveType: 'function',
          legend: {position: 'bottom'}
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        setInterval(function() {
          var data = new google.visualization.DataTable();  
          var temp = {{temparr|safe}};
          data.addColumn('number', 'Time');
          data.addColumn('number', 'Celsius');
          for (var i = 0; i < temp.length; i++) {
              console.log(temp[i]);
              //data.addRow([i, temp[i]]);
  
          }
          chart.draw(data, options);
        }, 7000);
      }



