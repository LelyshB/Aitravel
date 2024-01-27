// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
  
  // Add event listener to "Learn More" button
  const learnMoreBtn = document.querySelector('#about button');
  
  learnMoreBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = 'services.html';
  });
  