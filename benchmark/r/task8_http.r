fetch_url <- function(url) {
  tryCatch(
    list(success = TRUE, body = readLines(url, warn = FALSE)),
    error = function(e) list(success = FALSE, error = conditionMessage(e))
  )
}
