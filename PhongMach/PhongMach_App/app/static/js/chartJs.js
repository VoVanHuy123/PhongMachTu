
document.addEventListener("DOMContentLoaded", function () {
  
});

async function drawChart() {
  try {
      // Lấy giá trị từ form
      const month = document.getElementById('month').value;
      const year = document.getElementById('year').value;

      // Gửi yêu cầu tới API
      const response = await fetch(`/admin/report/get_revenue_info?month=${month}&year=${year}`, {
          // method: 'GET',
      });

      // Kiểm tra phản hồi có JSON không
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
          const result = await response.json();

          if (response.ok) {


              //Tạo biểu đồ với dữ liệu từ API
              let myChart = document.getElementById('myChart').getContext('2d');
        
            //   Nếu đã tồn tại chart trước đó, cần hủy chart cũ
              if (window.massPopChart) {
                window.massPopChart.destroy();
              }
        
              Chart.defaults.font.family = 'Lato';
              Chart.defaults.font.size = 18;
              Chart.defaults.color = '#777';
        
              window.massPopChart = new Chart(myChart, {
                type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
                data:{
                  labels:result.months,
                  datasets:[{
                    label:'Population',
                    data:result.moths_revenue,
                    //backgroundColor:'green',
                    backgroundColor:[
                      'rgba(255, 99, 132, 0.6)',
                      'rgba(54, 162, 235, 0.6)',
                      'rgba(255, 206, 86, 0.6)',
                      'rgba(75, 192, 192, 0.6)',
                      'rgba(153, 102, 255, 0.6)',
                      'rgba(255, 159, 64, 0.6)',
                      'rgba(255, 99, 132, 0.6)',
                      'rgba(255, 206, 86, 0.6)',
                      'rgba(75, 192, 192, 0.6)',
                      'rgba(153, 102, 255, 0.6)',
                      'rgba(255, 159, 64, 0.6)',
                      'rgba(255, 99, 132, 0.6)'
                    ],
                    borderWidth:1,
                    borderColor:'#777',
                    hoverBorderWidth:3,
                    hoverBorderColor:'#000'
                  }]
                },
                options:{
                  title:{
                    display:true,
                    text:'Largest Cities In Massachusetts',
                    fontSize:25
                  },
                  legend:{
                    display:true,
                    position:'right',
                    labels:{
                      fontColor:'#000'
                    }
                  },
                  layout:{
                    padding:{
                      left:50,
                      right:0,
                      bottom:0,
                      top:0
                    }
                  },
                  tooltips:{
                    enabled:true
                  }
                }
              });



          } else {
              alert(result.error || 'Không thể lấy dữ liệu.');
          }
      } else {
          throw new Error('Phản hồi không phải là JSON');
      }
  } catch (error) {
      console.error('Error fetching data:', error);
      alert('Có lỗi xảy ra khi tải dữ liệu.');
  }
}










 // Tạo biểu đồ với dữ liệu từ API
      // let myChart = document.getElementById('myChart').getContext('2d');

      // Nếu đã tồn tại chart trước đó, cần hủy chart cũ
      // if (window.massPopChart) {
      //   window.massPopChart.destroy();
      // }

      // Chart.defaults.font.family = 'Lato';
      // Chart.defaults.font.size = 18;
      // Chart.defaults.color = '#777';

      // window.massPopChart = new Chart(myChart, {
      //   type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
      //   data:{
      //     labels:['Boston', 'Worcester', 'Springfield', 'Lowell', 'Cambridge', 'New Bedford'],
      //     datasets:[{
      //       label:'Population',
      //       data:[
      //         617594,
      //         181045,
      //         153060,
      //         106519,
      //         105162,
      //         95072
      //       ],
      //       //backgroundColor:'green',
      //       backgroundColor:[
      //         'rgba(255, 99, 132, 0.6)',
      //         'rgba(54, 162, 235, 0.6)',
      //         'rgba(255, 206, 86, 0.6)',
      //         'rgba(75, 192, 192, 0.6)',
      //         'rgba(153, 102, 255, 0.6)',
      //         'rgba(255, 159, 64, 0.6)',
      //         'rgba(255, 99, 132, 0.6)'
      //       ],
      //       borderWidth:1,
      //       borderColor:'#777',
      //       hoverBorderWidth:3,
      //       hoverBorderColor:'#000'
      //     }]
      //   },
      //   options:{
      //     title:{
      //       display:true,
      //       text:'Largest Cities In Massachusetts',
      //       fontSize:25
      //     },
      //     legend:{
      //       display:true,
      //       position:'right',
      //       labels:{
      //         fontColor:'#000'
      //       }
      //     },
      //     layout:{
      //       padding:{
      //         left:50,
      //         right:0,
      //         bottom:0,
      //         top:0
      //       }
      //     },
      //     tooltips:{
      //       enabled:true
      //     }
      //   }
      // });