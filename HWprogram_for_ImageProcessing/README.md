# HWprogram_for_ImageProcessing

Verilog program for ImageProcessing

Quartus usage:  
select working directory -> in this directory, the files which result in complied was created.  
始めに選んだワーキングディレクトリに、コンパイルされたときに生成されるファイル群ができる。プログラムのあるディレクトリにするのが吉

The project name you decide on -> basically the same as your program file name  
自分で設定するプロジェクト名の部分は、作ったプログラム名と同じにしないと予期した動作をしない

If Analysis&Elaboration fail, it means that your program is mistake. Then you can modify in the Quartus(so, Quartus is IDE??).  
Analysis&Elaborationでエラーとなる時はコンパイルでエラーが出ているのでデバック。この時Quartus上で(左のEntitiy:Instanceから)ファイルを開いて編集&再コンパイル出来る。