document.addEventListener('DOMContentLoaded', function() {
    // Select all nav-headers
    const navHeaders = document.querySelectorAll('.nav-header');

    navHeaders.forEach(function(header, index) {
        // Create a hidden checkbox element (not used visually)
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'toggle-' + index;
        checkbox.classList.add('toggle-checkbox');

        // Insert the checkbox before the nav-header (dynamically)
        header.insertAdjacentElement('afterbegin', checkbox);

        // Initially hide the child items of each nav-header
        let nextSibling = header.nextElementSibling;
        while (nextSibling && !nextSibling.classList.contains('nav-header')) {
            nextSibling.style.display = 'none'; // Start with hidden child nav-items
            nextSibling = nextSibling.nextElementSibling;
        }

        // When the header is clicked, toggle the visibility of child items
        header.addEventListener('click', function() {
            const isVisible = checkbox.checked; // Check if it's currently open
            toggleNavItems(isVisible, header);  // Toggle child items visibility
            checkbox.checked = !isVisible;      // Update checkbox status
        });
    });

    // Function to toggle the visibility of child nav-items
    function toggleNavItems(isVisible, header) {
        let nextSibling = header.nextElementSibling;
        while (nextSibling && !nextSibling.classList.contains('nav-header')) {
            nextSibling.style.display = isVisible ? 'none' : 'block'; // Show/hide
            nextSibling = nextSibling.nextElementSibling;
        }
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Find all nav-headers
    const navHeaders = document.querySelectorAll('.nav-header');

    // Loop through each nav-header to check for the specific text
    navHeaders.forEach(function(header) {
        if (header.textContent.includes('Authentication and Authorization')) {
            // Replace the text
            header.textContent = header.textContent.replace('Authentication and Authorization', 'Authentication');
        }
    });




});
