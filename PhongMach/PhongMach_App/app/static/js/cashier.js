document.addEventListener("DOMContentLoaded", function (){
    confirmPay();
});
function confirmPay(){
    document.getElementById("confirmPayBtn").addEventListener("click", async function(){
        const medExamId = document.getElementById("medicalExamId").dataset.medicalExamId;
        console.log(medExamId);

        try{
            const response = await fetch('/cashier/pay',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Thêm header này
                },
                body: JSON.stringify({
                    medExamId : medExamId,
                })
            });
            const data = await response.json();
        
            // Kiểm tra trạng thái cập nhật
            if (data.success) {
                alert('Thanh toán thành công!');
                window.location.href = data.url; // Reload lại trang
            } else {
                alert('Thanh toán thất bại!');
                alert(data.message)
            }
        } catch (error) {
            // console.error('Error:', error);
            alert(error)
            alert('Có lỗi xảy ra, vui lòng thử lại!');
        }
    });
}