subroutine parse_int(s, value, success, error)
    character(len=*), intent(in) :: s
    integer, intent(out) :: value
    logical, intent(out) :: success
    character(len=*), intent(out) :: error
    integer :: ios

    read(s, *, iostat=ios) value
    if (ios == 0) then
        success = .true.
        error = ''
    else
        success = .false.
        value = 0
        error = 'Invalid integer format'
    end if
end subroutine parse_int
