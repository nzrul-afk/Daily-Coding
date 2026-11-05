package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
	"encoding/json"
)
type Target struct{
	Name string `json:"name"`
	URL string `json:"url"`
}
func worker(id int, jobs <-chan Target, results chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()
	client := http.Client{
		Timeout: 5 * time.Second,
	}
	
	for t := range jobs{
		start := time.Now()
		resp, err := client.Get(t.URL)
		if err != nil {
			results <- fmt.Sprintf("[DOWN] Worker #%d: %s (%s) - Gagal\n", id, t.Name, t.URL)
			continue
		}
		resp.Body.Close()
		durasi := time.Since(start)
		results <- fmt.Sprintf("[%d] Worker #%d: %s (%v)\n", resp.StatusCode, id, t.Name, durasi)
	}
}
func main(){
	fileLog, err := os.OpenFile("file.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("[ERROR] file gagal dibuka")
		return
	}
	defer fileLog.Close()
	baca, err := os.ReadFile("targets.json")
	if err != nil {
		fmt.Println("[ERROR] file gagal dibuka")
	}
	var daftarTarget []Target
	json.Unmarshal(baca, &daftarTarget)
	totalWorker := 10
	jobs := make(chan Target, len(daftarTarget))
	results := make(chan string, len(daftarTarget))
	var wg sync.WaitGroup

	for w := 0 ; w < totalWorker; w++ {
		wg.Add(1)
		go worker(w, jobs,results, &wg)
	}
	for _,target := range daftarTarget {
		jobs <- target
	}
	go func() {
        wg.Wait()
        close(results)
    }()

	close(jobs)

	for res := range results {
		fileLog.WriteString(res)
	}
}