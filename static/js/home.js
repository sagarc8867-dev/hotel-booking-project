/* ==========================================
   ROYAL STAY — HOME.JS
========================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ==========================
       CHECK-IN / CHECK-OUT DATES
    ========================== */

    const checkIn = document.getElementById('id_check_in');
    const checkOut = document.getElementById('id_check_out');

    if (checkIn && checkOut) {
        checkIn.addEventListener('change', function () {
            if (checkIn.value) {
                checkOut.min = checkIn.value;
                if (checkOut.value && checkOut.value <= checkIn.value) {
                    checkOut.value = '';
                }
            }
        });
    }


    /* ==========================
       FADE IN ON SCROLL
    ========================== */

    const cards = document.querySelectorAll(
        ".room-card,.testimonial-card"
    );

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0px)";
            }
        });
    }, {
        threshold: 0.15
    });

    cards.forEach(card => {
        card.style.opacity = "0";
        card.style.transform = "translateY(40px)";
        card.style.transition = ".7s ease";
        observer.observe(card);
    });

});