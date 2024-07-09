window.onscroll = function() {
    scrollFunction();
    hideCarouselIndicators();
};

function scrollFunction() {
    if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
        document.querySelector('.header').classList.add('fixed');
    } else {
        document.querySelector('.header').classList.remove('fixed');
    }
}

function hideCarouselIndicators() {
    var scrollPosY = window.scrollY;

    // 모든 캐러셀 인디케이터 버튼 가져오기
    var carouselButtons = document.querySelectorAll('#MainCarousel .carousel-indicators button');

    // 스크롤 위치가 0보다 클 경우 버튼 숨기기
    if (scrollPosY > 0) {
        carouselButtons.forEach(function(button) {
            button.style.display = 'none';
        });
    } else {
        carouselButtons.forEach(function(button) {
            button.style.display = 'block'; // 기본 값으로 변경하거나 필요에 따라 다른 값 설정
        });
    }
}


document.addEventListener("DOMContentLoaded", function() {
    const hamburgerIcon = document.getElementById('Sidebar-control');
    const sidebar = document.querySelector('.sidebar');

    hamburgerIcon.addEventListener('click', function(e) {
        e.preventDefault();
        sidebar.classList.toggle('active');
    });
});

window.addEventListener('scroll', function() {
    // Calculate the scroll position
    var scrollPos = window.scrollY;

    // Adjust the top position based on scroll position
    var carousel = document.getElementById('MainCarousel');
    carousel.style.top = scrollPos / 2 + 'px'; // Adjust the division factor as needed
});