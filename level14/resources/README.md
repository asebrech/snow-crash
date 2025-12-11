# 🚩 SnowCrash — Level14

## 🎯 Goal

Find the password for **flag14** (final level).

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
dr-x------ 1 level14 level14  100 Mar  5  2016 .
d--x--x--x 1 root    users    340 Aug 30  2015 ..
-r-x------ 1 level14 level14  220 Apr  3  2012 .bash_logout
-r-x------ 1 level14 level14 3518 Aug 30  2015 .bashrc
-r-x------ 1 level14 level14  675 Apr  3  2012 .profile
```

No binary or files in the home directory!

---

## 2. Analyze the getflag binary

Since there's nothing in level14's directory, the challenge must involve the `getflag` binary itself.

Examine the binary:

```bash
ls -la /bin/getflag
strings /bin/getflag
```

**Key findings:**

```
You should not reverse this
ptrace
getuid
Check flag.Here is your token : 
I`fA>_88eEd:=`85h0D8HE>,D
7`4Ci4=^d=J,?>i;6,7d416,7
<>B16\AD<C6,G_<1>^7ci>l4B
B8b:6,3fj7:,;bh>D@>8i:6@D
?4d@:,C>8C60G>8:h:Gb4?l,A
G8H.6,=4k5J0<cd/D@>>B:>:4
H8B8h_20B4J43><8>\ED<;j@3
78H:J4<4<9i_I4k0J^5>B1j`9
bci`mC{)jxkn<"uD~6%g7FK`7
Dc6m~;}f8Cj#xFkel;#&ycfbK
74H9D^3ed7k05445J0E4e;Da4
70hCi,E44Df[A4B/J@3f<=:`D
8_Dw"4#?+3i]q&;p6 gtw88EC
boe]!ai0FB@.:|L6l@A?>qJ}I
g <t61:|4_|!@IF.-62FH&G~DCK/Ekrvvdwz?v|
Nope there is no token here for you sorry. Try again :)
```

**Analysis:**
- The `getflag` binary contains **encrypted tokens** for all flag users
- It uses `getuid()` to determine which token to decrypt
- It has **anti-debugging protection** using `ptrace()`
- The message "You should not reverse this" appears when a debugger is detected

Check flag14's UID:

```bash
id flag14
```

**Output:**

```
uid=3014(flag14) gid=3014(flag14) groups=3014(flag14),1001(flag)
```

Level14's UID is **3014** (following the pattern: flag00=3000, flag01=3001, ..., flag14=3014)

---

## 3. Exploit with GDB - Bypass ptrace and fake UID

**The exploit strategy:**
1. Use GDB to debug `/bin/getflag`
2. Bypass the anti-debugging check by intercepting the `ptrace()` syscall
3. Make `ptrace()` return 0 (no debugger detected)
4. Intercept `getuid()` and make it return **3014** (flag14's UID)
5. The binary decrypts and prints the flag14 token

**Steps:**

Start GDB:

```bash
gdb /bin/getflag
```

Set up catchpoint for ptrace and breakpoint for getuid:

```gdb
(gdb) catch syscall ptrace
Catchpoint 1 (syscall 'ptrace' [26])
(gdb) break getuid
Breakpoint 2 at 0x80484b0
```

Run the program:

```gdb
(gdb) run
Starting program: /bin/getflag 

Catchpoint 1 (call to syscall ptrace), 0xb7fdd428 in __kernel_vsyscall ()
```

Bypass the anti-debugging check:

```gdb
(gdb) set $eax=0
(gdb) continue
Continuing.

Catchpoint 1 (returned from syscall ptrace), 0xb7fdd428 in __kernel_vsyscall ()
```

Force ptrace to return our value:

```gdb
(gdb) return (int)3014
Make selected stack frame return now? (y or n) y
#0  0xb7f14713 in ptrace () from /lib/i386-linux-gnu/libc.so.6
(gdb) continue
Continuing.

Breakpoint 2, 0xb7ee4cc0 in getuid () from /lib/i386-linux-gnu/libc.so.6
```

Now at the getuid breakpoint, fake the UID:

```gdb
(gdb) return (int)3014
Make selected stack frame return now? (y or n) y
#0  0x08048b02 in main ()
(gdb) continue
Continuing.
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
[Inferior 1 (process 2616) exited normally]
```

**Success!** The final token is: `7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ`

---

## 4. How it works

The `getflag` binary:
1. Uses `ptrace(PTRACE_TRACEME, 0, 1, 0)` to detect debuggers
   - If a debugger is attached, ptrace fails and the program exits
   - We bypass this by catching the syscall and forcing EAX=0 (success)

2. Calls `getuid()` to get the current user's UID
   - Each flag user has a different UID (flag00=3000, flag01=3001, ..., flag14=3014)
   - Uses the UID to select which encrypted token to decrypt
   - We intercept this and return 3014 to get flag14's token

3. Decrypts the corresponding token using the same algorithm from level13
   - The encrypted tokens are hardcoded in the binary
   - Each one corresponds to a different flag user

---

## 5. Get the flag

Use the token as the password for flag14:

```bash
su flag14
Password: 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```

Then run `getflag`:

```bash
getflag
```

**Congratulations!** You've completed all Snow Crash levels! 🎉

---

## 🏁 Flag

`7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ`
