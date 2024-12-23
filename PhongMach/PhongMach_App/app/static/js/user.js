document.addEventListener('DOMContentLoaded', async function () {

    fetchDoctorProfile();
    fetchUserProfile();
    expanExamDetail();
    // fetchUserPhone();

    
    
    const saveAccountChangesButton = document.getElementById('saveAccountChangesButton')
    if (saveAccountChangesButton){
        saveAccountChangesButton.addEventListener('click', async function () {
            const form = document.getElementById('editUserAccountForm');
            const formData = new FormData(form);
            console.log("Fetching user account...");
            fetchUserAccount(formData)
        },{ once: true });
    }
    async function fetchUserAccount(formData){
    
        try {
            const response = await fetch('/auth/edit_user_account', {
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
    
    
    };


    // document.getElementById('addPhone').onclick = addPhone();
        
},{ once: true });

function addPhone(){
    const phoneList = document.getElementById('phoneList');
        const newPhoneDiv = document.createElement('div');
        newPhoneDiv.classList.add('row', "d-flex", 'justify-content-center', 'align-items-center', 'phone-block');

        newPhoneDiv.innerHTML = `
            <div class="col-md-5 mb-3">
                <label for="phoneNumber" class="form-label">Số Điện Thoại:</label>
                <input type="text" id="phoneNumber" name="phone_numberr" class="form-control" placeholder="Nhập số điện thoại"  value = "">
            </div>
            <div class="col-md-6 mb-3">
                <label for="type_number" class="form-label">Loại số: </label>
                <input type="text" id="TypeNumber" name="type_number" class="form-control" placeholder="vd: cá nhân, văn phòng" value ="">
            </div>
            <div onclick = "deletePhone(event);" class="col-md-1 remove-phone"><i class="fa-solid fa-x"></i></div>
        `;

        phoneList.appendChild(newPhoneDiv);
}
function deletePhone(event){
    
        const phoneBlock = event.target.closest('.phone-block'); // Tìm phần tử cha gần nhất có class 'phone-block'
        if (phoneBlock) {
            if(confirm("xác nhận xóa")){

                phoneBlock.remove(); // Xóa phần tử
            }
        }
    
}

async function fetchUserProfile(){
    const saveChangesButton = document.getElementById('saveChangesButton')
    if (saveChangesButton){
        saveChangesButton.addEventListener('click', async function () {
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
        },{ once: true });
    }   
        
};

async function fetchUserPhone() {
    const savePhoneChangesButton = document.getElementById('savePhoneChangesButton');
    if (savePhoneChangesButton) {
        savePhoneChangesButton.addEventListener('click', async function () {
            // Tìm tất cả các input có tên phone_number và type_number
            const phoneNumbers = document.querySelectorAll('input[name="phone_numberr"]');
            const typeNumbers = document.querySelectorAll('input[name="type_number"]');

            // Chuẩn bị dữ liệu gửi
            const phoneData = [];
            phoneNumbers.forEach((phoneInput, index) => {
                phoneData.push({
                    phone_number: phoneInput.value,
                    type_number: typeNumbers[index]?.value || '',
                });
            });

            try {
                // Gửi dữ liệu qua AJAX
                const response = await fetch('/auth/edit_user_phone', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ phone_data: phoneData }),
                });

                const data = await response.json();

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
}

async function editUserAccount(){
    
}



async function fetchDoctorProfile() {
    const saveDoctorChangesButtonElemnet = document.getElementById('saveDoctorChangesButton');
   
    if (saveDoctorChangesButtonElemnet){
        saveDoctorChangesButtonElemnet.addEventListener('click', async function (event) {
            event.preventDefault();
            const form = document.getElementById('editUserForm');
            const formData = new FormData(form);

            try {
                const response = await fetch('/doctor_user/edit_doctor_info', {
                    method: 'POST',
                    body: formData,
                });

                const data = await response.json();

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
        },{ once: true });
    }
}


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

