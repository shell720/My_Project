#include<stdio.h>
#include<stdlib.h>
#include<omp.h>

#define N 2000

//ワーシャルフロイドの並列化の確認
int main(){
    int i, j, k;
    static int A[N][N], B[N][N];
    double t1, t2, t3, t4;
    
    long long res = 1234;
    for(i=0;i<N;i++) for(j=0;j<N;j++) if(i!=j){
        res = (res * 7 + 5678) % 100000007;
        A[i][j] = res;
        B[i][j] = res;
    }

    t1 = omp_get_wtime();
    for(k=0;k<N;k++){
        for(i=0;i<N;i++){
            for(j=0;j<N;j++){
                if(A[i][j] > A[i][k] + A[k][j]){
                    A[i][j] = A[i][k] + A[k][j];
                }
            }
        }
    }
    t2 = omp_get_wtime();

    t3 = omp_get_wtime();
    for(k=0;k<N;k++){
        #pragma omp parallel
        for(i=0;i<N;i++){
            for(j=0;j<N;j++){
                if(B[i][j] > B[i][k] + B[k][j]){
                    B[i][j] = B[i][k] + B[k][j];
                }
            }
        }
    }
    t4 = omp_get_wtime();

    printf("time: %f [s]\n", t2-t1);
    printf("time parallel: %f [s]\n", t4-t3);

    for (i=0; i<N; i++){
        for (j=0; j<N; j++){
            if (A[i][j] != B[i][j]) {
                printf("Not Equal");
            }
        }
    }
}