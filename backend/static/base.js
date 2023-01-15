//  this is for input validation that user only inputs valid input -->
// function validateForm() {
//     const url = document.getElementById('name').value;
//     const urlPattern = /^www\.[a-zA-Z0-9-]+\.com$/;

//     if (!urlPattern.test(name)) {
//         alert('Error: The URL you entered is not allowed');
//         return false;
//     } else {
//         return true;
//     }

// }


//page loading animation
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("#animation-button").addEventListener("click", function() {
        document.querySelector("#animation-container").style.display = "block";
    });

});




// this is for ticket maker  
const submitButton = document.getElementById('submit-button');

function updateButtonText() {
    submitButton.value = `Submit(Ticket #{{ ticket_number }})`;
}

submitButton.addEventListener('click', updateButtonText);













