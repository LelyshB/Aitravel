// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const sectionId = this.getAttribute('href');
    document.querySelector(sectionId).scrollIntoView({
      behavior: 'smooth'
    });
  });
});

// Add event listeners to navigation links
const navLinks = document.querySelectorAll('.nav-btn');

navLinks.forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const href = link.getAttribute('href');
    navigateToPage(href);
  });
});

// Add event listener to navigation toggle button
const navToggle = document.querySelector('.nav-toggle');

navToggle.addEventListener('click', () => {
  document.body.classList.toggle('nav-open');
});

// Navigate to the specified page with a transition animation or smooth scrolling
function navigateToPage(href) {
  const currentPage = document.querySelector('.current-page');
  const nextPage = document.querySelector(href);

  if (currentPage === nextPage) {
    // Scroll to the section if link is to a section on the same page
    nextPage.scrollIntoView({
      behavior: 'smooth'
    });
  } else {
    // Add animation classes and navigate to new page
    currentPage.classList.add('page-exit');
    nextPage.classList.add('page-enter');

    // Wait for animation to complete before updating classes and navigating to new page
    setTimeout(() => {
      currentPage.classList.remove('current-page', 'page-exit');
      nextPage.classList.add('current-page', 'page-enter');
      nextPage.classList.remove('page-enter');
      window.location.href = href;
    }, 1000);
  }
}
