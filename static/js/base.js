
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

// function toggleMenu() {
//     var x = document.querySelector('.hamburger')
//     var nav = document.querySelector('.nav')
//     var leftSection = document.querySelector('.left-section');
//     var rightSection = document.querySelector('.right-section');

//     if (x.style.display === 'none') {
//         // nav.style.display = 'flex';
//         nav.className = 'nav'

//     } else {
//         x.style.display = 'none';
//         nav.className += ' responsive-dropdown'
//         leftSection.className = 'responsive-dropdown'
//         rightSection.className = 'responsive-dropdown'

//     }
// }

// function showCategories() {
//     console.log('herere')
//     var categoryDropdown = document.getElementById('category-dropdown');
//     categoryDropdown.classList.toggle('show')
//     downCaret = document.querySelector('.fa-caret-down')
//     upCaret = document.querySelector('.fa-caret-up')
//     if (categoryDropdown.classList.contains('show')) {
//         downCaret.style.display = 'none'
//         upCaret.style.display = ''
//     } else {
//         downCaret.style.display = ''
//         upCaret.style.display = 'none'
//     }

//     if (categoryDropdown.classList.contains('show')) {
//         categoryDropdown.classList.remove('show')
//     } else {
//         categoryDropdown.classList.add('show')
//     }
// }

// window.onclick = function (e) {
//     if (!e.target.matches('.dropdown')) {
//         var categoryDropdown = document.getElementById('category-dropdown');
//         if (categoryDropdown.classList.contains('show')) {
//             categoryDropdown.classList.remove('show')
//         } else {
//             categoryDropdown.classList.add('show')
//         }
//     }
//     console.log('again')
// }


// window.addEventListener('scroll', function () {
//     const categoriesSection = document.getElementById('categories-section');
//     const categoriesPlaceholder = document.getElementById('categories-placeholder');
//     const categories = categoriesSection.cloneNode(true); // Clone the categories section

//     // Check if the categories section is out of view
//     if (categoriesSection.getBoundingClientRect().bottom <= 0) {
//         document.querySelector('.dropdown').style.display = ''
//         console.log(document.querySelector('.dropdown'))
//         // Move the cloned categories to the navbar placeholder
//         // categoriesPlaceholder.appendChild(categories);
//         // Remove the original categories from the main body
//         // categoriesSection.parentNode.removeChild(categoriesSection);
//     } else {
//         document.querySelector('.dropdown').style.display = 'none'

//     }
// });


// // toggle active class
const firstElement = document.querySelector('.first');
const secondElement = document.querySelector('.second');

function toggleActiveClass() {
    firstElement.classList.remove('active');
    secondElement.classList.remove('active');
    if (this == firstElement) {
        firstElement.classList.add('active');
    } else {
        secondElement.classList.add('active')
    }
}

firstElement.addEventListener('click', toggleActiveClass);
secondElement.addEventListener('click', toggleActiveClass);

// $(document).ready(function () {
//     $('.first,.second').on('click', function () {
//         $('.first,.second').removeClass('active');
//         $(this).addClass('active');
//     });
// })

// Fetch category list
// function fetchCategoris() {
//     fetch('/api/v1/category/')
//         .then(response => response.json())
//         .then(categories => {
//             const ul = document.getElementById('categories-list');
//             categories['results'].forEach(category => {
//                 const li = document.createElement('li');
//                 li.textContent = category.name;
//                 ul.appendChild(li);
//             });
//         })
//         .catch(error => console.log('Error', error))
// }

// fetchCategoris()

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

