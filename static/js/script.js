// Listen for the scroll event
window.addEventListener('scroll', function() {

    // Select the header element
    var header = document.querySelector('header');

    // Check if the scroll position is greater than 50 pixels
    if (window.scrollY > 50) {
        // If true, add 'sticky-top' class to make the header sticky
        header.setAttribute('class', 'sticky-top');
    } else {
        // If false, remove the class to position the header on top
        header.removeAttribute('class');
    }
});

// Waits for the DOM to be fully loaded before executing
document.addEventListener('DOMContentLoaded', function() {
    // Function to "populate" the "All" tab
    function populateAllTab() {
        var allContent = ''; // Assigned a variable to the content of the "All" tab
        // Loop through each tab-pane and add its content to the "All" tab
        var tabPanes = document.querySelectorAll('.tab-pane');
        tabPanes.forEach(function(tabPane) {
            if (!tabPane.classList.contains('active')) { // Avoid duplicating the "All" tab content
                allContent += tabPane.innerHTML;
            }
        });
        document.getElementById('all').innerHTML = allContent; // Set the content of the "All" tab
    }

    // Call the function when the page loads
    populateAllTab();

    // Call the function when the "All" tab is clicked
    var allTab = document.querySelector('a[href="#all"]');
    if (allTab) {
        allTab.addEventListener('click', populateAllTab);
    }
});