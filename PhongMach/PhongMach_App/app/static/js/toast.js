export function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');

    // Tạo thông báo mới
    const toast = document.createElement('div');
    toast.className = `toastt ${type}`;
    toast.textContent = message;

    // Thêm thông báo vào container
    toastContainer.appendChild(toast);

    // Tự động xóa thông báo sau 3 giây
    setTimeout(() => {
        toast.remove();
    }, 3000);
}