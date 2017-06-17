// exstra request for sync all fields
function get_users(){
    $.getJSON('/_get_users', function(data){
        $('#users').text('');
        data.users.forEach(function(elem){$('#users').append('<li>'+elem[0]+'   <a href="#" data-elem='+elem[0]+'>del</a></li>')});
        window.setTimeout(function(){$('#result').text('');}, 2000);
    });
}

 $(function(){
            //USER DELETING
            get_users();
            $("#users").on('click', 'li a' , function(){
                $.getJSON('/_del_user',{
                    name: $(this).data('elem')
                }, function(data){
                    console.log(data.result);
                    $('#result').text('');
                    get_users();
                });
                return false;
            });
            // USER REGISTRATION
            $('a#reg_btn').bind('click',function(){
                $.getJSON('/_reg_users',{
                    name: $('input[name="reg_name"]').val()
                }, function(data){
                    $('#result').text(data.result);
                    $('input[name="reg_name"]').val('');
                    get_users();
                });
                return false;
            });

            // LOTTERY
            $('#random').bind('click',function(){
                $.getJSON('/_random', function(data){
                    // if number of users is begger than 3
                    if (typeof data.result === 'object'){
                        $('#random__list').text('');
                        data.result.forEach(function(elem){$('#random__list').append('<li>'+elem[0]+'</li>')});
                    }else{
                        $('#random__list').text('');
                        $('#random__list').append('<li>'+data.result+'</li>')
                    }

                });
            });

        });