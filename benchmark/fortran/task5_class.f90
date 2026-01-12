module point_mod
    implicit none
    type :: Point
        real :: x, y
    contains
        procedure :: distance_to
    end type Point
contains
    function distance_to(self, other) result(d)
        class(Point), intent(in) :: self, other
        real :: d, dx, dy
        dx = self%x - other%x
        dy = self%y - other%y
        d = sqrt(dx*dx + dy*dy)
    end function distance_to
end module point_mod
