function getParameterByName(name) {
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

function sortObject(o) {
    var sorted = {},
    key, a = [];

    for (key in o) {
        if (o.hasOwnProperty(key)) {
                a.push(key);
        }
    }
    a.sort();

    for (key = 0; key < a.length; key++) {
        sorted[a[key]] = o[a[key]];
    }
    return sorted;
}

// Smooth scrolling when clicking on an in-page anchor
$('a').click(function(){
    $('html, body').animate({
        scrollTop: $( $(this).attr('href') ).offset().top
    }, 500);
    return false;
});

var chart;
var server = getParameterByName('server').toLowerCase()
$(document).ready(function() {
  document.title = document.title + ' - ' + server

  // config graph
  var options = {

    chart: {
      renderTo: 'modreq-graph',
      height: 250,
      // type: 'area', 
    },

    credits: {
      enabled: false
    },

    title: {
      text: 'daily requests'
    },

    subtitle: {
      text: server
    },

    tooltip: {
      formatter: function() {
           return this.x + ': <b>' + this.y + '</b>';}
    },  

    xAxis: {
      categories: [],
      type: 'date',
    },

    yAxis: [{ // left y axis
      title: {
        text: null
      },
      labels: {
        align: 'left',
        x: 3,
        y: 16,
        formatter: function() {
          return Highcharts.numberFormat(this.value, 0);
        }
      },
      showFirstLabel: false
    }, { // right y axis
      linkedTo: 0,
      gridLineWidth: 0,
      opposite: true,
      title: {
        text: null
      },
      labels: {
        align: 'right',
        x: -3,
        y: 16,
        formatter: function() {
          return Highcharts.numberFormat(this.value, 0);
        }
      },
      showFirstLabel: false
    }],

    legend: {
      enabled: false
    },

    series: [{
      name: 'Requests',
      color: '#007DC6',
      lineWidth: 2,
      marker: {
        radius: 3
      }
    }]
  };

  // Load the data and add it to the graph
  $.getJSON('/ajax/modreq?server=' + server, function(data) {
    var dates = [];
    var amounts = [];
    data = sortObject(data)

    $.each(data, function(key, val) {
      dates.push(key);
      amounts.push(val);
    });

    options.series[0].data = amounts;
    options.xAxis.categories = dates;
    chart = new Highcharts.Chart(options);
  });
});
