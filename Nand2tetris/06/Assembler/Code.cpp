#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <map>
#include <sstream>
#include <bitset>
#include <cctype>
#include <algorithm>

using std::string;
using std::cin;
using std::cout;
using std::endl;
using std::map;

string dest2binary(string dest){
    map< string, string> henkan;
    henkan[""]="000";
    henkan["M"]="001";
    henkan["D"]="010";
    henkan["MD"]="011";
    henkan["A"]="100";
    henkan["AM"]="101";
    henkan["AD"]="110";
    henkan["AMD"]="111";
    return henkan[dest];
}

string jump2binary(string jump){
    map< string, string> henkan;
    henkan[""]="000";
    henkan["JGT"]="001";
    henkan["JEQ"]="010";
    henkan["JGE"]="011";
    henkan["JLT"]="100";
    henkan["JNE"]="101";
    henkan["JLE"]="110";
    henkan["JMP"]="111";
    return henkan[jump];
}

string comp2binary(string comp){
    map< string, string> henkan;
    henkan["0"]=   "0101010";
    henkan["1"]=   "0111111";
    henkan["-1"]=  "0111010";
    henkan["D"]=   "0001100";
    henkan["A"]=   "0110000";
    henkan["M"]=   "1110000";
    henkan["!D"]=  "0001101";
    henkan["!A"]=  "0110001";
    henkan["!M"]=  "1110001";
    henkan["-D"]=  "0001111";
    henkan["-A"]=  "0110011";
    henkan["-M"]=  "1110011";
    henkan["D+1"]= "0011111";
    henkan["A+1"]= "0110111";
    henkan["M+1"]= "1110111";
    henkan["D-1"]= "0001110";
    henkan["A-1"]= "0110010";
    henkan["M-1"]= "1110010";
    henkan["D+A"]= "0000010";
    henkan["D+M"]= "1000010";
    henkan["D-A"]= "0010011";
    henkan["D-M"]= "1010011";
    henkan["A-D"]= "0000111";
    henkan["M-D"]= "1000111";
    henkan["D&A"]= "0000000";
    henkan["D&M"]= "1000000";
    henkan["D|A"]= "0010101";
    henkan["D|M"]= "1010101";
    return henkan[comp];
}

string int2bin(int x){ //Aコマンドでアドレスに変換
    std::stringstream ss;
    ss << static_cast<std::bitset <16> >(x);
    string x_bin = ss.str();
    return x_bin;
}

map< string, string> create_table(){
    map< string, string> SymbolTable;
    SymbolTable["SP"]=     int2bin(0);
    SymbolTable["LCL"]=    int2bin(1);
    SymbolTable["ARG"]=    int2bin(2);
    SymbolTable["THIS"]=   int2bin(3);
    SymbolTable["THAT"]=   int2bin(4);
    SymbolTable["R0"]=     int2bin(0);
    SymbolTable["R1"]=     int2bin(1);
    SymbolTable["R2"]=     int2bin(2);
    SymbolTable["R3"]=     int2bin(3);
    SymbolTable["R4"]=     int2bin(4);
    SymbolTable["R5"]=     int2bin(5);
    SymbolTable["R6"]=     int2bin(6);
    SymbolTable["R7"]=     int2bin(7);
    SymbolTable["R8"]=     int2bin(8);
    SymbolTable["R9"]=     int2bin(9);
    SymbolTable["R10"]=    int2bin(10);
    SymbolTable["R11"]=    int2bin(11);
    SymbolTable["R12"]=    int2bin(12);
    SymbolTable["R13"]=    int2bin(13);
    SymbolTable["R14"]=    int2bin(14);
    SymbolTable["R15"]=    int2bin(15);
    SymbolTable["SCREEN"]= int2bin(16384);
    SymbolTable["KBD"]=    int2bin(24576);
    return SymbolTable;
}

bool check_int(string str) //Aコマンドで受け取るのが数字かシンボルかどうかを判定する
{
    if (std::all_of(str.cbegin(), str.cend(), isdigit))
    {
        //std::cout << stoi(str) << std::endl;
        return true;
    }
    //std::cout << "not int" << std::endl;
    return false;
}


string get_address(map<string, string> &table, int &memory_number, string symbol){
    if (table.count(symbol)!=0) {
        return table[symbol];
    } else {
        string address=int2bin(memory_number++);
        table[symbol]=address;
        return address;
    }
}

void parser(string file, map<string, string> &table, bool shuukai=true){
    std::ifstream file_content(file);
    string command;
    std::smatch results;
    int address=16;
    int cnt_line=0;
    while (getline(file_content, command)){
        //cout<<command<<endl;
        //コメント部分は削除
        command= std::regex_replace(command, std::regex("//[^\n]*"), "");
        //改行、空白は削除
        command= std::regex_replace(command, std::regex("\\s+"), "");
        if (command.empty()) continue;
        if (std::regex_match(command, results, std::regex("(@)([\\w\\.\\$\\:]+)"))) {
            cnt_line++;
            //Aコマンド
            // 受け取るシンボル名　results[2].str();
            if (shuukai){
                if (check_int(results[2].str())){ //数値で受け取る時
                    string ACmd=int2bin(stoi(results[2].str()));
                    cout<<ACmd<<endl;
                }else { //変数シンボルで受け取る時
                    cout<<get_address(table, address, results[2].str())<<endl;
                }
            }
        } else if (std::regex_match(command, results, std::regex("(\\()([\\w\\.\\$\\:]+)(\\))"))) {
            //Lコマンド
            //cout<<results[2].str()<<endl;
                if (shuukai==false){
                    table[results[2].str()]=int2bin(cnt_line);
                } 
        } else {
            cnt_line++;
            if (shuukai){
                std::regex_match(command, results, std::regex("([ADM]*)(\\=?)([01ADM\\+\\-\\&\\|\\!]+)(\\;?)(\\w*)"));
                //cout<<command;
                string bin_dest, bin_jump, bin_comp;
                bin_dest=dest2binary(results[1].str());
                bin_comp=comp2binary(results[3].str());
                bin_jump=jump2binary(results[5].str());
                cout<<"111"<<bin_comp<<bin_dest<<bin_jump<<endl;
            }
        }
    }
    //return "Fin.";
}

int main(int argc, char *argv[]){ //char型ポインターでstringに
    //cout<<argc<<endl;
    if (argc!=2){
        cout<<"Error 一つのファイルを引数にしてください"<<endl;
        cout<<"使用方法: Code.cpp <ファイル名>"<<endl;
        return 0;
    } 
    string line;
    map<string, string> Table=create_table();
    parser(argv[1], Table, false);
    parser(argv[1], Table);
    //int address=16;
    //cout<<Table["OUTPUT_FIRST"]<<endl;
    //cout<<get_address(Table, address, "MEM")<<endl;
    //cout<<get_address(Table, address, "dis")<<endl;
    //cout<<get_address(Table, address, "SP")<<endl;

    return 0;
    //コマンドラインでリダイレクト　>./../ディレクトリ/ファイル名.hack
}
