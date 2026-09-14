from src.main import NedapClient

def test_client_init():
    client = NedapClient(host="192.168.1.100", port=8443, use_ssl=True)
    assert client.base_url == "https://192.168.1.100:8443"
    assert client.session.verify is False

def test_test_connectivity_failure_handling():
    # Ulasilamaz bir yerel porta istek atip hata firlatmadan False dondugunu test et
    client = NedapClient(host="127.0.0.1", port=65530, use_ssl=False)
    result = client.test_connectivity(timeout=1)
    assert result is False
