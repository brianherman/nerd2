function pad (str, max) {
  return str.length < max ? pad("0" + str, max) : str;
}

function loadRevision(rev) {
    rev = parseInt(rev);
    current = parseInt($('#current-rev').text());
    sname = $('#server-name').text();

    
    $('#rev-list a.selected').each(function() { $(this).removeClass('selected') });
    $('#label-rev-'+rev).addClass('selected');
    if (rev < current) {
        $('#map-download').show();
        $('#map-download').attr('href', '/backups/' + sname + '-rev' + pad(rev.toString(), 2) + '.tar.gz');
        
        $('#carto').show();
        $('#carto').attr('href', 'http://redditpublic.com/carto/' + sname + '/' + sname.substr(0,1) + pad(rev.toString(), 2) + '/carto/index.html');
    } else if (rev == current) {
        $('#map-download').hide();
        
        if (sname == 'survival') {
            $('#carto').hide();
        } else {
            $('#carto').show();
            $('#carto').attr('href', 'http://redditpublic.com/carto/' + sname + '/current/');
        }
    }
    
    
    $.getJSON('/static/json/creations/'+$('#server-name').text()+'_'+rev+'.json', function(data) {
        var list = $('<ul class="builds-1" />');
        $.each(data, function(i, v) {
            var inner = $('<li><a class="builds-wiki" href="http://redditpublic.com/wiki/' + v['page_title'] + '">'+ v['title'] + '</a></li>');
            if ('coordinates_normal' in v) {
                inner.append('<a class="builds-carto" href="' +
                    $('#carto').attr('href') + '#/' + v['coordinates_normal'][0] + '/64/' + v['coordinates_normal'][1] + '/-2/0/0' +
                    '">' + v['coordinates_normal'][0] + ', ' + v['coordinates_normal'][1] + '</a>');
            }
            list.append(inner);
        });
        $('#builds').html(list);

    });
    
}

$(document).ready(function(){
    $("#players-showhide").click(function () {
       $('#players-list').toggle();
       return false;
    });
    
    var loaded = false
    
    $('#rev-list li a').each(function() {
      $(this).click(function() {
        window.location.hash = '#rev-' + $(this).text();
        loadRevision($(this).text());
        return false;
      });
      if(window.location.hash == '#rev-' + $(this).text()) {
        $('html, body').animate({
          scrollTop: $('#builds-header').offset().top
        }, 0);
        loadRevision($(this).text());
        loaded = true;
      }
    });
    
    if (!loaded) {
        loadRevision($('#current-rev').text());
    }
});

//$(document).scroll(function(e){
//    $("#header").fadeTo(0, Math.min(1, 0.9 + window.scrollY/800));
//});

