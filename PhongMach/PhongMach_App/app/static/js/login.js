document.addEventListener('DOMContentLoaded', async function () {

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        let isValid = true;
    
        // Lấy giá trị từ các trường nhập
        const userName = document.getElementById('user-name').value.trim();
        const password = document.getElementById('password').value.trim();
        const errMsg = document.getElementById('msg-alert').textContent.trim();
        console.log(errMsg);
    
        // Reset thông báo lỗi
        document.getElementById('user-name-error').textContent = '';
        document.getElementById('password-error').textContent = '';
    
        // Kiểm tra tên đăng nhập
        if (userName === '') {
          document.getElementById('user-name-error').textContent = 'Vui lòng nhập tên đăng nhập!';
          isValid = false;
        } else if (userName.length < 3) {
          document.getElementById('user-name-error').textContent = 'Tên đăng nhập phải có ít nhất 3 ký tự!';
          isValid = false;
        }
    
        // Kiểm tra mật khẩu
        if (password === '') {
          document.getElementById('password-error').textContent = 'Vui lòng nhập mật khẩu!';
          isValid = false;  }
        // } else if (errMsg) {
        //   document.getElementById('password-error').textContent = 'Vui lòng nhập đúng mật khẩu';
        //   isValid = false;
        // }
    
        // Ngăn biểu mẫu gửi đi nếu không hợp lệ
        if (!isValid) {
          event.preventDefault();
        }
      });
});
