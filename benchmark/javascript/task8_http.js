async function fetchUrl(url) {
    try {
        const response = await fetch(url);
        const body = await response.text();
        return { success: true, body };
    } catch (error) {
        return { success: false, error: error.message };
    }
}
