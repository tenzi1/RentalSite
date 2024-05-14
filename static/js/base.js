/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
// function myFunction() {
//     var x = document.getElementById("myTopnav");
//     if (x.className === "topnav") {
//         x.className += " responsive";
//     } else {
//         x.className = "topnav";
//     }
// }

function toggleMenu() {
    var x = document.querySelector('.hamburger')
    var nav = document.querySelector('.nav')
    var leftSection = document.querySelector('.left-section');
    var rightSection = document.querySelector('.right-section');

    if (x.style.display === 'none') {
        // nav.style.display = 'flex';
        nav.className = 'nav'

    } else {
        x.style.display = 'none';
        nav.className += ' responsive-dropdown'
        leftSection.className = 'responsive-dropdown'
        rightSection.className = 'responsive-dropdown'

    }
}

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

console.log('herererer')

// Fetch category list
function fetchCategoris() {
    fetch('/api/v1/category/')
        .then(response => response.json())
        .then(categories => {
            const ul = document.getElementById('categories-list');
            categories['results'].forEach(category => {
                const li = document.createElement('li');
                li.textContent = category.name;
                ul.appendChild(li);
            });
        })
        .catch(error => console.log('Error', error))
}

fetchCategoris()
