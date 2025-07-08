# PyVulnScan - Comprehensive Security Scanner

---

## Türkçe

### Açıklama

PyVulnScan, web uygulamaları ve ağ sistemleri için geliştirilmiş, açık kaynaklı bir güvenlik tarayıcısıdır. Amacı, yaygın güvenlik zafiyetlerini tespit etmek ve sonuçları anlaşılır, çift dilli (Türkçe/İngilizce) bir rapor formatında sunmaktır.

### Özellikler

- **Web Uygulama Taraması:** Reflected XSS ve temel SQLi tespiti.
- **Ağ Taraması:** Açık port tespiti ve servis versiyon bilgisi (Banner Grabbing).
- **Raporlama:** Tarama sonuçlarını detaylı bir HTML raporu olarak oluşturma.

### Kurulum

1.  **Projeyi klonlayın:** `git clone https://github.com/kullanici/PyVulnScan.git && cd PyVulnScan`
2.  **Gerekli kütüphaneleri yükleyin:** `pip install -r requirements.txt`

### Kullanım

```bash
python main.py --url http://example.com --scan-type all --report-file report.html --lang tr
```

- `--url`: Taranacak hedef URL. (Zorunlu)
- `--scan-type`: Tarama türü (`web`, `port`, `all`). Varsayılan: `all`.
- `--report-file`: Rapor dosyasının adı. Varsayılan: `scan_report.html`.
- `--ports`: Taranacak portlar (`22,80,443` veya `1-1024`). Varsayılan: `80,443`.
- `--lang`: Rapor dili (`tr` veya `en`). Varsayılan: `en`.

---

## English

### Description

PyVulnScan is an open-source security scanner for web applications and network systems. It aims to detect common security vulnerabilities and present the results in a clear, bilingual (Turkish/English) report format.

### Features

- **Web Application Scanning:** Detects Reflected XSS and basic SQLi.
- **Network Scanning:** Detects open ports and service versions (Banner Grabbing).
- **Reporting:** Generates a detailed HTML report of the scan results.

### Installation

1.  **Clone the project:** `git clone https://github.com/kullanici/PyVulnScan.git && cd PyVulnScan`
2.  **Install dependencies:** `pip install -r requirements.txt`

### Usage

```bash
python main.py --url http://example.com --scan-type all --report-file report.html --lang en
```

- `--url`: The target URL to scan. (Required)
- `--scan-type`: Type of scan (`web`, `port`, `all`). Default: `all`.
- `--report-file`: Name of the report file. Default: `scan_report.html`.
- `--ports`: Ports to scan (`22,80,443` or `1-1024`). Default: `80,443`.
- `--lang`: Language of the report (`tr` or `en`). Default: `en`.

---

## License

This project is licensed under the GPL  License.