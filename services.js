// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
  
  // Add event listener to "Contact Us" button
  const contactUsBtn = document.querySelector('#services button');
  
  contactUsBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = 'contact.html';
  });
  