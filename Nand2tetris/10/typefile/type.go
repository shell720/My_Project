package typefile

//structを複数ファイルに跨って使用したいので、専用のファイルを作成

//Token そのトークンのワードと次へのポインタ、そのトークンの種類を所持する
type Token struct {
	Word  string
	Next  *Token
	Tkind string
}

type ParseVertex struct {
	Word      string
	Tkind     string
	Name      string //そのノードの名前
	ChildNum  int    //終端文字なら0
	ChildList []ParseVertex
}

type TableValue struct {
	Type string
	Attr string
	No   int
}
