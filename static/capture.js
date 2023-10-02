const video = document.getElementById('video');
const captureButton = document.getElementById('capture');
const canvas = document.getElementById('canvas');

// Access user's webcam
navigator.mediaDevices.getUserMedia({ video: true })
.then((stream) => {
    video.srcObject = stream;
})
.catch((err) => {
    console.error('Error accessing webcam:', err);
});

// Capture image from webcam and send to backend
captureButton.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the captured image to data URL and send to the backend
    const imageBlob = dataURItoBlob(canvas.toDataURL('image/jpeg'));

    const formData = new FormData();
    formData.append('image', imageBlob, 'captured_image.jpg');

    fetch('/face_verification', {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            // Redirect to the next page or index.html based on server response
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                console.error('Image capture failed:', data.message);
            }
        } else {
            console.error('Image capture failed:', data.message);
        }
    })
    .catch((error) => {
        console.error('Error capturing image:', error);
    });
});

// Helper function to convert data URI to Blob
function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
}