renderCategories();
// Fetch featured rental list
async function fetchFeaturedRentals() {
    try {
        const response = await fetch("/api/v1/rental/?is_featured=");
        const data = await response.json();
        return data;
    } catch (error) {
        console.log('Error fetching data:', error);
    }
}
// Function to Fetch Rental images
async function fetchRentalImages() {
    // 
}
// Function to render data
async function renderFeaturedRental() {
    const container = document.querySelector('.main-body');
    const data = await fetchFeaturedRentals();
    if (!data) {
        return;
    }

    data['results'].forEach(rental => {
        const card = document.createElement('div');
        card.classList.add('rental-card');

        const images = document.createElement('div')
        images.classList.add('main-image')

        if (rental.images.length > 1) {
            images.innerHTML = `<img src="${rental.images[0]}" class="rental-img">`

            const thumbnail = document.createElement('div')
            thumbnail.classList.add('thumbnails')
            for (let i = 1; i < rental.images.length; i++) {

                // img = document.createElement('img')
                thumbnail.innerHTML += `<img src="${rental.images[i]}" alt="Thumbnail">`;

            }

            images.appendChild(thumbnail)
        } else if (rental.images.length == 1) {
            images.innerHTML = `<img src="${rental.images[0]}" class="rental-img">`

        } else {
            images.innerHTML = `<img src="#" class="rental-img" style="width:257px">`

        }

        const wrapper = document.createElement('div')
        wrapper.classList.add('description-section')

        const title = document.createElement('h3');
        title.textContent = rental.title;

        const body = document.createElement('p');
        body.textContent = rental.description;

        const address = document.createElement('p')
        address.textContent = rental.address

        const owner = document.createElement('h6')
        owner.textContent = rental.owner

        wrapper.appendChild(title);
        wrapper.appendChild(body);
        wrapper.appendChild(address);
        wrapper.appendChild(owner);
        card.appendChild(images)
        card.appendChild(wrapper);
        container.appendChild(card);
    })
}
// function fetchFeturedRentals() {
//     fetch('/api/v1/rental/?is_featured=')
//         .then(response => response.json())
//         .then(featRentals => {
//             const rentaldiv = document.getElementsByClassName('description-sectioin')
//             featRentals['results'].forEach(rental => {
//                 const header = document.createElement('h3')
//                 header.textContent = rental.title
//                 const body = document.createElement('p')
//                 body.textContent = rental.description
//                 rentaldiv.appendChild(header)
//                 rentaldiv.appendChild(body)
//                 console.log('finalyyyy')
//             })
//         })
// }

renderFeaturedRental();


// Slider
// const rangeInput = document.querySelectorAll(".range-input input"),
//     priceInput = document.querySelectorAll(".price-input input"),
//     range = document.querySelector(".slider .progress");
// let priceGap = 1000;

// priceInput.forEach((input) => {
//     input.addEventListener("input", (e) => {
//         let minPrice = parseInt(priceInput[0].value),
//             maxPrice = parseInt(priceInput[1].value);

//         if (maxPrice - minPrice >= priceGap && maxPrice <= rangeInput[1].max) {
//             if (e.target.className === "input-min") {
//                 rangeInput[0].value = minPrice;
//                 range.style.left = (minPrice / rangeInput[0].max) * 100 + "%";
//             } else {
//                 rangeInput[1].value = maxPrice;
//                 range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
//             }
//         }
//     });
// });

// rangeInput.forEach((input) => {
//     input.addEventListener("input", (e) => {
//         let minVal = parseInt(rangeInput[0].value),
//             maxVal = parseInt(rangeInput[1].value);

//         if (maxVal - minVal < priceGap) {
//             if (e.target.className === "range-min") {
//                 rangeInput[0].value = maxVal - priceGap;
//             } else {
//                 rangeInput[1].value = minVal + priceGap;
//             }
//         } else {
//             priceInput[0].value = minVal;
//             priceInput[1].value = maxVal;
//             range.style.left = (minVal / rangeInput[0].max) * 100 + "%";
//             range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
//         }
//     });
// });


// var form = document.getElementById("filter-form");
// function handleForm(event, data) {
//     event.preventDefault();
//     console.log('submission.....')

//     const formData = new FormData(form);
//     console.log('formdata', formData)

//     for (key of formData.keys()) {
//         console.log(key);
//     }

//     const params = new URLSearchParams(formData).toString();
//     console.log('paras', params)

