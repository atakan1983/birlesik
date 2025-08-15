import os
import re
from datetime import datetime
from httpx import Client

# ---------------- Dengetv54 ----------------
class Dengetv54Manager:
    def __init__(self):
        self.httpx = Client(timeout=10, verify=False)
        self.base_stream_url = "https://four.zirvestream4.cfd/"
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
            11: "yayinss2.m3u8",
            13: "yayint1.m3u8",
            14: "yayint2.m3u8",
            15: "yayint3.m3u8",
            16: "yayinsmarts.m3u8",
            17: "yayinsms2.m3u8",
            18: "yayintrtspor.m3u8",
            19: "yayintrtspor2.m3u8",
            20: "yayintrt1.m3u8",
            21: "yayinas.m3u8",
            22: "yayinatv.m3u8",
            23: "yayintv8.m3u8",
            24: "yayintv85.m3u8",
            25: "yayinf1.m3u8",
            26: "yayinnbatv.m3u8",
            27: "yayineu1.m3u8",
            28: "yayineu2.m3u8",
            29: "yayinex1.m3u8",
            30: "yayinex2.m3u8",
            31: "yayinex3.m3u8",
            32: "yayinex4.m3u8",
            33: "yayinex5.m3u8",
            34: "yayinex6.m3u8",
            35: "yayinex7.m3u8",
            36: "yayinex8.m3u8"
        }

    def find_working_domain(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(54, 105):
            url = f"https://dengetv{i}.live/"
            try:
                r = self.httpx.get(url, headers=headers)
                if r.status_code == 200 and r.text.strip():
                    return url
            except:
                continue
        return "https://dengetv54.live/"  # fallback

    def build_m3u8_content(self, referer_url):
        m3u = []
        for idx, file_name in self.channel_files.items():
            channel_name = file_name.replace(".m3u8", "").capitalize()
            m3u.append(f'#EXTINF:-1 group-title="Dengetv54",{channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(f'#EXTVLCOPT:http-referrer={referer_url}')
            m3u.append(f'{self.base_stream_url}{file_name}')
        return "\n".join(m3u)

    def calistir(self):
        referer = self.find_working_domain()
        m3u = self.build_m3u8_content(referer)
        print(f"Dengetv54 içerik uzunluğu: {len(m3u)}")
        return m3u

# ---------------- XYZsports ----------------
class XYZsportsManager:
    def __init__(self):
        self.httpx = Client(timeout=10, verify=False)
        self.channel_ids = ["bein-sports-1", "bein-sports-2", "bein-sports-3"]

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
        return None, "https://www.xyzsports248.xyz/"

    def build_m3u8_content(self, base_url, referer_url):
        m3u = []
        for cid in self.channel_ids:
            channel_name = cid.replace("-", " ").title()
            m3u.append(f'#EXTINF:-1 group-title="Umitmod",{channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(f'#EXTVLCOPT:http-referrer={referer_url}')
            m3u.append(f'{base_url}{cid}/playlist.m3u8')
        return "\n".join(m3u)

    def calistir(self):
        html, referer = self.find_working_domain()
        base_url = "https://dummy.xyzsports.stream/"  # fallback dummy
        m3u = self.build_m3u8_content(base_url, referer)
        print(f"XYZsports içerik uzunluğu: {len(m3u)}")
        return m3u

# ---------------- Main ----------------
if __name__ == "__main__":
    CIKTI_DOSYASI = "Birlesik.m3u"  # Sabit dosya adı, config yok

    all_m3u = ["#EXTM3U"]

    # Dengetv54
    dengetv = Dengetv54Manager()
    all_m3u.append(dengetv.calistir())

    # XYZsports
    xyz = XYZsportsManager()
    all_m3u.append(xyz.calistir())

    # Timestamp ekle → workflow her zaman commit yapar
    all_m3u.append(f'# Generated: {datetime.utcnow().isoformat()}')

    with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
        f.write("\n".join(all_m3u))

    print(f"✅ Birleşik M3U oluşturuldu: {CIKTI_DOSYASI}")
