const toggleSpinner = () => {
    let loadingSpinners = document.querySelectorAll('.spinnerDisplay')

    loadingSpinners.forEach(function (spinner) {
        spinner.classList.toggle('d-none');
    });

    console.log("hell test")
}
let questionForm = document.getElementById("questionForm");

questionForm.addEventListener("submit", toggleSpinner);
