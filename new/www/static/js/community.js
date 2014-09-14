$(document).ready(function(){
    $("#reddit-showhide").click(function () {
       $('ul#reddit-posts li').slice(5).toggle();
       return false;
    });
    $("#forum-showhide").click(function () {
       $('ul#forum-posts li').slice(5).toggle();
       return false;
    });
    $("ul#reddit-posts li").slice(3).hide();
    $("ul#forum-posts li").slice(3).hide();
});
