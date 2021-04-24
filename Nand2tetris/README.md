# Just main production of Nand2tetris
コンピュータシステムの理論と実装
――モダンなコンピュータの作り方

## section 5
create a kind of CPU by hardware programming language  
1~4章までやった事を合わせ、CPUやメモリを作成した

## section 6
create program of assembly to machine language by cpp  
c++でアセンブリから機械語へ変換するプログラムの作成

## section 7
create program of VM language(Intermediate code) to assembly by Python3  
7,8章でPython(LLで動的型付けのため良くないが)で中間言語からアセンブラへの変換プログラム
そのうちRustで書き直したい

## section 10,11
creating program of compiler by go  
***goによるコンパイラの作成 パーサ  
go.modについて: go.modのあるファイルから探してimportされるようになる仕組み, 複数ファイルにまたがるもの(structなど)はそれ用のファイルを作成しimportするようにする  