# # 🚩 SnowCrash — Level00

## ## 🎯 Goal

Find the password for **flag00**.

---

# ## 1. Find the flag file

```bash
find / -user flag00 2>/dev/null
```

**Result:**

```
/usr/sbin/john
```

---

# ## 2. Read the file

```bash
cat /usr/sbin/john
```

You get:

```
cdiiddwpgswtgt
```

---

# ## 3. Identify the cipher

Go to:

🔗 [https://www.dcode.fr/cipher-identifier](https://www.dcode.fr/cipher-identifier)
Paste:

```
cdiiddwpgswtgt
```

dCode suggests **Affine** → go to the Affine solver.

---

# ## 4. Decrypt the text

Go to:

🔗 [https://www.dcode.fr/affine-cipher](https://www.dcode.fr/affine-cipher)
Paste the string
Click **Decrypt**

You get:

```
nottoohardhere
```

---

# ## ✅ Final Flag

```bash
su flag00
```

Enter the password:

```
nottoohardhere
```

Run:

```bash
getflag
```

---

# 🎉 **Final Token for Level00**

```
x24ti5gi3x0ol2eh4esiuxias
```
