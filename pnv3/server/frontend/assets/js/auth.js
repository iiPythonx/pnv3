// Initialization
const button = document.querySelector(`[type = "submit"]`);

// Handle resetting status
const status = document.querySelector("#status");
for (const element of document.querySelectorAll("input")) {
    element.addEventListener("keydown", () => { status.innerText = ""; });
}

// Handle state switching
let state = "register";
function update() {
    state = state === "login" ? "register" : "login";
    document.querySelector("#switcher").innerHTML = `
        ${state === "login" ? "No hostname" : "Already have a host"}?
        <a href = "#" id = "switch-type">${state === "login" ? "Make one here." : "Log in here."}</a>
    `;
    document.querySelector(`[type = "submit"]`).innerText = state === "login" ? "Login" : "Create Hostname";
    document.querySelector("#switch-type").addEventListener("click", update);
    status.innerText = "";
}

update();

// Event handling
document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    // Handle API response
    const response = await post(state, {
        hostname: document.querySelector("#hostname").value,
        password: document.querySelector("#password").value
    });
    if (response.code !== 200) return status.innerText = response.data.message;

    document.cookie = `authorization=${response.data.token}; path=/`;
    window.location.href = "/";
});
