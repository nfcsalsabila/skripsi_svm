#!/bin/bash
echo "Menyiapkan update ke GitHub..."
git add .
git commit -m "update terbaru"
git push
echo "Selesai dikirim ke GitHub ✅"
