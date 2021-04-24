package xmlEncoder

import (
	"Compiler/typefile"
)

func DFS(tree typefile.ParseVertex, file *string, p typefile.ParseVertex, idx int) {
	if tree.Name != "" && tree.Name != "HEAD" && tree.Name != "subCall" {
		*file += "<" + tree.Name + ">\n"
	}
	if len(tree.ChildList) == 0 {
		if tree.Word != "" {
			markup(tree, file)
		}
	}
	for i, v := range tree.ChildList {
		DFS(v, file, tree, i)
	}
	if tree.Name != "" && tree.Name != "HEAD" && tree.Name != "subCall" {
		*file += "</" + tree.Name + ">\n"
	}
}

func markup(t typefile.ParseVertex, file *string) {
	*file += "<" + t.Tkind + "> "
	*file += outputTerminal(t.Word)
	*file += " </" + t.Tkind + ">\n"
}

//outputTerminal: 終端文字の細かい変化
func outputTerminal(s string) string {
	var t string
	if s[0] == 34 {
		t = s[1 : len(s)-1]
	} else if s == "<" {
		t = "&lt;"
	} else if s == ">" {
		t = "&gt;"
	} else if s == "&" {
		t = "&amp;"
	} else {
		t = s
	}
	return t
}
