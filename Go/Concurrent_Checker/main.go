package main
import (
	"fmt"
	"net/http"
	"sync"
	"encoding/json"
	"os"
	"time"
)
type Target struct{
	Nama string `json:"name"`
	URL string `json:"url"`
}
func main() {
	fileLog, err := os.OpenFile("logfile.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
	fmt.Println("GAGAL MEMBUKA FILE", err)
	return 
	}
	baca, err := os.ReadFile("targets.json")
	if err != nil {
		fmt.Println("gagal membaca file")
		return
	}
	var wg sync.WaitGroup
	var daftarTarget []Target
	json.Unmarshal(baca, &daftarTarget)

	for _,target := range daftarTarget {
		wg.Add(1)
		go func(t Target) {
			defer wg.Done()
			start := time.Now()

			resp, err := http.Get(t.URL)
			if err != nil {
				fmt.Println("URL tidak ditemukan")
				return
			}
			defer resp.Body.Close()
			durasi := time.Since(start)
			pesan := fmt.Sprintf("[%d] %s (%s) SELESAI %v\n", resp.StatusCode, t.Nama, t.URL, durasi)
			fileLog.WriteString(pesan)

		}(target)
	}
	wg.Wait()
	fmt.Println("Semua server selesai dicek secara paralel!")
	fileLog.Close()

	}
	