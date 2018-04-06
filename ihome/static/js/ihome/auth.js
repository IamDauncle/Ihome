function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // TODO: 查询用户的实名认证信息

    $.get('/api/1.0/users/auth',function (response) {
        if(response.errno == '0'){
            $('#real-name').val(response.data.user_arth.real_name);
            $('#id-card').val(response.data.user_arth.id_card)

        }else {
            alert(response.errmsg)
        }

    });


    // TODO: 管理实名信息表单的提交行为
    $('#form-auth').submit(function (event) {
        event.preventDefault();

        var real_name = $('#real-name').val(),
            id_card = $('#id-card').val();
        if (!real_name){
            $('error-msg').show();
            return;
        }
        if (!id_card){
            $('error-msg').show();
            return;
        }

        var context = {
            'id_card' : id_card,
            'real_name':real_name

        };

         $.ajax({
                     url:'/api/1.0/users/auth',
                     type:'POST',
                     data:JSON.stringify(context),
                     contentType:'application/json',
                     headers:{'X-CSRFToken':getCookie('csrf_token')},
                     success:function (response) {
                         if (response.errno == '0'){
                             showSuccessMsg();
                             // 消除input的可用
                              $('#real-name').attr('disabled', true);
                                $('#id-card').attr('disabled', true);

                    // 将保存按钮影藏
                    $('.btn-success').hide();

                         }else if (response.errno == '4101'){
                             location.href = '/'
                         }
                         else {
                             alert(response.errmsg)
                         }


                     }


                 })




    })

});