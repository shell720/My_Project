#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double innerProduct(int n, double* X, double* Y){
    int i; double res = 0.0;
    for (int i=0; i<n; i++){
        res += X[i]*Y[i];
    }
    return res;
}

int main(int argc, char* argv[]){
    int i,j; int n,m; //(m,n)行列
    double scale, tmp;

    m = atoi(argv[1]);
    n = atoi(argv[2]);

    // A, B: (m,n)行列だが、列ベクトルに連続アクセスしたいので[n][m]とする
    // Aを直接変形してQとする
    double (*restrict A)[m]; double (*restrict B)[m]; double (*restrict R)[n];
    A = (double (* restrict)[m]) malloc(sizeof(double[m])*n);
    B = (double (* restrict)[m]) malloc(sizeof(double[m])*n);
    R = (double (* restrict)[n]) malloc(sizeof(double[n])*n);
    if (A == NULL || B == NULL || R == NULL) {
        printf("Erroe: out of memory");
        return 0;
    }

    srand(42);
    for (int i=0; i<n; i++){
        for (int j=0; j<m; j++){
            A[i][j]  = B[i][j] = 2.0 * rand() / RAND_MAX - 1.0;
        }
    }
    for (int i=0; i<n; i++){
        for (int j=i+1; j<n; j++){
            R[i][j] = 0.0;
        }
    }

    for (int i=0; i<n; i++){ //i列目の処理、i-1までは処理済
        R[i][i] = sqrt(innerProduct(m, A[i], A[i])); //qiの大きさを求めた
        scale = 1.0/R[i][i];
        for (int j=0; j<m; j++){
            A[i][j] *= scale; //Qについて、その列の大きさで割ってi列目までを確定させる
        }
        for (int j=i+1; j<n; j++){ //Qについてi列目の成分を抜き去る
            R[j][i] = innerProduct(m, A[i], A[j]);
            for (int k=0; k<m; k++){
                A[j][k] -= R[j][i]*A[i][k];
            }
        }
    }

    for (int i =0; i<m; i++){
        for (int j=0; j<n; j++){
            tmp = 0.0;
            for (int k=0; k<n; k++){
                tmp += A[k][i] * R[j][k];
            }
            printf("(res: %f, expect: %f)", tmp, B[j][i]);
        }
        printf("\n");
    }
    return 0;
}