package compileEngine

import (
	"Compiler/typefile"
	"fmt"
)

//CompilationEngine パーサ結果を返す
func CompilationEngine(t *typefile.Token) typefile.ParseVertex { //(*t)でTokenへアクセス
	var ret typefile.ParseVertex
	var f string
	ret.Name = "HEAD"
	var childs []typefile.ParseVertex
	if t.Word == "class" {
		res := compileClass(&t, &f)
		//fmt.Println(res)
		childs = append(childs, res)
	} else {
		fmt.Println("Error: Not start with class")
	}

	if t.Next != nil {
		fmt.Println("Error: Not finish code")
	}
	ret.ChildList = childs
	//fmt.Println(ret)
	return ret
}

func compileClass(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "class" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "class"
	var childs []typefile.ParseVertex
	for {
		var tmp typefile.ParseVertex
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		ret.ChildNum++
		if (*t).Word == "static" || (*t).Word == "field" {
			tmp = compileClassVarDec(t, file) //classVarDecのラストで返す
			(*t) = (*t).Next
			childs = append(childs, tmp)
			continue
		} else if (*t).Word == "constructor" || (*t).Word == "function" || (*t).Word == "method" {
			tmp = compileSubroutine(t, file) //subroutineDecのラストで返す
			(*t) = (*t).Next
			childs = append(childs, tmp)
			continue
		} else if (*t).Word == "}" {
			childs = append(childs, tmp)
			*file += "</" + "class" + ">\n"
			break
		}
		(*t) = (*t).Next
		childs = append(childs, tmp)
	}
	ret.ChildList = childs
	return ret
}
func compileClassVarDec(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "classVarDec" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "classVarDec"
	var childs []typefile.ParseVertex
	for {
		ret.ChildNum++
		var tmp typefile.ParseVertex
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		if (*t).Word == ";" {
			childs = append(childs, tmp)
			*file += "</" + "classVarDec" + ">\n"
			break
		}
		(*t) = (*t).Next
		childs = append(childs, tmp)
	}
	ret.ChildList = childs
	return ret
}
func compileSubroutine(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "subroutineDec" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "subroutineDec"
	var childs []typefile.ParseVertex
	var res typefile.ParseVertex
	res.Name = "subroutineBody"
	var subchilds []typefile.ParseVertex
	for {
		var tmp typefile.ParseVertex
		if (*t).Word == "(" {
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
			ret.ChildNum++
			(*t) = (*t).Next
			res := compileParameterList(t, file)
			childs = append(childs, res)
			ret.ChildNum++
			continue
		} else if (*t).Word == "{" {
			*file += "<" + "subroutineBody" + ">\n"
			ret.ChildNum++
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			subchilds = append(subchilds, tmp)
			res.ChildNum++
			(*t) = (*t).Next
			for { //varのぶん
				if (*t).Word == "var" {
					res.ChildNum++
					tmp1 := compileVarDec(t, file)
					subchilds = append(subchilds, tmp1)
				} else {
					break
				}
			}
			if (*t).Word == "}" { // もしstatementが０個
				*file += "<" + "statements" + ">\n"
				*file += "</" + "statements" + ">\n"
				var tmp typefile.ParseVertex
				tmp.Name = "statements"
				subchilds = append(subchilds, tmp)
				continue
			}
			tmp2 := compileStatements(t, file)
			subchilds = append(subchilds, tmp2)
			res.ChildNum++
			continue
		} else if (*t).Word == "}" {
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			subchilds = append(subchilds, tmp)
			*file += "</" + "subroutineBody" + ">\n"
			*file += "</" + "subroutineDec" + ">\n"
			res.ChildList = subchilds
			childs = append(childs, res)
			break
		}
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		ret.ChildNum++
		(*t) = (*t).Next
		childs = append(childs, tmp)
	}
	ret.ChildList = childs
	return ret
}
func compileParameterList(t **typefile.Token, file *string) typefile.ParseVertex {
	//()中のみ処理
	*file += "<" + "parameterList" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "parameterList"
	var childs []typefile.ParseVertex
	for {
		var tmp typefile.ParseVertex
		if (*t).Word == ")" {
			*file += "</" + "parameterList" + ">\n"
			break
		}
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		childs = append(childs, tmp)
		ret.ChildNum++
		(*t) = (*t).Next
	}
	ret.ChildList = childs
	return ret
}
func compileVarDec(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "varDec" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "varDec"
	var childs []typefile.ParseVertex
	for {
		var tmp typefile.ParseVertex
		ret.ChildNum++
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		childs = append(childs, tmp)
		if (*t).Word == ";" {
			*file += "</" + "varDec" + ">\n"
			(*t) = (*t).Next
			break
		}
		(*t) = (*t).Next
	}
	ret.ChildList = childs
	return ret
}
func compileStatements(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "statements" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "statements"
	var childs []typefile.ParseVertex
	for { //再帰から戻ってくる時はそれぞれのステートメントの末尾の次のトークンで帰ってくること
		var tmp typefile.ParseVertex
		if (*t).Word == "let" {
			tmp = compileLet(t, file)
		} else if (*t).Word == "if" {
			tmp = compileIf(t, file)
		} else if (*t).Word == "while" {
			tmp = compileWhile(t, file)
		} else if (*t).Word == "do" {
			tmp = compileDo(t, file)
		} else if (*t).Word == "return" {
			tmp = compileReturn(t, file)
		} else if (*t).Word == "}" {
			*file += "</" + "statements" + ">\n"
			break
		}
		childs = append(childs, tmp)
	}
	ret.ChildList = childs
	return ret
}
func compileDo(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "doStatement" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "doStatement"
	var childs []typefile.ParseVertex
	var tmp typefile.ParseVertex
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	*t = (*t).Next
	tmp1 := compileSubCall(t, file)
	childs = append(childs, tmp1)
	*t = (*t).Next
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	*file += "</" + "doStatement" + ">\n"
	*t = (*t).Next
	ret.ChildList = childs
	return ret
}
func compileLet(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "letStatement" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "letStatement"
	var childs []typefile.ParseVertex
	for {
		var tmp typefile.ParseVertex
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		childs = append(childs, tmp)
		if (*t).Word == "[" {
			(*t) = (*t).Next
			tmp1 := compileExpression(t, file)
			childs = append(childs, tmp1)
			continue
		} else if (*t).Word == "=" {
			(*t) = (*t).Next
			tmp2 := compileExpression(t, file)
			childs = append(childs, tmp2)
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
			break
		}
		(*t) = (*t).Next
	}
	*file += "</" + "letStatement" + ">\n"
	(*t) = (*t).Next
	ret.ChildList = childs
	return ret
}
func compileWhile(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "whileStatement" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "whileStatement"
	var childs []typefile.ParseVertex
	var tmp typefile.ParseVertex
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	tmp1 := compileExpression(t, file)
	childs = append(childs, tmp1)
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	tmp2 := compileStatements(t, file)
	childs = append(childs, tmp2)
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	*file += "</" + "whileStatement" + ">\n"
	(*t) = (*t).Next
	ret.ChildList = childs
	return ret
}
func compileReturn(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "returnStatement" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "returnStatement"
	var childs []typefile.ParseVertex
	var tmp typefile.ParseVertex
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	if (*t).Word != ";" {
		tmp1 := compileExpression(t, file)
		childs = append(childs, tmp1)
	}
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	*file += "</" + "returnStatement" + ">\n"
	(*t) = (*t).Next
	ret.ChildList = childs
	return ret
}
func compileIf(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "ifStatement" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "ifStatement"
	var childs []typefile.ParseVertex
	var tmp typefile.ParseVertex
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	tmp1 := compileExpression(t, file)
	childs = append(childs, tmp1)
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	tmp2 := compileStatements(t, file)
	childs = append(childs, tmp2)
	tmp.Word = (*t).Word
	tmp.Tkind = (*t).Tkind
	childs = append(childs, tmp)
	(*t) = (*t).Next
	for {
		var tmps typefile.ParseVertex
		if (*t).Word == "else" {
			tmps.Word = (*t).Word
			tmps.Tkind = (*t).Tkind
			childs = append(childs, tmps)
			(*t) = (*t).Next
			tmps.Word = (*t).Word
			tmps.Tkind = (*t).Tkind
			childs = append(childs, tmps)
			(*t) = (*t).Next
			tmp3 := compileStatements(t, file)
			childs = append(childs, tmp3)
			tmps.Word = (*t).Word
			tmps.Tkind = (*t).Tkind
			childs = append(childs, tmps)
			(*t) = (*t).Next
			continue
		} else {
			break
		}
	}
	*file += "</" + "ifStatement" + ">\n"
	ret.ChildList = childs
	return ret
}
func compileExpression(t **typefile.Token, file *string) typefile.ParseVertex {
	op := []string{"+", "-", "*", "/", "&", "|", "<", ">", "="}
	*file += "<" + "expression" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "expression"
	var childs []typefile.ParseVertex
	tmp1 := compileTerm(t, file) //帰ってきた時に次のトークンがopなら続ける
	childs = append(childs, tmp1)
	(*t) = (*t).Next
	for {
		var tmp typefile.ParseVertex
		if search(op, (*t).Word) {
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
			(*t) = (*t).Next
			tmp2 := compileTerm(t, file)
			childs = append(childs, tmp2)
			(*t) = (*t).Next
		} else {
			break
		}
	}
	*file += "</" + "expression" + ">\n"
	ret.ChildList = childs
	return ret
}
func compileTerm(t **typefile.Token, file *string) typefile.ParseVertex {
	*file += "<" + "term" + ">\n"
	var ret typefile.ParseVertex
	ret.Name = "term"
	var childs []typefile.ParseVertex
	var tmp typefile.ParseVertex
	if (*t).Tkind == "identifier" {
		if ((*t).Next).Word == "(" {
			tmp1 := compileSubCall(t, file)
			childs = append(childs, tmp1)
		} else if ((*t).Next).Word == "." {
			tmp1 := compileSubCall(t, file)
			childs = append(childs, tmp1)
		} else if ((*t).Next).Word == "[" {
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
			(*t) = (*t).Next
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
			(*t) = (*t).Next
			tmp1 := compileExpression(t, file)
			childs = append(childs, tmp1)
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
		} else {
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
		}
	} else if (*t).Word == "(" {
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		childs = append(childs, tmp)
		(*t) = (*t).Next
		tmp1 := compileExpression(t, file)
		childs = append(childs, tmp1)
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		childs = append(childs, tmp)
	} else if (*t).Word == "-" || (*t).Word == "~" {
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		childs = append(childs, tmp)
		(*t) = (*t).Next
		tmp1 := compileTerm(t, file)
		childs = append(childs, tmp1)
	} else {
		tmp.Word = (*t).Word
		tmp.Tkind = (*t).Tkind
		childs = append(childs, tmp)
	}
	*file += "<" + "/term" + ">\n"
	ret.ChildList = childs
	return ret
}
func compileSubCall(t **typefile.Token, file *string) typefile.ParseVertex {
	//expressionListが含まれる, )まで処理してそのノードを呼び出し元に返す
	var ret typefile.ParseVertex
	ret.Name = "subCall"
	var childs []typefile.ParseVertex
	var res typefile.ParseVertex
	res.Name = "expressionList"
	var subchilds []typefile.ParseVertex
	for {
		var tmp typefile.ParseVertex
		if (*t).Word == "(" {
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
			*file += "<" + "expressionList" + ">\n"
			*t = (*t).Next
			if (*t).Word == ")" {
				continue
			}
			tmp1 := compileExpression(t, file)
			subchilds = append(subchilds, tmp1)
			continue
		} else if (*t).Word == ")" {
			*file += "</" + "expressionList" + ">\n"
			res.ChildList = subchilds
			childs = append(childs, res)
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
			break
		} else if (*t).Word == "," {
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			subchilds = append(subchilds, tmp)
			*t = (*t).Next
			tmp1 := compileExpression(t, file)
			subchilds = append(subchilds, tmp1)
			continue
		} else {
			tmp.Word = (*t).Word
			tmp.Tkind = (*t).Tkind
			childs = append(childs, tmp)
		}
		*t = (*t).Next
	}
	ret.ChildList = childs
	return ret
}

//search: charで与えられた文字がarrayの要素かどうか調べる
func search(array []string, char string) bool {
	check := false
	for _, e := range array {
		if e == char {
			check = true
		}
	}
	return check
}
