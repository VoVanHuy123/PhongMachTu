
//chọn thuốc
function selectMedicine(medicine) {
  const medicineNameInput = document.getElementById('medicineName');
  const medicineUnitSelect = document.getElementById('medicineUnit');
  const medicineQuantityInput = document.getElementById('medicineQuantity');
  const medicineUsageInput = document.getElementById('medicineUsage');
  const medicineInventory = document.getElementById('medicineInventory');
  const addMedId = document.getElementById('add_med_id');

  // Điền thông tin thuốc vào các trường nhập liệu
  medicineNameInput.value = medicine.name;
  addMedId.value = medicine.id;
  medicineUnitSelect.innerHTML = '<option value="" disabled selected>Chọn đơn vị</option>';
  if (medicine.unit_list && medicine.unit_list.length > 0) {
      medicine.unit_list.forEach(unit => {
          const option = document.createElement('option');
          option.value = unit.unit_id;
          option.textContent = unit.unit_name;
          // console.log (option.textContent);
          medicineUnitSelect.appendChild(option);
      });
  }


  medicineUnitSelect.value = medicine.unit_default.id || ''; // Chọn đơn vị nếu có
  medicineInventory.value = medicine.inventory;
  medicineQuantityInput.value = 1; // Mặc định số lượng là 1
  medicineUnitSelect.addEventListener('change', function () {
      const selectedUnitId = this.value;
      if(selectedUnitId == medicine.unit_default.id){
        medicineInventory.value = medicine.inventory;
      }
      else{
        for(let convert of medicine.unit_convert_list ){
          if(convert.target_unit_id == selectedUnitId){
            medicineInventory.value = medicine.inventory/convert.convert_rate;
          }
        }
      };
      
  });

};


  // modal search med
