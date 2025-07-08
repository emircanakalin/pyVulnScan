import socket
import re
import sys

def parse_ports(port_range_str):
    """
    Port aralığı string'ini (örn: "22,80,443", "1-1024") ayrıştırır ve bir set döner.
    """
    ports = set()
    if not port_range_str:
        return ports

    # Virgülle ayrılmış portları ve aralıkları böl
    parts = port_range_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Port aralığı (örn: 1-1024)
            try:
                start, end = map(int, part.split('-'))
                if 0 < start <= end <= 65535:
                    ports.update(range(start, end + 1))
            except ValueError:
                print(f"Uyarı: Geçersiz port aralığı '{part}' atlanıyor.")
        else:
            # Tek port
            try:
                port_num = int(part)
                if 0 < port_num <= 65535:
                    ports.add(port_num)
            except ValueError:
                print(f"Uyarı: Geçersiz port numarası '{part}' atlanıyor.")
    return sorted(list(ports))

def grab_banner(sock):
    """
    Açık bir soketten banner (servis bilgisi) yakalamaya çalışır.
    """
    try:
        sock.settimeout(2)
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        return banner
    except socket.timeout:
        return "Servis bilgisi alınamadı (Timeout)."
    except Exception:
        return "Servis bilgisi alınamadı."

def scan(host, port_str):
    """
    Belirtilen host ve portlarda tarama yapar.
    """
    open_ports_info = []
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Hata: Hostname çözümlenemedi: {host}", file=sys.stderr)
        return []
    ports_to_scan = parse_ports(port_str)

    print(f"[*] {host} ({target_ip}) için portlar taranıyor...")

    for port in ports_to_scan:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    print(f"  [+] Port {port}/tcp açık.")
                    banner = grab_banner(sock)
                    print(f"    - Servis: {banner}")
                    open_ports_info.append({
                        'port': port,
                        'status': 'Açık',
                        'banner': banner
                    })
        except socket.error as e:
            # Bu portta bir sorun oldu, diğerlerine devam et
            pass

    if not open_ports_info:
        print("[-] Açık port bulunamadı.")

    return open_ports_info