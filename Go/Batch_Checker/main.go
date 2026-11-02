package main
import (
	"fmt"
	"encoding/json"
	"net/http"
	"os"
	"time"
)
type Target struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}
func main() {

	fileLog, err := os.OpenFile("batch_report.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("GAGAL MEMBUKA FILE", err)
		return 
	}
	baca, err := os.ReadFile("targets.json")
	if err != nil {
		fmt.Println("FILE GA BENER")
	}

	var daftarTarget []Target
	json.Unmarshal(baca, &daftarTarget)
	
	for _, target := range daftarTarget {
		start := time.Now()
		checking, err := http.Get(target.URL)
		if err != nil {

        continue
    	}
		var log string
		switch checking.StatusCode {
			case 200:
				log ="AMAN"
			case 301, 302:
				log ="REDIRECT"
			case 404:
				log ="PAGE NOT FOUND"
			case 500, 502, 503:
				log ="CRASH"
		}
		checking.Body.Close()

		durasi := time.Since(start)
		woi := fmt.Sprintf("Server: %s dinyatakan %s respon selama %v\n", target.Name, log, durasi)
		fileLog.WriteString(woi)
		
	}
	defer fileLog.Close()
	fmt.Println("\n=== SELESAI: Laporan tersimpan di batch_report.log ===")
	
	}




