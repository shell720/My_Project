package vmWriter

import (
	"Compiler/symbolTable"
	"Compiler/typefile"
)

var classSymTable = map[string]*typefile.TableValue{}
var subrouSymTable = map[string]*typefile.TableValue{}
var cstStaticCnt = 0
var cstFieldCnt = 0
var sstArgCnt = 0
var sstVarCnt = 0

func DFS(tree typefile.ParseVertex, file *string, p typefile.ParseVertex, idx int) {
	if tree.Name == "subroutineDec" { //シンボルテーブルをリセットする
		subrouSymTable["this"] = &typefile.TableValue{Type: p.ChildList[1].Word, Attr: "argument", No: sstArgCnt}
		sstArgCnt++
	}
	if len(tree.ChildList) == 0 {
		//fmt.Println(p.Name)
		if tree.Word != "" {
			symbolTable.Symbol(tree, p, idx, &classSymTable, &subrouSymTable, &cstStaticCnt, &cstFieldCnt, &sstArgCnt, &sstVarCnt)
		}
	}
	for i, v := range tree.ChildList {
		DFS(v, file, tree, i)
	}
	if p.Name == "subroutineDec" { //シンボルテーブルをリセットする
		if idx == p.ChildNum-1 {
			subrouSymTable = map[string]*typefile.TableValue{}
			sstVarCnt = 0
			sstArgCnt = 0
		}
	}
}

//ct map[string]typefile.TableValue, st map[string]typefile.TableValue
