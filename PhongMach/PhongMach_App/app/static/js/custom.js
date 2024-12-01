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

//chọn thuốc
function selectMedicine(medicine) {

  const medicineNameInput = document.getElementById('medicineName');
  const medicineUnitSelect = document.getElementById('medicineUnit');
  const medicineQuantityInput = document.getElementById('medicineQuantity');
  const medicineUsageInput = document.getElementById('medicineUsage');

  // Điền thông tin thuốc vào các trường nhập liệu
  medicineNameInput.value = medicine.name;

  medicineUnitSelect.innerHTML = '<option value="" disabled selected>Chọn đơn vị</option>';
  if (medicine.unit_list && medicine.unit_list.length > 0) {
      medicine.unit_list.forEach(unit => {
          const option = document.createElement('option');
          option.value = unit;
          option.textContent = unit;
          medicineUnitSelect.appendChild(option);
      });
  }

  medicineUnitSelect.value = medicine.unit || ''; // Chọn đơn vị nếu có
  medicineQuantityInput.value = 1; // Mặc định số lượng là 1
}
// modal search med
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchMedicine');
    const categorySelect = document.getElementById('medicineSelect');
    const medicineList = document.querySelector('.medicine-list-group');

    const confirmAddMedicineButton = document.getElementById('confirmAddMedicine');
    const medicineTableBody = document.getElementById('table-body-med-list');
    

    // Lắng nghe sự kiện tìm kiếm thuốc
    function fetchMedicines() {
      const query = searchInput.value.trim();
      const category = categorySelect.value;


      fetch(`/doctor_user/search_medicine?query=${query}&category=${category}`)
        .then(response => response.json())
        .then(data => {
          medicineList.innerHTML = ''; // Xóa danh sách cũ
          if (data.length === 0) {
            medicineList.innerHTML = `<div class="text-center text-muted">Không tìm thấy thuốc</div>`;
            return;
          }
          data.forEach(medicine => {
            const button = document.createElement('button');
            button.type = 'button';
            button.classList.add('list-group-item', 'list-group-item-action');
            button.textContent = medicine.name;
            button.dataset.id = medicine.id; // Gán ID thuốc vào data attribute
            button.dataset.unit = medicine.unit;
            console.log(medicine.unit)
            button.addEventListener('click', () => selectMedicine(medicine));
            medicineList.appendChild(button);
          });
        })
        .catch(error => {
          console.error('Error fetching medicines:', error);
        });
    }
    searchInput.addEventListener('input', fetchMedicines);
    categorySelect.addEventListener('change', fetchMedicines);


    

    // sự kiện xác nhận thêm thuốc
    confirmAddMedicineButton.addEventListener('click', () => {
      // Lấy thông tin thuốc từ modal
      const medicineName = document.getElementById('medicineName').value;
      const medicineUnit = document.getElementById('medicineUnit').value;
      const medicineQuantity = document.getElementById('medicineQuantity').value;
      const medicineUsage = document.getElementById('medicineUsage').value;
    
      // Kiểm tra thông tin có hợp lệ không
      if (!medicineName || !medicineUnit || !medicineQuantity || !medicineUsage) {
        alert('Vui lòng nhập đầy đủ thông tin thuốc!');
        return;
      }
    
      // Tạo một dòng mới trong bảng
      const newRow = document.createElement('tr');
    
      // Lấy số thứ tự hiện tại từ bảng (tự động tăng STT)
      const currentRowCount = medicineTableBody.querySelectorAll('tr').length;
      const newRowHTML = `
        <td>${currentRowCount + 1}</td>
        
        <td>
          <p>${medicineName}</p>
        </td>
        <td>
          <p>${medicineUnit}</p>
        </td>
        <td>
          <p>${medicineQuantity}</p>
        </td>
        <td>
          <p >${medicineUsage}</p>
        </td>
        <td>
          <button class="btn btn-primary btn-sm btn-med">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-danger btn-sm btn-med btn-delete-med">
            <i class="bi bi-x-circle"></i>
          </button>
        </td>
      `;
      newRow.innerHTML = newRowHTML;
    
      // Thêm dòng mới vào bảng
      medicineTableBody.appendChild(newRow);
    
      // Đóng modal
      const modal = document.getElementById('addMedicineModal');
      const modalInstance = bootstrap.Modal.getInstance(modal);
      modalInstance.hide();
    
      // Xóa dữ liệu cũ trong modal
      document.getElementById('medicineName').value = '';
      document.getElementById('medicineUnit').value = '';
      document.getElementById('medicineQuantity').value = 1;
      document.getElementById('medicineUsage').value = '';
    });


    //sự kiện xác nhận đơn thuốc
    document.getElementById("confirm-medical-exam").addEventListener("click", async () => {
      const diagnosis = document.getElementById("diagnosis").value;
      const examDate = document.getElementById("examDate").innerText;
      const patientId = document.getElementById("patient-id").value; 
      const examRegistrationId = document.getElementById("exam-registration-id").value
  
      // Thu thập thông tin thuốc
      const medicines = Array.from(document.querySelectorAll("#table-body-med-list tr")).map(row => {
          const cells = row.querySelectorAll("td"); 
          return {
              name: cells[1].innerText,
              unit: cells[2].innerText,
              quantity: parseFloat(cells[3].innerText),
              instruct: cells[4].innerText
          };
      });
  
      // Gửi dữ liệu đến backend
      const response = await fetch("/doctor_user/create-medical-exam", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({
              diagnosis,
              examDate,
              patientId,
              medicines,
              examRegistrationId,
          }),
      });
  
      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        alert("Success create medical exam.");
        // Redirect 
        window.location.href = result.redirect_url;
      } else {
          console.error(result.message);
          alert("Failed to create medical exam.");
      }
    });

    //sự kiện xóa
    // Lắng nghe sự kiện xóa trên bảng
    document.getElementById("table-body-med-list").addEventListener("click", function (event) {
      if (event.target.classList.contains("btn-delete-med") || event.target.closest(".btn-delete-med")) {
        console.log("zo");
          // Tìm đến dòng cha (<tr>) chứa nút xóa
          const row = event.target.closest("tr");

          // Hiển thị xác nhận xóa
          const isConfirmed = confirm("Are you sure you want to delete this row?");
          if (isConfirmed) {
              // Xóa dòng khỏi bảng
              row.remove();

              // Cập nhật lại số thứ tự (STT)
              updateRowNumbers();
          }
      }
    });

  // Hàm cập nhật lại STT sau khi xóa
    function updateRowNumbers() {
      const rows = document.querySelectorAll("#table-body-med-list tr");
      rows.forEach((row, index) => {
          const firstCell = row.querySelector("td:first-child");
          if (firstCell) {
              firstCell.textContent = index + 1; // Cập nhật số thứ tự (1-based index)
          }
      });
    }
});