document.addEventListener('DOMContentLoaded', function () {
  window.selectMedicine = selectMedicine;
  const searchInput = document.getElementById('searchMedicine');
  const categorySelect = document.getElementById('medicineSelect');
  const medicineList = document.querySelector('.medicine-list-group');

  const confirmAddMedicineButton = document.getElementById('confirmAddMedicine');
  const medicineTableBody = document.getElementById('table-body-med-list');
    

    // Lắng nghe sự kiện tìm kiếm thuốc=============================================
  function fetchMedicines() {
    const query = searchInput.value.trim();
    const category = categorySelect.value;


    fetch(`/doctor_user/api/search_medicine?query=${query}&category=${category}`)
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


    







  // sự kiện xác nhận thêm thuốc=======================================================
  confirmAddMedicineButton.addEventListener('click', async () => {
    // Lấy thông tin thuốc từ modal
    const medicineName = document.getElementById('medicineName').value;
    const medicineUnit = document.getElementById('medicineUnit');
    const selectedValueText = medicineUnit.options[medicineUnit.selectedIndex].text;
    const selectedValueId =medicineUnit.value;
    const medicineQuantity = document.getElementById('medicineQuantity').value;
    const medicineUsage = document.getElementById('medicineUsage').value;
    const selected_medicine_id = document.getElementById('add_med_id').value;
    
  
    // Kiểm tra thông tin có hợp lệ không
    if (!medicineName || !medicineUnit || !medicineQuantity || !medicineUsage) {
      showToast('Vui lòng nhập đầy đủ thông tin thuốc!','error')
      return;
    }
    try {
      // Gửi yêu cầu đến backend
      const response = await fetch('/doctor_user/api/add_medicine', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              medicine_id: parseInt(selected_medicine_id),
              unit_id: parseInt(selectedValueId) ,
              quantity: parseFloat(medicineQuantity),
          }),
      });
      console.log("1")
      const data = await response.json();

      if (!response.ok) {
          // Hiển thị thông báo lỗi từ backend
          console.error("Error from backend:", data.message); // Log lỗi backend
          showToast(data.message,'error');
          // alert(data.message);
          return;
      }
      else{
        // Nếu thành công, thêm thuốc vào danh sách
        //lấy danh sách đơn vị của thuốc
        const list_unit = data.list_unit;
        
          

          // Kiểm tra xem thuốc đã tồn tại trong bảng chưa
          const existingRow = Array.from(medicineTableBody.querySelectorAll('tr')).find(row => {
            const medIdInput = row.querySelector('#selected_medicine_id');
            const unitIdInput = row.querySelector('#selected_unit_id');
            return (
                medIdInput && unitIdInput &&
                parseInt(medIdInput.value) === parseInt(selected_medicine_id) &&
                parseInt(unitIdInput.value) === parseInt(selectedValueId)
            );
        });

        if (existingRow) {
          // Thuốc đã tồn tại -> Cập nhật số lượng và cách dùng
          const quantityCell = existingRow.querySelector('.col-quantity');
          const usageCell = existingRow.querySelector('.col-med-usage');

          // Cập nhật số lượng
          const currentQuantity = parseFloat(quantityCell.textContent);
          const updatedQuantity = currentQuantity + parseFloat(medicineQuantity);
          quantityCell.textContent = updatedQuantity;
          // Cập nhật cách dùng
          usageCell.textContent = medicineUsage;

          showToast('Cập nhật thành công số lượng và cách dùng thuốc!', 'success');
        } else {
          // Tạo một dòng mới trong bảng
          const newRow = document.createElement('tr');
          // Chuyển danh sách unit sang dạng JSON để lưu vào `data-units`
          const unitsData = JSON.stringify(list_unit);
          newRow.setAttribute('data-units', unitsData);
        
          // Lấy số thứ tự hiện tại từ bảng (tự động tăng STT)
          const currentRowCount = medicineTableBody.querySelectorAll('tr').length;
          const newRowHTML = `
            
            <input type = "hidden" id = "selected_medicine_id" value = "${selected_medicine_id}">
            <input type = "hidden" id = "selected_unit_id" value = "${selectedValueId}">
            <td>${currentRowCount + 1}</td>
            
            <td>
              <p class = "col-med-name">${medicineName}</p>
            </td>
            <td>
              <p class = "col-med-unit">${selectedValueText}</p>
            </td>
            <td>
              <p class = "col-quantity">${medicineQuantity}</p>
            </td>
            <td>
              <p class = "col-med-usage">${medicineUsage}</p>
            </td>
            <td>
              <button class="btn btn-primary btn-sm btn-med btn-edit-med">
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
          showToast(data.message,'success');
        }
        
          // Đóng modal
          const modal = document.getElementById('addMedicineModal');
          const modalInstance = bootstrap.Modal.getInstance(modal);
          modalInstance.hide();
          document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());

          modal.addEventListener('hidden.bs.modal', function () {
              // Khôi phục lại các thuộc tính của body
              document.body.style.overflow = '';         // Khôi phục overflow
              document.body.style.paddingRight = '';     // Loại bỏ padding-right
          });
          

          // Xóa dữ liệu cũ trong modal
          document.getElementById('medicineName').value = '';
          document.getElementById('medicineUnit').value = '';
          document.getElementById('medicineQuantity').value = 1;
          document.getElementById('medicineUsage').value = '';
      // TODO: Cập nhật giao diện thêm thuốc vào bảng
      }


      
      
  } catch (error) {
      console.error('Lỗi:', String(error));
      alert('Đã xảy ra lỗi khi thêm thuốc.');
      return;
  }
  
  });




  //sự kiện xác nhận đơn thuốc==============================================================
  document.getElementById("confirm-medical-exam").addEventListener("click", async () => {
    const diagnosis = document.getElementById("diagnosis").value;
    const examDate = document.getElementById("examDate").innerText;
    const patientId = document.getElementById("patient-id").value; 
    const examRegistrationId = document.getElementById("exam-registration-id").value


    

    // Thu thập thông tin thuốc
    const medicines = Array.from(document.querySelectorAll("#table-body-med-list tr")).map(row => {
        const cells = row.querySelectorAll("td"); 
        const med_id = row.querySelector("#selected_medicine_id")
        if (med_id) {
          console.log("Element found:", med_id);
        } else {
            console.log("Element not found");
        }
        const selected_unit_id = row.querySelector("#selected_unit_id")
        if (selected_unit_id) {
          console.log("Element found:", selected_unit_id);
        } else {
            console.log("Element not found");
        }
        return {
            name: cells[1].innerText,
            unit: cells[2].innerText,
            quantity: parseFloat(cells[3].innerText),
            instruct: cells[4].innerText,
            med_id : parseInt(med_id.value),
            selected_unit_id : parseInt(selected_unit_id.value)
        };
    });
    
    if(diagnosis && medicines.length != 0){
      // Gửi dữ liệu đến backend
      const response = await fetch("/doctor_user/api/create-medical-exam", {
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
      // Redirect 
      window.location.href = result.redirect_url;
    } else {
      
        console.error(result.message);
        alert("Failed to create medical exam.");
    }
    }
    else{
      if(!diagnosis){
        alert("Vui lòng nhập chuẩn đoán");
      }else {
        alert("Vui lòng thêm thuốc");
      }
    }
  });



  //sự kiện xóa / edit==========================================================================
  // Lắng nghe sự kiện xóa / edit trên bảng 
  document.getElementById("table-body-med-list").addEventListener("click", function (event) {
    if (event.target.classList.contains("btn-delete-med") || event.target.closest(".btn-delete-med")) {
      
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
    else if (event.target.classList.contains("btn-edit-med") || event.target.closest(".btn-edit-med")) {
      
      const row = event.target.closest("tr");
  
      // Lấy thông tin thuốc từ dòng
      const medicineName = row.querySelector(".col-med-name").innerText;
      const selectedUnitId = row.querySelector("#selected_unit_id").value;
      const medicineQuantity = row.querySelector(".col-quantity").innerText;
      const medicineUsage = row.querySelector(".col-med-usage").innerText;

      // Lấy danh sách đơn vị từ `data-units` đã lưu vào tr trước đó
      const unitsData = JSON.parse(row.getAttribute("data-units"));
  
      // Điền dữ liệu vào modal
      document.getElementById("editMedicineName").value = medicineName;
      document.getElementById("editMedicineQuantity").value = medicineQuantity;
      document.getElementById("editMedicineUsage").value = medicineUsage;

      const editMedicineUnit = document.getElementById("editMedicineUnit");
      editMedicineUnit.innerHTML = '<option value="" disabled>Chọn đơn vị</option>';
      // Thêm danh sách đơn vị vào `editMedicineUnit`
      unitsData.forEach(unit => {
        const option = document.createElement("option");
        option.value = unit.id;
        option.textContent = unit.name;

        // Chọn đơn vị hiện tại
        if (unit.id == selectedUnitId) {
          option.selected = true;
        }

        editMedicineUnit.appendChild(option);
      });
  
      // Hiển thị modal
      const editModal = new bootstrap.Modal(document.getElementById("editMedicineModal"));
      
      editModal.show();
  
      // Lưu lại hàng được chỉnh sửa
      window.currentEditRow = row;
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
  };

  // hàm cập nhật thông tin hàng =======
  function updateRow(){
    // Lấy thông tin từ modal
    const newUnitId = document.getElementById("editMedicineUnit")
    const newQuantity = document.getElementById("editMedicineQuantity").value;
    const newUsage = document.getElementById("editMedicineUsage").value;
  
    if (!newQuantity || !newUsage) {
      showToast("Vui lòng nhập đầy đủ thông tin!", "error");
      return;
    }
  
    // Cập nhật thông tin trên bảng
    const unitIdValue = window.currentEditRow.querySelector("#selected_unit_id");
    const unitName = window.currentEditRow.querySelector(".col-med-unit");
    const quantityCell = window.currentEditRow.querySelector(".col-quantity");
    const usageCell = window.currentEditRow.querySelector(".col-med-usage");
    quantityCell.textContent = newQuantity;
    usageCell.textContent = newUsage;
    unitIdValue.value = newUnitId.value
    unitName.textContent = newUnitId.options[newUnitId.selectedIndex].textContent;
  
    // Đóng modal
    const editModal = bootstrap.Modal.getInstance(document.getElementById("editMedicineModal"));
    editModal.hide();
    // document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
  
    // Xóa tham chiếu đến hàng hiện tại
    window.currentEditRow = null;
  
    showToast("Cập nhật thuốc thành công!", "success");
  };
  //thêm sự kiện xác nhận thay đổi thuốc========================================
  document.getElementById("confirmEditMedicine").addEventListener("click", () => {
    if (!window.currentEditRow) return;
    updateRow()
    
  });



  
  // thêm sự kiện lập danh phiếu khám============================================
  document.getElementById('createMedicalExam').addEventListener('click', function () {
    // event.preventDefault();  // Ngăn việc gửi form
    console.log("Button clicked");
    // Lấy giá trị của các trường input
    console.log("vào");
    const patientId = document.getElementById('patient-id').value.trim();
    const examDay = document.getElementById('exam-dayy').value.trim();
    const examRegistrationId = document.getElementById('exam-registration-id').value.trim();

    // Kiểm tra nếu tất cả các trường đã có giá trị
    if (patientId && examDay && examRegistrationId) {
        // Nếu hợp lệ, submit form
        document.getElementById('createMedExamForm').submit();
    } else {
        // Nếu không hợp lệ, thông báo cho người dùng
        alert('Vui lòng điền đầy đủ thông tin trước khi lập phiếu khám!');
    }
});


});