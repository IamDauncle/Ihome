function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    // TODO: 添加登录表单提交操作
    $('.form-login').submit(function (even) {
        // 阻止表单的自动提交
        // 获取手机号，密码
        // 参数判断
        // ajax/post请求
        even.preventDefault();
        var mobile = $('#mobile').val(),
            password = $('#password').val();
        if (!mobile){  //手机号码为空
            $('#mobile-err span').html('请输入手机号码')
            $('#mobile-msg').show()
        }
        if (!password){
             $('#password-err span').html('请输入手机号码')
            $('#password-msg').show()
        }
        var context = {
            'mobile' : mobile,
            'password' : password
        };
        $.ajax({
            url:'/api/1.0/sessions',
            type:'post',
            data:JSON.stringify(context),
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if (response.errno == '0'){
                    location.href = '/'
                }else {
                    alert(response.errmsg)
                }


            }


        })





    })




    // $(".form-login").submit(function(e){
    //     e.preventDefault();
    //     mobile = $("#mobile").val();
    //     passwd = $("#password").val();
    //     if (!mobile) {
    //         $("#mobile-err span").html("请填写正确的手机号！");
    //         $("#mobile-err").show();
    //         return;
    //     }
    //     if (!passwd) {
    //         $("#password-err span").html("请填写密码!");
    //         $("#password-err").show();
    //         return;
    //     }
    // });
});
