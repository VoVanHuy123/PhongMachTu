document.addEventListener('DOMContentLoaded', function () {

    fetchProfile();
});

async function fetchProfile(){
    
    document.getElementById('saveChangesButton').addEventListener('click', async function () {
        const form = document.getElementById('editUserForm');
        const formData = new FormData(form);
    
        try {
            // Gửi dữ liệu qua AJAX bằng fetch
            const response = await fetch('/auth/edit_user', {
                method: 'POST',
                body: formData,
            });
    
            // Chuyển đổi phản hồi thành JSON
            const data = await response.json();
    
            // Kiểm tra trạng thái cập nhật
            if (data.success) {
                alert('Cập nhật thành công!');
                location.reload(); // Reload lại trang
            } else {
                alert('Cập nhật thất bại!');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Có lỗi xảy ra, vui lòng thử lại!');
        }
    });
        
};

