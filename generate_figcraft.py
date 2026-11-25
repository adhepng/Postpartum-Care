import json
import zipfile
import os

# Postpartum Care Design System Palette
PALETTE = {
    "champagne": {"r": 0.984, "g": 0.957, "b": 0.922, "a": 1.0, "hex": "#FBF4EB"},
    "blush": {"r": 0.984, "g": 0.851, "b": 0.898, "a": 1.0, "hex": "#FBD9E5"},
    "cherry_blossom": {"r": 0.969, "g": 0.773, "b": 0.843, "a": 1.0, "hex": "#F7C5D7"},
    "tickle_me_pink": {"r": 0.949, "g": 0.514, "b": 0.686, "a": 1.0, "hex": "#F283AF"},
    "raspberry_rose": {"r": 0.769, "g": 0.212, "b": 0.439, "a": 1.0, "hex": "#C43670"},
    "sunset": {"r": 0.953, "g": 0.800, "b": 0.592, "a": 1.0, "hex": "#F3CC97"},
    "white": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0, "hex": "#FFFFFF"},
    "text_dark": {"r": 0.180, "g": 0.133, "b": 0.157, "a": 1.0, "hex": "#2E2228"},
    "text_muted": {"r": 0.478, "g": 0.400, "b": 0.439, "a": 1.0, "hex": "#7A6670"},
    "border_light": {"r": 0.925, "g": 0.843, "b": 0.871, "a": 1.0, "hex": "#ECD7DE"},
    "card_bg": {"r": 1.0, "g": 0.984, "b": 0.976, "a": 1.0, "hex": "#FFFBF9"},
    "tag_bg": {"r": 0.969, "g": 0.898, "b": 0.929, "a": 1.0, "hex": "#F7E5ED"},
}

