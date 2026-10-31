import argparse
import json
from day_08_task1_logger import SecurityLogger
from day_08_task2_prober import SystemProber

parser = argparse.ArgumentParser(description="Recon Tools")
parser.add_argument("-a", "--target", required=True, help="Ip atau domain target" )
parser.add_argument("-m", "--mode", choices=["ping", "dns", "full"], default="ping", help="Mode probing")
parser.add_argument("-v", "--verbose", action="store_true", help="Aktifkan debug logging")
parser.add_argument("-o", "--output", help="Nama file JSON untuk menyimpan hasil")

args = parser.parse_args()
log = SecurityLogger(verbose=args.verbose)
log.handler()
prober = SystemProber()
log.info(f"Memulai recon pada target: {args.target}")
if args.mode == "ping" or args.mode == "full":
    log.info(f"Menjalankan ICMP Ping probe ke {args.target}...")
    res_ping = prober.ping(args.target)
    if res_ping["alive"]:
        log.info(f"Ping sukses: Host UP")
    else:
        log.warning(f"Ping gagal: Host DOWN")
if args.mode == "dns" or args.mode == "full":
    log.info(f"Menjalankan lookup DNS probe ke {args.target}...")
    res_dns = prober.check_dns(args.target)
    if res_dns["resolved"]:
        log.info("DNS lookup sukses")
    else:
        log.warning("DNS lookup gagal")

if args.output:
    report = {
        "target": args.target,
        "mode": args.mode
    }
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    log.info(f"Hasil disimpan ke {args.output}")
    