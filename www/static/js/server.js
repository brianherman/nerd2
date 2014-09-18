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
        if ((sname == 'pve' && rev > 10) || (sname == 'creative' && rev > 24) || (sname == 'survival' && rev > 20)) {
            $('#carto').attr('href', 'http://redditpublic.com/carto/' + sname + '/' + sname.substr(0,1) + pad(rev.toString(), 2) + '/index.html');
        } else if (sname == 'creative' && rev == 24) {
            $('#carto').attr('href', 'http://redditpublic.com/carto/' + sname + '/current/index.html');
        } else {
            $('#carto').attr('href', 'http://redditpublic.com/carto/' + sname + '/' + sname.substr(0,1) + pad(rev.toString(), 2) + '/carto/index.html');
        }
    } else if (rev == current) {
        $('#map-download').hide();
        
        if (sname == 'survival') {
            $('#carto').hide();
        } else {
            $('#carto').show();
            $('#carto').attr('href', 'http://nerd.nu/maps/' + sname + '/');
        }
    }
    
    $.getJSON('/api/get_creations?server='+sname+'&revision='+rev, function(data) {
        var list = $('<ul class="builds" />');
        $.each(data, function(i, v) {
            var inner = $('<li><a class="builds-wiki" href="http://redditpublic.com/wiki/' + v['name'] + '">'+ v['name'] + '</a></li>');
            inner.append('<a class="builds-carto" href="' +
                $('#carto').attr('href') + '#/' + v['x'] + '/64/' + v['z'] + '/-2/0/0' +
                '">' + v['x'] + ', ' + v['z'] + '</a>');
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
