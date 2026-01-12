fun parseInt(s: String): Result<Int> = runCatching { s.toInt() }
