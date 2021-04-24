package main

import (
	"fmt"
	"sync"

	"bufio"
	"crypto/sha256"
	"encoding/hex"
	"log"
	"os"
	"time"
)

func main() {
	//引数のpathの取得
	var filename string
	filename = os.Args[1]

	//ファイルとのストリームを繋ぐ
	fp, err := os.Open(filename)
	if err != nil {
		fmt.Println("Error: Cannot open the file")
	}
	defer fp.Close()

	src := bufio.NewScanner(fp)

	//並列処理の為の準備
	//c := make(chan string)
	linecount := 0
	wg := &sync.WaitGroup{}
	mutex := &sync.Mutex{}
	m := map[int]string{}

	for src.Scan() {
		wg.Add(1)
		go func(s string, i int) {
			mutex.Lock()
			m[i] = shaHex(s)
			mutex.Unlock()
			//log.Println(s, shaHex(s))
			time.Sleep(1 * time.Second)
			wg.Done()
		}(src.Text(), linecount)
		linecount++
	}

	wg.Wait()

	for i := 0; i < 5; i++ {
		s, _ := m[i]
		log.Println(s)
	}
	time.Sleep(5 * time.Second)
	log.Println("End")
}

func shaHex(input string) string {
	//sha256を計算しそれを16進数に直す
	//sting -> [hoge]byte -> []byte->string
	checksum := sha256.Sum256([]byte(input))
	dump16 := hex.Dump(checksum[:])
	return dump16
}