class FigcraftDocBuilder:
    def __init__(self, doc_name="Postpartum Care - Desktop UI"):
        self.doc_name = doc_name
        self.next_id = 1
        self.nodes = {}
        self.page_id = self._alloc_id()
        
        # Create page 1
        self.nodes[str(self.page_id)] = {
            "id": self.page_id,
            "name": "Postpartum Care Desktop UI",
            "type": "page",
            "background": {"r": 0.94, "g": 0.93, "b": 0.92, "a": 1.0},
            "flows": [],
            "prototype": {"device": "None", "background": {"r": 0.94, "g": 0.93, "b": 0.92, "a": 1.0}, "rotation": "portrait"},
            "guides": [],
            "children": [],
            "width": 0.0,
            "height": 0.0
        }

    def _alloc_id(self):
        nid = self.next_id
        self.next_id += 1
        return nid

    def add_solid_fill(self, color_dict):
        c = {k: color_dict[k] for k in ["r", "g", "b", "a"]}
        return [{
            "type": "solid",
            "color": c,
            "opacity": 1.0,
            "visible": True,
            "blend": "normal"
        }]

    def add_solid_stroke(self, color_dict, weight=1.0):
        c = {k: color_dict[k] for k in ["r", "g", "b", "a"]}
        return [{
            "type": "solid",
            "color": c,
            "opacity": 1.0,
            "visible": True,
            "blend": "normal"
        }]

    def create_frame(self, parent_id, name, x, y, width, height, fill_color=None, stroke_color=None, radius=0.0, clip=True):
        fid = self._alloc_id()
        node = {
            "id": fid,
            "name": name,
            "type": "frame",
            "parent": parent_id,
            "children": [],
            "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
            "width": float(width),
            "height": float(height),
            "clip": clip,
            "fills": self.add_solid_fill(fill_color) if fill_color else [],
            "strokes": self.add_solid_stroke(stroke_color) if stroke_color else [],
            "corners": {"radii": [float(radius)] * 4, "smoothing": 0.0} if radius > 0 else {"radii": [0.0, 0.0, 0.0, 0.0], "smoothing": 0.0}
        }
        self.nodes[str(fid)] = node
        if parent_id and str(parent_id) in self.nodes:
            self.nodes[str(parent_id)]["children"].append(fid)
        return fid

    def create_rectangle(self, parent_id, name, x, y, width, height, fill_color=None, stroke_color=None, radius=0.0):
        rid = self._alloc_id()
        node = {
            "id": rid,
            "name": name,
            "type": "rectangle",
            "parent": parent_id,
            "children": [],
            "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
            "width": float(width),
            "height": float(height),
            "fills": self.add_solid_fill(fill_color) if fill_color else [],
            "strokes": self.add_solid_stroke(stroke_color) if stroke_color else [],
            "corners": {"radii": [float(radius)] * 4, "smoothing": 0.0} if radius > 0 else {"radii": [0.0, 0.0, 0.0, 0.0], "smoothing": 0.0}
        }
        self.nodes[str(rid)] = node
        if parent_id and str(parent_id) in self.nodes and "children" in self.nodes[str(parent_id)]:
            self.nodes[str(parent_id)]["children"].append(rid)
        return rid

    def create_text(self, parent_id, name, text, x, y, width, height, font_size=14.0, font_style="Regular", fill_color=None, align_h="left"):
        tid = self._alloc_id()
        c = fill_color if fill_color else PALETTE["text_dark"]
        node = {
            "id": tid,
            "name": name,
            "type": "text",
            "characters": text,
            "parent": parent_id,
            "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
            "width": float(width),
            "height": float(height),
            "fills": self.add_solid_fill(c),
            "style": {
                "font_family": "Inter",
                "font_style": font_style,
                "font_size": float(font_size),
                "line_height": {"unit": "percent", "value": 140.0},
                "letter_spacing": {"unit": "percent", "value": 0.0},
                "decoration": "none",
                "case": "original",
                "fills": None,
                "link": None
            }
        }
        self.nodes[str(tid)] = node
        if parent_id and str(parent_id) in self.nodes and "children" in self.nodes[str(parent_id)]:
            self.nodes[str(parent_id)]["children"].append(tid)
        return tid

    def save(self, filepath):
        doc = {
            "format": "figcraft",
            "version": 1,
            "imageIndex": [],
            "name": self.doc_name,
            "pages": [self.page_id],
            "current_page": self.page_id,
            "next_id": self.next_id,
            "styles": [],
            "variables": {"collections": [], "variables": []},
            "document_colors": [],
            "comments": [],
            "nodes": self.nodes
        }
        
        with zipfile.ZipFile(filepath, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("document.json", json.dumps(doc, indent=2))
        print(f"Saved {filepath} with {len(self.nodes)} nodes successfully!")

def build_postpartum_figcraft():
    builder = FigcraftDocBuilder("Postpartum Care - Desktop UI")
    page = builder.page_id

    # -------------------------------------------------------------
    # 0. FOUNDATIONS & COLOR PALETTE FRAME (x: 0, y: -500, w: 1440, h: 380)
    # -------------------------------------------------------------
    ds_frame = builder.create_frame(page, "Foundations & Color System", 0, -500, 1440, 380, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_text(ds_frame, "DS Title", "🎨 Postpartum Care — Color Palette & Design Tokens", 40, 30, 800, 32, font_size=22, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(ds_frame, "DS Subtitle", "Berdasarkan pedoman warna proyek: Tickle Me Pink, Champagne, Blush, Cherry Blossom, Raspberry Rose, dan Sunset.", 40, 70, 900, 24, font_size=14, font_style="Regular", fill_color=PALETTE["text_muted"])
    
    swatches = [
        ("TICKLE ME PINK", PALETTE["tickle_me_pink"], "#F283AF", "Accent / Highlight State"),
        ("CHAMPAGNE", PALETTE["champagne"], "#FBF4EB", "Primary Page Background"),
        ("BLUSH", PALETTE["blush"], "#FBD9E5", "Card Surface / Soft Borders"),
        ("CHERRY BLOSSOM", PALETTE["cherry_blossom"], "#F7C5D7", "Pill Background / Tags"),
        ("RASPBERRY ROSE", PALETTE["raspberry_rose"], "#C43670", "Primary CTA / Brand Color"),
        ("SUNSET", PALETTE["sunset"], "#F3CC97", "Warm Badge / Notice Accent"),
    ]
    sw_w, sw_h = 190, 160
    for idx, (sname, scolor, shex, sdesc) in enumerate(swatches):
        sx = 40 + idx * 225
        card = builder.create_frame(ds_frame, f"Swatch {sname}", sx, 120, sw_w, sw_h, scolor, PALETTE["border_light"], radius=12)
        # text container at bottom
        sub_box = builder.create_rectangle(card, "Text Box", 0, 95, sw_w, 65, PALETTE["white"], None, radius=0)
        builder.create_text(card, "Swatch Name", sname, 12, 102, 166, 16, font_size=11, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(card, "Swatch Hex", shex, 12, 120, 166, 14, font_size=11, font_style="Regular", fill_color=PALETTE["raspberry_rose"])
        builder.create_text(card, "Swatch Desc", sdesc, 12, 136, 166, 14, font_size=9, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Helper function to create standard Desktop Navbar
    def add_desktop_navbar(parent_frame, active_tab="Beranda"):
        nav = builder.create_frame(parent_frame, "Top Navbar", 0, 0, 1440, 80, PALETTE["white"], PALETTE["border_light"], radius=0)
        # Logo
        builder.create_text(nav, "Brand Logo", "🌸 PostpartumCare", 48, 26, 260, 30, font_size=20, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
        
        # Navigation Items
        tabs = [
            ("Beranda", 320),
            ("Mood Check-In", 440),
            ("Daily Journal", 600),
            ("Micro-Relaxation", 740),
            ("Edukasi", 910),
            ("Bantuan Profesional", 1020)
        ]
        for tname, tx in tabs:
            is_active = (tname == active_tab)
            tc = PALETTE["raspberry_rose"] if is_active else PALETTE["text_dark"]
            tf = "Bold" if is_active else "Regular"
            builder.create_text(nav, f"Nav - {tname}", tname, tx, 30, 130, 24, font_size=14, font_style=tf, fill_color=tc)
            if is_active:
                builder.create_rectangle(nav, "Active Line", tx, 64, 40, 3, PALETTE["raspberry_rose"], None, radius=2)
        
        # User profile chip
        pchip = builder.create_frame(nav, "User Chip", 1230, 18, 160, 44, PALETTE["champagne"], PALETTE["blush"], radius=22)
        builder.create_rectangle(pchip, "Avatar", 8, 7, 30, 30, PALETTE["raspberry_rose"], None, radius=15)
        builder.create_text(pchip, "Avatar Text", "R", 18, 12, 20, 20, font_size=14, font_style="Bold", fill_color=PALETTE["white"])
        builder.create_text(pchip, "User Name", "Ibu Rani", 46, 9, 100, 14, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(pchip, "User Phase", "Hari ke-12", 46, 24, 100, 12, font_size=10, font_style="Regular", fill_color=PALETTE["text_muted"])

    # -------------------------------------------------------------
    # SCREEN 1: BERANDA / DASHBOARD (x: 0, y: 0, w: 1440, h: 1024)
    # -------------------------------------------------------------
    s1 = builder.create_frame(page, "Screen 1 — Beranda", 0, 0, 1440, 1024, PALETTE["champagne"], PALETTE["border_light"], radius=0)
    add_desktop_navbar(s1, "Beranda")

    # Welcome Banner
    banner = builder.create_frame(s1, "Hero Banner", 48, 110, 1344, 180, PALETTE["blush"], PALETTE["border_light"], radius=16)
    builder.create_text(banner, "Greeting", "Halo, Ibu Rani! 🌸", 40, 28, 600, 32, font_size=24, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(banner, "Phase Text", "Hari ke-12 Masa Pemulihan Pascapersalinan", 40, 68, 600, 22, font_size=16, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(banner, "Encouragement", "Setiap hari adalah langkah baru. Luangkan waktu sejenak untuk memeluk diri sendiri di antara riuhnya merawat buah hati.", 40, 96, 750, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])
    
    # Disclaimer Pill in Banner
    dpill = builder.create_frame(banner, "Disclaimer Pill", 40, 130, 520, 32, PALETTE["white"], PALETTE["cherry_blossom"], radius=16)
    builder.create_text(dpill, "Pill Text", "🛡️ Pendamping Kesejahteraan Emosional • Bukan Pengganti Diagnosis Medis", 16, 8, 488, 16, font_size=11, font_style="Medium", fill_color=PALETTE["raspberry_rose"])

    # 3 Quick Action Cards
    card_w = 426
    # 1. Mood Check-in Card
    c1 = builder.create_frame(s1, "Quick Card - Mood", 48, 316, card_w, 230, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_rectangle(c1, "Badge Mood", 24, 24, 36, 36, PALETTE["blush"], None, radius=18)
    builder.create_text(c1, "Icon Mood", "✨", 33, 30, 24, 24, font_size=16, font_style="Regular")
    builder.create_text(c1, "Title Mood", "Mood Check-In Hari Ini", 72, 28, 300, 24, font_size=16, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(c1, "Status Mood", "Status: Belum diisi hari ini", 72, 54, 300, 18, font_size=12, font_style="Regular", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(c1, "Desc Mood", "Kenali ritme emosi dan perasaanmu hari ini agar dapat memahami kebutuhan dirimu.", 24, 90, 378, 44, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])
    btn1 = builder.create_frame(c1, "Button Isi Mood", 24, 155, 378, 48, PALETTE["raspberry_rose"], None, radius=12)
    builder.create_text(btn1, "Btn Label", "Catat Mood Sekarang  ➔", 115, 14, 200, 20, font_size=14, font_style="Bold", fill_color=PALETTE["white"])

    # 2. Micro-Relaxation Card
    c2 = builder.create_frame(s1, "Quick Card - Relaxation", 48 + card_w + 33, 316, card_w, 230, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_rectangle(c2, "Badge Audio", 24, 24, 36, 36, PALETTE["champagne"], None, radius=18)
    builder.create_text(c2, "Icon Audio", "🎧", 33, 30, 24, 24, font_size=16, font_style="Regular")
    builder.create_text(c2, "Title Audio", "Micro-Relaxation (3 Menit)", 72, 28, 300, 24, font_size=16, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(c2, "Status Audio", "Latihan napas singkat & jeda tenang", 72, 54, 300, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])
    builder.create_text(c2, "Desc Audio", "Cukup 3 menit di sela menyusui untuk melepas ketegangan otot bahu dan memulihkan fokus.", 24, 90, 378, 44, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])
    btn2 = builder.create_frame(c2, "Button Play Audio", 24, 155, 378, 48, PALETTE["tickle_me_pink"], None, radius=12)
    builder.create_text(btn2, "Btn Label", "▶  Putar Relaksasi 3 Menit", 110, 14, 200, 20, font_size=14, font_style="Bold", fill_color=PALETTE["white"])

    # 3. Daily Journal Card
    c3 = builder.create_frame(s1, "Quick Card - Journal", 48 + (card_w + 33)*2, 316, card_w, 230, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_rectangle(c3, "Badge Journal", 24, 24, 36, 36, PALETTE["sunset"], None, radius=18)
    builder.create_text(c3, "Icon Journal", "📖", 33, 30, 24, 24, font_size=16, font_style="Regular")
    builder.create_text(c3, "Title Journal", "Daily Journal Privat", 72, 28, 300, 24, font_size=16, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(c3, "Status Journal", "Ruang aman tanpa takut dihakimi", 72, 54, 300, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])
    builder.create_text(c3, "Desc Journal", "Ungkapkan pikiran, kelelahan, maupun rasa syukurmu dalam jurnal terenkripsi pribadi.", 24, 90, 378, 44, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])
    btn3 = builder.create_frame(c3, "Button Tulis Jurnal", 24, 155, 378, 48, PALETTE["champagne"], PALETTE["border_light"], radius=12)
    builder.create_text(btn3, "Btn Label", "✍️  Tulis Catatan Harian", 115, 14, 200, 20, font_size=14, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    # Lower Section: Recommended Articles & Professional Support
    sec_title = builder.create_text(s1, "Sec Title", "Panduan Edukasi Sesuai Fase Anda", 48, 576, 500, 26, font_size=18, font_style="Bold", fill_color=PALETTE["text_dark"])
    
    # 3 Article Teasers
    art_w = 426
    articles = [
        ("Mengenali Baby Blues vs PPD", "Kesehatan Mental", "3 mnt baca", "Pelajari perbedaan mendasar antara emosi wajar pasca salin dan tanda butuh bantuan."),
        ("Nutrisi Kunci Pemulihan Ibu", "Pemulihan Fisik", "4 mnt baca", "Asupan cairan, serat, dan protein esensial untuk mempercepat proses pemulihan luka."),
        ("Manajemen Waktu Bersama Bayi", "Perawatan Diri", "5 mnt baca", "Strategi realistis membagi waktu tidur, makan, dan istirahat tanpa rasa bersalah."),
    ]
    for i, (atitle, acat, atime, adesc) in enumerate(articles):
        ax = 48 + i * (art_w + 33)
        acard = builder.create_frame(s1, f"Article {i+1}", ax, 615, art_w, 200, PALETTE["white"], PALETTE["border_light"], radius=14)
        # Category pill
        catp = builder.create_frame(acard, "Cat Pill", 24, 20, 130, 26, PALETTE["tag_bg"], None, radius=13)
        builder.create_text(catp, "Cat Text", acat, 12, 5, 110, 16, font_size=10, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
        builder.create_text(acard, "Read Time", atime, 330, 24, 80, 16, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])
        builder.create_text(acard, "Art Title", atitle, 24, 58, 370, 24, font_size=15, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(acard, "Art Desc", adesc, 24, 88, 370, 40, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])
        builder.create_text(acard, "Read More", "Baca Artikel Lengkap ➔", 24, 155, 200, 20, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    # Bottom Support Banner
    pro_bar = builder.create_frame(s1, "Pro Support Bar", 48, 845, 1344, 130, PALETTE["card_bg"], PALETTE["sunset"], radius=16)
    builder.create_text(pro_bar, "Pro Title", "💬 Butuh Teman Berbagi atau Bantuan Profesional?", 36, 28, 700, 26, font_size=17, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(pro_bar, "Pro Desc", "Temukan bidan, psikolog perinatal, dan konselor laktasi bersertifikat yang siap mendampingi perjalanan pemulihanmu dengan empati.", 36, 60, 850, 40, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])
    btn_pro = builder.create_frame(pro_bar, "Btn Pro", 1080, 42, 220, 46, PALETTE["raspberry_rose"], None, radius=12)
    builder.create_text(btn_pro, "Btn Text", "Buka Direktori Bantuan ➔", 24, 13, 180, 20, font_size=13, font_style="Bold", fill_color=PALETTE["white"])

    # -------------------------------------------------------------
    # SCREEN 2: MOOD CHECK-IN (x: 1600, y: 0, w: 1440, h: 1024)
    # -------------------------------------------------------------
    s2 = builder.create_frame(page, "Screen 2 — Mood Check-In", 1600, 0, 1440, 1024, PALETTE["champagne"], PALETTE["border_light"], radius=0)
    add_desktop_navbar(s2, "Mood Check-In")

    # Left Column: Check-in Form
    f2_left = builder.create_frame(s2, "Mood Form Column", 48, 110, 800, 860, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_text(f2_left, "Title", "Bagaimana Suasana Hatimu Hari Ini?", 40, 36, 600, 28, font_size=20, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(f2_left, "Sub", "Luangkan waktu 1 menit untuk mengenali apa yang sedang dirasakan tubuh dan pikiranmu.", 40, 72, 680, 22, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])
    
    # 5 Mood Selectors
    emojis = [
        ("😊", "Senang & Nyaman", "Rileks, bahagia"),
        ("😐", "Cukup Netral", "Biasa saja"),
        ("😫", "Lelah / Drop", "Butuh tidur ekstra"),
        ("😰", "Cemas / Khawatir", "Banyak pikiran"),
        ("😢", "Sedih / Kewalahan", "Ingin menangis"),
    ]
    builder.create_text(f2_left, "Select Label", "1. Pilih ekspresi yang paling mendekati perasaanmu:", 40, 120, 400, 20, font_size=14, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    for idx, (emo, elabel, edesc) in enumerate(emojis):
        ey = 155 + idx * 72
        is_selected = (idx == 2) # Lelah selected as sample
        card_bg = PALETTE["blush"] if is_selected else PALETTE["card_bg"]
        card_str = PALETTE["raspberry_rose"] if is_selected else PALETTE["border_light"]
        ecard = builder.create_frame(f2_left, f"Mood Card {idx+1}", 40, ey, 720, 60, card_bg, card_str, radius=12)
        builder.create_text(ecard, "Emoji", emo, 24, 12, 36, 36, font_size=24, font_style="Regular")
        builder.create_text(ecard, "Label", elabel, 72, 14, 250, 18, font_size=14, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(ecard, "Desc", edesc, 72, 34, 300, 16, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])
        if is_selected:
            builder.create_text(ecard, "Badge Sel", "✓ Terpilih", 620, 20, 80, 18, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    # Factor Tags
    builder.create_text(f2_left, "Tags Label", "2. Faktor apa yang paling mempengaruhimu saat ini? (Bisa pilih lebih dari satu)", 40, 535, 680, 20, font_size=14, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    factors = ["Kurang Tidur", "Menyusui Sakit", "Dukungan Pasangan", "Nyeri Jahitan", "Bayi Menangis", "Kelelahan Rumah", "Keluarga Berkunjung"]
    fx = 40
    fy = 570
    for tag in factors:
        tw = len(tag) * 9 + 28
        tpill = builder.create_frame(f2_left, f"Tag {tag}", fx, fy, tw, 36, PALETTE["champagne"], PALETTE["blush"], radius=18)
        builder.create_text(tpill, "Text", tag, 14, 9, tw-20, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_dark"])
        fx += tw + 12
        if fx > 650:
            fx = 40
            fy += 46

    # Note Textarea
    builder.create_text(f2_left, "Note Label", "3. Catatan tambahan (opsional):", 40, 670, 400, 20, font_size=14, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    note_box = builder.create_frame(f2_left, "Input Box", 40, 700, 720, 70, PALETTE["white"], PALETTE["border_light"], radius=10)
    builder.create_text(note_box, "Placeholder", "Semalam terbangun 4 kali karena si kecil kolik, badan terasa sangat lelah...", 16, 14, 680, 40, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Submit Button
    btn_save_mood = builder.create_frame(f2_left, "Btn Save Mood", 40, 790, 720, 48, PALETTE["raspberry_rose"], None, radius=12)
    builder.create_text(btn_save_mood, "Label", "Simpan Catatan Mood Hari Ini", 250, 14, 250, 20, font_size=14, font_style="Bold", fill_color=PALETTE["white"])

    # Right Column: History & Trends
    f2_right = builder.create_frame(s2, "Mood History Column", 876, 110, 516, 860, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_text(f2_right, "Hist Title", "Riwayat Suasana Hati (7 Hari)", 32, 36, 400, 26, font_size=18, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(f2_right, "Hist Sub", "Catatan emosi mingguan untuk melihat pola pemulihan.", 32, 68, 440, 20, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Sample History Items
    history = [
        ("Hari ini, 11 Nov", "😫 Lelah / Drop", "14:20 WIB", "Kurang tidur malam", PALETTE["sunset"]),
        ("Kemarin, 10 Nov", "😊 Senang & Nyaman", "09:15 WIB", "Bisa tidur siang 2 jam", PALETTE["blush"]),
        ("Senin, 09 Nov", "😐 Cukup Netral", "11:00 WIB", "Menyusui lancar", PALETTE["champagne"]),
        ("Minggu, 08 Nov", "😰 Cemas / Khawatir", "21:30 WIB", "Bayi menangis terus", PALETTE["cherry_blossom"]),
        ("Sabtu, 07 Nov", "😫 Lelah / Drop", "15:45 WIB", "Pekerjaan rumah menumpuk", PALETTE["sunset"]),
    ]
    for h_idx, (hdate, hmood, htime, hnote, hcolor) in enumerate(history):
        hy = 110 + h_idx * 95
        hcard = builder.create_frame(f2_right, f"Hist Item {h_idx+1}", 32, hy, 452, 80, PALETTE["card_bg"], PALETTE["border_light"], radius=12)
        builder.create_rectangle(hcard, "Indicator", 16, 16, 8, 48, hcolor, None, radius=4)
        builder.create_text(hcard, "H Date", hdate, 36, 16, 200, 16, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(hcard, "H Mood", hmood, 36, 36, 250, 18, font_size=13, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
        builder.create_text(hcard, "H Note", hnote, 36, 54, 300, 16, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])
        builder.create_text(hcard, "H Time", htime, 350, 16, 90, 16, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Insight Box in Right Column
    ins_box = builder.create_frame(f2_right, "Insight Box", 32, 610, 452, 210, PALETTE["champagne"], PALETTE["sunset"], radius=14)
    builder.create_text(ins_box, "Ins Title", "💡 Pola Refleksi Anda", 24, 20, 300, 22, font_size=15, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(ins_box, "Ins Text 1", "• Rasa lelah dominan terjadi di pertengahan sore hari.", 24, 55, 400, 20, font_size=12, font_style="Medium", fill_color=PALETTE["text_dark"])
    builder.create_text(ins_box, "Ins Text 2", "• Hari yang diawali dengan relaksasi 3 menit menunjukkan suasana hati lebih stabil.", 24, 85, 400, 36, font_size=12, font_style="Medium", fill_color=PALETTE["text_dark"])
    builder.create_text(ins_box, "Ins Text 3", "• Jangan ragu meminta bantuan pasangan saat merasa beban tubuh mencapai batas.", 24, 130, 400, 36, font_size=12, font_style="Medium", fill_color=PALETTE["text_dark"])

    # -------------------------------------------------------------
    # SCREEN 3: DAILY JOURNAL (x: 3200, y: 0, w: 1440, h: 1024)
    # -------------------------------------------------------------
    s3 = builder.create_frame(page, "Screen 3 — Daily Journal", 3200, 0, 1440, 1024, PALETTE["champagne"], PALETTE["border_light"], radius=0)
    add_desktop_navbar(s3, "Daily Journal")

    # Left Column: Journal Editor
    j_left = builder.create_frame(s3, "Journal Editor Col", 48, 110, 840, 860, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_text(j_left, "Title", "Tulis Refleksi & Jurnal Harian", 40, 36, 600, 28, font_size=20, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(j_left, "Sub", "Ruang aman dan privat untuk menuliskan segala hal yang sedang berkecamuk di pikiranmu.", 40, 70, 700, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Title Input
    builder.create_text(j_left, "Label Title", "Judul Catatan:", 40, 115, 200, 18, font_size=13, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    j_title_box = builder.create_frame(j_left, "Title Box", 40, 140, 760, 46, PALETTE["white"], PALETTE["border_light"], radius=10)
    builder.create_text(j_title_box, "Sample Title", "Hari ke-12: Menghargai proses kecil yang sering luput disadari", 16, 13, 720, 20, font_size=14, font_style="Medium", fill_color=PALETTE["text_dark"])

    # Tag Selector
    builder.create_text(j_left, "Label Tags", "Pilih Tag Perasaan:", 40, 205, 200, 18, font_size=13, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    jtags = [("#lelah", True), ("#bersyukur", True), ("#cemas", False), ("#sayangBayi", True), ("#kewalahan", False), ("#butuhJeda", True)]
    jtx = 40
    for tstr, tactive in jtags:
        tw = len(tstr) * 9 + 30
        tcol = PALETTE["blush"] if tactive else PALETTE["card_bg"]
        tstrcol = PALETTE["raspberry_rose"] if tactive else PALETTE["border_light"]
        ttxtcol = PALETTE["raspberry_rose"] if tactive else PALETTE["text_muted"]
        tp = builder.create_frame(j_left, f"Tag {tstr}", jtx, 230, tw, 34, tcol, tstrcol, radius=17)
        builder.create_text(tp, "Tag Txt", tstr, 12, 8, tw-20, 16, font_size=12, font_style="Bold" if tactive else "Regular", fill_color=ttxtcol)
        jtx += tw + 10

    # Body Textarea
    builder.create_text(j_left, "Label Body", "Isi Curahan Hati:", 40, 285, 200, 18, font_size=13, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    j_body_box = builder.create_frame(j_left, "Body Box", 40, 310, 760, 430, PALETTE["white"], PALETTE["border_light"], radius=10)
    sample_journal = (
        "Hari ini tubuh terasa begitu lelah, tapi ketika melihat senyum kecil si bayi saat digendong, "
        "ada rasa hangat yang susah dijelaskan.\n\n"
        "Terkadang aku merasa bersalah ketika ingin istirahat sejenak dan menyerahkan bayi ke suami, "
        "tapi aku belajar bahwa ibu yang bahagia dan cukup istirahat adalah yang terbaik untuk bayi.\n\n"
        "Hari ini aku berhasil makan siang tepat waktu dan melakukan relaksasi napas 3 menit. "
        "Kemajuan kecil yang patut dirayakan."
    )
    builder.create_text(j_body_box, "Content", sample_journal, 20, 20, 720, 380, font_size=14, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Action Buttons
    btn_save_j = builder.create_frame(j_left, "Btn Save J", 40, 770, 240, 48, PALETTE["raspberry_rose"], None, radius=12)
    builder.create_text(btn_save_j, "Lbl", "Simpan ke Jurnal Pribadi", 35, 14, 180, 20, font_size=13, font_style="Bold", fill_color=PALETTE["white"])
    
    btn_cancel_j = builder.create_frame(j_left, "Btn Cancel J", 300, 770, 140, 48, PALETTE["white"], PALETTE["border_light"], radius=12)
    builder.create_text(btn_cancel_j, "Lbl", "Batal / Reset", 30, 14, 80, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Right Column: Saved Entries
    j_right = builder.create_frame(s3, "Saved Entries Col", 916, 110, 476, 860, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_text(j_right, "Title Entries", "Daftar Jurnal Tersimpan", 32, 36, 350, 26, font_size=18, font_style="Bold", fill_color=PALETTE["text_dark"])
    
    # Search in saved journals
    j_search = builder.create_frame(j_right, "Search Box", 32, 75, 412, 42, PALETTE["card_bg"], PALETTE["border_light"], radius=10)
    builder.create_text(j_search, "Search Plh", "🔍  Cari catatan atau tanggal...", 16, 12, 300, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])

    # List of entries
    entries = [
        ("28 Okt 2026", "Hari pertama sendirian menjaga bayi saat suami kerja", "#cemas #lelah", "Rasanya campur aduk dan panik saat bayi menangis tanpa henti..."),
        ("27 Okt 2026", "Malam yang panjang dan pelajaran tentang kesabaran", "#lelah #butuhJeda", "Kurang tidur membuat kepalaku pusing. Untung ibu datang membantu..."),
        ("25 Okt 2026", "Kunjungan pertama ke dokter anak", "#bersyukur", "Berat badan si kecil naik dengan baik. Hati merasa sangat lega..."),
    ]
    for idx, (edate, etitle, etags, esnippet) in enumerate(entries):
        ey = 135 + idx * 160
        ec = builder.create_frame(j_right, f"Entry {idx+1}", 32, ey, 412, 145, PALETTE["card_bg"], PALETTE["border_light"], radius=12)
        builder.create_text(ec, "Date", edate, 18, 14, 150, 16, font_size=11, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
        builder.create_text(ec, "Tags", etags, 220, 14, 180, 16, font_size=11, font_style="Medium", fill_color=PALETTE["text_muted"])
        builder.create_text(ec, "Title", etitle, 18, 36, 370, 20, font_size=13, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(ec, "Snippet", esnippet, 18, 62, 370, 36, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])
        builder.create_text(ec, "Action Edit", "✏️ Ubah", 18, 115, 60, 16, font_size=11, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(ec, "Action Del", "🗑️ Hapus", 90, 115, 60, 16, font_size=11, font_style="Regular", fill_color=PALETTE["raspberry_rose"])

    # -------------------------------------------------------------
    # SCREEN 4: MICRO-RELAXATION (x: 4800, y: 0, w: 1440, h: 1024)
    # -------------------------------------------------------------
    s4 = builder.create_frame(page, "Screen 4 — Micro-Relaxation", 4800, 0, 1440, 1024, PALETTE["champagne"], PALETTE["border_light"], radius=0)
    add_desktop_navbar(s4, "Micro-Relaxation")

    # Center Player Box
    player_box = builder.create_frame(s4, "Player Center Frame", 270, 120, 900, 560, PALETTE["white"], PALETTE["border_light"], radius=20)
    builder.create_text(player_box, "Title", "Micro-Relaxation: Napas & Ketenangan Batin", 0, 36, 900, 30, font_size=22, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(player_box, "Subtitle", "Latihan pernapasan 3 menit untuk meredakan ketegangan fisik dan kecemasan ibu.", 0, 72, 900, 22, font_size=14, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Big Breathing Visual Circle
    circle_outer = builder.create_frame(player_box, "Breathing Circle Outer", 350, 125, 200, 200, PALETTE["blush"], PALETTE["cherry_blossom"], radius=100)
    circle_inner = builder.create_frame(circle_outer, "Breathing Circle Inner", 25, 25, 150, 150, PALETTE["white"], PALETTE["tickle_me_pink"], radius=75)
    builder.create_text(circle_inner, "Circle Text 1", "Tarik Napas...", 25, 52, 100, 20, font_size=13, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(circle_inner, "Circle Text 2", "4 detik", 35, 78, 80, 16, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Audio Timer & Waveform
    builder.create_text(player_box, "Timer", "02:41 / 03:00", 0, 350, 900, 28, font_size=20, font_style="Bold", fill_color=PALETTE["text_dark"])
    
    # Progress Bar
    prog_bg = builder.create_frame(player_box, "Progress BG", 150, 395, 600, 8, PALETTE["champagne"], None, radius=4)
    prog_fill = builder.create_rectangle(prog_bg, "Progress Fill", 0, 0, 480, 8, PALETTE["raspberry_rose"], None, radius=4)

    # Audio Controls
    ctrl_frame = builder.create_frame(player_box, "Controls Bar", 360, 430, 180, 60, None, None, radius=0)
    # Rewind
    builder.create_rectangle(ctrl_frame, "Rewind Btn", 0, 10, 40, 40, PALETTE["champagne"], None, radius=20)
    builder.create_text(ctrl_frame, "Rewind Icon", "⏮", 12, 20, 20, 20, font_size=14, font_style="Bold", fill_color=PALETTE["text_dark"])
    # Play/Pause main
    builder.create_rectangle(ctrl_frame, "Play Main", 60, 0, 60, 60, PALETTE["raspberry_rose"], None, radius=30)
    builder.create_text(ctrl_frame, "Play Icon", "⏸", 82, 16, 24, 24, font_size=18, font_style="Bold", fill_color=PALETTE["white"])
    # Stop
    builder.create_rectangle(ctrl_frame, "Stop Btn", 140, 10, 40, 40, PALETTE["champagne"], None, radius=20)
    builder.create_text(ctrl_frame, "Stop Icon", "⏹", 152, 20, 20, 20, font_size=14, font_style="Bold", fill_color=PALETTE["text_dark"])

    # Bottom Session Options
    builder.create_text(s4, "More Sessions Title", "Pilihan Sesi Relaksasi 3 Menit Lainnya", 270, 715, 400, 24, font_size=17, font_style="Bold", fill_color=PALETTE["text_dark"])
    sessions = [
        ("Pelepas Ketegangan Bahu & Leher", "Fokus meredakan kaku otot akibat posisi menyusui.", "3 Menit"),
        ("Afirmasi Kebaikan Diri Ibu", "Kalimat positif untuk mengikis rasa bersalah & lelah.", "3 Menit"),
        ("Relaksasi Menjelang Tidur Singkat", "Menenangkan pikiran aktif sebelum power nap.", "3 Menit")
    ]
    for idx, (stitle, sdesc, sdur) in enumerate(sessions):
        sx = 270 + idx * 310
        scard = builder.create_frame(s4, f"Session {idx+1}", sx, 755, 280, 160, PALETTE["white"], PALETTE["border_light"], radius=14)
        builder.create_text(scard, "Dur", sdur, 20, 16, 100, 16, font_size=11, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
        builder.create_text(scard, "Title", stitle, 20, 40, 240, 36, font_size=13, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(scard, "Desc", sdesc, 20, 82, 240, 36, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])
        builder.create_text(scard, "Play", "▶ Putar Sesi", 20, 126, 120, 16, font_size=11, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    # -------------------------------------------------------------
    # SCREEN 5: GUIDED INFORMATION / EDUKASI (x: 6400, y: 0, w: 1440, h: 1024)
    # -------------------------------------------------------------
    s5 = builder.create_frame(page, "Screen 5 — Guided Information", 6400, 0, 1440, 1024, PALETTE["champagne"], PALETTE["border_light"], radius=0)
    add_desktop_navbar(s5, "Edukasi")

    # Header & Search
    builder.create_text(s5, "Title", "Pusat Panduan & Informasi Pascapersalinan", 48, 110, 600, 30, font_size=22, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(s5, "Subtitle", "Artikel berbasis literatur kesehatan terpercaya untuk mendampingi masa transisi menjadi ibu.", 48, 146, 750, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Search Bar & Filter Buttons
    search_bar = builder.create_frame(s5, "Search Input", 48, 185, 1344, 50, PALETTE["white"], PALETTE["border_light"], radius=12)
    builder.create_text(search_bar, "Placeholder", "🔍  Cari topik artikel (misal: baby blues, nyeri jahitan, jadwal tidur, laktasi)...", 24, 16, 600, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Category Tabs
    categories = ["Semua Kategori", "Pemulihan Fisik", "Kesehatan Mental Ibu", "Menyusui & Bayi", "Perawatan Diri & Nutrisi"]
    cx = 48
    for idx, cat_name in enumerate(categories):
        is_active = (idx == 0)
        cbg = PALETTE["raspberry_rose"] if is_active else PALETTE["white"]
        ctxt = PALETTE["white"] if is_active else PALETTE["text_dark"]
        cstr = None if is_active else PALETTE["border_light"]
        cw = len(cat_name) * 8 + 36
        cp = builder.create_frame(s5, f"Cat Tab {idx+1}", cx, 252, cw, 38, cbg, cstr, radius=19)
        builder.create_text(cp, "Text", cat_name, 18, 10, cw-20, 18, font_size=12, font_style="Bold" if is_active else "Regular", fill_color=ctxt)
        cx += cw + 12

    # Article Grid (2 rows x 3 columns)
    grid_articles = [
        ("Mengenali Baby Blues vs Depresi Pascapersalinan", "Kesehatan Mental", "4 mnt baca", "Perubahan hormon drastis wajar memicu tangis emosional di minggu pertama, namun kenali tanda saat itu menetap."),
        ("Panduan Merawat Luka Jahitan Caesar & Normal", "Pemulihan Fisik", "5 mnt baca", "Langkah menjaga kebersihan luka, tanda bahaya infeksi, dan kapan harus segera kontrol ke dokter obgyn."),
        ("Manajemen Overthinking & Rasa Bersalah Ibu", "Kesehatan Mental", "3 mnt baca", "Mengapa kita sering merasa 'bukan ibu yang baik' dan bagaimana teknik mindful self-compassion bekerja."),
        ("Posisi Menyusui yang Ergonomis & Nyaman", "Menyusui & Bayi", "4 mnt baca", "Mencegah puting lecet dan nyeri punggung bawah dengan penopang bantal menyusui yang tepat."),
        ("Pola Makan Pemulih Energi & Pelancar ASI", "Nutrisi", "3 mnt baca", "Kombinasi makanan kaya zat besi, protein, dan hidrasi optimal tanpa perlu diet ketat yang melelahkan."),
        ("Kapan Waktu yang Tepat Menghubungi Tenaga Profesional?", "Dukungan Medis", "4 mnt baca", "Tolak ukur objektif kapan ibu perlu menjadwalkan konseling psikologis atau pemeriksaan bidan.")
    ]
    card_gw = 426
    card_gh = 290
    for idx, (gatitle, gacat, gatime, gadesc) in enumerate(grid_articles):
        row = idx // 3
        col = idx % 3
        gx = 48 + col * (card_gw + 33)
        gy = 310 + row * (card_gh + 24)
        
        gcard = builder.create_frame(s5, f"Grid Article {idx+1}", gx, gy, card_gw, card_gh, PALETTE["white"], PALETTE["border_light"], radius=14)
        # Visual header placeholder
        img_ph = builder.create_frame(gcard, "Image Header", 0, 0, card_gw, 100, PALETTE["blush"], None, radius=0)
        builder.create_text(img_ph, "Icon Category", "📚  Panduan Postpartum", 24, 38, 200, 20, font_size=13, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
        
        # Category Tag
        cat_tag = builder.create_frame(gcard, "Tag", 20, 115, 130, 24, PALETTE["champagne"], PALETTE["border_light"], radius=12)
        builder.create_text(cat_tag, "Tag Txt", gacat, 10, 4, 110, 14, font_size=10, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
        builder.create_text(gcard, "Read Time", gatime, 330, 118, 80, 16, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])
        
        builder.create_text(gcard, "Title", gatitle, 20, 150, 386, 42, font_size=14, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(gcard, "Desc", gadesc, 20, 198, 386, 44, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])
        
        builder.create_text(gcard, "Read More", "Baca Artikel Selengkapnya ➔", 20, 254, 200, 18, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    # -------------------------------------------------------------
    # SCREEN 6: DIREKTORI & PEMESANAN PROFESIONAL (x: 8000, y: 0, w: 1440, h: 1024)
    # -------------------------------------------------------------
    s6 = builder.create_frame(page, "Screen 6 — Direktori & Bantuan", 8000, 0, 1440, 1024, PALETTE["champagne"], PALETTE["border_light"], radius=0)
    add_desktop_navbar(s6, "Bantuan Profesional")

    # Empathy Notice Banner
    notice = builder.create_frame(s6, "Empathy Notice", 48, 105, 1344, 76, PALETTE["sunset"], None, radius=12)
    builder.create_text(notice, "Notice Text 1", "🧡 Jangan Ragukan Diri Anda: Meminta Bantuan adalah Bentuk Keberanian dan Kasih Sayang", 28, 16, 800, 20, font_size=14, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(notice, "Notice Text 2", "Platform ini mempermudah pencarian tenaga profesional tervalidasi. Seluruh sesi dilakukan melalui saluran komunikasi aman.", 28, 42, 1100, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Left Column: Professional Directory Cards
    p_left = builder.create_frame(s6, "Directory Col", 48, 200, 780, 770, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_text(p_left, "Title", "Direktori Tenaga Profesional Berlisensi", 32, 28, 500, 26, font_size=18, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(p_left, "Sub", "Pilih psikolog perinatal, bidan, atau konselor laktasi sesuai kebutuhanmu.", 32, 58, 600, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])

    professionals = [
        ("Rina Kusuma, M.Psi., Psikolog", "Psikolog Klinis Perinatal & Trauma Salin", "Pengalaman 8 tahun • SIP: 1029/PSI/2020", "Rp 200.000 / sesi 60 mnt", "Chat WhatsApp / Google Meet", True),
        ("Bidan Nurul Aisyah, S.Tr.Keb", "Konselor Laktasi & Pendampingan Postpartum", "Pengalaman 12 tahun • IBI No: 8841/DKI", "Rp 150.000 / sesi 45 mnt", "Konsultasi Chat & Video", False),
        ("dr. Sarah Anindya, Sp.OG", "Spesialis Obstetri & Ginekologi (Konsultasi Pemulihan)", "RSUP Fatmawati • STR Aktif", "Rp 250.000 / sesi 45 mnt", "Google Meet Video Call", False)
    ]
    for idx, (pname, pspec, pexp, pfee, pmedia, is_sel) in enumerate(professionals):
        py = 95 + idx * 215
        pbg = PALETTE["card_bg"] if not is_sel else PALETTE["blush"]
        pborder = PALETTE["raspberry_rose"] if is_sel else PALETTE["border_light"]
        pcard = builder.create_frame(p_left, f"Pro Card {idx+1}", 32, py, 716, 195, pbg, pborder, radius=14)
        
        # Avatar placeholder
        builder.create_rectangle(pcard, "Avatar", 24, 24, 60, 60, PALETTE["tickle_me_pink"], None, radius=30)
        builder.create_text(pcard, "Avatar Icon", "👩‍⚕️", 40, 40, 30, 30, font_size=20, font_style="Regular")
        
        # Info
        builder.create_text(pcard, "Name", pname, 100, 24, 400, 22, font_size=15, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(pcard, "Spec", pspec, 100, 50, 450, 18, font_size=13, font_style="Semi Bold", fill_color=PALETTE["raspberry_rose"])
        builder.create_text(pcard, "Exp", pexp, 100, 72, 450, 16, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])
        
        # Fee & Media
        builder.create_text(pcard, "Fee", f"Biaya: {pfee}", 100, 104, 300, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
        builder.create_text(pcard, "Media", f"Media: {pmedia}", 100, 126, 350, 16, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])
        
        btn_sel = builder.create_frame(pcard, "Btn Select Pro", 540, 120, 150, 42, PALETTE["raspberry_rose"], None, radius=10)
        sel_text = "✓ Dipilih" if is_sel else "Pilih Tenaga"
        builder.create_text(btn_sel, "Btn Lbl", sel_text, 38, 12, 80, 18, font_size=12, font_style="Bold", fill_color=PALETTE["white"])

    # Right Column: Booking Form & Status
    p_right = builder.create_frame(s6, "Booking Col", 856, 200, 536, 770, PALETTE["white"], PALETTE["border_light"], radius=16)
    builder.create_text(p_right, "Title Booking", "Formulir Pemesanan Sesi", 32, 28, 400, 26, font_size=18, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(p_right, "Sub Booking", "Konfirmasi jadwal dan media konsultasi dengan tenaga pilihan.", 32, 58, 450, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Chosen professional chip
    ch_chip = builder.create_frame(p_right, "Chosen Chip", 32, 90, 472, 50, PALETTE["champagne"], PALETTE["border_light"], radius=10)
    builder.create_text(ch_chip, "Lbl", "Konsultasi dengan:", 16, 15, 120, 18, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])
    builder.create_text(ch_chip, "Name", "Rina Kusuma, M.Psi., Psikolog", 136, 15, 320, 18, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    # Date Picker
    builder.create_text(p_right, "Date Lbl", "Pilih Tanggal Sesi:", 32, 160, 200, 18, font_size=12, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    d_box = builder.create_frame(p_right, "Date Box", 32, 185, 472, 42, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(d_box, "Txt", "📅  Kamis, 12 November 2026", 16, 12, 300, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Time Picker
    builder.create_text(p_right, "Time Lbl", "Pilih Jam Konsultasi:", 32, 240, 200, 18, font_size=12, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    hours = ["10:00 WIB", "14:00 WIB", "16:00 WIB", "19:30 WIB"]
    hx = 32
    for h_idx, h_str in enumerate(hours):
        h_sel = (h_idx == 1)
        h_bg = PALETTE["blush"] if h_sel else PALETTE["white"]
        h_str_c = PALETTE["raspberry_rose"] if h_sel else PALETTE["border_light"]
        h_t_c = PALETTE["raspberry_rose"] if h_sel else PALETTE["text_dark"]
        h_btn = builder.create_frame(p_right, f"Hour {h_str}", hx, 265, 106, 36, h_bg, h_str_c, radius=8)
        builder.create_text(h_btn, "Txt", h_str, 16, 9, 80, 16, font_size=11, font_style="Bold" if h_sel else "Regular", fill_color=h_t_c)
        hx += 122

    # Media Selector
    builder.create_text(p_right, "Media Lbl", "Media Komunikasi:", 32, 320, 200, 18, font_size=12, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    m_box = builder.create_frame(p_right, "Media Box", 32, 345, 472, 42, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(m_box, "Txt", "📹  Google Meet (Panggilan Video)", 16, 12, 300, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Note
    builder.create_text(p_right, "Note Lbl", "Keluhan Singkat yang Ingin Didiskusikan:", 32, 405, 300, 18, font_size=12, font_style="Semi Bold", fill_color=PALETTE["text_dark"])
    n_box = builder.create_frame(p_right, "Note Box", 32, 430, 472, 70, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(n_box, "Txt", "Merasa sering menangis tiba-tiba di malam hari dan overthinking tentang perawatan bayi...", 14, 12, 440, 46, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Submit Booking
    btn_sub_book = builder.create_frame(p_right, "Btn Submit Booking", 32, 520, 472, 48, PALETTE["raspberry_rose"], None, radius=12)
    builder.create_text(btn_sub_book, "Txt", "Kirim Permintaan Sesi Konsultasi  ➔", 110, 14, 280, 20, font_size=13, font_style="Bold", fill_color=PALETTE["white"])

    # Booking History Status
    builder.create_text(p_right, "Title Status", "Status Permintaan Sesi Aktif", 32, 590, 300, 22, font_size=14, font_style="Bold", fill_color=PALETTE["text_dark"])
    
    status_card = builder.create_frame(p_right, "Status Card 1", 32, 620, 472, 115, PALETTE["champagne"], PALETTE["sunset"], radius=12)
    builder.create_text(status_card, "Date Info", "12 Nov 2026 • 14:00 WIB", 18, 14, 200, 16, font_size=11, font_style="Bold", fill_color=PALETTE["text_dark"])
    # Status Pill
    s_pill = builder.create_frame(status_card, "Status Pill", 310, 12, 145, 26, PALETTE["sunset"], None, radius=13)
    builder.create_text(s_pill, "Txt", "⏳ Menunggu Konfirmasi", 10, 5, 130, 16, font_size=10, font_style="Bold", fill_color=PALETTE["text_dark"])
    
    builder.create_text(status_card, "Pro Info", "Konselor: Rina Kusuma, M.Psi., Psikolog", 18, 42, 350, 18, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(status_card, "Note Info", "Media: Google Meet • Menunggu penerimaan jadwal oleh tenaga profesional.", 18, 66, 420, 36, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])

    # -------------------------------------------------------------
    # SCREEN 7: HALAMAN MASUK (LOGIN) (x: 9600, y: 0, w: 1440, h: 1024)
    # -------------------------------------------------------------
    s7 = builder.create_frame(page, "Screen 7 — Halaman Masuk (Login)", 9600, 0, 1440, 1024, PALETTE["champagne"], PALETTE["border_light"], radius=0)
    
    # Top Minimal Header for Auth
    nav_auth_1 = builder.create_frame(s7, "Top Auth Header", 0, 0, 1440, 80, PALETTE["white"], PALETTE["border_light"], radius=0)
    builder.create_text(nav_auth_1, "Logo", "🌸 PostpartumCare", 60, 26, 260, 30, font_size=20, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(nav_auth_1, "Back Home", "← Kembali ke Beranda", 1220, 30, 160, 20, font_size=13, font_style="Bold", fill_color=PALETTE["text_muted"])

    # Left Branding Card
    auth_l1 = builder.create_frame(s7, "Auth Left Card", 80, 120, 600, 840, PALETTE["blush"], PALETTE["border_light"], radius=20)
    builder.create_text(auth_l1, "Badge", "🌸 Ruang Pendamping Pribadi", 48, 48, 300, 24, font_size=13, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(auth_l1, "Heading", "Selamat Datang Kembali,\nIbu Hebat.", 48, 90, 500, 70, font_size=30, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(auth_l1, "Desc", "Masa pascapersalinan adalah perjalanan berharga. Masuk ke akunmu untuk melanjutkan pencatatan suasana hati, menulis curahan jurnal, dan mengakses panduan pemulihan.", 48, 180, 480, 70, font_size=14, font_style="Regular", fill_color=PALETTE["text_muted"])
    
    # Left Visual Quote Box
    q_box1 = builder.create_frame(auth_l1, "Quote Box", 48, 300, 504, 200, PALETTE["white"], PALETTE["cherry_blossom"], radius=16)
    builder.create_text(q_box1, "Quote Text", "“Ibu tidak perlu menjadi sempurna untuk menjadi ibu yang luar biasa bagi si kecil. Rawatlah dirimu sebagaimana engkau merawat buah hatimu.”", 32, 36, 440, 90, font_size=14, font_style="Regular", fill_color=PALETTE["text_dark"])
    builder.create_text(q_box1, "Quote Author", "— Komunitas Postpartum Care", 32, 140, 300, 20, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    
    # Left Trust Indicators
    builder.create_text(auth_l1, "Trust 1", "🔒 Data jurnal & mood 100% tersimpan privat", 48, 540, 400, 24, font_size=12, font_style="Medium", fill_color=PALETTE["text_dark"])
    builder.create_text(auth_l1, "Trust 2", "👩‍⚕️ Informasi ditinjau oleh psikolog & bidan bersertifikat", 48, 575, 450, 24, font_size=12, font_style="Medium", fill_color=PALETTE["text_dark"])
    builder.create_text(auth_l1, "Trust 3", "🛡️ Sesuai standar UU Pelindungan Data Pribadi", 48, 610, 400, 24, font_size=12, font_style="Medium", fill_color=PALETTE["text_dark"])

    # Right Login Form Card
    auth_r1 = builder.create_frame(s7, "Login Form Card", 720, 120, 640, 840, PALETTE["white"], PALETTE["border_light"], radius=20)
    builder.create_text(auth_r1, "Form Title", "Masuk ke Akun Anda", 48, 48, 400, 32, font_size=24, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(auth_r1, "Form Sub", "Pilih peran akun dan masukkan kredensial terdaftar.", 48, 86, 450, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Role Selector Tabs
    roles = ["Ibu Pascasalin", "Tenaga Medis", "Admin"]
    rx = 48
    for idx, rname in enumerate(roles):
        is_sel = (idx == 0)
        rbg = PALETTE["blush"] if is_sel else PALETTE["card_bg"]
        rstr = PALETTE["raspberry_rose"] if is_sel else PALETTE["border_light"]
        rtxt = PALETTE["raspberry_rose"] if is_sel else PALETTE["text_dark"]
        rbtn = builder.create_frame(auth_r1, f"Role Tab {idx+1}", rx, 126, 168, 42, rbg, rstr, radius=10)
        builder.create_text(rbtn, "Txt", rname, 24, 12, 120, 18, font_size=12, font_style="Bold" if is_sel else "Regular", fill_color=rtxt)
        rx += 186

    # Email Input
    builder.create_text(auth_r1, "Lbl Email", "Alamat Email", 48, 200, 200, 20, font_size=13, font_style="Bold", fill_color=PALETTE["text_dark"])
    e_box1 = builder.create_frame(auth_r1, "Input Email", 48, 226, 544, 48, PALETTE["white"], PALETTE["border_light"], radius=10)
    builder.create_text(e_box1, "Val", "ibu.rani@example.com", 16, 14, 400, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Password Input
    builder.create_text(auth_r1, "Lbl Pwd", "Kata Sandi", 48, 296, 200, 20, font_size=13, font_style="Bold", fill_color=PALETTE["text_dark"])
    p_box1 = builder.create_frame(auth_r1, "Input Pwd", 48, 322, 544, 48, PALETTE["white"], PALETTE["border_light"], radius=10)
    builder.create_text(p_box1, "Val", "••••••••••••", 16, 14, 300, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Remember Me & Forgot Password
    builder.create_text(auth_r1, "Remember Me", "☑ Ingat saya di perangkat ini", 48, 390, 250, 20, font_size=12, font_style="Regular", fill_color=PALETTE["text_dark"])
    builder.create_text(auth_r1, "Forgot Pwd", "Lupa kata sandi?", 480, 390, 120, 20, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    # Login Button
    btn_login = builder.create_frame(auth_r1, "Btn Login", 48, 436, 544, 52, PALETTE["raspberry_rose"], None, radius=12)
    builder.create_text(btn_login, "Txt", "Masuk ke Akun Sekarang  ➔", 180, 16, 240, 22, font_size=14, font_style="Bold", fill_color=PALETTE["white"])

    # Switch to Register
    builder.create_text(auth_r1, "No Account", "Belum memiliki akun Postpartum Care?", 130, 520, 260, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])
    builder.create_text(auth_r1, "Link Register", "Daftar di Sini", 395, 520, 120, 20, font_size=13, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    # Quick Demo Login Box
    demo_box = builder.create_frame(auth_r1, "Demo Box", 48, 590, 544, 180, PALETTE["champagne"], PALETTE["sunset"], radius=14)
    builder.create_text(demo_box, "Demo Title", "⚡ Akses Demo Cepat (Pengujian Sistem / UAS)", 24, 20, 450, 20, font_size=13, font_style="Bold", fill_color=PALETTE["text_dark"])
    
    # 3 Demo Chips
    d1 = builder.create_frame(demo_box, "Demo Ibu", 24, 54, 496, 36, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(d1, "Txt", "👩‍🍼 Masuk sebagai Ibu Rani (Hari ke-12 Pascasalin)", 16, 9, 450, 18, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    
    d2 = builder.create_frame(demo_box, "Demo Pro", 24, 96, 496, 36, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(d2, "Txt", "👩‍⚕️ Masuk sebagai Rina Kusuma, M.Psi. (Tenaga Profesional)", 16, 9, 450, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
    
    d3 = builder.create_frame(demo_box, "Demo Admin", 24, 138, 496, 36, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(d3, "Txt", "⚙️ Masuk sebagai Admin Sistem (Pengelola Konten)", 16, 9, 450, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])


    # -------------------------------------------------------------
    # SCREEN 8: HALAMAN DAFTAR (SIGN IN / REGISTER) (x: 11200, y: 0, w: 1440, h: 1024)
    # -------------------------------------------------------------
    s8 = builder.create_frame(page, "Screen 8 — Halaman Daftar (Sign In / Register)", 11200, 0, 1440, 1024, PALETTE["champagne"], PALETTE["border_light"], radius=0)
    
    # Top Minimal Header for Auth
    nav_auth_2 = builder.create_frame(s8, "Top Auth Header", 0, 0, 1440, 80, PALETTE["white"], PALETTE["border_light"], radius=0)
    builder.create_text(nav_auth_2, "Logo", "🌸 PostpartumCare", 60, 26, 260, 30, font_size=20, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(nav_auth_2, "Back Home", "← Kembali ke Beranda", 1220, 30, 160, 20, font_size=13, font_style="Bold", fill_color=PALETTE["text_muted"])

    # Left Branding Card
    auth_l2 = builder.create_frame(s8, "Register Left Card", 80, 110, 560, 860, PALETTE["blush"], PALETTE["border_light"], radius=20)
    builder.create_text(auth_l2, "Badge", "🌸 Bergabung Bersama Kami", 40, 40, 300, 24, font_size=13, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(auth_l2, "Heading", "Mulai Perjalanan\nKesejahteraan Anda.", 40, 80, 480, 70, font_size=28, font_style="Bold", fill_color=PALETTE["text_dark"])
    builder.create_text(auth_l2, "Desc", "Dapatkan ruang aman untuk mencatat suasana hati harian, jurnal refleksi pribadi, relaksasi napas 3 menit, dan pendampingan terpercaya.", 40, 165, 480, 60, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Feature List
    reg_features = [
        ("✨ Mood Check-In Harian", "Kenali ritme emosi dan faktor pemicu kelelahan harian."),
        ("📖 Daily Journal Terenkripsi", "Ruang aman tanpa takut dihakimi dengan tag perasaan."),
        ("🎧 Micro-Relaxation 3 Menit", "Latihan relaksasi praktis di sela menyusui dan merawat bayi."),
        ("👩‍⚕️ Konsultasi Tenaga Terpercaya", "Kemudahan akses ke psikolog perinatal dan bidan konselor laktasi.")
    ]
    for idx, (ftitle, fdesc) in enumerate(reg_features):
        fy = 250 + idx * 85
        f_card = builder.create_frame(auth_l2, f"Feature Card {idx+1}", 40, fy, 480, 72, PALETTE["white"], PALETTE["border_light"], radius=12)
        builder.create_text(f_card, "Title", ftitle, 20, 14, 400, 18, font_size=13, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
        builder.create_text(f_card, "Desc", fdesc, 20, 38, 440, 18, font_size=11, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Right Registration Form Card
    auth_r2 = builder.create_frame(s8, "Register Form Card", 680, 110, 680, 860, PALETTE["white"], PALETTE["border_light"], radius=20)
    builder.create_text(auth_r2, "Form Title", "Buat Akun Postpartum Care", 48, 36, 450, 30, font_size=22, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    builder.create_text(auth_r2, "Form Sub", "Lengkapi formulir di bawah untuk memulai pendampingan digital.", 48, 70, 500, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])

    # Role Selector (Ibu / Tenaga Profesional)
    builder.create_text(auth_r2, "Role Lbl", "Pilih Peran Pengguna:", 48, 105, 200, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
    r_tab1 = builder.create_frame(auth_r2, "Role Ibu", 48, 130, 280, 40, PALETTE["blush"], PALETTE["raspberry_rose"], radius=10)
    builder.create_text(r_tab1, "Txt", "👩‍🍼 Ibu Pascasalin (Utama)", 40, 10, 200, 18, font_size=12, font_style="Bold", fill_color=PALETTE["raspberry_rose"])
    
    r_tab2 = builder.create_frame(auth_r2, "Role Pro", 350, 130, 280, 40, PALETTE["card_bg"], PALETTE["border_light"], radius=10)
    builder.create_text(r_tab2, "Txt", "👩‍⚕️ Tenaga Profesional / Konselor", 30, 10, 230, 18, font_size=12, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Nama Lengkap
    builder.create_text(auth_r2, "Lbl Nama", "Nama Lengkap", 48, 185, 200, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
    n_box2 = builder.create_frame(auth_r2, "Input Nama", 48, 208, 584, 44, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(n_box2, "Val", "Rani Anindita", 16, 12, 300, 18, font_size=13, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Email
    builder.create_text(auth_r2, "Lbl Email", "Alamat Email", 48, 265, 200, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
    e_box2 = builder.create_frame(auth_r2, "Input Email", 48, 288, 584, 44, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(e_box2, "Val", "rani.anindita@email.com", 16, 12, 300, 18, font_size=13, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Tanggal Persalinan (Crucial field from Report Table 3.8!)
    builder.create_text(auth_r2, "Lbl Tgl", "Tanggal Persalinan / Perkiraan Lahir (Khusus Ibu)", 48, 345, 450, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
    t_box2 = builder.create_frame(auth_r2, "Input Tgl", 48, 368, 584, 44, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(t_box2, "Val", "📅  30 Oktober 2026 (Digunakan untuk menentukan fase pemulihan harian)", 16, 12, 550, 18, font_size=12, font_style="Regular", fill_color=PALETTE["raspberry_rose"])

    # Kata Sandi & Konfirmasi Sandi
    builder.create_text(auth_r2, "Lbl Pwd", "Kata Sandi", 48, 425, 200, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
    p_box2 = builder.create_frame(auth_r2, "Input Pwd", 48, 448, 280, 44, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(p_box2, "Val", "••••••••••••", 16, 12, 200, 18, font_size=13, font_style="Regular", fill_color=PALETTE["text_dark"])

    builder.create_text(auth_r2, "Lbl Conf Pwd", "Konfirmasi Kata Sandi", 352, 425, 200, 18, font_size=12, font_style="Bold", fill_color=PALETTE["text_dark"])
    cp_box2 = builder.create_frame(auth_r2, "Input Conf Pwd", 352, 448, 280, 44, PALETTE["white"], PALETTE["border_light"], radius=8)
    builder.create_text(cp_box2, "Val", "••••••••••••", 16, 12, 200, 18, font_size=13, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Checkbox Privacy
    builder.create_text(auth_r2, "Privacy Agreement", "☑ Saya menyetujui Ketentuan Layanan & Kebijakan Privasi Perlindungan Data Pribadi", 48, 515, 580, 20, font_size=11, font_style="Regular", fill_color=PALETTE["text_dark"])

    # Register Button
    btn_reg = builder.create_frame(auth_r2, "Btn Register", 48, 555, 584, 50, PALETTE["raspberry_rose"], None, radius=12)
    builder.create_text(btn_reg, "Txt", "Daftar Akun Baru Sekarang  ➔", 185, 15, 260, 22, font_size=14, font_style="Bold", fill_color=PALETTE["white"])

    # Switch to Login
    builder.create_text(auth_r2, "Have Account", "Sudah memiliki akun Postpartum Care?", 170, 630, 260, 20, font_size=13, font_style="Regular", fill_color=PALETTE["text_muted"])
    builder.create_text(auth_r2, "Link Login", "Masuk di Sini", 420, 630, 120, 20, font_size=13, font_style="Bold", fill_color=PALETTE["raspberry_rose"])

    output_path = "postpartum-care.figcraft"
    builder.save(output_path)
    return output_path

if __name__ == "__main__":
    build_postpartum_figcraft()
