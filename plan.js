function submitForm(event) {
  event.preventDefault();
  console.log("submitForm called");

  // Extract preferences and fears from the form
  const preferences = Array.from(document.querySelectorAll("input[name='preferences[]']:checked")).map((checkbox) => checkbox.value);
  const fears = Array.from(document.querySelectorAll("input[name='fear[]']:checked")).map((checkbox) => checkbox.value);

  // Create a data object to send to the server
  const data = {
    budget_from: document.getElementById("budget-from").value,
    budget_to: document.getElementById("budget-to").value,
    travel_date_from: document.getElementById("travel-date-from").value,
    travel_date_to: document.getElementById("travel-date-to").value,
    num_travelers: document.getElementById("num-travelers").value,
    preferences: preferences,
    fears: fears,
  };

  fetch('https://travel-app-2wsl4uslja-uc.a.run.app/submit', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      return response.json();
  })
  .then(result => {
      // Display the recommended destination or error message on the page
      displayResult(result);
  })
  .catch(error => {
      console.error('Error:', error);
      displayResult({error: "An error occurred while processing your request. Please try again later."});
  });
}

function displayResult(result) {
  resultContainer.style.display = 'block';

  let resultTitle = document.getElementById('result-title');
  let resultLocation = document.getElementById('result-location');
  let resultActivities = document.getElementById('result-activities');
  let resultCluster = document.getElementById('result-cluster');

  if (result.error) {
    resultTitle.innerText = result.error;
    resultLocation.innerText = '';
    resultActivities.innerText = '';
    resultCluster.innerText = '';
  } else {
    resultTitle.innerText = `Recommended destination: ${result.name}`;
    resultLocation.innerText = `Location: ${result.location}`;
    resultActivities.innerText = `Activities: ${result.activities.join(', ')}`;
    resultCluster.innerText = `Cluster: ${result.cluster}`;
  }
}

const form = document.getElementById("plan-form");
form.addEventListener('submit', submitForm);

// Hide the result container by default
const resultContainer = document.getElementById('result-container');
resultContainer.style.display = 'none';
