# parallel-processing
色々な並列化プログラミング
## OMP
CのOpenMPによる並列化。  
FindPrimeAndSum: ある範囲の中の整数それぞれについて最大の素数を求めて、その総和を求める。  
Warshell-Floyd: これでワーシャルフロイドの並列化ができると聞いてやってみたけど、やっばり出来ない
## MPI
CのMPIによる並列化。  
dijkstra: 全点対最短路をダイクストラの並列化によって求める、ワーシャルフロイドとの比較。  

## sha256_hexDump
Goの並列化。ファイルの各行を読み込んでSHA256チェックサムのHEXダンプを計算し、元の行の並び通りに出力する。
## QR_decompositon
QR分解をOMPとMPIで高速化する。QR分解は修正グラムシュミットを用いる。