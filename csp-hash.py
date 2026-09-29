# Recalcula los hashes de los <script> en línea de index.html y actualiza la
# Content-Security-Policy. Ejecutar después de editar cualquier script:
#   python csp-hash.py
import base64, hashlib, re, pathlib

p = pathlib.Path(__file__).with_name("index.html")
html = p.read_text(encoding="utf-8")
scripts = re.findall(r"<script>(.*?)</script>", html, flags=re.S)
hashes = " ".join(
    "'sha256-" + base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode() + "'"
    for s in scripts
)
new, n = re.subn(r"script-src [^;]*;", f"script-src {hashes} https://cdnjs.cloudflare.com;", html, count=1)
if n != 1:
    raise SystemExit("No se encontró la política CSP en index.html")
p.write_text(new, encoding="utf-8", newline="\n")
print(f"{len(scripts)} scripts en línea; CSP actualizada.")
