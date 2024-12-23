document.addEventListener("DOMContentLoaded", function () {
    // Lấy tất cả các nút có lớp 'btn-remove-unit'
    const removeButtons = document.querySelectorAll('.btn-remove-unit');

    removeButtons.forEach(button => {
        // Thêm sự kiện click vào mỗi nút 'Xóa'
        button.addEventListener('click', function() {
            // Lấy phần tử cha (unit-row) của nút 'Xóa'
            const unitRow = button.closest('.unit-row');

            // Xóa phần tử 'unit-row' khỏi DOM
            if (unitRow) {
                unitRow.remove();
            }
        });
    });

    document.getElementById('add-unit').addEventListener('click', async  function () {
        const unitList = document.getElementById('unit-list');
        const unitDiv = document.createElement('div');
        unitDiv.classList.add('row', 'align-items-center', 'mb-3','d-flex', 'justify-content-between','border','container','mt-2','p-3',"unit-row");

        let optionsHTML = '';
        try {
            const response = await fetch('/api/units');
            const units = await response.json();
            optionsHTML = units.map(unit => `<option value="${unit.id}">${unit.name}</option>`).join('');
        } catch (error) {
            alert('Không thể tải dữ liệu đơn vị.');
            return;
        }


        unitDiv.innerHTML = `
            
                <div class="">
                    <label class="form-label">Đơn Vị:</label>
                    <select class="form-select unit-select" required>
                        <option value="" disabled selected>Chọn đơn vị</option>
                        ${optionsHTML}
                    </select>
                </div>
                <div class="">
                    <label class="form-label">Giá:</label>
                    <input type="number" class="form-control unit-price" placeholder="Nhập giá" required>
                </div>
                <div class ="">
                    <label class="form-label">Quy Đổi:</label>
                    <input type = "number" class = "form-control convert-rate" placeholder="Nhập giá trị quy đổi" required>
                </div>
                <div class="text-end">
                    <button type="button" class="btn btn-danger btn-remove-unit">Xóa</button>
                </div>
        
        `;
        unitList.appendChild(unitDiv);

        

        // Xử lý sự kiện xóa đơn vị
        unitDiv.querySelector('.btn-remove-unit').addEventListener('click', function () {
            console.log("click")
            unitList.removeChild(unitDiv);
        });
    });

    function getData(){
        const medIdElement = document.getElementById('med-id')
        let medId = null;
        if (medIdElement){
            medId = medIdElement.value;
        }
        const medicineName = document.getElementById('medicine-name').value;
        const inventory = document.getElementById('inventory').value;
        const defaultUnit = document.getElementById('default-unit').value;
        const defaultUnitPrice = document.getElementById('default-unit-price').value;
        const categories = Array.from(document.getElementById('categories').selectedOptions).map(opt => opt.value);

        // const units = Array.from(document.querySelectorAll('.unit-select')).map((select, index) => {
        //     const unitId = select.value;
        //     const unitPrice = document.querySelectorAll('.unit-price')[index].value;
        //     const convertRate = document.querySelectorAll('.convert-rate')[index].value;
        //     return { unit_id: unitId, unit_price: unitPrice, convert_rate: convertRate };
        // });

        const unitElements = document.querySelectorAll('.unit-select');
        const units = unitElements.length > 0 ? Array.from(unitElements).map((select, index) => {
            const unitId = select.value || null;
            const unitPriceElement = document.querySelectorAll('.unit-price')[index];
            const convertRateElement = document.querySelectorAll('.convert-rate')[index];

            const unitPrice = unitPriceElement ? unitPriceElement.value : null;
            const convertRate = convertRateElement ? convertRateElement.value : null;

            return { unit_id: unitId, unit_price: unitPrice, convert_rate: convertRate };
        })
        : [];

        return {
            medId,
            medicine_name : medicineName,
            inventory,
            default_unit: defaultUnit,
            default_unit_price: defaultUnitPrice,
            categories,
            units,
        }
    }

    // Xử lý gửi dữ liệu
    const submuitBtn = document.getElementById('submit-btn');
    console.log(submuitBtn)
    if (submuitBtn) {
        submuitBtn.addEventListener('click', async function () {

            const data = getData()
    
            // Gửi dữ liệu qua API
            try {
                const response = await fetch('/admin/medicine/new/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });
    
                const result = await response.json();
                if (response.ok) {
                    alert(result.message);
                    window.location.href = result.redirect_url;
                } else {
                    alert(result.error || 'Có lỗi xảy ra.');
                }
            } catch (error) {
                alert('Không thể gửi dữ liệu.');
            }
        });
    }
    

    const editBtn = document.getElementById("edit-submit-btn");
    if (editBtn) {
        editBtn.addEventListener("click", async function () {
            const data = getData()
            try {

                const response = await fetch(`/admin/medicine/edit/${data.medId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });
                const result = await response.json();
                if (response.ok) {
                    alert(result.message);
                    // window.location.reload();
                    window.location.href = result.redirect_url;
                } else {
                    alert(result.error || 'Có lỗi xảy ra.');
                }
            } catch (error) {
                alert('Không thể gửi dữ liệu.');
            }
        });
    } else {
        console.error("edit-submit-btn không tồn tại trong DOM.");
    }
});


