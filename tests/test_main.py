from src.main import main

def test_main_runs():
    # main fonksiyonunun hatasiz calistigini dogrula
    assert main() is None
