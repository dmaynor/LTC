Point <- setRefClass("Point",
  fields = list(x = "numeric", y = "numeric"),
  methods = list(
    initialize = function(x = 0, y = 0) {
      .self$x <- x
      .self$y <- y
    },
    distance_to = function(other) {
      sqrt((x - other$x)^2 + (y - other$y)^2)
    }
  )
)
