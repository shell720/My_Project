package jackTokenizer

import (
	"Compiler/typefile"
	"io/ioutil"
	"os"
	"strconv"
)

//予約語
var symbol = []string{"{", "}", "(", ")", "[", "]", ".", ",",
	";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
var keyword = []string{"class", "constructor", "function", "method",
	"field", "static", "var", "int", "char", "boolean", "void", "true",
	"false", "null", "this", "let", "do", "if", "else", "while", "return"}

//Tokenizer ファイルを開いて字句解析
func Tokenizer(fpath string) *typefile.Token {
	//ファイルを開く
	f, err := os.Open(fpath)
	errOutput(err)
	defer f.Close()

	b, err := ioutil.ReadAll(f) // bをfor rangeでstring変換すると1文字ずつ取得できる
	errOutput(err)

	//文字列を字句解析
	head := strToToken(b) //headに開始トークン
	var tokenxml string
	tokenKind(head, &tokenxml)

	//fmt.Println(tokenxml)
	return head
}

//strToToken 文字列を分割して終端文字に
//コメント削除、空白スペースを手がかりに分ける、symbolが現れても分ける
func strToToken(b []byte) *typefile.Token {
	l := len(b)
	var head typefile.Token // 開始を表すノードにしたいが返り値の調整のため次のcurが開始ノード
	cur := new(typefile.Token)
	head.Next = cur
	for i := 0; i < l; {
		switch {
		case string(b[i:i+2]) == "//": //コメントアウト処理1
			for {
				i++
				if string(b[i]) == "\n" {
					break
				}
			}
			i++
			continue

		case string(b[i:i+2]) == "/*": //コメントアウト処理2
			for {
				i++
				if string(b[i:i+2]) == "*/" {
					break
				}
			}
			i += 2
			continue

		case string(b[i]) == " " || string(b[i]) == "\n": //改行または空白
			i++
			continue

		case b[i] == 13:
			i++
			continue

		case b[i] == 9: //タブコード
			i++
			continue

		case search(symbol, string(b[i])):
			//fmt.Println(string(b[i]))
			s := string(b[i])
			cur = tokenConnect(cur, s)
			i++
			//fmt.Println(cur.Word)

		case b[i] == 34: //ダブルクォートで始まる文字列を処理
			startIdx := i
			for {
				i++
				if b[i] == 34 {
					i++
					break
				}
			}
			//fmt.Println(string(b[startIdx:i]))
			s := string(b[startIdx:i])
			cur = tokenConnect(cur, s)
			//fmt.Println(cur.Word)

		default:
			startIdx := i
			for {
				i++
				if string(b[i]) == " " || string(b[i]) == "\n" {
					break
				} else if search(symbol, string(b[i])) { //symbolで区切る
					break
				}
			}
			//fmt.Println(string(b[startIdx:i]))
			s := string(b[startIdx:i])
			cur = tokenConnect(cur, s)
			//fmt.Println(cur.Word)
		}
	}
	return head.Next.Next
}

//tokenKind: トークンの種類を決定する　(&トークン結果を書き込む)
func tokenKind(t *typefile.Token, file *string) {
	*file += "<tokens>\n"
	for { //終了はt.next　== nil
		var kind string
		_, err := strconv.Atoi(t.Word)
		doubleQuote := "\""
		byteDQ := []byte(doubleQuote)
		switch {
		case search(keyword, t.Word):
			kind = "keyword"
		case search(symbol, t.Word):
			kind = "symbol"
		case t.Word[0] == byteDQ[0]:
			kind = "stringConstant"
		case err == nil:
			kind = "integerConstant"
		default:
			kind = "identifier"
		}
		t.Tkind = kind

		markup(t, file)

		if t.Next == nil {
			break
		} else {
			t = t.Next
		}
	}
	*file += "</tokens>\n"
}

//tokenConnect　トークンを繋ぐ
func tokenConnect(cur *typefile.Token, s string) *typefile.Token {
	Next := &typefile.Token{Word: s}
	cur.Next = Next
	return Next
}

func markup(t *typefile.Token, file *string) {
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

//errOutput エラー検出＆出力
func errOutput(e error) {
	if e != nil {
		panic(e)
	}
}
