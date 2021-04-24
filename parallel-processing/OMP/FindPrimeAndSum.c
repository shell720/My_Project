//ompはスレッド並列(同時書き込みに注意)
//icc -O3 -qopenmp  オプションなしで並列化せずに実行可能
//基本的には普段通りコードを書いて　<omp.h> と　#pragma hoge　を追加するだけ
#include<stdio.h>
#include<omp.h>

#define L 1000LL
#define R 20000000LL

int main(){
  long long n, i, j, t;
  long long answer;
  double t1, t2;

  t1 = omp_get_wtime();

  answer = 0;
  #pragma omp parallel for reduction(+: answer) private(j) schedule(dynamic,10)
  for(i=R; i>=L; i--){
    t = i;
    for(j=2; j*j<=i; j++){
      if(i%j==0){
        t = j;
        break;
      }
    }
    answer += t;
  }

  t2 = omp_get_wtime();

  printf("answer %lld\n", answer);
  printf("time %f\n", t2-t1);
  
  return 0;
}
