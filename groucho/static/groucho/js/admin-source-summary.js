(function(groucho, $) {
    var sourceTotalColor = '#555555CC';
    var sourceBreakdownColors = ['#E15554CC', '#E1BC29CC', '#3BB273CC', '#7768AECC', '#3590F3CC'];

    var updateHistoricalChart = function(historicalChart, sourceIndex, sourceIp) {
        $.get(groucho.admin.sourceSummaryUrl, {ip: sourceIp}, function(data) {
            var color = sourceTotalColor;
            if(sourceIndex < sourceBreakdownColors.length)
                color = sourceBreakdownColors[sourceIndex];

            historicalChart.data.datasets[0].label = sourceIp ? 'Source IP - ' + sourceIp : 'Total Requests';
            historicalChart.data.datasets[0].borderColor = [color];
            historicalChart.data.datasets[0].backgroundColor = [color];
            historicalChart.data.datasets[0].data = [];
            historicalChart.data.labels = [];
            $(data.days).each(function(index, day) {
                historicalChart.data.datasets[0].data.push(day.requests);
                historicalChart.data.labels.push(day.day);
            });

            historicalChart.update();
        }).fail(function() {
            alert('Failed to retrieve data');
        });
    };

    $().ready(function() {
        var historicalChart = new Chart(document.getElementById('source_history').getContext('2d'), {
            type: 'line',
            data: {
                datasets: [{
                    backgroundColor: [sourceTotalColor],
                    borderColor: [sourceTotalColor],
                    label: 'Total Requests',
                    fill: false
                }]
            }
        });

        var summaryDoughnutContext = document.getElementById('summary_doughnut').getContext('2d');
        var summaryDoughnut = new Chart(summaryDoughnutContext, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: groucho.admin.sourceSummaryIpCounts,
                    backgroundColor: sourceBreakdownColors
                }],
                labels: groucho.admin.sourceSummaryIps
            },
            options: {
                onClick: function(event, item) {
                    updateHistoricalChart(historicalChart, item[0]._index, item[0]._model.label);
                },
                legend: {
                    position: 'bottom'
                }
            }
        });

        $('.source_ip').click(function() {
            updateHistoricalChart(
                historicalChart,
                $(this).data('index'),
                $(this).data('ip'),
            );
        });

        $('.total_ip').click(function() {
            updateHistoricalChart(historicalChart);
        });

        // initialize charts
        updateHistoricalChart(historicalChart);
    });

})(groucho, django.jQuery);