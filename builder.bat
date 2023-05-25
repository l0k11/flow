@echo off
cd web
npm run build
cd ..
python .\api.py