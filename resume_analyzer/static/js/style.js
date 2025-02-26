document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#resumeForm").addEventListener("submit", function (event) {
        let fileInput = document.querySelector("input[type='file']");
        if (!fileInput.value) {
            alert("Please select a resume file to upload!");
            event.preventDefault();
        }
    });
});
