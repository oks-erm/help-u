(function () {
  'use strict';
  // select helper
  const select = (el, all = false) => {
    el = el.trim();
    if (all) {
      return [...document.querySelectorAll(el)];
    } else {
      return document.querySelector(el);
    }
  };

  // event listener setter
  const on = (type, el, listener, all = false) => {
    let selectElement = select(el, all);
    if (selectElement) {
      if (all) {
        selectElement.forEach((e) => e.addEventListener(type, listener));
      } else {
        selectElement.addEventListener(type, listener);
      }
    }
  };

  // listener for scroll
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener);
  };

  // header onscroll animation
  let header = $('#header');
  if (header) {
    const headerScrolled = () => {
      if ($(window).scrollTop() > 100) {
        header.addClass('header-scrolled');
      } else {
        header.removeClass('header-scrolled');
      }
    };
    $(window).on('load', headerScrolled);
    $(document).on('scroll', headerScrolled);
  }

  // logo onscroll animation
  let logo = $('#small-img-logo');
  if (logo) {
    const logoScrolled = () => {
      if ($(window).scrollTop() > 400) {
        logo.addClass('small-logo-scrolled');
      } else {
        logo.removeClass('small-logo-scrolled');
      }
    };
    $(window).on('load', logoScrolled);
    $(document).on('scroll', logoScrolled);
  }

  // shevron arrow onscroll animation
  let arrow = $('.arrow');
  if (arrow) {
    const arrowScrolled = () => {
      if ($(window).scrollTop() > 80) {
        arrow.addClass('arrow-scrolled');
      } else {
        arrow.removeClass('arrow-scrolled');
      }
    };
    $(window).on('load', arrowScrolled);
    $(document).on('scroll', arrowScrolled);
  }

  // mobile navbar
  on('click', '.mobile-nav-toggle', function (e) {
    select('#navbar').classList.toggle('navbar-mobile');
    this.classList.toggle('bi-list');
    this.classList.toggle('bi-x');
  });

  // Preloader
  let loader = $('#loader');
  if (loader) {
    $(window).on('load', () => {
      loader.remove();
    });
  }

  // Animation on scroll
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false,
    });
  });

  // back to the top
  let backtotop = $('.back-to-top');
  if (backtotop) {
    const toggleBacktotop = () => {
      if ($(window).scrollTop() > 100) {
        backtotop.addClass('active');
      } else {
        backtotop.removeClass('active');
      }
    };
    $(window).on('load', toggleBacktotop);
    $(document).on('scroll', toggleBacktotop);
  }

  // navbar links active state on scroll
  let navbarlinks = $('#navbar .scrollto');
  const navbarlinksActive = () => {
    let position = $(window).scrollTop() + 200;
    navbarlinks.each(function () {
      if (!$(this).attr('href')) return;
      let section = $(this).attr('href');
      if (!$(section).length) return;
      if (
        position >= $(section).offset().top &&
        position <= $(section).offset().top + $(section).height()
      ) {
        $(this).addClass('active');
      } else {
        $(this).removeClass('active');
      }
    });
  };
  $(window).on('load', navbarlinksActive);
  $(document).on('scroll', navbarlinksActive);

  //map toolkit
  $('.geo')
    .mouseover(function () {
      $(this).children('.preview').show();
    })
    .mouseout(function () {
      $(this).children('.preview').hide();
    });

  //messages
  $('.alert').delay(3000).fadeOut(1000);

  //modal
  $('#buttonClose').on('click', function () {
    $('.modal').hide();
    $('.modal-backdrop').hide();
  });
})();
