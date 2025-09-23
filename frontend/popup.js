// popup.js - Frontend Logic

// Function to get video ID from YouTube URL
function getYouTubeVideoId(url) {
    const regex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

document.addEventListener('DOMContentLoaded', () => {
    const videoIdInput = document.getElementById('videoId');
    const questionInput = document.getElementById('question');
    const askButton = document.getElementById('askButton');
    const answerDiv = document.getElementById('answer');

    // Automatically fill the video ID if the user is on a YouTube video page
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const currentTab = tabs[0];
        if (currentTab && currentTab.url.includes("youtube.com/watch")) {
            const videoId = getYouTubeVideoId(currentTab.url);
            if (videoId) {
                videoIdInput.value = videoId;
            }
        }
    });

    askButton.addEventListener('click', async () => {
        const videoId = videoIdInput.value.trim();
        const question = questionInput.value.trim();

        if (!videoId || !question) {
            answerDiv.textContent = 'Please provide both a video ID and a question.';
            return;
        }

        // Show loading state
        answerDiv.textContent = 'Thinking...';
        askButton.disabled = true;
        askButton.textContent = 'Processing...';

        try {
            // Send the data to your Flask backend
            const response = await fetch('http://127.0.0.1:5000/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    video_id: videoId,
                    question: question,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            answerDiv.textContent = data.answer;

        } catch (error) {
            console.error('Error:', error);
            answerDiv.textContent = 'Failed to connect to the backend. Is the Python server running?';
        } finally {
            // Reset button state
            askButton.disabled = false;
            askButton.textContent = 'Ask';
        }
    });
});