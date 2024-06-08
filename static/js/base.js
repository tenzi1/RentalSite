
let show = true;

function showCheckboxes() {
    let checkboxes = document.getElementById("categories");
    let up_arrow = document.getElementsByClassName('categoryUp')[0]
    let down_arrow = document.getElementsByClassName('categoryDown')[0]

    if (show) {
        checkboxes.style.display = "block";
        up_arrow.style.display = 'inline-block'
        down_arrow.style.display = 'none'
        show = false;
    } else {
        down_arrow.style.display = 'inline-block'
        up_arrow.style.display = 'none'
        checkboxes.style.display = "none";
        show = true;
    }
}

const elements = document.querySelectorAll('.header-child');

elements.forEach(element => {

    element.addEventListener('click', () => {
        elements.forEach(el => el.classList.remove('active'));
        element.classList.toggle('active');
        console.log('lakjdflajldskjflkasd', element)
    });
    element.addEventListener('click', renderRental)
});


// // toggle active class
// const firstElement = document.querySelector('.featured-rental');
// const secondElement = document.querySelector('.latest-rental');


// function toggleActiveClass() {
//     firstElement.classList.remove('active');
//     secondElement.classList.remove('active');
//     if (this == firstElement) {
//         firstElement.classList.add('active');
//     } else {
//         secondElement.classList.add('active')
//     }
// }
// firstElement.addEventListener('click', toggleActiveClass);
// secondElement.addEventListener('click', toggleActiveClass);
// firstElement.addEventListener('click', renderRental)
// secondElement.addEventListener('click', renderRental)


// Fetch Categories
async function fetchCategories() {
    try {
        const response = await fetch("/api/v1/category/");
        const data = await response.json();
        return data;
    } catch (error) {
        console.log('Error fetching data:', error)
    }
}

// Render Categories
async function renderCategories() {
    const container = document.getElementById('categories');
    const data = await fetchCategories();
    if (!data) {
        return;
    }

    data['results'].forEach(category => {
        input = document.createElement('input')
        input.type = "checkbox"
        input.id = category.id
        label = document.createElement('label')
        label.for = category.id
        label.appendChild(input)
        label.innerHTML += ` ${category.name}`

        container.appendChild(label);
    })
}

// Return Min and Max rent price of available rentals
let cahced_rent_range = null
async function fetch_rent_range() {
    try {
        const response = await fetch('/api/v1/rent_range/')
        const data = await response.json();
        return data;
    } catch (error) {
        console.log('Error fetching data:', error)

    }
}

async function get_rent_range() {
    if (cahced_rent_range == null) {
        cahced_rent_range = await fetch_rent_range();
    }
    return cahced_rent_range;
}

async function renderRentRange() {
    const rentRange = await get_rent_range();
    var minPriceInput = document.querySelector(".input-min");
    var maxPriceInput = document.querySelector(".input-max");
    minPriceInput.value = rentRange.min_rent;
    maxPriceInput.value = rentRange.max_rent;
}

// common function handleEvent
// returns search parameter
function getSearchQuery() {
    let searchInput = document.querySelector('.search-input')
    let sortInput = document.querySelector('.form-sort')
    let queryDict = {
        'search': searchInput.value,
        'ordering': sortInput.value
    }
    let queryParams = new URLSearchParams(queryDict).toString()
    return queryParams
}
// returns filter key values
function getFilterQuery() {
    const filterData = {}

    // Add checkbox inputs
    const categoriesCheckbox = document.querySelectorAll('#categories input[type=checkbox]');
    let categories = []
    categoriesCheckbox.forEach((checkbox) => {
        if (checkbox.checked) {
            categories.push(parseInt(checkbox.id))
        }
    })
    filterData['category'] = categories
    // filterData.append('categories', categories)

    // Add currency inputs
    const minPriceInput = document.querySelector('.input-min');
    const maxPriceInput = document.querySelector('.input-max');
    filterData['min_rent'] = minPriceInput.value;
    filterData['max_rent'] = maxPriceInput.value;

    // Add location input
    const locationInput = document.querySelector('.location-input input');
    filterData['address'] = locationInput.value;

    const headerChild = document.querySelector('.main-header .active')
    if (headerChild.classList.contains('featured-rental')) {
        filterData['featured'] = true
    } else if (headerChild.classList.contains('owned-rental')) {
        filterData['owned'] = true
    }

    let filterParams = new URLSearchParams(filterData).toString()
    return filterParams
}


