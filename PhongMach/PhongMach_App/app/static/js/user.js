document.addEventListener('DOMContentLoaded', function () {

    fetchProfile();
});

async function fetchProfile(){
    try {
        const response = await fetch("/auth/api/user_page/", { method: "GET" });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message);
        }

        const data = await response.json();
        updateUserInformation(data.user);
    } catch (error) {
        console.error("Error fetching profile:", error);
    }
        
};
function updateUserInformation(user) {
    const userInfor = document.getElementById("user-informations");

    userInfor.innerHTML = `
        <div class="text-center">
            <img src="${user.image}" alt="${user.first_name} ${user.last_name}" class="user-profile">
            <h3>${user.first_name} ${user.last_name}</h3>
            <p>${user.gender}</p>
            <p>${user.birth_day}</p>
            <div class="d-flex align-items-center justify-content-center mb-3">
                <i class="fas fa-star text-info"></i>
                <i class="fas fa-star text-info"></i>
                <i class="fas fa-star text-info"></i>
                <i class="fas fa-star text-info"></i>
                <i class="fas fa-star text-info"></i>
            </div>
        </div>
        <div class="personal-info container">
            <h3>Personal Information</h3>
            <ul class="personal-list">
                <li class="row align-items-center mb-3">
                    <div class="col-2 text-center">
                        <i class="bi bi-envelope-at"></i>
                    </div>
                    <div class="col-10 text-start">
                        ${user.email}
                    </div>
                </li>
                <li class="row align-items-center">
                    <div class="col-2 text-center">
                        <i class="bi bi-telephone"></i>
                    </div>
                    <div class="col-10 text-start">
                        ${user.phone_number ? user.phone_number : "No phone number available"}
                    </div>
                </li>
            </ul>
        </div>
        <a type="button" class="btn btn-small btn-block btn-success text-center d-flex justify-content-center align-items-center" href="#">
            Edit
        </a>
    `;
}