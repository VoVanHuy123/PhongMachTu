document.addEventListener('DOMContentLoaded', function () {

    fetchDoctorProfile();
    fetchUserProfile();
    expanExamDetail();
});

async function fetchUserProfile(){
    const saveChangesButton = document.getElementById('saveChangesButton')
    if (saveChangesButton){
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
    }
    
    
        
};
async function fetchDoctorProfile(){
    const saveDoctorChangesButtonElemnet = document.getElementById('saveDoctorChangesButton')
    if(saveDoctorChangesButtonElemnet){
        document.getElementById('saveDoctorChangesButton').addEventListener('click', async function () {
            const form = document.getElementById('editUserForm');
            const formData = new FormData(form);
        
            try {
                // Gửi dữ liệu qua AJAX bằng fetch
                const response = await fetch('/doctor_user/edit_doctor_info', {
                    method: 'POST',
                    body: formData,
                });
        
                // Chuyển đổi phản hồi thành JSON
                const data = await response.json();
        
                // Kiểm tra trạng thái cập nhật
                if (data.success) {
                    alert('Cập nhật thành công! 1');
                    location.reload(); // Reload lại trang
                } else {
                    alert('Cập nhật thất bại!');

                }
            } catch (error) {
                console.error('Error:', error);
                alert('Có lỗi xảy ra, vui lòng thử lại!');
            }
        });
    }
    
        
};


async function expanExamDetail(){
    document.querySelectorAll('#expan-icon').forEach(icon => {
        icon.addEventListener('click', async function () {
            const medicalExamId = this.getAttribute('data-medical-exam-id');
            const detailExamBody = this.closest('.card').querySelector('.detail-exam-body');
            const detailBody = detailExamBody.querySelector("#examDetailContent");
            // Kiểm tra trạng thái đóng/mở
            if (detailExamBody.style.display === 'block') {
                // Nếu đang mở, thì đóng lại
                detailExamBody.style.display = 'none';
                this.querySelector('i').classList.remove('bi-chevron-bar-up');
                this.querySelector('i').classList.add('bi-chevron-bar-down');
            } else {
                // Nếu đang đóng, thì mở và tải dữ liệu
                detailExamBody.style.display = 'block';
                this.querySelector('i').classList.remove('bi-chevron-bar-down');
                this.querySelector('i').classList.add('bi-chevron-bar-up');
    
                // Gửi yêu cầu để lấy dữ liệu nếu chưa có
                if (!detailBody.innerHTML.trim()) {
                    try {
                        const response = await fetch('/auth/patient_exam_details', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ medical_exam_id: medicalExamId })
                        });
    
                        if (response.ok) {
                            const data = await response.json();
                            detailBody.innerHTML = data.map((detail, index) => `
                                <div class="row mt-2">
                                    <div class="col-1">${index + 1}</div>
                                    <div class="col-4">${detail.medicine_name}</div>
                                    <div class="col-1">${detail.quantity}</div>
                                    <div class="col-2">${detail.unit}</div>
                                    <div class="col-4">${detail.instruct}</div>
                                </div>
                                    <hr/>
                            `).join('');
                        } else {
                            console.error('Failed to fetch exam details');
                            detailExamBody.innerHTML = '<p class="text-danger">Unable to load details.</p>';
                        }
                    } catch (error) {
                        console.error('Error fetching exam details:', error);
                        detailExamBody.innerHTML = '<p class="text-danger">An error occurred while fetching details.</p>';
                    }
                }
            }
        });
    });
};

