subroutine double_evens(nums, n, result, m)
    integer, intent(in) :: nums(n), n
    integer, intent(out) :: result(n), m
    integer :: i
    m = 0
    do i = 1, n
        if (mod(nums(i), 2) == 0) then
            m = m + 1
            result(m) = nums(i) * 2
        end if
    end do
end subroutine double_evens
