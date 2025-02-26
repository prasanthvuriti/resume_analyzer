document.addEventListener("DOMContentLoaded", function () {
    let ctaButton = document.querySelector(".cta-button");
    if (ctaButton) {
        ctaButton.addEventListener("mouseover", function () {
            ctaButton.style.transform = "scale(1.15)";
            ctaButton.style.boxShadow = "0px 4px 8px rgba(255, 59, 125, 0.3)";
        });
        ctaButton.addEventListener("mouseout", function () {
            ctaButton.style.transform = "scale(1)";
            ctaButton.style.boxShadow = "none";
        });
    }
});
