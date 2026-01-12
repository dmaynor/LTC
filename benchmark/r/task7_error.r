parse_int <- function(s) {
  result <- tryCatch(
    list(success = TRUE, value = as.integer(s)),
    warning = function(w) list(success = FALSE, error = conditionMessage(w)),
    error = function(e) list(success = FALSE, error = conditionMessage(e))
  )
  result
}
