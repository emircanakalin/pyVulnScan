import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_forms(url):
    """Verilen URL'deki tüm HTML formlarını toplar."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find_all("form")
    except requests.RequestException as e:
        print(f"Hata: {url} adresine ulaşılamadı. ({e})")
        return []

def get_form_details(form):
    """Bir formun detaylarını (action, method, inputlar) ayıklar."""
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def scan_xss(url):
    """Reflected XSS zafiyeti için tarama yapar."""
    print(f"  [*] XSS zafiyeti için taranıyor: {url}")
    forms = get_forms(url)
    xss_payload = "<script>alert('xss')</script>"
    vulnerabilities = []

    for form in forms:
        form_details = get_form_details(form)
        target_url = urljoin(url, form_details["action"])
        
        data = {}
        for input_tag in form_details["inputs"]:
            if input_tag["type"] == "text" and input_tag["name"]:
                data[input_tag["name"]] = xss_payload

        try:
            if form_details["method"] == "post":
                response = requests.post(target_url, data=data, timeout=5)
            else:
                response = requests.get(target_url, params=data, timeout=5)
            
            if xss_payload in response.text:
                vuln = {
                    "type": "Reflected XSS",
                    "url": target_url,
                    "payload": xss_payload,
                    "form_details": form_details
                }
                vulnerabilities.append(vuln)
                print(f"    [!] Potansiyel XSS zafiyeti bulundu: {target_url}")

        except requests.RequestException:
            pass
            
    return vulnerabilities

def scan_sqli(url):
    """Temel SQL Injection zafiyeti için URL parametrelerini tarar."""
    print(f"  [*] SQL Injection zafiyeti için taranıyor: {url}")
    sqli_payload = "' OR '1'='1"
    sql_error_messages = [
        "you have an error in your sql syntax",
        "warning: mysql_fetch_array()",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated"
    ]
    vulnerabilities = []
    
    parsed_url = urlparse(url)
    if not parsed_url.query:
        return vulnerabilities # Parametre yoksa tarama yapma

    # Her bir parametreyi ayrı ayrı test et
    for param in parsed_url.query.split('&'):
        try:
            key, value = param.split('=')
            test_url = url.replace(f"{key}={value}", f"{key}={value}{sqli_payload}")
            
            try:
                response = requests.get(test_url, timeout=5)
                for error in sql_error_messages:
                    if error in response.text.lower():
                        vuln = {
                            "type": "SQL Injection",
                            "url": test_url,
                            "payload": sqli_payload
                        }
                        if vuln not in vulnerabilities:
                            vulnerabilities.append(vuln)
                            print(f"    [!] Potansiyel SQLi zafiyeti bulundu: {test_url}")
                        break # Bir hata bulundu, diğerlerini aramaya gerek yok
            except requests.RequestException:
                pass
        except ValueError:
            continue # Parametre formatı bozuksa (örn: 'param' ama '=' yok) atla
            
    return vulnerabilities


def scan(url):
    """Belirtilen URL için tüm web zafiyet taramalarını çalıştırır."""
    vulnerabilities = []
    vulnerabilities.extend(scan_xss(url))
    vulnerabilities.extend(scan_sqli(url))
    return vulnerabilities