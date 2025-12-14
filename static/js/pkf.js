$(document).ready(function () {

    var swiper = new Swiper ('.swiper-container', {
        pagination: '.swiper-pagination',
        effect: 'coverflow',
        preloadImages: true,
        updateOnImagesReady: true,
        observer: true,
        observeParents: true,
        autoHeight: true,
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        slidesPerView: '3',
        paginationHide: false,
        paginationClickable: true,
        coverflow: {
            rotate: 50,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows : true
        },
        breakpoints: {
            1024: {
                slidesPerView: 3
            },
            768: {
                slidesPerView: 3
            },
            480: {
                slidesPerView: 1
            },
            320: {
                slidesPerView: 1
            }
        }
    });

    $('#mp-logo-slider').slick({
        autoplay: true,
        autoplaySpeed: 3000,
        dots: false,
        arrows: true,
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });

    // Category page certificates slider call
    $('#mp-certificates-slider').slick({
        autoplay: true,
        autoplaySpeed: 3000,
        //dots: true,
        arrows: true,
        infinite: false,
        slidesToShow: 4,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                    //infinite: true,
                    //dots: true
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });

    lightbox.option({
        albumLabel: "Изображение %1 из %2"
    });


    $(function(){
        $('.navbar-mmenu .dropdown').hover(function() {
            // Handler in
            if ($(window).outerWidth() > 974) {
                // Desktop behavior
                $(this).addClass('open');
            } else {
                // Mobile behavior
            }
        }, function() {
            // Handler out
            if ($(window).outerWidth() > 974) {
                // Desktop behavior
                $(this).removeClass('open');
            } else {
                // Mobile behavior
            }
        });
    });

    // Scroll to top button
    $('#back-to-top').click(function () {
        $('#back-to-top').tooltip('hide');
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    }).tooltip();


    // Window scroll events
    $(window).scroll(function () {

        // Scroll to top behavior
        if ($(this).scrollTop() > 50) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }

        // Get sticky header height
        var stickyStartHeight = $('header').outerHeight() + $('.head').outerHeight() + $('.main-menu').outerHeight();

        // Sticky header behavior
        if ($(this).scrollTop() > stickyStartHeight) {
            $('.sticky-header').addClass("open");
        } else {
            $('.sticky-header').removeClass("open");
        }


        // Get sticky header height
        var stickyHeaderTopbar = stickyStartHeight;

        // Sticky header behavior
        if ($(this).scrollTop() > stickyHeaderTopbar) {
            $('.sticky-header-topbar').addClass("open");
        } else {
            $('.sticky-header-topbar').removeClass("open");
        }

    });

    $('.popup-youtube').magnificPopup({
        type: 'iframe'
        //type: 'image'
        // other options
    });






    $('.readmore-ul').readmore({ //вызов плагина
        speed: 250, //скорость раскрытия скрытого текста (в миллисекундах)
        //maxHeight: 85, //высота раскрытой области текста (в пикселях)
        collapsedHeight: 120,
        heightMargin: 0, //избегание ломания блоков, которые больше maxHeight (в пикселях)
        moreLink: '<div class="readmore-block"><a href="#" class="readmore">Показать ещё</a></div>', //ссылка "Читать далее", можно переименовать
        lessLink: '<div class="readmore-block"><a href="#" class="readmore">Скрыть</a></div>' //ссылка "Скрыть", можно переименовать
    });

    $(document).on( 'shown.bs.tab', 'a[data-toggle=\'tab\']', function (e) {
        $('.readmore-ul').readmore({ //вызов плагина
            speed: 250, //скорость раскрытия скрытого текста (в миллисекундах)
            //maxHeight: 85, //высота раскрытой области текста (в пикселях)
            collapsedHeight: 120,
            heightMargin: 0, //избегание ломания блоков, которые больше maxHeight (в пикселях)
            moreLink: '<div class="readmore-block"><a href="#" class="readmore">Показать ещё</a></div>', //ссылка "Читать далее", можно переименовать
            lessLink: '<div class="readmore-block"><a href="#" class="readmore">Скрыть</a></div>' //ссылка "Скрыть", можно переименовать
        });
    });

    // mmenu
    $("#mmenu").mmenu({
        //wrappers: ["bootstrap3"],
        "extensions": [
            "theme-dark",
            "border-full",
            "pagedim-black"
        ],
        "setSelected": {
            "hover": true
        }
    }, {
        language: "ru"
    });


    /*Панели*/
    $(document).on('click', '.panel-heading span.clickable', function (e) {
        var $this = $(this);
        if (!$this.hasClass('panel-collapsed')) {
            $this.parents('.panel').find('.panel-body').slideDown();
            $this.addClass('panel-collapsed');
        } else {
            $this.parents('.panel').find('.panel-body').slideUp();
            $this.removeClass('panel-collapsed');
        }
    });
    $(document).on('click', '.panel-click', function (e) {
        var $this = $(this);
        if (!$this.hasClass('panel-collapsed')) {
            $this.parents('.panel').find('.panel-body').slideDown();
            $this.addClass('panel-collapsed');
        } else {
            $this.parents('.panel').find('.panel-body').slideUp();
            $this.removeClass('panel-collapsed');
        }
    });



    $('.readmore-gost').readmore({ //вызов плагина
        speed: 250, //скорость раскрытия скрытого текста (в миллисекундах)
        collapsedHeight: 22,
        heightMargin: 0, //избегание ломания блоков, которые больше maxHeight (в пикселях)
        moreLink: '<div class="readmore-block"><a href="#" class="readmore">Показать ещё</a></div>', //ссылка "Читать далее", можно переименовать
        lessLink: '<div class="readmore-block"><a href="#" class="readmore">Скрыть</a></div>' //ссылка "Скрыть", можно переименовать
    });

    $('.readmore-stamp').readmore({ //вызов плагина
        speed: 250, //скорость раскрытия скрытого текста (в миллисекундах)
        collapsedHeight: 22,
        heightMargin: 0, //избегание ломания блоков, которые больше maxHeight (в пикселях)
        moreLink: '<div class="readmore-block"><a href="#" class="readmore">Показать ещё</a></div>', //ссылка "Читать далее", можно переименовать
        lessLink: '<div class="readmore-block"><a href="#" class="readmore">Скрыть</a></div>' //ссылка "Скрыть", можно переименовать
    });


});

$("h1 > a").click(function () {

    if($(".h1-block").hasClass("open")) {
        $(this).parents("h1").parent().removeClass("open");
    } else {
        $(this).parents("h1").parent().addClass("open");
    }
   
});


