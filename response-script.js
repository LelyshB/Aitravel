function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    let regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    let results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    let resultData = getUrlParameter('result');
    let result = JSON.parse(resultData);
  
    displayResult(result);
  });
  
  function displayResult(result) {
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
  