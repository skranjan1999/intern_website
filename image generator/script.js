async function generateImage() {
    const prompt = document.getElementById("imagePrompt").value;
    if (!prompt) return alert("Enter a prompt!");

    const response = await fetch("http://localhost:5000/generate/image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById("generatedImage").src = data.image_url;
        document.getElementById("generatedImage").classList.remove("hidden");
    } else {
        alert("Error: " + data.error);
    }
}

async function generateVideo() {
    const prompt = document.getElementById("videoPrompt").value;
    if (!prompt) return alert("Enter a prompt!");

    const response = await fetch("http://localhost:5000/generate/video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById("generatedVideo").src = data.video_url;
        document.getElementById("generatedVideo").classList.remove("hidden");
    } else {
        alert("Error: " + data.error);
    }
}

async function generateImageToVideo() {
    const fileInput = document.getElementById("imageUpload");
    if (!fileInput.files.length) return alert("Upload an image!");

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("http://localhost:5000/generate/image-to-video", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById("generatedImageVideo").src = data.video_url;
        document.getElementById("generatedImageVideo").classList.remove("hidden");
    } else {
        alert("Error: " + data.error);
    }
}
