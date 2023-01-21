import fs from 'fs';
import path from 'path';
const { JSDOM } = require('jsdom');
global.Event = require('events').Event;

jest.mock('aos/dist/aos.css', () => {
  return {
    init: jest.fn(),
  };
});

jest.mock('bootstrap/js/src/collapse', () => {
  return {
    init: jest.fn(),
  };
});

jest.mock('aos', () => {
  return {
    init: jest.fn(),
  };
});

// set up a simulated browser environment
const htmlDocPath = path.join(
  process.cwd(),
  'static/assets/js/__tests__/html.html'
);
const html = fs.readFileSync(htmlDocPath).toString();
const dom = new JSDOM(html);
global.window = dom.window;
global.document = dom.window.document;
global.$ = require('jquery');

const main = require('../main.js');

beforeEach(() => {
  const dom = new JSDOM(html);
  global.window = dom.window;
  global.document = dom.window.document;
});

describe('select', () => {
  test('should select an element', () => {
    const expected = document.querySelector('#hero');
    const el = main.select('#hero');

    expect(el).toEqual(expected);
  });

  test('should select multiple elements', () => {
    const expected = [...document.querySelectorAll('.section-title')];
    const el = main.select('.section-title', true);

    expect(el).toEqual(expected);
  });
});

describe('on', () => {
  test('on adds an event listener to a single element', () => {
    const listener = jest.fn();
    const el = document.querySelector('#hero');

    main.on('click', '#hero', listener, false);
    el.click();

    expect(listener).toHaveBeenCalled();
  });

  test('on adds an event listener to multiple elements', () => {
    const expected = [...document.querySelectorAll('.section-title')];
    const listener = jest.fn();
    main.on('click', '.section-title', listener, true);
    expected[0].click();
    expected[1].click();

    expect(listener).toHaveBeenCalledTimes(2);
  });
});

describe('onscroll', () => {
  test('onscroll should call the listener function when the element is scrolled', () => {
    const listener = jest.fn();
    const el = document.querySelector('#hero');

    main.onscroll(el, listener);
    const scrollEvent = new window.CustomEvent('scroll');
    el.dispatchEvent(scrollEvent);

    expect(listener).toHaveBeenCalled();
  });
});

