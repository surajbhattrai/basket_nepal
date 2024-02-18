(function () {
    var swiper = new Swiper('.hero-section', {
        autoplay: true,
        loop: true,
        autoplay: {
        disableOnInteraction: false,
        delay: 4000,
        },
        navigation: {
        nextEl: '.hero-section-button-next',
        prevEl: '.hero-section-button-prev',
        },
    });

    var responsiveBreakpoint = new Swiper('.store-slider', {
    slidesPerView: 2,
    spaceBetween: 10,
    loop: true,
    navigation: {
        nextEl: '.store-slider-button-next',
        prevEl: '.store-slider-button-prev',
        },
    breakpoints: {
        640: {
        slidesPerView: 2,
        spaceBetween: 20,
        },
        768: {
        slidesPerView: 4,
        spaceBetween: 40,
        },
        1024: {
        slidesPerView: 6,
        spaceBetween: 20,
        },
    }
    });

    var navigation = new Swiper('.js-swiper-navigation', {
        navigation: {
          nextEl: '.js-swiper-navigation-button-next',
          prevEl: '.js-swiper-navigation-button-prev',
        },
      });

    
      
    // Product Slider

    var galleryThumbs = new Swiper('.js-swiper-gallery-thumbs', {
        spaceBetween: 0,
        slidesPerView: 5,
        freeMode: true,
        watchSlidesVisibility: true,
        watchSlidesProgress: true,
    });

    var galleryTop = new Swiper('.js-swiper-gallery-main', {
        autoplay: true,
        loop: true,
        spaceBetween: 10,
        navigation: {
            nextEl: '.js-swiper-gallery-button-next',
            prevEl: '.js-swiper-gallery-button-prev',
        },
        thumbs: {
            swiper: galleryThumbs
        }
    });
})()


