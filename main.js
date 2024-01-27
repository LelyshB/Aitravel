// main.js

import { handleNavLinkClick } from './scripts.js';

const navLinks = document.querySelectorAll('nav a[data-scroll]');
navLinks.forEach(link => {
    link.addEventListener('click', handleNavLinkClick);
});
