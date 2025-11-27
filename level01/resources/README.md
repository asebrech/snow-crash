# 🚩 SnowCrash — Level01

## 🎯 Goal

Find the password for **flag01**.

---

## 1. Search for files owned by flag01

```bash
find / -user flag01 2>/dev/null
```

**Result:**

```
(no files found)
```

---

## 2. Check /etc/passwd file

```bash
cat /etc/passwd
```

Look for the flag01 entry:

```
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

**Key observation:** Instead of `x` in the password field, there's an actual hash: `42hDRfypTqqnw`

This is a **DES-encrypted password hash** (old Unix crypt format).

---

## 3. Crack the hash with John the Ripper

🔗 [https://www.openwall.com/john/](https://www.openwall.com/john/)

Create a file with the flag01 entry:

```bash
echo "42hDRfypTqqnw" > flag01.passwd
```

Use John the Ripper to crack it:

```bash
john /tmp/flag01.passwd
```

**Result:**

```
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 256/256 AVX2])
Press 'q' or Ctrl-C to abort, almost any other key for status
abcdefg          (?)
1g 0:00:00:00 100% 2/3 25.00g/s 19200p/s 19200c/s 19200C/s dance..bigman
```

Password cracked: **`abcdefg`**

**To see the password again later:**

```bash
john --show flag01.passwd
```

---

## ✅ Final Flag

```bash
su flag01
```

Enter the password:

```
abcdefg
```

Run:

```bash
getflag
```

---

## 🎉 **Final Token for Level01**

```
f2av5il02puano7naaf6adaaf
```
