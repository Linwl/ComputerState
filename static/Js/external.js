//获取CPU状态
function getCPUstate()
{
$.post("http://192.168.0.204:6411", { Cpustatus: "GetCpu" },
   function(data){
     $('#cpustatus').text(data);
     InitCpuChart(data)
   });
}

//初始化CPU曲线图
function InitCpuChart(data)
{
          // 基于准备好的dom，初始化echarts图表
           var myChart = echarts.init(document.getElementById('cpu'),'vintage');
           //获取服务器CPU利用率

           if(cpuarr.length<60)
           {
           cpuarr.push(data)
           }
           else
           {
            cpuarr.shift();
            cpuarr.push(data)
           }
  option = {
    title : {
        text: '服务器CPU使用率',
        subtext: '数据来自服务器59'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
     data: [
            {
                name:'CPU利用率',
                textStyle:{fontWeight:'bold', color:'#2E8CC4'}
            }
        ]
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : interval
        }
    ],
    yAxis : [
        {
            type : 'value',

        }
    ],
    series : [
        {
            name:'CPU利用率',
            type:'line',
            symbol:'none',
            smooth:true,
            itemStyle: {normal:
             {
            areaStyle: {
            color:'#F1F6FA',
            type: 'default'
            },
            lineStyle:{
             color:'#2E8CC4',
             width:'1'
            }
            }
            },
            data:cpuarr
        },

    ]
};
            // 为echarts对象加载数据
            myChart.setOption(option);
}

//获取内存状态
function getMemorystate()
{
$.post("http://192.168.0.204:6411", { Cpustatus: "GetMemory" },
   function(data){
     $('#memorystate').text(data);
     InitMemoryChart(data)
   });
}

function InitMemoryChart(data)
{
         // 基于准备好的dom，初始化echarts图表
         var myChart = echarts.init(document.getElementById('memory'),'macarons');
           //获取服务器CPU利用率
              if(memarr.length<60)
           {
           memarr.push(data)
           }
           else
           {
            memarr.shift();
            memarr.push(data)
           }

   option = {
    title : {
        text: '服务器内存使用率',
        subtext: '数据来自服务器59'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:[ {
                name:'内存使用率',
                textStyle:{fontWeight:'bold', color:'#9528B4'}
            }]
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : interval
        }
    ],
    yAxis : [
        {
            type : 'value',

        }
    ],
    series : [
        {
            name:'内存使用率',
            type:'line',
            smooth:true,
            symbol:'none',
            itemStyle: {normal:
             {
            areaStyle: {
            color:'#F4F2F4',
            type: 'default'
            },
            lineStyle:{
             color:'#9528B4',
             width:'1'
            }
            }
            },
            data:memarr
        },

    ]
};
            // 为echarts对象加载数据
            myChart.setOption(option);
}