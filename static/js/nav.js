document.querySelector('.notification').onclick = function (e) {
    notificationContainer = document.querySelector('.notification-container')
    notificationContainer.classList.toggle('visually-hidden')
}

notifyContainer = document.querySelector('.notification')

const notifySocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/notify/'
);

notifySocket.onopen = function (e) {
    console.log('Socket successfully connected.')
}

notifySocket.onclose = function (e) {
    console.log('Socket closed unexpectedly')
}

notifySocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    setMessage(message);
}

function setMessage(message) {
    console.log('message')
    console.log(message)
    count = document.querySelector('.badge').value
    console.log(count)
}