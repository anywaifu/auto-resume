// Tab activation function (defined globally)
function activateTab(clickedTab) {
    document.querySelectorAll('.tab-btn').forEach(tab => {
        tab.classList.remove('border-purple-500', 'font-medium');
    });
    clickedTab.classList.add('border-purple-500', 'font-medium');
    clickedTab.classList.remove('border-transparent');
}

document.addEventListener('DOMContentLoaded', function() {
    // Save button functionality
    const saveButton = document.getElementById('save-button');
    if (saveButton) {
        saveButton.addEventListener('click', function() {
            // In a real app, we would collect all form data
            // For now, just show a notification
            showNotification('Resume saved successfully!', 'success');
        });
    }

    // Download button functionality
    const downloadButton = document.getElementById('download-button');
    if (downloadButton) {
        downloadButton.addEventListener('click', function() {
            // In a real app, we would generate a PDF
            // For now, just show a notification
            showNotification('Resume downloaded as PDF', 'success');
        });
    }

    // Function to refresh the resume preview
    function refreshResumePreview() {
        fetch('/api/resume/section/preview')
            .then(response => response.text())
            .then(html => {
                const previewContainer = document.querySelector('.resume-preview');
                if (previewContainer) {
                    previewContainer.outerHTML = html;
                }
            }).catch(error => {
                console.error('Error refreshing preview:', error);
            });
    }

    // Shows a notification message
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500' : 'bg-red-500'
        } text-white transition-opacity duration-500`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Remove the notification after 3 seconds
        setTimeout(() => {
            notification.classList.add('opacity-0');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 500);
        }, 3000);
    }

    // Add HTMX event listeners
    document.body.addEventListener('htmx:afterSwap', function(event) {
        // If the changed element is an input or textarea in the form,
        // refresh the preview
        if (event.detail.target && 
            (event.detail.target.matches('input, textarea') || event.detail.target.closest('input, textarea'))) {
            // This would update the preview with the latest data
            console.log('Form updated, should refresh preview');
            refreshResumePreview();
        }
    });

    // Initialize AI interaction UI
    htmx.on('htmx:afterRequest', function(event) {
        if (event.detail.elt.matches('[hx-post="/api/ai/enhance"]')) {
            showNotification('Text enhanced with AI!', 'success');
        }

        if (event.detail.elt.matches('[hx-post="/api/ai/generate-points"]')) {
            showNotification('AI-generated points added!', 'success');
        }
    });

});