




        $(document).ready(function(){
            $(window).scroll(function(){
                // Sticky navbar on scroll
                if(this.scrollY > 20){
                    $('.navbar').addClass("sticky");
                } else {
                    $('.navbar').removeClass("sticky");
                }

                // Scroll-up button show/hide
                if(this.scrollY > 500){
                    $('.scroll-up-btn').addClass("show");
                } else {
                    $('.scroll-up-btn').removeClass("show");
                }
            });

            // Slide-up script
            $('.scroll-up-btn').click(function(){
                $('html').animate({scrollTop: 0});
                $('html').css("scrollBehavior", "auto");
            });

            // Smooth scroll on menu items click
            $('.navbar .menu li a').click(function(){
                $('html').css("scrollBehavior", "smooth");
            });

            // Toggle menu/navbar script
            $('.menu-btn').click(function(){
                $('.navbar .menu').toggleClass("active");
                $('.menu-btn i').toggleClass("active");
            });

            // Typing effect for "Coding is ..." using Typed.js
            new Typed(".typing-coding", {
                strings: ["like Art", "the Future", "Everything"],
                typeSpeed: 100,
                backSpeed: 60,
                loop: true
            });

            // Typing effect for "Hello, my name is ..." using Typed.js
            new Typed(".typing-name", {
                strings: ["", "Guillermo", "Iranzo"],
                typeSpeed: 100,
                backSpeed: 60,
                loop: true
            });

            // Typing effect for the section "home" using Typed.js
            new Typed(".typing", {
                strings: ["Front-End Developer", "Web Designer"],
                typeSpeed: 100,
                backSpeed: 60,
                loop: true
            });
        });
        
      
    