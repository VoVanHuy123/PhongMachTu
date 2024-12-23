function examTimeRender(selectedDate){
    let doctorId = document.getElementById("doctor_id").value
    document.getElementById("exam_day").value = selectedDate
    updateExamTimes(selectedDate,doctorId)
}

async function updateExamTimes(selectedDate,doctorId){
    const scheduleContainer = document.querySelector('.schedule');
    // Gửi yêu cầu tới API
    const response = await fetch('/appointment/api/get_exam_times', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            doctor_id: doctorId,
            exam_day: selectedDate,
        }),
    });

    const data = await response.json();
    // Xóa nội dung cũ
    scheduleContainer.innerHTML = '';
    
    if(data.is_available){
        data.exam_times.forEach(time => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = `btn w-100 time-slot ${time.is_booked || time.status === 'disabled' ? 'is-booked' : 'btn-success'}`;
            button.innerHTML = `${time.start_time} - ${time.end_time}`;
            if (time.is_booked || time.status === 'disabled') {
                button.disabled = true;
            } else {
                button.onclick = function () {
                    document.getElementById('exam_time_id').value = time.id;
                    document.getElementById('appoint_detail_form').submit();
                };
            }
            console.log("vào");
            const col = document.createElement('div');
            col.className = 'col-2 mb-3';
            col.appendChild(button);
    
            scheduleContainer.appendChild(col);
        });
    } else{
        const msg = document.createElement('h5');
        msg.textContent = "Số Lượng bệnh nhân đã đủ cho ngày hôm nay! xin lỗi vì sự bất tiện này"
        scheduleContainer.appendChild(msg);
    }
    // Render danh sách giờ khám
    
}