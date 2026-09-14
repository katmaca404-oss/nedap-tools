import sys
from src.card_calculator import CardCalculator, print_card_report

def main():
    if len(sys.argv) < 2:
        print("\nKullanim:")
        print("  python -m src.main --hex <HEX_DEGER>          (Ornek: python -m src.main --hex 1A2B3C4D)")
        print("  python -m src.main --dec <DECIMAL_DEGER>      (Ornek: python -m src.main --dec 439041101)")
        print("  python -m src.main --wiegand <FC> <CARD_NO>   (Ornek: python -m src.main --wiegand 101 2540)")
        
        # Test / Ornek Calisma
        print("\nOrnek Demo Kart Calistiriliyor (Hex: 3C4A5B12)...")
        report = CardCalculator.from_hex("3C4A5B12")
        print_card_report(report)
        return

    mode = sys.argv[1].lower()
    
    if mode == "--hex" and len(sys.argv) >= 3:
        report = CardCalculator.from_hex(sys.argv[2])
        print_card_report(report)
    elif mode == "--dec" and len(sys.argv) >= 3:
        report = CardCalculator.from_decimal(int(sys.argv[2]))
        print_card_report(report)
    elif mode == "--wiegand" and len(sys.argv) >= 4:
        fc = int(sys.argv[2])
        cn = int(sys.argv[3])
        report = CardCalculator.from_wiegand26(fc, cn)
        print_card_report(report)
    else:
        print("Hatali parametre girildi. Lutfen argumanlari kontrol edin.")

if __name__ == "__main__":
    main()
