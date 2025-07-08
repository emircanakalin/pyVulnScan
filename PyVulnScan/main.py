import argparse
import sys
from urllib.parse import urlparse

from scanner import web_scanner, port_scanner
from reporter import report_generator

def main():
    parser = argparse.ArgumentParser(description="PyVulnScan - Kapsamlı Güvenlik Tarayıcısı")
    parser.add_argument('--url', required=True, help='Taranacak hedef web uygulamasının tam URL\'si.')
    parser.add_argument('--scan-type', default='all', choices=['web', 'port', 'all'], help='Yapılacak tarama türü.')
    parser.add_argument('--report-file', default='scan_report.html', help='Oluşturulacak HTML rapor dosyasının adı.')
    parser.add_argument('--ports', default='80,443', help='Taranacak port aralığı. Örnek: "22,80,443" veya "1-1024".')
    parser.add_argument('--lang', default='en', choices=['tr', 'en'], help='Raporlama dili (tr/en).')

    args = parser.parse_args()

    # URL'den domain adını al
    try:
        target_host = urlparse(args.url).hostname
        if not target_host:
            raise ValueError("Geçersiz URL formatı.")
    except ValueError as e:
        print(f"Hata: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Hedef: {args.url}")
    print(f"[*] Sunucu: {target_host}")
    print(f"[*] Tarama Tipi: {args.scan_type}")
    print("-" * 50)

    # Tarama sonuçlarını saklamak için bir sözlük
    scan_results = {
        'target_url': args.url,
        'target_host': target_host,
        'web_vulns': [],
        'open_ports': []
    }

    if args.scan_type in ['web', 'all']:
        print("[+] Web uygulaması zafiyet taraması başlatılıyor...")
        scan_results['web_vulns'] = web_scanner.scan(args.url)
        print("[+] Web taraması tamamlandı.")

    if args.scan_type in ['port', 'all']:
        print("\n[+] Port taraması başlatılıyor...")
        scan_results['open_ports'] = port_scanner.scan(target_host, args.ports)
        print("[+] Port taraması tamamlandı.")

    # Rapor oluşturma
    print("\n[*] Rapor oluşturuluyor...")
    report_generator.create_html_report(scan_results, args.report_file, args.lang)
    print(f"[+] Rapor başarıyla '{args.report_file}' dosyasına kaydedildi.")

    print("\n[*] Tarama tamamlandı.")

if __name__ == "__main__":
    main()