
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
    console.log('inside renderrange', renderRentRange)
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
    } else if (headerChild.classList.contains('favorite')) {
        filterData['favorite'] = true
    } else if (headerChild.classList.contains('booked-rental')) {
        filterData['booking'] = true
    }

    let filterParams = new URLSearchParams(filterData).toString()
    return filterParams
}

let nextPageExist = true;
let currentPage
let isLoading = false;
let totalCount = 0;
let currentCount = 0;

async function fetchRentals(page = 1) {

    console.log("page number inside of FETCHRENTALS", page)
    queryParams = getSearchQuery();
    filterParams = getFilterQuery();

    try {
        const response = await fetch(`/api/v1/rental?page=${page}&${queryParams}&${filterParams}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log('Error fetching data:', error);
    }
}

async function renderRental(event) {
    console.log('inside render rental.......');
    event.preventDefault();
    const container = document.querySelector('.main-body');
    container.innerHTML = '';
    currentPage = 1; // Reset to the first page
    totalCount = 0;
    currentCount = 0;
    nextPageExist = true;
    isLoading = false;
    console.log("current page in render rental", currentPage)
    await loadRentals(currentPage, container);
}

async function loadRentals(page, container) {
    if (isLoading || !nextPageExist) return;
    isLoading = true;

    const data = await fetchRentals(page);
    console.log("fetching page", page, data)
    if (!data) {
        console.log("no data");
        isLoading = false;
        return;
    }

    nextPageExist = data.next ? true : false;

    console.log("inside of loadrentals current page", page)
    // Update rental count and current page
    totalCount = data.count;
    currentCount += data.results.length;
    document.getElementById('rental-count').textContent = `${currentCount} of ${totalCount} Rentals`;

    data.results.forEach(rental => {
        // Create rental card and append to container (same code as before)
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card mb-3';

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

        // Create the card title h4
        const cardTitle = document.createElement('h4');
        cardTitle.className = 'card-title';
        cardTitle.textContent = rental.title;

        // Create the first card text p
        const cardText1 = document.createElement('p');
        cardText1.className = 'card-text';
        cardText1.textContent = rental.description.slice(0, 150) + "...";

        const cardText2 = document.createElement('p');
        cardText2.className = 'card-text';
        cardText2.innerHTML = `<b>Location</b> : ${rental.address.split(',').slice(0, 2)}`;

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
        cardText4.innerHTML = `<b>Rental Price</b> :  Rs. ${rental.monthly_rent}`;

        const anchor = document.createElement('a');
        anchor.className = 'btn btn-dark me-1';
        anchor.innerHTML = 'View';
        anchor.href = `/rental_detail/${rental.id}/`;

        // Append the card title and texts to the card body
        cardBodyDiv.appendChild(cardTitle);
        cardBodyDiv.appendChild(cardText1);
        cardBodyDiv.appendChild(cardText2);
        cardBodyDiv.appendChild(cardText4);
        cardBodyDiv.appendChild(cardText3);
        cardBodyDiv.appendChild(anchor);

        const headerChild = document.querySelector('.main-header .active');
        if (headerChild.classList.contains('featured-rental')) {
            // filterData['featured'] = true
        } else if (headerChild.classList.contains('owned-rental')) {
            const anchor2 = document.createElement('a');
            anchor2.className = 'btn btn-dark';
            anchor2.textContent = 'Bookings';
            anchor2.href = `/bookings/${rental.id}/`;
            cardBodyDiv.appendChild(anchor2);
        } else if (headerChild.classList.contains('favorite')) {
            // filterData['favorite'] = true
        } else if (headerChild.classList.contains('booked-rental')) {
            const anchor2 = document.createElement('a');
            anchor2.className = 'btn btn-dark';
            anchor2.textContent = 'Bookings';
            anchor2.href = `/booking/${rental.id}/`;
            cardBodyDiv.appendChild(anchor2);
        }

        // Append the card body to the right column
        colRight.appendChild(cardBodyDiv);

        // Append the columns to the row
        rowDiv.appendChild(colLeft);
        rowDiv.appendChild(colRight);

        // Append the row to the card
        cardDiv.appendChild(rowDiv);

        // Finally, append the card to the body of the document
        container.appendChild(cardDiv);
    });

    isLoading = false;
    currentPage = page;
}

const container = document.querySelector('.main-body');
container.addEventListener('scroll', async () => {
    if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
        currentPage++;

        console.log("BEFORE calling loadrental from scroll event", currentPage)
        await loadRentals(currentPage, container);
    }
});

const elements = document.querySelectorAll('.header-child');

elements.forEach(element => {
    element.addEventListener('click', async (event) => {
        elements.forEach(el => el.classList.remove('active'));
        element.classList.add('active');
        console.log("before calling render renatl current page", currentPage)
        console.log("=================================================")
        await renderRental(event); // Ensure renderRental is called on click and waits for completion
    });
});


document.getElementById('search-form').addEventListener('submit', renderRental)
document.querySelector('.search-icon').addEventListener('click', renderRental)
document.getElementById('filter-form').addEventListener('submit', renderRental)

document.addEventListener('DOMContentLoaded', async (event) => {
    await renderCategories();
    await renderRentRange();
    await renderRental(event);


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

