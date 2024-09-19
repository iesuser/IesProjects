document.addEventListener("DOMContentLoaded", function() {
    const projectId = document.getElementById("projectId").getAttribute("data-project-id");
    const carouselInner = document.getElementById('carouselInner');
    const carouselIndicators = document.getElementById('carouselIndicators');

    // Fetch and display images when the DOM is fully loaded
    fetchImages();

    function fetchImages() {
        fetch(`/api/project/${projectId}/images`)
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data) && data.length > 0) {
                    populateCarousel(data);
                } else {
                    displayPlaceholderImage();
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    function populateCarousel(images) {
        carouselInner.innerHTML = '';
        carouselIndicators.innerHTML = '';

        images.forEach((image, index) => {
            const item = createCarouselItem(image.path, image.id, index);
            carouselInner.appendChild(item);

            const indicator = createIndicator(index);
            carouselIndicators.appendChild(indicator);
        });
    }

    function createCarouselItem(imagePath, imageId, index) {
        const item = document.createElement('div');
        item.className = `carousel-item imageProjectDiv${index === 0 ? ' active' : ''}`;
        item.setAttribute('data-slide-to', index);

        const img = createImageElement(`/images/${projectId}/${imagePath}`);
        const deleteIcon = createDeleteIcon(imageId, item);
        const zoomIcon = createZoomIcon(imagePath);


        item.appendChild(img);
        item.appendChild(deleteIcon);
        item.appendChild(zoomIcon);
        return item;
    }

    function createImageElement(src) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = 'Project Image';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        img.onerror = () => img.src = '/static/img/image_not_available.webp';
        return img;
    }

    function createDeleteIcon(imageId, carouselItem) {
        const deleteIcon = document.createElement('img');
        deleteIcon.src = '/static/img/trash_icon.svg';
        deleteIcon.alt = 'Trash Icon';
        deleteIcon.style.position = 'absolute';
        deleteIcon.style.width = '30px';
        deleteIcon.style.height = '30px';
        deleteIcon.style.top = '10px';
        deleteIcon.style.right = '200px';
        deleteIcon.style.cursor = 'pointer';
        deleteIcon.onclick = () => deleteImage(projectId, imageId, carouselItem);
        return deleteIcon;
    }

    function createZoomIcon(imagePath) {
        // Create anchor element
        const zoomLink = document.createElement('a');
        zoomLink.href = `/images/${projectId}/${imagePath}`;
        zoomLink.target = '_blank'; // Optional: opens in a new tab
        zoomLink.style.position = 'absolute';
        zoomLink.style.top = '10px';
        zoomLink.style.right = '150px';

        // Create zoom icon (img element)
        const zoomIcon = document.createElement('img');
        zoomIcon.src = '/static/img/zoom_icon.svg';
        zoomIcon.alt = 'Zoom Icon';
        zoomIcon.style.width = '30px';
        zoomIcon.style.height = '30px';
        zoomIcon.style.cursor = 'pointer';

        zoomLink.appendChild(zoomIcon);
        return zoomLink;
    }

    function createIndicator(index) {
        const indicator = document.createElement('button');
        indicator.type = 'button';
        indicator.setAttribute('data-bs-target', '#carouselExampleIndicators');
        indicator.setAttribute('data-bs-slide-to', index);
        indicator.className = index === 0 ? 'active' : '';
        indicator.setAttribute('aria-current', index === 0 ? 'true' : 'false');
        indicator.setAttribute('aria-label', `Slide ${index + 1}`);
        return indicator;
    }

    function deleteImage(projectId, imageId) {
        if (!confirm('დარწმუნებული ხართ რომ გსურთ ამ სურათის წაშლა?')) return;

        const token = sessionStorage.getItem('access_token');

        // makeApiRequest is in the globalAccessControl.js
        makeApiRequest(`/api/project/${projectId}/images/${imageId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(data => {
            if (data.message) {
                showAlert('success', data.message);
                // Optionally, remove the row from the table
                fetchImages();
            } else if (data.error) {
                showAlert('danger', data.error || 'Error: გაუმართავი სურათის წაშლა.');
            }
        })
        .catch(error => {
            console.error('Error during deleting image:', error);
        });
    }

    document.getElementById('uploadButton').onclick = function() {
        uploadImages();
    };

    function uploadImages() {
        const inputElement = document.getElementById('images');
        const files = inputElement.files;

        if (files.length === 0) {
            showAlert('danger', 'გთხოვთ აირჩიოთ სურათები.');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }

        const token = sessionStorage.getItem('access_token');

        uploadingSpinner.style.display = 'flex'; // Show spinner

        // makeApiRequest is in the globalAccessControl.js
        makeApiRequest(`/api/project/${projectId}/images`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        })
        .then(data => {
            if (data.message) {
                inputElement.value = '';
                showAlert('success', data.message);
                // Optionally, remove the row from the table
                fetchImages(); // Refresh carousel dynamically
            } else if (data.error) {
                showAlert('danger', data.error || 'Error: გაუმართავი სურათის დამატება.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            // Hide the spinner after the upload is complete
            uploadingSpinner.style.display = 'none';
        });
    }

    function displayPlaceholderImage() {
        carouselInner.innerHTML = ''; // Clear existing images
        const item = document.createElement('div');
        item.className = `carousel-item imageProjectDiv active`;
        item.setAttribute('data-slide-to', 0);

        const img = createImageElement('/static/img/image_not_available.png');

        item.appendChild(img);
        carouselInner.appendChild(item);
    }
});
