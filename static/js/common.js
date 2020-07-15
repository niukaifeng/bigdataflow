$(function () {
		$('#sample_3').DataTable({
            language: {
                "processing":   "处理中...",
                "lengthMenu":   "_MENU_ 记录/页",
                "zeroRecords":  "没有匹配的记录",
                "info":         "第 _START_ 至 _END_ 项记录，共 _TOTAL_ 项",
                "infoEmpty":    "第 0 至 0 项记录，共 0 项",
                "infoFiltered": "(由 _MAX_ 项记录过滤)",
                "infoPostFix":  "",
                "search":       "搜索:",
                "url":          "",
                "decimal": ",",
                "thousands": ".",
                "emptyTable":"未找到符合条件的数据",
                "paginate": {
                    "first":    "首页",
                    "previous": "上页",
                    "next":     "下页",
                    "last":     "末页"
                }
            },
            "paging": true,
            "lengthChange": true,
            "searching": true,
            "ordering": true,
            "order": [[ 0, "desc" ]],
            "info": true,
            "iDisplayLength": 10,
            "autoWidth": false,
            sSearch:"标题检索",
            bLengthChange:true,
            pageLength: 10,//每页显示10条数
            serverSide: true,
            ajax: function (data, callback, settings) {
                //封装相应的请求参数，这里获取页大小和当前页码
                var pagesize = data.length;//页面显示记录条数，在页面显示每页显示多少项的时候,页大小
                var start = data.start;//开始的记录序号
                var page = (data.start / data.length)+1;//当前页码
                var searchKey = data.search.value;

                var order = "";
                 if(data.order) {
                      $.each(data.order,function(index,value){
                         var col = data.order[index].column;
                         $.each(data.columns,function(i,v) {
                         var name = data.columns[i].name;
                             if(name) {
                                order = name + ","+data.order[0].dir;
                             }
                         })
                      })
                 }

                var data = {
                    page: page,
                    pagesize: pagesize,//这里只传了当前页和页大小，如果有其他参数，可继续封装
                    category:"all",
                    searchKey:searchKey,
                    order:order,

                };
                var json={
                        dataArray:JSON.stringify(data)
                };
                $.ajax({
                    type: "GET",
                    url: "/workflow/setpagedata",
                    cache : false,  //禁用缓存
                    data: json,   //传入已封装的参数
                    dataType: "json",//返回数据格式为json
                    success: function(data) {
                        var arr = "";
                        if ('object' == typeof data) {
                            arr = data;
                        } else {
                            arr = $.parseJSON(data);//将json字符串转化为了一个Object对象
                        }

                        var returnData = {};

                        returnData.recordsTotal = arr.totalCount;
                        returnData.recordsFiltered = arr.totalCounts;
                        returnData.data = arr.data;


                        callback(returnData);
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                        console.log("查询失败");
                    }
                });
            },
            columns: [
                {"name":"flowid","data": "flowid", "defaultContent": "<td></td>"},
                {"name":"projectid","data": "projectid", "defaultContent": "<td></td>"},
                {"name":"title","data": "title", "defaultContent": "<td></td>"},
                {"name":"state_name","data": "state_name", "defaultContent": "<td></td>"},
                {"name":"creator","data": "creator", "defaultContent": "<td></td>"},
                {"name":"gmt_created","data": "gmt_created", "defaultContent": "<td></td>"},
                {"name":"gmt_modified","data": "gmt_modified", "defaultContent": "<td></td>"},
                {"name":"action","data": "action", "defaultContent": "<td></td>"}
            ]
        });
    });