
program heat

    implicit none

    integer :: ii, jj, kk, N, t_steps, curr_step

    real :: scale

    real, dimension(:,:,:), allocatable :: curr_T, future_T

    ! Note : The default domain is a cube, so the number of 
    !        discretization cells in x, y, and z are the same
    write(*,*) "Enter the Number of discretization cells N: "
    read(*,*) N
    write(*,*) "Enter number of time steps : "
    read(*,*) t_steps

    write(*,*) "N = ", N
    write(*,*) "Time steps = ", t_steps

    allocate(curr_T(N,N,N), future_T(N,N,N))

    ! Insert Serialbox calls here for initialization
    
    !$ser init directory='./data' prefix="HEAT" unique_id=.true.
    !$ser mode write
    !$ser on

    curr_T   = 0.0
    future_T = 0.0

    scale = 0.1

    curr_T(2:N-1, 2:N-1, 2:N-1) = 1.0

    ! Insert Serialbox calls to create a savepoint to save initial starting data
    !$ser savepoint 'starting_heat'
    !$ser data init_T=curr_T scale=scale t_steps=t_steps

    do curr_step = 1,t_steps
        do kk = 2,N-1
            do jj = 2,N-1
                do ii = 2,N-1
                    future_T(ii,jj,kk) = curr_T(ii,jj,kk)              &
                                        + scale * (curr_T(ii-1,jj,kk)   &
                                                    -2.0*curr_T(ii,jj,kk) &
                                                    +curr_T(ii+1,jj,kk))  &
                                        + scale * (curr_T(ii,jj-1,kk)   &
                                                    -2.0*curr_T(ii,jj,kk) &
                                                    +curr_T(ii,jj+1,kk))  &
                                        + scale * (curr_T(ii,jj,kk-1)   &
                                                    -2.0*curr_T(ii,jj,kk) &
                                                    +curr_T(ii,jj,kk+1))
                enddo
            enddo
        enddo

        curr_T = future_T

    enddo
    
    ! Insert Serialbox calls to create a savepoint to write finalized data
    !$ser savepoint 'final_heat'
    !$ser data final_T=curr_T
    !$ser cleanup

end program
