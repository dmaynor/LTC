program word_count
    implicit none
    character(len=256) :: word
    character(len=256), allocatable :: words(:)
    integer, allocatable :: counts(:)
    integer :: ios, n, i, j, found
    logical :: exists

    n = 0
    allocate(words(1000), counts(1000))
    counts = 0

    open(10, file='input.txt', status='old')
    do
        read(10, *, iostat=ios) word
        if (ios /= 0) exit
        found = 0
        do i = 1, n
            if (trim(words(i)) == trim(word)) then
                counts(i) = counts(i) + 1
                found = 1
                exit
            end if
        end do
        if (found == 0) then
            n = n + 1
            words(n) = word
            counts(n) = 1
        end if
    end do
    close(10)

    open(20, file='output.txt', status='replace')
    do i = 1, n
        write(20, '(A,": ",I0)') trim(words(i)), counts(i)
    end do
    close(20)
end program word_count
