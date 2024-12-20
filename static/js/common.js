function toggleEdit(field, editMode = true) {
    const displayElement = document.getElementById(`${field}-display`);
    const formElement = document.getElementById(`${field}-form`);
    const rowElement = document.getElementById(`${field}-row`);

    if (editMode) {
        // Switch to edit mode
        displayElement.style.display = 'none';
        formElement.style.display = 'block';
        rowElement.querySelector('.edit-btn').style.display = 'none';
    } else {
        // Switch back to display mode
        displayElement.style.display = 'inline';
        formElement.style.display = 'none';
        rowElement.querySelector('.edit-btn').style.display = 'inline';
    }
}

