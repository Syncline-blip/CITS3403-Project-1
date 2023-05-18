
    // Define an array of element ids
    var collapseElementIds = ["favouritesCollapse", "scoreboardCollapse", "membersCollapse"];

    // Define a function to handle the common behavior
    function handleCollapse(elementId) {
        var collapseButton = document.getElementById(elementId + "Button");
        var collapse = document.getElementById(elementId);

        // Initially hide on small screens
        if (window.innerWidth < 768) {
            collapse.style.display = "none";
        }

        // Add click event listener to the header
        collapseButton.addEventListener("click", function () {
            // This check will ensure the following code only runs for small screens
            if (window.innerWidth <= 767) {
                var arrow = $(this).find('.arrow');
                

                if (collapse.style.display === "none") {
                    collapse.style.display = "block";
                    arrow.html('&#x25B2;').addClass('upArrow').data('open', true); // Change to up arrow
                } else {
                    collapse.style.display = "none";
                    arrow.html('&#x25BC;').removeClass('upArrow').data('open', false); // Change to down arrow
                }
            }
        });
    }

    // Call the function for each element id
    collapseElementIds.forEach(handleCollapse);

    // Handle screen resize
    window.addEventListener("resize", function () {
        if (window.innerWidth >= 768) {
            collapseElementIds.forEach(function (elementId) {
                document.getElementById(elementId).style.display = "block";
            });
        } else {
            collapseElementIds.forEach(function (elementId) {
                document.getElementById(elementId).style.display = "none";
            });
        }
    });
