async function playNewsReport() {
    try {
        const audioFile = await eel.get_news_audio()();
        console.log("Audio file retrieved successfully.");
        var audio = document.getElementById('newsAudio');
        var source = document.getElementById('audioSource');
        source.src = audioFile;
        audio.load();
        audio.play();
    } catch (error) {
        console.error("Error playing news report:", error);
    }
}