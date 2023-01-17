/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./static/assets/js/main.js":
/*!**********************************!*\
  !*** ./static/assets/js/main.js ***!
  \**********************************/
/***/ ((module) => {

eval("function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }\nfunction _nonIterableSpread() { throw new TypeError(\"Invalid attempt to spread non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.\"); }\nfunction _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === \"string\") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === \"Object\" && o.constructor) n = o.constructor.name; if (n === \"Map\" || n === \"Set\") return Array.from(o); if (n === \"Arguments\" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }\nfunction _iterableToArray(iter) { if (typeof Symbol !== \"undefined\" && iter[Symbol.iterator] != null || iter[\"@@iterator\"] != null) return Array.from(iter); }\nfunction _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }\nfunction _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]; return arr2; }\nvar main = function () {\n  'use strict';\n\n  // select helper\n  var select = function select(el) {\n    var all = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;\n    el = el.trim();\n    if (all) {\n      return _toConsumableArray(document.querySelectorAll(el));\n    } else {\n      return document.querySelector(el);\n    }\n  };\n\n  // event listener setter\n  var on = function on(type, el, listener) {\n    var all = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : false;\n    var selectElement = select(el, all);\n    if (selectElement) {\n      if (all) {\n        selectElement.forEach(function (e) {\n          return e.addEventListener(type, listener);\n        });\n      } else {\n        selectElement.addEventListener(type, listener);\n      }\n    }\n  };\n\n  // listener for scroll\n  var onscroll = function onscroll(el, listener) {\n    el.addEventListener('scroll', listener);\n  };\n\n  // header onscroll animation\n  var selectHeader = select('#header');\n  if (selectHeader) {\n    var headerScrolled = function headerScrolled() {\n      if (window.scrollY > 100) {\n        selectHeader.classList.add('header-scrolled');\n      } else {\n        selectHeader.classList.remove('header-scrolled');\n      }\n    };\n    window.addEventListener('load', headerScrolled);\n    onscroll(document, headerScrolled);\n  }\n\n  // logo onscroll animation\n  var selectLogo = select('#small-img-logo');\n  if (selectLogo) {\n    var logoScrolled = function logoScrolled() {\n      if (window.scrollY > 400) {\n        selectLogo.classList.add('small-logo-scrolled');\n      } else {\n        selectLogo.classList.remove('small-logo-scrolled');\n      }\n    };\n    window.addEventListener('load', logoScrolled);\n    onscroll(document, logoScrolled);\n  }\n\n  // shevron arrow onscroll animation\n  var selectArrow = select('.arrow');\n  if (selectArrow) {\n    var arrowScrolled = function arrowScrolled() {\n      if (window.scrollY > 80) {\n        selectArrow.classList.add('arrow-scrolled');\n      } else {\n        selectArrow.classList.remove('arrow-scrolled');\n      }\n    };\n    window.addEventListener('load', arrowScrolled);\n    onscroll(document, arrowScrolled);\n  }\n\n  // mobile navbar\n  on('click', '.mobile-nav-toggle', function (e) {\n    select('#navbar').classList.toggle('navbar-mobile');\n    this.classList.toggle('bi-list');\n    this.classList.toggle('bi-x');\n  });\n\n  // Preloader\n  var loader = select('#loader');\n  if (loader) {\n    window.addEventListener('load', function () {\n      loader.remove();\n    });\n  }\n\n  // Animation on scroll\n  window.addEventListener('load', function () {\n    AOS.init({\n      duration: 1000,\n      easing: 'ease-in-out',\n      once: true,\n      mirror: false\n    });\n  });\n\n  // back to the top\n  var backtotop = select('.back-to-top');\n  if (backtotop) {\n    var toggleBacktotop = function toggleBacktotop() {\n      if (window.scrollY > 100) {\n        backtotop.classList.add('active');\n      } else {\n        backtotop.classList.remove('active');\n      }\n    };\n    window.addEventListener('load', toggleBacktotop);\n    onscroll(document, toggleBacktotop);\n  }\n\n  // navbar links active state on scroll\n  var navbarlinks = select('#navbar .scrollto', true);\n  var navbarlinksActive = function navbarlinksActive() {\n    var position = window.scrollY + 200;\n    navbarlinks.forEach(function (navbarlink) {\n      if (!navbarlink.hash) return;\n      var section = select(navbarlink.hash);\n      if (!section) return;\n      if (position >= section.offsetTop && position <= section.offsetTop + section.offsetHeight) {\n        navbarlink.classList.add('active');\n      } else {\n        navbarlink.classList.remove('active');\n      }\n    });\n  };\n  window.addEventListener('load', navbarlinksActive);\n  onscroll(document, navbarlinksActive);\n  $('.geo').mouseover(function () {\n    $(this).children('.preview').show();\n  }).mouseout(function () {\n    $(this).children('.preview').hide();\n  });\n  $('.alert').delay(3000).fadeOut(1000);\n  $('#buttonClose').on('click', function () {\n    $('.modal').hide();\n    $('.modal-backdrop').hide();\n  });\n  return {\n    select: select,\n    on: on,\n    onscroll: onscroll\n  };\n}();\nmodule.exports = main;\n\n//# sourceURL=webpack://help-u/./static/assets/js/main.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./static/assets/js/main.js");
/******/ 	
/******/ })()
;