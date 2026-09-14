import requests
from typing import Optional, Dict, Any

class NedapClient:
    def __init__(self, host: str, port: int = 8443, use_ssl: bool = True, verify_ssl: bool = False):
        protocol = "https" if use_ssl else "http"
        self.base_url = f"{protocol}://{host}:{port}"
        self.session = requests.Session()
        self.session.verify = verify_ssl

    def test_connectivity(self, timeout: int = 5) -> bool:
        """Sunucu erisilebilirligini test eder."""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=timeout)
            return response.status_code < 500
        except requests.exceptions.RequestException:
            return False

    def send_rest_command(self, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """AEOS REST uclarina istek gonderir."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(url, json=payload or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            return {"error": str(err)}

def main():
    client = NedapClient(host="127.0.0.1")
    print("Nedap AEOS modulu hazir. Hedef sunucu:", client.base_url)

if __name__ == "__main__":
    main()
