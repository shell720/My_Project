package symbolTable

import (
	"Compiler/typefile"
	"fmt"
)

func Symbol(t typefile.ParseVertex, p typefile.ParseVertex, i int,
	ct *map[string]*typefile.TableValue, st *map[string]*typefile.TableValue,
	cSCnt *int, cFCnt *int, sArgCnt *int, sVarCnt *int) {

	if t.Tkind == "identifier" {
		fmt.Print(t.Word, " ,")
		//fmt.Print(p.ChildList, " ,")
		//fmt.Print(p.Name, " ,")

		if p.Name == "subCall" {
			//文法としてclassかsubroutineが呼ばれるとこるなら、ここで先に識別子のカテゴリを処理する
			//typeでclassとして定義される以外を処理
			if i != 0 && p.ChildList[i-1].Word == "." {
				fmt.Print("category: subroutine")
			} else if p.ChildList[i+1].Word == "." {
				fmt.Print("category: class")
			} else if p.ChildList[i+1].Word == "(" {
				fmt.Print("category: subroutine")
			}
		} else if p.Name == "class" {
			fmt.Print("category: class")
		} else if p.Name == "parameterList" {
			if i%3 == 1 {
				fmt.Print("category: argument")
				fmt.Print(", 型: ", p.ChildList[i-1].Word)
				(*st)[t.Word] = &typefile.TableValue{Type: p.ChildList[1].Word, Attr: "var", No: *sArgCnt}
				*sArgCnt++
			} else {
				fmt.Print("category: class")
			}
		} else {
			if i != 1 {
				if p.ChildList[0].Word == "var" {
					fmt.Print("category: var")
					fmt.Print(", 型: ", p.ChildList[1].Word)
					(*st)[t.Word] = &typefile.TableValue{Type: p.ChildList[1].Word, Attr: "var", No: *sVarCnt}
					*sVarCnt++
				} else if p.ChildList[0].Word == "static" {
					fmt.Print("category: static")
					fmt.Print(", 型: ", p.ChildList[1].Word)
					(*ct)[t.Word] = &typefile.TableValue{Type: p.ChildList[1].Word, Attr: "static", No: *cSCnt}
					*cSCnt++
				} else if p.ChildList[0].Word == "field" {
					fmt.Print("category: field")
					fmt.Print(", 型: ", p.ChildList[1].Word)
					(*ct)[t.Word] = &typefile.TableValue{Type: p.ChildList[1].Word, Attr: "field", No: *cFCnt}
					*cFCnt++
				} else if p.ChildList[0].Word == "function" || p.ChildList[0].Word == "constructor" || p.ChildList[0].Word == "method" {
					fmt.Print("category: subroutine")
					//fmt.Print(", 型: ", p.ChildList[1].Word)
					//classSymTable[t.Word]
				} else {
					{ //既に定義されている場合 ローカルテーブルを先に探す
						v1, ok1 := (*st)[t.Word]
						v2, ok2 := (*ct)[t.Word]
						if ok1 {
							vTable := *v1
							fmt.Print(vTable.Attr)
							fmt.Print(", ", vTable.No)
						} else if ok2 {
							vTable := *v2
							fmt.Print(vTable.Attr)
							fmt.Print(", ", vTable.No)
						}
					}
				}
			} else { //既に定義されている場合
				v1, ok1 := (*st)[t.Word]
				v2, ok2 := (*ct)[t.Word]
				if ok1 {
					vTable := *v1
					fmt.Print(vTable.Attr)
					fmt.Print(", ", vTable.No)
				} else if ok2 {
					vTable := *v2
					fmt.Print(vTable.Attr)
					fmt.Print(", ", vTable.No)
				} else {
					fmt.Print("category: class")
				}
			}
		}

		fmt.Println("")
	}
}
