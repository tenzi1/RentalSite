document.querySelector('.notification-container').onclick = function (e) {
    notificationContainer = document.querySelector('.notifications-popup')
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
    const count = data.count;
    setCount(count);
}

function setCount(count) {
    console.log('count===>', count)
    badge = document.querySelector('.notification-container .badge')

    if (count > 0) {
        badge.textContent = count
        badge.classList.remove('visually-hidden')
    } else {
        badge.classList.add('visually-hidden')
    }
}
