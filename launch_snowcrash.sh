#!/bin/bash

qemu-system-x86_64 \
  -cdrom ./SnowCrash.iso \
  -boot d \
  -m 2048 \
  -net nic \
  -net user,hostfwd=tcp::2222-:4242

