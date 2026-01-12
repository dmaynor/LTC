function parseInt(s) {
    const num = Number(s);
    if (isNaN(num) || !Number.isInteger(num))
        return { success: false, error: "Invalid integer format" };
    return { success: true, value: num };
}
