import hashlib, pathlib, subprocess, time, urllib.request
import streamlit as st

URL = "https://github.com/p1neappleXpress/OpenFlux/releases/download/v0.17.1/openflux-linux-amd64"
SHA = "c0d00461e8cc59e48429b239fd8044b1c1aaa3769968a7c9160c488f4bd63f3b"
BIN = pathlib.Path("/tmp/openflux")
LOG = pathlib.Path("/tmp/openflux.log")
KEY = pathlib.Path("/tmp/of.key")

@st.cache_resource
def start():
    if not BIN.exists() or hashlib.sha256(BIN.read_bytes()).hexdigest() != SHA:
        urllib.request.urlretrieve(URL, BIN)
        BIN.chmod(0o755)
    KEY.write_text(st.secrets["OF_KEY"])
    f = open(LOG, "ab")
    return subprocess.Popen(
        [str(BIN), "--role=exit", "--mode=l4", "--transport=yandex",
         "--url", st.secrets["OF_DOC"], "--encryption-key-file", str(KEY)],
        stdout=f, stderr=f)

st.title("ok")
try:
    doc = st.secrets["OF_DOC"]
    key = st.secrets["OF_KEY"]
except Exception:
    st.write("no config")
    st.stop()

p = start()
if p.poll() is not None:
    start.clear()
    p = start()
time.sleep(2)
st.write("running" if p.poll() is None else "stopped")