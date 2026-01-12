import java.net.URI

fun fetchUrl(url: String): Result<String> = runCatching {
    URI(url).toURL().readText()
}
