const socket = io();

document.addEventListener('DOMContentLoaded', (event) => {
  // This function will run after the document is fully loaded
  const button = document.querySelector('.generateButton');
  const textArea = document.getElementById('promptInput');

  // Function to handle sending the prompt
  function handleSendPrompt() {
    const message = textArea.value;
    sendPrompt(message);
    textArea.readOnly = true; // Lock the textarea
  }

  // Event listener for button click
  button.addEventListener('click', handleSendPrompt);

  // Event listener for Enter key in textarea
  textArea.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent the default action to stop new line
      handleSendPrompt();
    }
  });
});



function updateStatus(assistant, message) {
  // Define the colors for each assistant type
  const colors = {
      'User': 'green',
      'PromptAI': 'blue',
      'CodingAI': 'purple',
      'Function': 'red'
  };

  // Find the updates section
  const updatesSection = document.querySelector('.updates-section');

  // Check if there is a loader present and update the last update with the assistant message
  const lastUpdateWithLoader = updatesSection.querySelector('.update .loader');
  if (lastUpdateWithLoader) {
      // Remove the loader class
      lastUpdateWithLoader.classList.remove('loader');
      // Create a new circle icon div with the correct color
      const circleIconDiv = document.createElement('div');
      circleIconDiv.className = 'circle-icon-' + colors[assistant];
      // Insert the new circle icon div before the paragraph in the last update
      lastUpdateWithLoader.parentNode.insertBefore(circleIconDiv, lastUpdateWithLoader.nextSibling);
      // Update the text content of the paragraph
      //lastUpdateWithLoader.nextElementSibling.textContent = assistant + ': ' + message;
  }

  // Create a new update with the loader for the new message
  const newUpdate = document.createElement('div');
  newUpdate.className = 'update';
  if (assistant === 'Function') {
      newUpdate.innerHTML = `
        <span class="loader"></span>
        <p>${assistant}: <code>${message}</code></p>
    `;
  } else {
      newUpdate.innerHTML = `
        <span class="loader"></span>
        <p>${assistant}: ${message}</p>
    `;
  }
  updatesSection.appendChild(newUpdate);
}

updateWebsitePreview = function (pictureLink) {
  // picture link is a string like this : "/webpreview//Users/ryanvogel/Desktop/WebDevGPT/flask/webpreview/websiteSaved.png'"
  
}

socket.on('update_status', function(data) {
    if (data.assistant === 'WEBPIC') {
        updateWebsitePreview(data.message);
    }
    updateStatus(data.assistant, data.message);
});

function sendPrompt(message) {
  socket.emit('send_prompt', {prompt: message});
}
