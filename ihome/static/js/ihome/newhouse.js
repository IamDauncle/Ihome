function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/1.0/areas',function (response) {

        if (response.errno == '0'){

            var html = template('areas-tmpl',{'areas':response.data.areas_list});
            $('#area-id').html(html)
        }else {
            alert(response.errmsg)
        }

    });



    // TODO: 处理房屋基本信息提交的表单数据

    $('#form-house-info').submit(function (event) {
        event.preventDefault();

        var context = {};

        // ---这里的是房屋的出租信息---
        // serializeArray()是获取表单中所有input标签，然后放在一个数组对象中，
        // map是用来遍历对象，这里是用来遍历数组对象  表里出来的boj就是每个input标签
        $(this).serializeArray().map(function (obj) {
            context[obj.name] = obj.value;

        });


        //--这里的是房屋的设备信息---复选框内容
        // 复选框内容多选，把多选框有选择的存在一个列表中
        facilities = [];

        // 遍历所有选中的复选框 ，
        $(':checkbox:checked').each(function(index,elem){
            // [1,2,,3,4]
            facilities[index] = elem.value;
        });

        context['facilities'] = facilities;



         $.ajax({
                     url:'/api/1.0/houses',
                     type:'post',
                     data:JSON.stringify(context),
                     contentType:'application/json',
                     headers:{'X-CSRFToken':getCookie('csrf_token')},
                     success:function (response) {
                         if (response.errno == '0'){
                             $('#form-house-info').hide();
                             $('#form-house-image').show();

                             // 将后端生成的house_id传入到上传图片的<input>
                            $('#house-id').val(response.data.house_id);
                         }else if (response.errno == '4101'){
                             location.href = '/'
                         }else {
                             alert(response.errmsg)
                         }


                     }


                 })






    });







    // TODO: 处理图片表单的数据

     $('#form-house-image').submit(function (event) {
        event.preventDefault();

        $(this).ajaxSubmit({
            url:'/api/1.0/houses/image',
            type:'post',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if (response.errno == '0') {
                    $('.house-image-cons').append('<img src="'+response.data.house_image_url+'">');
                } else if (response.errno == '4101')  {
                    location.href = '/';
                } else {
                    alert(response.errmsg);
                }
            }
        });
    });







});