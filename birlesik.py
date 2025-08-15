import os
import json
import re
from httpx import Client

# ---------------- Dengetv54 ----------------
class Dengetv54Manager:
    def __init__(self):
        self.httpx = Client(timeout=10, verify=False)
        self.base_stream_url = "https://four.zirvestream4.cfd/"
        self.referer_url = None
        self.channel_files = {
            1: "yayinzirve.m3u8",
            2: "yayin1.m3u8",
            3: "yayininat.m3u8",
            4: "yayinb2.m3u8",
            5: "yayinb3.m3u8",
            6: "yayinb4.m3u8",
            7: "yayinb5.m3u8",
            8: "yayinbm1.m3u8",
            9: "yayinbm2.m3u8",
            10: "yayinss.m3u8",
        }

    def find_working_domain(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(54, 105):
            test_domain = f"https://dengetv{i}.live/"
            try:
                r = self.httpx.get(test_domain, headers=headers)
                if r.status_code == 200 and r.text.strip():
                    return test_domain
            except:
                continue
        return None

    def build_m3u8_content(self):
        m3u_content = []
        for idx, file_name in self.channel_files.items():
            channel_name = file_name.replace(".m3u8", "").capitalize()
            m3u_content.append(f'#EXTINF:-1 group-title="Dengetv54",{channel_name}')
            m3u_content.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u_content.append(f'#EXTVLCOPT:http-referrer={self.referer_url}')
            m3u_content.append(f"{self.base_stream_url}{file_name}")
        return "\n".join(m3u_content)

    def calistir(self):
        self.referer_url = self.find_working_domain() or "https://dengetv54.live/"
        m3u = self.build_m3u8_content()
        print(f"Dengetv54 içerik uzunluğu: {len(m3u)}")
        return m3u

# ---------------- XYZsports ----------------
class XYZsportsManager:
    def __init__(self):
        self.httpx = Client(timeout=10, verify=False)
        self.channel_ids = [
            "bein-sports-1", "bein-sports-2", "bein-sports-3"
        ]

    def find_working_domain(self, start=248, end=350):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(start, end + 1):
            url = f"https://www.xyzsports{i}.xyz/"
            try:
                r = self.httpx.get(url, headers=headers)
                if r.status_code == 200 and "uxsyplayer" in r.text:
                    return r.text, url
            except:
                continue
        return None, None

    def build_m3u8_content(self, base_stream_url, referer_url):
        m3u = []
        for cid in self.channel_ids:
            channel_name = cid.replace("-", " ").title()
            m3u.append(f'#EXTINF:-1 group-title="Spor",{channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(f'#EXTVLCOPT:http-referrer={referer_url}')
            m3u.append(f'{base_stream_url}{cid}/playlist.m3u8')
        return "\n".join(m3u)

    def calistir(self):
        html, referer_url = self.find_working_domain()
        if not html:
            print("XYZsports: Domain bulunamadı, dummy içerik oluşturuluyor.")
            referer_url = "https://www.xyzsports248.xyz/"
        base_stream_url = "https://dummy.xyzsports.stream/"  # Placeholder
        m3u = self.build_m3u8_content(base_stream_url, referer_url)
        print(f"XYZsports içerik uzunluğu: {len(m3u)}")
        return m3u

# ---------------- Main ----------------
if __name__ == "__main__":
    CIKTI_DOSYASI = "kanallar.m3u"
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
        CIKTI_DOSYASI = cfg.get("ana_m3u_dosyasi", CIKTI_DOSYASI)

    all_m3u = ["#EXTM3U"]

    dengetv = Dengetv54Manager()
    all_m3u.append(dengetv.calistir())

    xyz = XYZsportsManager()
    all_m3u.append(xyz.calistir())

    with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
        f.write("\n".join(all_m3u))

    print(f"✅ kanallar M3U oluşturuldu: {CIKTI_DOSYASI}")
