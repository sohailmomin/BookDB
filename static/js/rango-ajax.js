$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
$.get('/suggest/', {suggestion: query}, function(data){
        $('#books').html(data);
    });
});