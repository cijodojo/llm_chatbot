document.getElementById('send-btn').addEventListener('click', function () {
  sendMessage();
});

document.getElementById('user-input').addEventListener('keypress', function (event) {
  if (event.key === 'Enter') {
      sendMessage();
  }
});

function sendMessage() {
  const inputField = document.getElementById('user-input');
  const message = inputField.value.trim();
  
  if (message === '') return;

  appendMessage('user-message', message);
  inputField.value = '';

  setTimeout(() => {
      fetch('http://localhost:3333/chatbot', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ query: message })
      })
      .then(response => response.json())
      .then(data => {
          appendMessage('bot-message', data);
      })
      .catch(error => {
          console.error('Error:', error);
          appendMessage('bot-message', 'Error: Unable to reach the server.');
      });
  }, 500);
}

function appendMessage(senderClass, message) {
  const chatWindow = document.getElementById('chat-window');

  const messageContainer = document.createElement('div');
  messageContainer.classList.add('message-container', senderClass);
  
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.innerText = message;

  messageContainer.appendChild(messageElement);
  chatWindow.appendChild(messageContainer);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
