function updateExamDay() {
    // Lấy giá trị ngày được chọn từ dropdown
    const selectedDate = document.getElementById("date-dropdown").value;
    
    // Gán giá trị ngày được chọn vào input hidden
    document.getElementById("exam_day").value = selectedDate;
}

function updateExamDayAndSubmit(selectedDate) {
    // Cập nhật giá trị của input hidden 'exam_day'
    document.getElementById('exam_day').value = selectedDate;

    // Submit form chọn ngày
    document.getElementById('date-form').submit();
}

function fillPatientInfo(row) {
    // Lấy thông tin từ các data-* attributes
    const firstName = row.dataset.firstName;
    const lastName = row.dataset.lastName;
    const gender = row.dataset.gender;
    const birthDay = row.dataset.birthDay;
    const email = row.dataset.email;
    const symptom = row.dataset.symptom;
    const image = row.dataset.image;
    const phone = row.dataset.phone;
    const patient_id = row.dataset.patientId;
    const date = row.dataset.date;
    const exam_registration_id = row.dataset.examRegistrationId;
     
    // Điền thông tin vào các trường tương ứng
    document.querySelector("#patient-name").textContent = `${firstName} ${lastName}`;
    document.querySelector("#patient-gender").textContent = gender || "Không rõ";
    document.querySelector("#patient-birth-day").textContent = birthDay || "Không rõ";
    document.querySelector("#email").value = email || "";
    document.querySelector("#symptoms").value = symptom || "";
    document.querySelector("#phone").value = phone || "";
    document.querySelector("#image").src = image || "https://via.placeholder.com/100";
    document.querySelector("#patient-id").value = patient_id ;
    document.querySelector("#exam-dayy").value = date ;
    document.querySelector("#exam-registration-id").value = exam_registration_id ;
}

