package main

import (
	"fmt"
	"flag"
	"os"
)

func main() {
	hostprt := flag.String("host", "192.168.1.1", "IP target")
	portprt := flag.Int("port", 80, "Port target")

	flag.Parse()

	env := os.Getenv("APP_ENV")
	if env == "" {
		env = "development"
	}
	status := "PORT_STANDAR"
	if *portprt != 80 && *portprt != 443 {
		status = "PORT_NON_STANDAR"
	}

	logData := fmt.Sprintf("[ENV: %s] Target: %s:%d -> Status %s\n", env, *hostprt, *portprt, status)
	err := os.WriteFile("incident.log", []byte(logData), 0644)
	if err != nil {
		fmt.Println("[ERROR]: Gagal menulis file log:", err)
	}
	
	fmt.Println("=== PROBER SELESAI ===")
	fmt.Printf("Berhasil mencatat audit ke incident.log untuk %s:%d!\n", *hostprt, *portprt)
}