//     // fetch("/api/v1/rental/", {
//     //     method: 'GET',
//     //     body: JSON.stringify(data)
//     // })
// }
// form.addEventListener('submit', handleForm);



// document.getElementById('filter-form').addEventListener('submit', function (event) {
//     event.preventDefault(); // Prevent the form from submitting normally

//     const formData = new FormData(this);
//     console.log('entr', formData.entries())
//     // Example of capturing checkbox values
//     const categoriesCheckbox = document.querySelectorAll('#categories input[type=checkbox]');
//     let categories = []
//     categoriesCheckbox.forEach((checkbox) => {
//         if (checkbox.checked) {
//             categories.push(parseInt(checkbox.id))
//         }
//     })
//     formData.append('categories', categories)

//     const minPriceInput = document.querySelector('.input-min');
//     const maxPriceInput = document.querySelector('.input-max');
//     formData.append('min_price', minPriceInput.value);
//     formData.append('max_price', maxPriceInput.value);

//     // Example of capturing text input values
//     const locationInput = document.querySelector('.location-input input');
//     formData.append('location', locationInput.value);
//     // Now you can use formData to send via fetch or XMLHttpRequest
//     console.log(Object.fromEntries(formData)); // Convert FormData to an object for debugging
// });


function getQueryData(event) {
    event.preventDefault()
    console.log('dhererr')
    const form = document.getElementById('filter-form')
    const formData = new FormData(form);
    //capturing checkbox values
    const categoriesCheckbox = document.querySelectorAll('#categories input[type=checkbox]');
    let categories = []
    categoriesCheckbox.forEach((checkbox) => {
        if (checkbox.checked) {
            categories.push(parseInt(checkbox.id))
        }
    })
    formData.append('categories', categories)

    // Capturing Monthly rent inputs
    const minPriceInput = document.querySelector('.input-min');
    const maxPriceInput = document.querySelector('.input-max');
    formData.append('min_price', minPriceInput.value);
    formData.append('max_price', maxPriceInput.value);

    // Example of capturing text input values
    const locationInput = document.querySelector('.location-input input');
    formData.append('location', locationInput.value);

    const search = document.querySelector('.search-input');
    formData.append('search', search.value)

    const params = new URLSearchParams({ 'ordering': '-date_added', 'search': search.value }).toString()
    console.log('paramsss', params)

    console.log(Object.fromEntries(formData)); // Convert FormData to an object for debugging

    console.log('search', search.value)
}

// const searchform = document.getElementById('search-form')
// searchform.addEventListener('submit', getQueryData)

// const searchbtn = document.querySelector('.search-icon')
// searchbtn.addEventListener('click', getQueryData)


// common function handleEvent
// returns search parameter
function getSearchQuery() {
    searchInput = document.querySelector('.search-input')
    let queryDict = {
        'search': searchInput.value,
        'ordering': '-date_added'
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
    filterData['categories'] = categories
    // filterData.append('categories', categories)

    // Add currency inputs
    const minPriceInput = document.querySelector('.input-min');
    const maxPriceInput = document.querySelector('.input-max');
    filterData['min_price'] = minPriceInput.value;
    filterData['max_price'] = maxPriceInput.value;

    // Add location input
    const locationInput = document.querySelector('.location-input input');
    filterData['location'] = locationInput.value;

    return filterData;
}
// 
// console.log('before')
// result = getSearchQuery()
// console.log(result)
// console.log('after')
// getFilterQuery()
// console.log('finis')

function handleFormSubmission(event) {
    event.preventDefault()
    console.log('hererer')

    queryParams = getSearchQuery()
    filterQueries = getFilterQuery()

    fetch(`/api/v1/rental?${queryParams}`)
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data)
        })
        .catch(error => {
            console.error('Error:', error)
        })

    console.log('query', queryParams)
    console.log('filters', filterQueries)
}

document.getElementById('search-form').addEventListener('submit', handleFormSubmission)
document.querySelector('.search-icon').addEventListener('click', handleFormSubmission)
document.getElementById('filter-form').addEventListener('submit', handleFormSubmission)