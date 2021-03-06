var cur_page = 1; // 当前页
var next_page = 1; // 下一页
var total_page = 1;  // 总页数
var house_data_querying = true;   // 是否正在向后台获取数据

// 解析url中的查询字符串
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

// 更新用户点选的筛选条件
function updateFilterDateDisplay() {
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").eq(0).children("span").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }
}


// 更新房源列表信息
// action表示从后端请求的数据在前端的展示方式
// 默认采用追加方式
// action=renew 代表页面数据清空从新展示
function updateHouseData(action) {
    var areaId = $(".filter-area>li.active").attr("area-id");
    if (undefined == areaId) areaId = "";
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var sortKey = $(".filter-sort>li.active").attr("sort-key");
    var params = {
        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
    };
    // TODO: 获取房屋列表信息
    // 关键属性--house_data_querying  判断是否下拉获取资源,防止暴力刷资源
    //--cur_page --total_page --next_page
    // 判断当前页与总页数的关系.如果小于总页数, 下一页码数加1 .就是在获得下一页资源后,现在的当前页就等于之前的下一页,下一页就等于之前的下一页加1

    //1.需要显示当前页的房屋介绍
    // 2.需要判断是否是下拉屏幕获取数据  action == 'renew'是重新加载页面
    //3.设置属性  house_data_querying 记录加载状态; 正在加载状态为True,表示不可上拉获取更多.
    // 等没有在加载状态时,赋值为false,表示可以下拉获取新资源
    //3.新页拼接在前面数据之后

     $.get('/api/1.0/houses/search',params,function (response) {

         house_data_querying = false;
            if(response.errno == '0'){
                total_page = response.data.pages;

                var html = template('house-list-tmpl',{'houses':response.data.house_detail_list});
                if(action == 'renew'){ // 如果是重新加载页面的,就直接获取页面信息
                    $('.house-list').html(html);
                }else { // 如果是下拉数据的,就拼接数据

                    cur_page = next_page;

                    $('.house-list').append(html);
                }

            }else {
                alert(response.errmsg)
            }
    });












}

$(document).ready(function(){
    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start-date").val(startDate); 
    $("#end-date").val(endDate); 
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    if (!areaName) areaName = "位置区域";
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);





    // 获取筛选条件中的城市区域信息
    $.get("/api/1.0/areas", function(data){
        if ("0" == data.errno) {
            var areaId = queryData["aid"];
            if (areaId) {
                for (var i=0; i<data.data.areas_list.length; i++) {
                    areaId = parseInt(areaId);
                    if (data.data.areas_list[i].aid == areaId) {
                        $(".filter-area").append('<li area-id="'+ data.data.areas_list[i].aid+'" class="active">'+ data.data.areas_list[i].aname+'</li>');
                    } else {
                        $(".filter-area").append('<li area-id="'+ data.data.areas_list[i].aid+'">'+ data.data.areas_list[i].aname+'</li>');
                    }
                }
            } else {
                for (var i=0; i<data.data.areas_list.length; i++) {
                    $(".filter-area").append('<li area-id="'+ data.data.areas_list[i].aid+'">'+ data.data.areas_list[i].aname+'</li>');
                }
            }
            // 在页面添加好城区选项信息后，更新展示房屋列表信息
            updateHouseData("renew");
            var windowHeight = $(window).height();
            // 为窗口的滚动添加事件函数
            window.onscroll=function(){
                // var a = document.documentElement.scrollTop==0? document.body.clientHeight : document.documentElement.clientHeight;
                var b = document.documentElement.scrollTop==0? document.body.scrollTop : document.documentElement.scrollTop;
                var c = document.documentElement.scrollTop==0? document.body.scrollHeight : document.documentElement.scrollHeight;
                // 如果滚动到接近窗口底部
                if(c-b<windowHeight+50){
                    // 如果没有正在向后端发送查询房屋列表信息的请求
                    if (!house_data_querying) {
                        // 将正在向后端查询房屋列表信息的标志设置为真
                        house_data_querying = true;
                        // 如果当前页面数还没到达总页数
                        if(cur_page < total_page) {
                            // 将要查询的页数设置为当前页数加1
                            next_page = cur_page + 1;
                            // 向后端发送请求，查询下一页房屋数据// 向后端发送请求，查询下一页房屋数据
                            updateHouseData();
                        } else {
                            house_data_querying = false;
                        }
                    }
                }
            }
        }
    });

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    var $filterItem = $(".filter-item-bar>.filter-item");
    $(".filter-title-bar").on("click", ".filter-title", function(e){
        var index = $(this).index();
        if (!$filterItem.eq(index).hasClass("active")) {
            $(this).children("span").children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
            $(this).siblings(".filter-title").children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).addClass("active").siblings(".filter-item").removeClass("active");
            $(".display-mask").show();
        } else {
            $(this).children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).removeClass('active');
            $(".display-mask").hide();
            updateFilterDateDisplay();
        }
    });
    $(".display-mask").on("click", function(e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();
        cur_page = 1;
        next_page = 1;
        total_page = 1;
        updateHouseData("renew");

    });
    $(".filter-item-bar>.filter-area").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html($(this).html());
        } else {
            $(this).removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html("位置区域");
        }
    });
    $(".filter-item-bar>.filter-sort").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(2).children("span").eq(0).html($(this).html());
        }
    })
})
