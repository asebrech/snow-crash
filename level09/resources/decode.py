#!/usr/bin/env python3
# Decoder for level09: each byte is shifted by its position
# To decode: subtract the position from each byte

token_hex = "66346b6d6d36707c3d827f70826e838244428344757b7f8c89"

decoded = ""
for i, byte in enumerate(bytes.fromhex(token_hex)):
    decoded += chr((byte - i) % 256)

print(f"Password: {decoded}")
