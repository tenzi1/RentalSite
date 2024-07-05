// notification socket
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
    console.log(
        'onmessage'
    )
    const data = JSON.parse(e.data);
    const count = data.count;
    setCount(count);
}
// console.log(
//     'inside off navjs'
// )
// console.log('socket', socket)

// socket.onmessage = function (e) {
//     console.log('notification=====>')
//     const data = JSON.parse(e.data);
//     if (data.type == 'notification') {
//         console.log('inside of notification ======')
//         setCount(data.count)
//     }
// }
// socket.onmessage = function (e) {
//     const data = JSON.parse(e.data);
//     const count = data.count;
//     setCount(count);
// }
function setCount(count) {
    badge = document.querySelector('.notification-container .badge')

    if (count > 0) {
        badge.textContent = count
        badge.classList.remove('visually-hidden')
    } else {
        badge.classList.add('visually-hidden')
    }
}

// chat socket
// const chatSocket = new WebSocket(
//     "ws://"
//     + window.location.host
//     + '/ws/chat/'
// )

// function showMessage(data) {
//     badge = document.querySelector('.message-container .badge')

//     if (data) {
//         badge.classList.remove('visually-hidden')
//     }
// }
// chatSocket.onmessage = function (e) {
//     const data = JSON.parse(e.data)

//     showMessage(data)
// }

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Function to fetch notifications
function fetchNotifications() {
    return fetch('/api/v1/notifications/', {
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            if (!data) {
                console.log('No data received');
                return [];
            }
            return data.results;
        })
        .catch(error => {
            console.error('Error fetching notifications:', error);
            return [];
        });
}

// Function to render notifications
function renderNotifications(notifications) {
    const notificationGroup = document.querySelector('.notifications')
    notificationGroup.innerHTML = '';

    if (notifications.length == 0) {
        notificationGroup.innerHTML = '<small>Currently no new notifications are available.</small>'
    } else {
        notifications.forEach(notification => {
            const notificationElement = document.createElement('div');
            if (!notification.read) {
                notificationElement.classList.add('notification', 'unread');
            } else {
                notificationElement.classList.add('notification');
            }
            notificationElement.id = notification.id
            notificationElement.innerHTML = `

        <a href="http://${window.location.host}/booking/${notification.rental_id}/">
            <div class="time">Rental • ${moment(notification.created_at).fromNow()}</div>
            <div class="content">${notification.message}</div>
        </a>`;
            notificationGroup.appendChild(notificationElement)
        });
    }


}

// Event handler for clicking the notification container
document.querySelector('.notification-container').onclick = function (e) {
    const notificationContainer = document.querySelector('.notifications-popup');
    notificationContainer.classList.toggle('visually-hidden');  // Toggle visibility

    // Fetch and render notifications if the container is not hidden
    if (!notificationContainer.classList.contains('visually-hidden')) {
        fetchNotifications().then(notifications => {
            renderNotifications(notifications);
        });
    }
};

document.addEventListener('DOMContentLoaded', function () {
    var container = document.querySelector('.notifications');

    container.onclick = function (event) {
        var target = event.target;

        // Check if the clicked element is within a notification item
        while (target && !target.classList.contains('notification')) {
            target = target.parentNode;
        }

        if (target && target.classList.contains('notification')) {
            // Prevent the default anchor click behavior
            event.preventDefault();

            // Get the anchor element within the notification item
            var anchor = target.querySelector('a');

            // Fetch API to mark the notification as read
            fetch('/api/v1/notifications/mark_read/', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken // Include the CSRF token in the request header
                },
                body: JSON.stringify({ ids: [target.id] })
            })
                .then(response => {
                    if (response.ok) {
                        window.location.href = anchor.href;
                    }
                })
                .catch(error => {
                    console.error('Error marking notification as read:', error);
                });
        }
    };

    document.querySelector('.mark-read').onclick = function (e) {
        fetch("/api/v1/notifications/mark_all_read/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({})


        })
    }
});

// 

// Chat 
document.querySelector('.message-icon').onclick = function (e) {
    const notificationContainer = document.querySelector('.messages-popup');
    notificationContainer.classList.toggle('visually-hidden');  // Toggle visibility

    // Fetch and render notifications if the container is not hidden
    if (!notificationContainer.classList.contains('visually-hidden')) {
        fetchNotifications().then(notifications => {
            renderNotifications(notifications);
        });

    }
};

document.querySelectorAll('.chat-item').forEach(function (item) {
    item.addEventListener('click', function (e) {
        document.querySelector('.messages-popup').classList.add('visually-hidden');
        document.querySelector('.chat-container').classList.remove('visually-hidden');
    });
});


// document.querySelector('.close-icon').onclick = function (e) {
//     document.querySelector('.chat-container').classList.add('visually-hidden')
// }
