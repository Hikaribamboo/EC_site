document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('welcome-modal');
    const closeModal = document.getElementById('close-modal');
    if (modal) {
        closeModal.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }
});

