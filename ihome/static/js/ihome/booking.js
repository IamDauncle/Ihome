function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}



$(document).ready(function(){
    // TODO: 判断用户是否登录
    //判断是否又登陆,没登陆就跳转到l扥股页面
    $.get('/api/1.0/index/sessions',function (response) {
        if(!(response.data.user_id && response.data.user_name)){
            location.href = '/login.html'
        }
    });



    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg("日期有误，请重新选择!");
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var queryData = decodeQuery();
    var houseId = queryData["hid"];

    // TODO: 获取房屋的基本信息

    $.get('/api/1.0/houses/'+houseId,function (response) {

        if (response.errno == '0'){
            //填充房屋图片,使用房屋图片的[0]张图作为展示
            $('.house-info>img').attr('src',response.data.house_data_dict.img_urls[0]);
            $('.house-text>h3').html(response.data.house_data_dict.title);
            $('.house-text span').html((response.data.house_data_dict.price/100).toFixed(2))

        }else {
            alert(response.errmsg)
        }

    });

    // TODO: 订单提交
    $('.submit-btn').on('click',function () {

          var start_date = $('#start-date').val(),
            end_date = $('#end-date').val();
        if(!start_date){
            alert('请选择入住时间')
        }
        if(!end_date){
            alert('请选择离开时间')
        }
        var context = {
          'start_date':start_date,
            'end_date':end_date,
            'house_id':houseId
        };

         $.ajax({
             url:'/api/1.0/orders',
             type:'post',
             data:JSON.stringify(context),
             contentType:'application/json',
             headers:{'X-CSRFToken':getCookie('csrf_token')},
             success:function (response) {


                 if (response.errno == '0'){
                     location.href = '/orders.html'
                 }else if(response.errno == '4101') {
                     location.href = '/login.html'
                 } else {
                     alert(response.errmsg)
                 }
             }
                 })
    });















})
