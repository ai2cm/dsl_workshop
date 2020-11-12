
program serialBox_tutorial

    implicit none

    integer          :: int0, ii, jj
    real             :: real0

    double precision, dimension(:,:), allocatable :: dp_arr0

    ! Initialize Serialbox
    !$ser init directory='./data' prefix='example' unique_id=.true.
    !$ser mode write
    !$ser on
    
    ! Set up the data as indicated in the above cell
    int0  = 7
    real0 = 8.9

    allocate(dp_arr0(10,11))

    do jj = 1, 11
        do ii = 1, 10
            dp_arr0(ii,jj) = (jj-1) + ii + 0.1
            !write(*,*) 'dp_arr0(', ii, ',', jj, ') = ', dp_arr0(ii,jj)
        enddo
    enddo
    ! Write out the data as indicated in the above cell using Serialbox
    !$ser savepoint 'input_data'
    !$ser data int0=int0 real0=real0
    !$ser data dp_arr0=dp_arr0

    !!$ser cleanup
   
end program
