
program heat

    implicit none

    integer :: ii, jj, kk, N, t_steps, curr_step, nx, ny, nz, nhalo

    real :: scale

    double precision, dimension(:,:,:), allocatable :: curr_Heat, future_Heat

    write(*,*) "Enter the Number of discretization cells N: "
    read(*,*) N
    write(*,*) "Enter number of time steps : "
    read(*,*) t_steps

    write(*,*) "N = ", N
    write(*,*) "Time steps = ", t_steps

    ! Note : Currently, the default domain is a cube, so the number of 
    !        discretization cells in x, y, and z are the same
    nhalo = 1
    nx = N
    ny = N
    nz = N
    allocate(curr_Heat(nx+2*nhalo,ny+2*nhalo,nz), future_Heat(nx+2*nhalo,ny+2*nhalo,nz))
   
    !***Insert Serialbox calls here for initialization***
    !$ser init directory='./data' prefix="HEAT" unique_id=.true.
    !$ser mode write
    !$ser on

    curr_Heat   = 0.0
    future_Heat = 0.0

    scale = 0.1

    curr_Heat(nhalo+1:nx-nhalo, nhalo+1:ny-nhalo, nhalo+1:nz-nhalo) = 1.0

    !***Insert Serialbox calls to create a savepoint to save initial starting data***
    !$ser savepoint 'starting_heat'
    !$ser data init_T=curr_Heat scale=scale t_steps=t_steps nhalo=nhalo
    do curr_step = 1,t_steps
        do kk = 2,nz-1
            do jj = nhalo,ny-nhalo-1
                do ii = nhalo+1,nx-nhalo-1
                    future_Heat(ii,jj,kk) = curr_Heat(ii,jj,kk)              &
                                        + scale * (curr_Heat(ii-1,jj,kk)   &
                                                    -2.0*curr_Heat(ii,jj,kk) &
                                                    +curr_Heat(ii+1,jj,kk))  &
                                        + scale * (curr_Heat(ii,jj-1,kk)   &
                                                    -2.0*curr_Heat(ii,jj,kk) &
                                                    +curr_Heat(ii,jj+1,kk))  &
                                        + scale * (curr_Heat(ii,jj,kk-1)   &
                                                    -2.0*curr_Heat(ii,jj,kk) &
                                                    +curr_Heat(ii,jj,kk+1))
                enddo
            enddo
        enddo

        curr_Heat = future_Heat

    enddo
    
    !***Insert Serialbox calls to create a savepoint to write finalized data***
    !$ser savepoint 'final_heat'
    !$ser data final_T=curr_Heat
    !$ser cleanup

end program
