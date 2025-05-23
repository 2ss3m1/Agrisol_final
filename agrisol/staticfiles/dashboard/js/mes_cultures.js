document.addEventListener('DOMContentLoaded', function() {
    const addPlantBtn = document.getElementById('add-plant-btn');
    
    if (addPlantBtn) {
        addPlantBtn.addEventListener('click', function() {
            const plantModalElement = document.getElementById('plantModal');
            if (plantModalElement) {
                const plantModal = new bootstrap.Modal(plantModalElement);
                plantModal.show();
            } else {
                console.error("Element #plantModal not found");
            }
        });
    } else {
        console.error("Element #add-plant-btn not found");
    }

    const deleteForms = document.querySelectorAll('.delete-form');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            if (confirm('Êtes-vous sûr de vouloir supprimer cette culture ?')) {
                this.submit();
            }
        });
    });
    
});