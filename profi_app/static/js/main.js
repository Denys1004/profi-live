
const navSlide = () =>{
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    // to add animation what we build in css (@keyframes navLinkFade), we grabing individual links (.nav-links li)
    const navLinks = document.querySelectorAll('nav .nav-links li');

    burger.addEventListener('click', ()=>{ 
        nav.classList.toggle('nav-active');

        //Animate Links
        navLinks.forEach((link, index) =>{
            if(link.style.animation){
                link.style.animation = '';
            }else{
                link.style.animation = `navLinkFade 0.4s ease forwards ${index / 10}s`;
            }
        });

        // Burger Animation (to make it cross)
        burger.classList.toggle('toggle');

    });
}
navSlide();



// scroll to top
const btnScrollToTop = document.querySelector("#btnScrollToTop");
btnScrollToTop.addEventListener("click", function () {
  $("html, body").animate({ scrollTop: 0 }, "slow");
});

$(window).scroll(function() {
    if ($(this).scrollTop()) {
        $('#scroll-arrow:hidden').stop(true, true).fadeIn();
    } else {
        $('#scroll-arrow').stop(true, true).fadeOut();
    }
});



$('.alert').alert()
