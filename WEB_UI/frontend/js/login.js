// login.js
// Mock implementation for login flow
function performLogin(username, password) {
    if(username === "admin" && password === "admin123") {
        localStorage.setItem("rover_auth_token", "mock_jwt_token_here");
        window.location.href = "security.html";
    } else {
        alert("Invalid credentials or account locked.");
    }
}
