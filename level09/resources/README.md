# 🚩 SnowCrash — Level09

## 🎯 Goal

Find the password for **flag09**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-sr-x 1 flag09  level09 7640 Mar  5  2016 level09
----r--r-- 1 flag09  level09   26 Mar  5  2016 token
```

A setuid binary `level09` and a readable `token` file.

---

## 2. Analyze the token file

Read the token:

```bash
cat token
```

**Output:**

```
f4kmm6p|=�p�n��DB�Du{��
```

The token appears to be encoded/encrypted.

---

## 3. Analyze the binary

Run the binary:

```bash
./level09
```

**Output:**

```
You need to provied only one arg.
```

Test with simple inputs to understand the cipher:

```bash
./level09 "AAAA"
```

**Output:**

```
ABCD
```

```bash
./level09 "abcdefgh"
```

**Output:**

```
acegikmo
```

**Analysis:**
- `AAAA` → `ABCD`: A+0=A, A+1=B, A+2=C, A+3=D
- `abcdefgh` → `acegikmo`: a+0=a, b+1=c, c+2=e, d+3=g, etc.

**The cipher:** Each character is shifted by its **index position** (0-indexed).
- Encoding: `encoded[i] = original[i] + i`
- Decoding: `original[i] = encoded[i] - i`

---

## 4. Decode the token

Get the token in hex format:

```bash
cat token | xxd
```

**Output:**

```
0000000: 6634 6b6d 6d36 707c 3d82 7f70 826e 8382  f4kmm6p|=..p.n..
0000010: 4442 8344 757b 7f8c 890a                 DB.Du{....
```

Create a Python decoder script (`decode.py`):

```python
#!/usr/bin/env python3
# Decoder for level09: each byte is shifted by its position
# To decode: subtract the position from each byte

token_hex = "66346b6d6d36707c3d827f70826e838244428344757b7f8c89"

decoded = ""
for i, byte in enumerate(bytes.fromhex(token_hex)):
    decoded += chr((byte - i) % 256)

print(f"Password: {decoded}")
```

Run the decoder:

```bash
python3 decode.py
```

**Output:**

```
Password: f3iji1ju5yuevaus41q1afiuq
```

---

## 5. Get the flag

Switch to flag09 user:

```bash
su flag09
```

Password: `f3iji1ju5yuevaus41q1afiuq`

Run getflag:

```bash
getflag
```

---

## ✅ Result

Output:

```
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
```

---

## 🎉 **Final Token for Level09**

```
s5cAJpM8ev6XHw998pRWG728z
```
