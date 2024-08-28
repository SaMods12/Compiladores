document.addEventListener('DOMContentLoaded', function() {
    const clearButton = document.querySelector('.clear');


clearButton.addEventListener('click', function() {
textarea.value = '';
document.querySelector('#resultTable tbody').innerHTML = '';
});

});