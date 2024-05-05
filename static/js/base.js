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
    console.log('I am printing.....')
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

function showCategories() {
    var categoryDropdown = document.getElementById('category-dropdown');
    categoryDropdown.classList.toggle('show')
    downCaret = document.querySelector('.fa-caret-down')
    upCaret = document.querySelector('.fa-caret-up')
    if (categoryDropdown.classList.contains('show')) {
        downCaret.style.display = 'none'
        upCaret.style.display = ''
    } else {
        downCaret.style.display = ''
        upCaret.style.display = 'none'
    }

    //     if (categoryDropdown.classList.contains('show')) {
    //         categoryDropdown.classList.remove('show')
    //     } else {
    //         categoryDropdown.classList.add('show')
    //     }
}

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
