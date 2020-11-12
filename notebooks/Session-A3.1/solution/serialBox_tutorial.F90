
module mod0
    type der_data_type
    
        integer :: int0
        real    :: real0
            
        double precision, dimension(:,:), allocatable :: dp_arr0
            
    end type der_data_type
end module mod0

program serialBox_tutorial
    use mod0
    implicit none

    integer          :: int0, ii, jj
    real             :: real0

    real, dimension(:,:), allocatable :: dp_arr0

    type(der_data_type) dd_Type
            
    ! Initialize Serialbox
    !$ser init directory='./data' prefix='example' unique_id=.true.
    !$ser mode write
    !$ser on
    
    ! Set up the data as indicated in the above cell
    int0  = 7
    real0 = 8.9

    allocate(dp_arr0(10,11))

    dd_Type%int0  = 7
    dd_Type%real0 = 8.9
    allocate(dd_Type%dp_arr0(10,11))
    
    do jj = 1, 11
        do ii = 1, 10
            dp_arr0(ii,jj) = (jj-1) + ii + 0.1
            dd_Type%dp_arr0(ii,jj) = (jj-1) + ii + 0.1
            !write(*,*) 'dp_arr0(', ii, ',', jj, ') = ', dp_arr0(ii,jj)
        enddo
    enddo
    ! Write out the data as indicated in the above cell using Serialbox
    !$ser savepoint 'input_data'
    !$ser data int0=int0 real0=real0
    !$ser data dp_arr0=dp_arr0
    !$ser data ddt_int0=dd_Type%int0 ddt_real0=dd_Type%real0 ddt_arr0=dd_Type%dp_arr0
    !!$ser cleanup
   
end program
