# 🚩 SnowCrash — Level02

## 🎯 Goal

Find the password for **flag02**.

---

## 1. Check the current directory

```bash
ls -la
```

**Result:**

```
----r--r-- 1 flag02  level02 8302 Aug 30  2015 level02.pcap
```

A `.pcap` file is a **packet capture file** containing network traffic.

The file has no read permissions for the owner. Add read permission:

```bash
chmod u+r level02.pcap
```

---

## 2. Copy the file to local machine

From your local machine:

```bash
scp -P 2222 level02@localhost:~/level02.pcap ~/Documents/snow-crash/resources/level02/
```

---

## 3. Analyze with Wireshark

🔗 [https://www.wireshark.org/](https://www.wireshark.org/)

Launch Wireshark → **File** → **Open** → select `level02.pcap`

---

## 4. Follow the TCP Stream

1. Right-click on any packet → **Follow → TCP Stream**
2. You'll see a login attempt with username and password
3. Change view from "ASCII" to **"Hex Dump"** at the bottom

---

## 5. Decode the password

In the hex dump, you'll find:

```
000000B9  66                                                 f
000000BA  74                                                 t
000000BB  5f                                                 _
000000BC  77                                                 w
000000BD  61                                                 a
000000BE  6e                                                 n
000000BF  64                                                 d
000000C0  72                                                 r
000000C1  7f                                                 .
000000C2  7f                                                 .
000000C3  7f                                                 .
000000C4  4e                                                 N
000000C5  44                                                 D
000000C6  52                                                 R
000000C7  65                                                 e
000000C8  6c                                                 l
000000C9  7f                                                 .
000000CA  4c                                                 L
000000CB  30                                                 0
000000CC  4c                                                 L
000000CD  0d                                                 .
```

**Key:** `7f` is the DEL/backspace character

**Decoding process:**
1. Type: `ft_wandr`
2. Backspace 3 times (`7f 7f 7f`) → deletes `d`, `r` leaving `ft_wan`
3. Type: `NDRel`
4. Backspace 1 time (`7f`) → deletes `l` leaving `ft_wanNDRe`
5. Type: `L0L`

**Final password:** `ft_waNDReL0L`

---

## ✅ Final Flag

```bash
su flag02
```

Enter the password:

```
ft_waNDReL0L
```

Run:

```bash
getflag
```

---

## 🎉 **Final Token for Level02**

```
kooda2puivaav1idi4f57q8iq
```
