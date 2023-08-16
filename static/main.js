function openTab(tabName) {
    if (tabName === 'allvideos') {
        window.location.href = '/allvideos';
    } else if (tabName === 'analytics') {
        window.location.href = '/analytics';
    }
}


function openModal(videoSrc) {


    fetch(`http://127.0.0.1:5000/tiktok?id=${videoSrc}`)
        .then(response => response.json()) // Parse the response as JSON
        .then(data => {
            const videoUrl = data.video_url; // Extract the video URL from the JSON response

            const modal = document.getElementById('videoModal');
            const modalVideo = document.getElementById('modalVideo');

            modalVideo.src = "http://127.0.0.1:5000/stream?url_base64=" + btoa(videoUrl);
            modal.style.display = 'flex';
        })
        .catch(error => console.log('error', error));



}

function fetchVideosByRegion() {
    const selectedRegion = document.getElementById('regions').value;

    fetch(`http://127.0.0.1:5000/fetchvideosregion?region=${selectedRegion}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            window.location.reload();

        })
        .catch(error => console.log('Error fetching videos:', error));
}


function closeModal() {
    const modal = document.getElementById('videoModal');
    const modalVideo = document.getElementById('modalVideo');

    modalVideo.src = '';
    modal.style.display = 'none';
}