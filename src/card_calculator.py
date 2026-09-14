from typing import Dict, Any

class CardCalculator:
    @staticmethod
    def clean_hex(hex_str: str) -> str:
        cleaned = hex_str.strip().replace(" ", "").replace(":", "").replace("-", "")
        if cleaned.lower().startswith("0x"):
            cleaned = cleaned[2:]
        return cleaned.upper()

    @classmethod
    def from_hex(cls, hex_input: str) -> Dict[str, Any]:
        raw_hex = cls.clean_hex(hex_input)
        if len(raw_hex) % 2 != 0:
            raw_hex = "0" + raw_hex

        byte_data = bytes.fromhex(raw_hex)
        hex_be = raw_hex
        hex_le = byte_data[::-1].hex().upper()

        dec_be = int(hex_be, 16)
        dec_le = int(hex_le, 16)

        res = {
            "hex_be": hex_be,
            "hex_le": hex_le,
            "dec_be": dec_be,
            "dec_le": dec_le,
            "byte_len": len(byte_data),
            "wiegand26": None
        }

        if len(byte_data) in (3, 4):
            val_24 = dec_be & 0xFFFFFF
            fc = (val_24 >> 16) & 0xFF
            cn = val_24 & 0xFFFF
            res["wiegand26"] = f"FC: {fc} | CN: {cn}"

        return res

    @classmethod
    def from_dec(cls, dec_val: int) -> Dict[str, Any]:
        hex_val = f"{dec_val:X}"
        return cls.from_hex(hex_val)

    @classmethod
    def from_wiegand(cls, fc: int, cn: int) -> Dict[str, Any]:
        raw_24 = ((fc & 0xFF) << 16) | (cn & 0xFFFF)
        return cls.from_hex(f"{raw_24:06X}")
