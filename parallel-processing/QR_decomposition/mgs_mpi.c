#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<mpi.h>

double innerp(int N, double *X, double *Y){
  int i;
  double res;

  res = 0.0;
  for(i=0;i<N;i++){
    res += X[i] * Y[i];
  }
  return res;
}

void QR(int M, int N, double (*restrict A)[M], double (*restrict R)[N]){
  int i, j, k;
  double scale;
  
  for(i=0;i<N;i++){
    for(j=i+1;j<N;j++){
      R[i][j] = 0.0; /* Note that R is (mathematically) upper triangular. Note also the order of the indices. */
    }
  }

  for(i=0;i<N;i++){
    R[i][i] = sqrt(innerp(M, A[i], A[i])); /* (Euclidean) norm of A[i] */
    scale = 1.0 / R[i][i];
    for(j=0;j<M;j++){
      A[i][j] *= scale; /* Scaling (normalization) */
    }
    for(j=i+1;j<N;j++){
      R[j][i] = innerp(M, A[i], A[j]);
      for(k=0;k<M;k++){
        A[j][k] -= R[j][i] * A[i][k]; /* i-th component subtracted */
      }
    }
  }
}

int main(int argc, char **argv){
  int i, j, k, M, N; /* M, N: matrix size (M x N) */
  double scale, temp;

  int Mk, Np, M1, M2;
  double t1, t2, t3, t4;

  int my_rank, num_proc;
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &num_proc);
  MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

  M = atoi(argv[1]);
  N = atoi(argv[2]);

  M1 = (long long) M * my_rank / num_proc;
  M2 = (long long) M * (my_rank + 1) / num_proc;
  Mk = M2 - M1;
  Np = N * num_proc;

  double (*restrict A)[M], (*restrict B)[M], (*restrict R)[N]; /* B is a copy of A (for verification) */
  A = (double (*restrict)[M]) malloc(sizeof(double[M])*N);
  B = (double (*restrict)[M]) malloc(sizeof(double[M])*N);
  R = (double (*restrict)[N]) malloc(sizeof(double[N])*N);

  double (*restrict Ak)[Mk], (*restrict Qk)[Mk], (*restrict Rg)[Np];
  Ak = (double (*restrict)[Mk]) malloc(sizeof(double[Mk])*N);
  Qk = (double (*restrict)[Mk]) malloc(sizeof(double[Mk])*N);
  Rg = (double (*restrict)[Np]) malloc(sizeof(double[Np])*N);

  double *restrict y, *restrict v, *restrict beta;
  y=(double *restrict)malloc(sizeof(double)*M);
  v=(double *restrict)malloc(sizeof(double)*N);
  beta=(double *restrict)malloc(sizeof(double)*N);
  
  if(A==NULL || B==NULL || R==NULL || Ak==NULL || Qk==NULL || Rg==NULL || y==NULL || v==NULL || beta==NULL){ /*Terminate if memory not allocated*/
    puts("out of memory");
    return 0;
  }

  if(my_rank==0){
    srand(1); /* Fix the random seed */
    for(i=0;i<N;i++){
      for(j=0;j<M;j++){
	B[i][j] = A[i][j] = 2.0 * rand() / RAND_MAX - 1.0; /*Each element is a random number between -1 and 1*/
      }
    }
    for(i=0;i<M;i++){
      y[i] = 2.0 * rand() / RAND_MAX - 1.0;
    }
  }

  MPI_Barrier(MPI_COMM_WORLD);
  t1 = MPI_Wtime();

  // Step 1: A -> Ak (MPI)
  if(my_rank==0){
    for(i=0;i<Mk;i++) for(j=0;j<N;j++) Ak[j][i] = A[j][i];

    for(k=1;k<num_proc;k++){
      M1 = (long long) M * k / num_proc;
      M2 = (long long) M * (k+1) / num_proc;
      for(i=M1;i<M2;i++){
	for(j=0;j<N;j++){
	  MPI_Send(A[j]+i, 1, MPI_DOUBLE, k, 0, MPI_COMM_WORLD);
	}
      }
    }
  } else {
    for(i=0;i<Mk;i++){
      for(j=0;j<N;j++){
	MPI_Recv(Ak[j]+i, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
    }
  }

  t3 = MPI_Wtime();

  // Step 2: Ak ---> Ak * R (QR decomp.)
  QR(Mk, N, Ak, R);

  // Step 3: R -> Rg (MPI)
  if(my_rank==0){
    for(i=0;i<N;i++) for(j=0;j<N;j++) Rg[j][i] = R[j][i];
    for(k=1;k<num_proc;k++){
      for(i=0;i<N;i++){
	for(j=0;j<N;j++){
	  MPI_Recv(Rg[j]+i+N*k, 1, MPI_DOUBLE, k, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
	}
      }
    }
  } else {
    for(i=0;i<N;i++){
      for(j=0;j<N;j++){
	MPI_Send(R[j]+i, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
      }
    }
  }

  for(i=0;i<Np;i++){
    for(j=0;j<N;j++){
      MPI_Bcast(Rg[j]+i, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    }
  }

  // Step 4: Rg ---> Rg * R (QR decomp.)
  QR(Np, N, Rg, R);

  // Step 5: Qk = Ak * Rg
  for(i=0;i<Mk;i++){
    for(j=0;j<N;j++){
      Qk[j][i] = 0.0;
      for(k=0;k<N;k++){
	Qk[j][i] += Ak[k][i] * Rg[j][k+N*my_rank];
      }
    }
  }

  t4 = MPI_Wtime();

  // Step 6: Qk -> A (MPI)
  if(my_rank==0){
    for(i=0;i<Mk;i++) for(j=0;j<N;j++) A[j][i] = Qk[j][i];

    for(k=1;k<num_proc;k++){
      M1 = (long long) M * k / num_proc;
      M2 = (long long) M * (k+1) / num_proc;
      for(i=M1;i<M2;i++){
	for(j=0;j<N;j++){
	  MPI_Recv(A[j]+i, 1, MPI_DOUBLE, k, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
	}
      }
    }
  } else {
    for(i=0;i<Mk;i++){
      for(j=0;j<N;j++){
	MPI_Send(Qk[j]+i, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
      }
    }
  }


  MPI_Barrier(MPI_COMM_WORLD);
  t2 = MPI_Wtime();

  if(my_rank == 0){
    /* Verification for A = QR. Note that Q (in mathematics) is denoted by A in the program. */
    for(i=0;i<M;i+=1+M/10){
      for(j=0;j<N;j+=1+N/10){
	temp = 0.0;
	for(k=0;k<N;k++){
	  temp += A[k][i] * R[j][k];
	}
	printf("(%f %f) ", B[j][i], temp); /* Mathematically speaking, the original a_{ij} and the obtained (QR)_{ij} */
      }
      puts("");
    }
    puts("");

    for(i=0;i<N;i++){
      v[i] = 0.0;
      for(j=0;j<M;j++){
        v[i] += A[i][j] * y[j];
      }
    }

    for(i=N-1;i>=0;i--){
      beta[i] = v[i];
      for(j=i+1;j<N;j++){
        beta[i] -= R[j][i] * beta[j];
      }
      beta[i] /= R[i][i];
    }

    for(i=0;i<N;i+=1+N/10){
      printf("beta[%d] = %f\n", i, beta[i]);
    }

    puts("");
    printf("timing %f sec\n", t2-t1);
    printf("timing %f sec\n", t4-t3);
  }

  MPI_Finalize();
  return 0;
}

// mpiicc -O3 -std=c99 mgs_mpi.c
// tssrun -A p=3 mpiexec.hydra ./a.out 1000 5

// beta[0] = 0.001510
// beta[1] = -0.005433
// beta[2] = -0.030114
// beta[3] = -0.051595
// beta[4] = 0.041524
