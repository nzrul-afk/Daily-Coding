package main

import (
	"fmt"
	"net/http"
	"regexp"
	"strings"
	"time"
	"os"
)

func main() {
	start := time.Now()
	resp, err := http.Get("https://www.whatsapp.com")
	if err != nil {
		fmt.Println("no such host atau connection refused")
		return
	}
	var log string
	defer resp.Body.Close()
	finish := time.Since(start)
	switch resp.StatusCode {
	case 200:
		log ="Server dinyatakan sehat"
	case 301, 302:
		log ="Server redirect"
	case 404:
		log ="Halaman Server ga ada"
	case 500, 502, 503:
		log ="backend server lagi crash atau down"
	default:
		log =fmt.Sprintf("Status lain: %d", resp.StatusCode)
	}

	reg := regexp.MustCompile(`\.([^.]+)\.`)
	re := reg.FindStringSubmatch(resp.Request.URL.Host)
	regfinal := strings.ToUpper(re[1])
	fmt.Printf(`[%d] (%s) %s - respon dalam %s`, resp.StatusCode, regfinal, log, finish)
	fil, err := os.OpenFile("Network.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
	fmt.Println("[ERROR] Gagal membuka file:", err)
	return
}
	defer fil.Close()
	_, err = fil.WriteString(fmt.Sprintf("[%d] (%s) %s - respon dalam %s\n", resp.StatusCode, regfinal, log, finish))
}