(bool Success, int Value, string? Error) ParseInt(string s)
{
    if (int.TryParse(s, out int value))
        return (true, value, null);
    return (false, 0, "Invalid integer format");
}
