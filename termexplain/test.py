import subprocess, hashlib, os, re

packages = [
    "google-generativeai==0.3.0",
    "click==8.1.0",
    "rich==13.0.0",
    "colorama==0.4.6",
    "python-dotenv==1.0.0",
    "requests==2.31.0"
]

os.makedirs("wheels", exist_ok=True)

def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

for pkg in packages:
    print(f"\n📦 Processing: {pkg}")
    subprocess.run(["pip", "download", "--no-deps", pkg, "-d", "wheels"])
    files = os.listdir("wheels")
    for f in files:
        if pkg.split("==")[0].lower().replace("-", "_") in f.lower():
            sha = sha256sum(f"wheels/{f}")
            print(f'''resource "{pkg.split("==")[0]}" do
  url "https://files.pythonhosted.org/packages/source/{pkg[0].lower()}/{pkg.split("==")[0].lower()}/{f}"
  sha256 "{sha}"
end\n''')
