package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)
type Target struct{
	Name string `json:"name"`
	URL string `json:"url"`
}
func main(){
	fileLog, err := os.OpenFile("logfile.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("file gagal dibikin")
	}
	baca, err := os.ReadFile("targets.json")
	if err != nil {
		fmt.Println("error: file tidak bisa dibaca")
		return
	}
	var daftarTarget []Target
	json.Unmarshal(baca, &daftarTarget)
	var wg sync.WaitGroup
	hasilChan := make(chan string, len(daftarTarget))
	for _,target :=range daftarTarget{
		wg.Add(1)
		go func(t Target) {
			defer wg.Done()
			start := time.Now()
			tembak, err := http.Get(target.URL)
			if err != nil {
				fmt.Println("Gagal ngescan")
				return
			}
			tembak.Body.Close()
			timeStam:= time.Since(start)
			pesan := fmt.Sprintf("[%d] %s (%s) SELESAI %v\n", tembak.StatusCode, target.Name, target.URL, timeStam)
			hasilChan <- pesan
		}(target)
	}
	wg.Wait()
	close(hasilChan)
	for pesan := range hasilChan {
		fmt.Print(pesan) 
		fileLog.WriteString(pesan) 
	}
	fileLog.Close()
}