//////////
async function fetchRentals(event) {
    event.preventDefault()

    queryParams = getSearchQuery()
    filterParams = getFilterQuery()

    try {
        const response = await fetch(`/api/v1/rental?${queryParams}&${filterParams}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log('Error fetching data:', error);
    }
}

// Function to render data

async function renderRental(event) {

    const container = document.querySelector('.main-body');
    container.innerHTML = '';
    const data = await fetchRentals(event);
    if (!data) {
        return;
    }
    data['results'].forEach(rental => {
        // Create the outermost div
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card mb-3';
        // cardDiv.style.maxWidth = '540px';

        // Create the row div
        const rowDiv = document.createElement('div');
        rowDiv.className = 'row g-0';

        // Create the left column div
        const colLeft = document.createElement('div');
        colLeft.className = 'col-md-4';

        // Create the image element
        const img = document.createElement('img');
        if (rental.images.length >= 1) {
            img.src = rental.images[0];
        }
        img.className = 'img-fluid rounded-start';
        img.alt = '...'; // Replace... with your alt text

        // Append the image to the left column
        colLeft.appendChild(img);

        // Create the right column div
        const colRight = document.createElement('div');
        colRight.className = 'col-md-8';

        // Create the card body div
        const cardBodyDiv = document.createElement('div');
        cardBodyDiv.className = 'card-body';

        // Create the card title h5
        const cardTitle = document.createElement('h5');
        cardTitle.className = 'card-title';
        cardTitle.textContent = rental.title;

        // Create the first card text p
        const cardText1 = document.createElement('p');
        cardText1.className = 'card-text';
        cardText1.textContent = rental.description.slice(0, 150) + "...";

        const cardText2 = document.createElement('p');
        cardText2.className = 'card-text';
        cardText2.textContent = rental.address.split(',').slice(0, 2);
        // Create the second card text p
        const cardText3 = document.createElement('p');
        cardText3.className = 'card-text';
        if (rental.days_since_modified > 1) {
            cardText3.innerHTML = `<small class="text-muted">Last updated ${rental.days_since_modified} days ago</small>`;
        } else if (rental.days_since_modified == 1) {
            cardText3.innerHTML = `<small class="text-muted">Last updated ${rental.days_since_modified} day ago</small>`;
        } else {
            cardText3.innerHTML = `<small class="text-muted">Last updated today</small>`;
        }

        const cardText4 = document.createElement('p');
        cardText4.className = 'card-text';
        cardText4.innerHTML = `Rs. ${rental.monthly_rent}`;

        const anchor = document.createElement('a');
        anchor.className = 'filter-btn'
        anchor.innerHTML = 'View'
        anchor.href = `/rental_detail/${rental.id}/`
        // Append the card title and texts to the card body
        cardBodyDiv.appendChild(cardTitle);
        cardBodyDiv.appendChild(cardText1);
        cardBodyDiv.appendChild(cardText2);
        cardBodyDiv.appendChild(cardText4);
        cardBodyDiv.appendChild(cardText3);
        cardBodyDiv.appendChild(anchor)

        // Append the card body to the right column
        colRight.appendChild(cardBodyDiv);

        // Append the columns to the row
        rowDiv.appendChild(colLeft);
        rowDiv.appendChild(colRight);

        // Append the row to the card
        cardDiv.appendChild(rowDiv);

        // Finally, append the card to the body of the document
        const container = document.querySelector('.main-body');

        container.appendChild(cardDiv);

    })
}
// async function renderRental(event) {

//     const container = document.querySelector('.main-body');
//     container.innerHTML = '';
//     const data = await fetchRentals(event);
//     if (!data) {
//         return;
//     }
//     data['results'].forEach(rental => {
//         const card = document.createElement('div');
//         card.classList.add('rental-card');

//         const images = document.createElement('div')
//         images.classList.add('main-image')

//         if (rental.images.length > 1) {
//             images.innerHTML = `<img src="${rental.images[0]}" class="rental-img">`

//             const thumbnail = document.createElement('div')
//             thumbnail.classList.add('thumbnails')
//             for (let i = 1; i < rental.images.length; i++) {

//                 // img = document.createElement('img')
//                 thumbnail.innerHTML += `<img src="${rental.images[i]}" alt="Thumbnail">`;

//             }

//             images.appendChild(thumbnail)
//         } else if (rental.images.length == 1) {
//             images.innerHTML = `<img src="${rental.images[0]}" class="rental-img">`

//         } else {
//             images.innerHTML = `<img src="#" class="rental-img" style="width:257px">`

//         }

//         const wrapper = document.createElement('div')
//         wrapper.classList.add('description-section')

//         const title = document.createElement('h3');
//         title.textContent = rental.title;

//         const body = document.createElement('p');
//         body.textContent = rental.description;

//         const address = document.createElement('p')
//         address.textContent = rental.address

//         const rent = document.createElement('p')
//         rent.textContent = `Rs. ${rental.monthly_rent}`

//         const owner = document.createElement('h6')
//         owner.textContent = rental.owner

//         wrapper.appendChild(title);
//         wrapper.appendChild(body);
//         wrapper.appendChild(address);
//         wrapper.appendChild(rent)
//         wrapper.appendChild(owner);
//         card.appendChild(images)
//         card.appendChild(wrapper);
//         container.appendChild(card);
//     })
// }

document.getElementById('search-form').addEventListener('submit', renderRental)
document.querySelector('.search-icon').addEventListener('click', renderRental)
document.getElementById('filter-form').addEventListener('submit', renderRental)

document.addEventListener('DOMContentLoaded', (event) => {
    renderCategories();
    renderRentRange();
    renderRental(event);


});

function resetFilter() {
    // Resetting checkboxes (assuming they are dynamically added)
    var checkboxes = document.querySelectorAll("#categories input[type='checkbox']");
    checkboxes.forEach(function (checkbox) {
        checkbox.checked = false;
    });

    renderRentRange();
    // Resetting location input
    var locationInput = document.querySelector(".location-input input");
    locationInput.value = "";
}

