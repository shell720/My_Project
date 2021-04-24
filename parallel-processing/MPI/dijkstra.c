#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>

#define N 2000
#define INF 2001002003
static int A[N][N];
int dis[N];
int used[N];

void dijkstra (int s, int dis[N]){
  //cでqueueを用いた実装は大変面倒なのでナイーブに実装
  int i;
  for (i=0; i<N; i++){
    dis[i] = INF;
    used[i] = 0;
  }
  dis[s] = 0;
  while (1) {
    int min = INF;
    int now = -1;
    for (i=0 ; i<N; i++){
      if (used[i] == 0 && dis[i] < min ) {
        min = dis[i];
        now = i;
      }
    }
    used[now] = 1;
    //もし全てusedされている
    if (min == INF) break;

    for (i=0; i<N; i++){
      if (dis[i] > dis[now] + A[now][i]) {
        dis[i] = dis[now] + A[now][i];
      }
    }
  }
}

int main(int argc, char **argv){
  int i, j, k;
  int my_rank, num_proc;
  double tm1, tm2;
  long long res;
  //static int A[N][N];
  int myL, myR, tmp;
  long long ans, sum;
  
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &num_proc);
  MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

  res = 1234;
  for(i=0;i<N;i++) for(j=0;j<N;j++) if(i!=j){
    res = (res * 7 + 5678) % 100000007;
    A[i][j] = res;
    //printf("%d, ", A[i][j]);
  }


  MPI_Barrier(MPI_COMM_WORLD);
  tm1 = MPI_Wtime();

  //全ての頂点からダイクストラ
  tmp = N % num_proc; // 割り切れない残りぶん

  myL = N / num_proc * my_rank; //区間の始まり
  myL += (tmp > my_rank ? my_rank : tmp); //うまくずらす
  myR = N / num_proc * (my_rank + 1);
  myR += (tmp > my_rank+1 ? my_rank+1 : tmp);

  sum = 0;
  for(i=myL; i<myR; i++){
    dijkstra(i, dis);
    for (j=0; j<N; j++) sum += dis[j];
  }
  
  // それぞれのsumの結果をプロセス0に集約し合計を取り、それをansに格納ss
  MPI_Reduce(&sum, &ans, 1, MPI_LONG_LONG_INT, MPI_SUM, 0, MPI_COMM_WORLD);
  MPI_Barrier(MPI_COMM_WORLD);
  tm2 = MPI_Wtime();
  
  // parallelize
  for(k=0;k<N;k++){
    for(i=0;i<N;i++){
      for(j=0;j<N;j++){
        if(A[i][j] > A[i][k] + A[k][j]){
          A[i][j] = A[i][k] + A[k][j];
        }
      }
    }
  }
  
  if(my_rank==0){
    res = 0;
    for(i=0;i<N;i++) for(j=0;j<N;j++) res += A[i][j];
    printf("Running time: %f sec\n", tm2-tm1);
    printf("Sum: %lld\n", res);
    printf("Ansewer: %lld\n", ans);
  }
  
  MPI_Finalize();
  return 0;
}
