const ctx = document.getElementById('myChart');
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
        label: 'Sale for each state',
        data: [],
        backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
        borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
        borderWidth: 1,
        showLine: true,
        spanGaps: true
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
  var out_html = '';
    const myJSON1 = JSON.parse({{ final_data | tojson}});
    var keys = Object.keys(myJSON1);
    var out_html1 = '';
    const myJSON11 = JSON.parse({{ final_list1 | tojson}});
    var keys11 = Object.keys(myJSON11);

    for (let i = 0; i < 14; i++) {
      out_html = Object.values(myJSON1[i]);
      out_html1 = Object.values(myJSON11[i]);
      myChart.data.datasets[0].data.push(out_html);
      myChart.data.labels.push(out_html1);
      myChart.update();
    }
    