#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<omp.h>

double innerp(int N, double *X, double *Y){
  int i;
  double res;

  res = 0.0;
  // Don't change!
  for (i = 0; i < N; i++){
    res += X[i] * Y[i];
  }
  return res;
}

void dswap(int N, double *restrict X, double *restrict Y){
  int i;
  double t;

  // omp
  #pragma omp parallel for private(t)
  for (i = 0; i < N; i++){
    t = X[i];
    X[i] = Y[i];
    Y[i] = t;
  }
}


int main(int argc, char **argv){
  int i, j, k, M, N;
  double scale, temp, t1, t2;
  int max_thread = omp_get_max_threads();
  double max_value[100];
  int max_index[100];
  double tmp1;

  M = atoi(argv[1]);
  N = atoi(argv[2]);

  double (*restrict A)[M], (*restrict B)[M], (*restrict R)[N];
  A = (double (*restrict)[M]) malloc(sizeof(double[M]) * N);
  B = (double (*restrict)[M]) malloc(sizeof(double[M]) * N);
  R = (double (*restrict)[N]) malloc(sizeof(double[N]) * N);
  if (A == NULL || B == NULL || R == NULL){
    puts("out of memory");
    return 0;
  }

  int *restrict pivot;
  double *restrict nrm2;
  pivot = (int (*restrict)) malloc(sizeof(int) * N);
  nrm2 = (double (*restrict)) malloc(sizeof(double) * N);
  if (pivot == NULL || nrm2 == NULL){
    puts("out of memory");
    return 0;
  }

  srand(1);
  // Don't change!
  for (i = 0; i < N; i++){
    for (j = 0; j < M; j++){
      B[i][j] = A[i][j] = 2.0 * rand() / RAND_MAX - 1.0;
    }
  }

  // omp
  #pragma omp parallel for
  for (i = 0; i < N; i++){
    pivot[i] = i;
    nrm2[i] = 0;
  }
  nrm2[0] = innerp(M, A[0], A[0]);

  // omp
  #pragma omp parallel for private(j)
  for (i = 0; i < N; i++){
    for (j = 0; j < N; j++){
      R[i][j] = 0.0;
    }
  }

  t1 = omp_get_wtime();
  for (i = 0; i < N; i++){
    temp = tmp1 = nrm2[i];
    j = i;
    // omp (relatively difficult)
    #pragma omp parallel for
    for (k=0; k<= max_thread; k++){
      max_value[k] = temp;
      max_index[k] = j;
    }
    #pragma omp parallel for private(tmp1) schedule(dynamic, 5)
    for (k = i + 1; k < N; k++){
      if (nrm2[k] <= 0) { // 0以下なら真面目に計算する
        nrm2[k] = innerp(M, A[k], A[k]);
      }
      if (tmp1 < nrm2[k]){
        tmp1 = nrm2[k];
	      max_value[omp_get_thread_num()] = nrm2[k];
      	max_index[omp_get_thread_num()] = k;
      }
    }
    for (k = 0; k<=max_thread; k++){
      if (temp < max_value[k]){
        temp = max_value[k];
        j = max_index[k];
      }
    }
    printf("max: %f,  ", sqrt(temp)); printf("pivot: %d\n", j);
    if (temp == 0.0) break;
    if (j != i){
      dswap(M, A[i], A[j]);
      dswap(i, R[i], R[j]);
      k = pivot[i];  pivot[i] = pivot[j];  pivot[j] = k;
      nrm2[j] = nrm2[i]; //ノルムの値も入れ替え
    }

    R[i][i] = sqrt(temp);
    scale = 1.0 / R[i][i];

    // omp
    #pragma omp parallel for
    for (j = 0; j < M; j++){
      A[i][j] *= scale;
    }

    // omp
    #pragma omp parallel for private(k)
    for (j = i+1; j < N; j++){
      R[j][i] = innerp(M, A[i], A[j]);
      nrm2[j] -= R[j][i]* R[j][i];
      for (k = 0; k < M; k++){
	      A[j][k] -= R[j][i] * A[i][k];
      }
    }
  }
  t2 = omp_get_wtime();

  for (i = 0; i < M; i += 1 + M/10){
    for (j = 0; j < N; j += 1 + N/10){
      temp = 0.0;
      for (k = 0; k < N; k++){
	      temp += A[k][i] * R[j][k];
      }
      //printf("(%f %f) ", B[pivot[j]][i], temp);
    }
    puts("");
  }
  printf("time = %f sec\n", t2 - t1);

  return 0;
}
