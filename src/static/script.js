// script.js
document.getElementById('generateBtn').addEventListener('click', async () => {
    const topic = document.getElementById('topic').value;
    if (!topic) {
        alert('Please enter a topic');
        return;
    }

    // Display a loading message or animation (optional)
    document.getElementById('videoContainer').innerHTML = 'Generating video...';

    try {
        const response = await fetch('/generate-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic })
        });

        if (response.ok) {
            const data = await response.json();
            const videoUrl = data.videoUrl;
            document.getElementById('videoContainer').innerHTML = `<video id="generatedVideo" controls src="${videoUrl}"></video>`;
        } else {
            document.getElementById('videoContainer').innerHTML = 'Failed to generate video.';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('videoContainer').innerHTML = 'Error generating video.';
    }
});
