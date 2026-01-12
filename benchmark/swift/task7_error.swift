func parseInt(_ s: String) -> Result<Int, Error> {
    if let value = Int(s) {
        return .success(value)
    }
    return .failure(NSError(domain: "ParseError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Invalid integer format"]))
}
