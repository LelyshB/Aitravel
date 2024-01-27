// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
  
  // Add event listener to "Get Started" button
  const getStartedBtn = document.querySelector('#home button');
  
  getStartedBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = 'services.html';
  });
  