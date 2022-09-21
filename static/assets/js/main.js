(function () {
    "use strict";

    // select helper
    const select = (el, all = false) => {
      el = el.trim()
      if (all) {
        return [...document.querySelectorAll(el)]
      } else {
        return document.querySelector(el)
      }
    }

    // event listener setter
    const on = (type, el, listener, all = false) => {
      let selectElement = select(el, all)
      if (selectElement) {
        if (all) {
          selectElement.forEach(e => e.addEventListener(type, listener))
        } else {
          selectElement.addEventListener(type, listener)
        }
      }
    }

    // listener for scroll
    const onscroll = (el, listener) => {
      el.addEventListener('scroll', listener)
    }

    // header onscroll animation
    let selectHeader = select('#header')
    if (selectHeader) {
      const headerScrolled = () => {
        if (window.scrollY > 100) {
          selectHeader.classList.add('header-scrolled')
        } else {
          selectHeader.classList.remove('header-scrolled')
        }
      }
      window.addEventListener('load', headerScrolled)
      onscroll(document, headerScrolled)
    }

    // logo onscroll animation
    let selectLogo = select('#small-img-logo')
    if (selectLogo) {
      const logoScrolled = () => {
        if (window.scrollY > 400) {
          selectLogo.classList.add('small-logo-scrolled')
        } else {
          selectLogo.classList.remove('small-logo-scrolled')
        }
      }
      window.addEventListener('load', logoScrolled)
      onscroll(document, logoScrolled)
    }

    // shevron arrow onscroll animation
    let selectArrow = select('.arrow')
    if (selectArrow) {
      const arrowScrolled = () => {
        if (window.scrollY > 80) {
          selectArrow.classList.add('arrow-scrolled')
        } else {
          selectArrow.classList.remove('arrow-scrolled')
        }
      }
      window.addEventListener('load', arrowScrolled)
      onscroll(document, arrowScrolled)
    }

    // mobile navbar
    on('click', '.mobile-nav-toggle', function (e) {
      select('#navbar').classList.toggle('navbar-mobile')
      this.classList.toggle('bi-list')
      this.classList.toggle('bi-x')
    })

    // Preloader
    let loader = select('#loader');
    if (loader) {
      window.addEventListener('load', () => {
        loader.remove()
      });
    }

    // Animation on scroll   
    window.addEventListener('load', () => {
      AOS.init({
        duration: 1000,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      })
    });

    // back to the top
    let backtotop = select('.back-to-top')
    if (backtotop) {
      const toggleBacktotop = () => {
        if (window.scrollY > 100) {
          backtotop.classList.add('active')
        } else {
          backtotop.classList.remove('active')
        }
      }
      window.addEventListener('load', toggleBacktotop)
      onscroll(document, toggleBacktotop)
    }
    
    // navbar links active state on scroll
    let navbarlinks = select('#navbar .scrollto', true)
    const navbarlinksActive = () => {
      let position = window.scrollY + 200
      navbarlinks.forEach(navbarlink => {
        if (!navbarlink.hash) return
        let section = select(navbarlink.hash)
        if (!section) return
        if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
          navbarlink.classList.add('active')
        } else {
          navbarlink.classList.remove('active')
        }
      })
    }
    window.addEventListener('load', navbarlinksActive)
    onscroll(document, navbarlinksActive)

    $(".geo").mouseover(function() {
      $(this).children(".preview").show();
    }).mouseout(function () {
      $(this).children(".preview").hide();
    });

    $(".alert").delay(3000).fadeOut(1000);

    })()