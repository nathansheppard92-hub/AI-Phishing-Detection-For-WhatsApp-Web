
//confirmation the page has loaded
console.log("Permissions page loaded successfully")

document.addEventListener("DOMContentLoaded", () => {

    const submitButton = document.getElementById("submitButton");
    submitButton.addEventListener("click", submitFunction);
})

function submitFunction() 
{   
    document.body.classList.add("fade-out");

    setTimeout(() => {
        window.location.href = "index.html";
    }, 300);
}