$(document).ready(function(){
    $("#reddit-showhide").click(function () {
       $('ul#reddit-posts li').slice(5).toggle();
       return false;
    });
    $("ul.community li").slice(5).hide();
});
