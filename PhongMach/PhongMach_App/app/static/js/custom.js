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