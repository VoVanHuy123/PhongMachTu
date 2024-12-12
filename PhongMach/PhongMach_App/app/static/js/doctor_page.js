document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('createMedicalExam').addEventListener('click', function() {
        
        // Thực hiện hành động của bạn ở đây
        const patientId = document.getElementById('patient-id').value.trim();
        const examDay = document.getElementById('exam-dayy').value.trim();
        const examRegistrationId = document.getElementById('exam-registration-id').value.trim();
        const form = document.getElementById('createMedExamForm');
        const urlForCreateMedical = document.getElementById('urlForCreateMedical').value.trim();
        // Đổi action của form thành 'doctor_user.create_medical'
        form.action = `${urlForCreateMedical}`;

        // Kiểm tra nếu tất cả các trường đã có giá trị
        if (patientId && examDay && examRegistrationId) {
            // Nếu hợp lệ, submit form
            form.submit();
        } else {
            // Nếu không hợp lệ, thông báo cho người dùng
            alert('Vui lòng điền đầy đủ thông tin trước khi lập phiếu khám!');
        }
    }); 
    document.getElementById('medicHistoryButton').addEventListener('click', async function() {
        
        // Thực hiện hành động của bạn ở đây
        const patientId = document.getElementById('patient-id').value.trim();
        const urlForPatientHistory = document.getElementById('urlForPatientHistory').value.trim();
        
        const form = document.getElementById('createMedExamForm');
        // Đổi action của form thành 'doctor_user.create_medical'
        form.action = `${urlForPatientHistory}`;
        form.submit();
       
        
    }); 
    
    
    
});