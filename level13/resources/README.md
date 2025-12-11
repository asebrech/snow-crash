# 🚩 SnowCrash — Level13

## 🎯 Goal

Find the password for **flag13**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-sr-x+ 1 flag13  level13 7677 Mar  5  2016 level13
```

A setuid binary that belongs to flag13.

---

## 2. Analyze the binary

Run the binary:

```bash
./level13
```

**Output:**

```
UID 2013 started us but we we expect 4242
```

The binary checks our UID and expects it to be **4242**.

Examine with strings:

```bash
strings level13
```

**Key findings:**

```
UID %d started us but we we expect %d
boe]!ai0FB@.:|L6l@A?>qJ}I
your token is %s
```

**Analysis:**
- The binary calls `getuid()` to check the current user's UID
- Our UID is **2013** (user level13)
- The binary expects UID **4242**
- There's an encrypted token: `boe]!ai0FB@.:|L6l@A?>qJ}I`
- If the UID check passes, it decrypts and prints the token
- **Vulnerability:** We can use GDB to intercept `getuid()` and force it to return 4242

---

## 3. Exploit with GDB

**The exploit strategy:**
1. Use GDB to debug the binary
2. Set a breakpoint on the `getuid()` function
3. When the breakpoint is hit, force the function to return **4242**
4. Let the program continue with the fake UID

**Steps:**

Start GDB:

```bash
gdb ./level13
```

Set a breakpoint on `getuid`:

```gdb
(gdb) break getuid
Breakpoint 1 at 0xb7ee4cc0
```

Run the program:

```gdb
(gdb) run
Starting program: /home/user/level13/level13

Breakpoint 1, 0xb7ee4cc0 in getuid () from /lib/i386-linux-gnu/libc.so.6
```

Force the function to return 4242:

```gdb
(gdb) return (int)4242
Make selected stack frame return now? (y or n) y
#0  0x0804859a in main ()
```

Continue execution:

```gdb
(gdb) continue
Continuing.
your token is 2A31L79asukciNyi8uppkEuSx
[Inferior 1 (process 1925) exited with code 050]
```

**Success!** The binary prints the decrypted token: `2A31L79asukciNyi8uppkEuSx`

---

## 4. How it works

The `getuid()` system call returns the real user ID of the calling process. By using GDB's `return` command:
1. We intercept the function before it completes
2. Force it to return our chosen value (4242) instead of the actual UID (2013)
3. The binary's UID check passes
4. The decryption routine runs and reveals the token

**Alternative method** - Set the EAX register directly:

```gdb
(gdb) break getuid
(gdb) run
(gdb) finish
(gdb) set $eax=4242
(gdb) continue
```

---

## 5. Get the flag

Use the token as the password for flag13:

```bash
su flag13
Password: 2A31L79asukciNyi8uppkEuSx
```

Then run `getflag`:

```bash
getflag
```

---

## 🏁 Flag

`2A31L79asukciNyi8uppkEuSx`
