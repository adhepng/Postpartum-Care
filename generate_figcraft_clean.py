import json
import zipfile

PALETTE = {
    "champagne": "#FBF4EB",
    "blush": "#FBD9E5",
    "cherry": "#F7C5D7",
    "tickle": "#F283AF",
    "rose": "#C43670",
    "sunset": "#F3CC97",
    "white": "#FFFFFF",
    "card": "#FFFBF9",
    "dark": "#2E2228",
    "muted": "#7A6670",
    "border": "#ECD7DE",
    "soft": "#F7E5ED",
}


def color(hex_value, alpha=1.0):
    value = hex_value.lstrip("#")
    return {
        "r": int(value[0:2], 16) / 255.0,
        "g": int(value[2:4], 16) / 255.0,
        "b": int(value[4:6], 16) / 255.0,
        "a": float(alpha),
    }


def paint(hex_value, alpha=1.0):
    return [{
        "type": "solid",
        "color": color(hex_value, alpha),
        "opacity": 1.0,
        "visible": True,
        "blend": "normal",
    }]


def shadow(alpha=0.10, offset=10.0, radius=30.0):
    return [{
        "type": "dropShadow",
        "color": color("#C43670", alpha),
        "offset": [0.0, float(offset)],
        "radius": float(radius),
        "spread": 0.0,
        "blend": "normal",
        "show_behind": False,
        "visible": True,
    }]


class Builder:
    def __init__(self, name):
        self.name = name
        self.next_id = 1
        self.nodes = {}
        self.page_id = self.alloc()
        self.nodes[str(self.page_id)] = {
            "id": self.page_id,
            "name": "Postpartum Care",
            "type": "page",
            "background": color(PALETTE["champagne"]),
            "flows": [],
            "prototype": {
                "device": "None",
                "background": color(PALETTE["champagne"]),
                "rotation": "portrait",
            },
            "guides": [],
            "children": [],
            "width": 0.0,
            "height": 0.0,
        }

    def alloc(self):
        value = self.next_id
        self.next_id += 1
        return value

    def add(self, parent, node):
        self.nodes[str(node["id"])] = node
        if parent is not None and str(parent) in self.nodes:
            self.nodes[str(parent)]["children"].append(node["id"])
        return node["id"]

    def frame(self, parent, name, x, y, w, h, fill=None, stroke=None, radius=0.0,
              clip=True, shadow_alpha=None, shadow_offset=10.0, shadow_radius=30.0):
        node = {
            "id": self.alloc(),
            "name": name,
            "type": "frame",
            "parent": parent,
            "children": [],
            "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
            "width": float(w),
            "height": float(h),
            "clip": clip,
            "fills": paint(fill) if fill else [],
            "strokes": paint(stroke) if stroke else [],
            "corners": {
                "radii": [float(radius)] * 4,
                "smoothing": 0.0,
            },
        }
        if shadow_alpha is not None:
            node["effects"] = shadow(shadow_alpha, shadow_offset, shadow_radius)
        return self.add(parent, node)

    def rect(self, parent, name, x, y, w, h, fill=None, radius=0.0):
        node = {
            "id": self.alloc(),
            "name": name,
            "type": "rectangle",
            "parent": parent,
            "children": [],
            "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
            "width": float(w),
            "height": float(h),
            "fills": paint(fill) if fill else [],
            "strokes": [],
            "corners": {
                "radii": [float(radius)] * 4,
                "smoothing": 0.0,
            },
        }
        return self.add(parent, node)

    def text(self, parent, name, value, x, y, w, h, size=14.0, weight="Regular",
             fill=None, align="left", line_height=140.0, letter_spacing=0.0):
        node = {
            "id": self.alloc(),
            "name": name,
            "type": "text",
            "characters": value,
            "auto_resize": "height",
            "style": {
                "font_family": "Poppins",
                "font_style": weight,
                "font_size": float(size),
                "line_height": {"unit": "percent", "value": float(line_height)},
                "letter_spacing": {"unit": "percent", "value": float(letter_spacing)},
                "decoration": "none",
                "case": "original",
                "fills": None,
                "link": None,
            },
            "parent": parent,
            "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
            "width": float(w),
            "height": float(h),
            "fills": paint(fill or PALETTE["dark"]),
            "child_layout": {
                "sizing_h": "hug",
                "sizing_v": "hug",
                "absolute": False,
                "min_w": None,
                "max_w": None,
                "min_h": None,
                "max_h": None,
                "grid_column": None,
                "grid_row": None,
                "grid_column_span": 0,
                "grid_row_span": 0,
            },
        }
        if align != "left":
            node["align_h"] = align
        return self.add(parent, node)

    def button(self, parent, name, label, x, y, w, h, fill=None, text_fill=None,
               stroke=None, size=14.0, weight="SemiBold", radius=None,
               shadow_alpha=None):
        radius = h / 2.0 if radius is None else radius
        box = self.frame(parent, name, x, y, w, h, fill, stroke, radius,
                         shadow_alpha=shadow_alpha)
        self.text(box, "Label", label, 0, (h - size * 1.35) / 2.0, w, size * 1.6,
                  size=size, weight=weight, fill=text_fill or PALETTE["white"],
                  align="center")
        return box

    def pill(self, parent, name, label, x, y, w, h, fill=None, text_fill=None,
             stroke=None, size=12.0, weight="SemiBold"):
        return self.button(parent, name, label, x, y, w, h, fill, text_fill,
                           stroke, size, weight, radius=h / 2.0)

    def circle(self, parent, name, x, y, size, fill, label=None, label_fill=None,
               label_size=14.0, weight="Bold", stroke=None, shadow_alpha=None):
        box = self.frame(parent, name, x, y, size, size, fill, stroke, size / 2.0,
                         shadow_alpha=shadow_alpha)
        if label:
            self.text(box, "Initials", label, 0, (size - label_size * 1.3) / 2.0,
                      size, label_size * 1.6, size=label_size, weight=weight,
                      fill=label_fill or PALETTE["rose"], align="center")
        return box

    def line(self, parent, name, x, y, w, fill=None, h=1.0):
        return self.rect(parent, name, x, y, w, h, fill or PALETTE["border"])

    def save(self, path):
        doc = {
            "format": "figcraft",
            "version": 1,
            "imageIndex": [],
            "name": self.name,
            "pages": [self.page_id],
            "current_page": self.page_id,
            "next_id": self.next_id,
            "styles": [],
            "variables": {"collections": [], "variables": []},
            "document_colors": [],
            "comments": [],
            "nodes": self.nodes,
        }
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("document.json", json.dumps(doc, indent=2))
        print("Saved %s with %d nodes" % (path, len(self.nodes)))


def logo(builder, parent, x=0, y=0, compact=False):
    tile = builder.frame(parent, "Logo Tile", x, y, 38, 38, PALETTE["blush"],
                         PALETTE["border"], 11)
    builder.text(tile, "Logo Mark", "P", 0, 3, 38, 30, size=20, weight="Bold",
                 fill=PALETTE["rose"], align="center")
    builder.text(parent, "Brand", "PostpartumCare", x + 50, y - 1, 210, 24,
                 size=18 if not compact else 16, weight="Bold",
                 fill=PALETTE["rose"], letter_spacing=-2.0)
    builder.text(parent, "Brand Sub", "Pendamping Ibu Pascapersalinan",
                 x + 50, y + 22, 240, 16, size=10, weight="Medium",
                 fill=PALETTE["muted"])


def landing_nav(builder, page):
    nav = builder.frame(page, "Landing Nav", 0, 0, 1440, 80, PALETTE["white"],
                        PALETTE["border"], 0)
    logo(builder, nav, 80, 21)
    links = [("Fitur", 760), ("Cara Kerja", 842), ("Profesional", 948),
             ("Cerita Ibu", 1070)]
    for label, lx in links:
        builder.text(nav, "Nav " + label, label, lx, 32, 100, 20, size=13,
                     weight="Medium", fill=PALETTE["dark"])
    builder.button(nav, "Nav Login", "Masuk", 1188, 22, 90, 38,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 13,
                   radius=19)
    builder.button(nav, "Nav Register", "Mulai Gratis", 1290, 22, 120, 38,
                   PALETTE["rose"], PALETTE["white"], None, 13, radius=19,
                   shadow_alpha=0.12)


def app_header(builder, screen, active="Beranda", profile_active=False):
    header = builder.frame(screen, "App Header", 0, 0, 1440, 80,
                           PALETTE["white"], PALETTE["border"], 0)
    logo(builder, header, 32, 21, compact=True)
    items = [("Beranda", 92), ("Mood Check-In", 112), ("Daily Journal", 110),
             ("Micro-Relaxation", 132), ("Edukasi", 82), ("Bantuan Profesional", 152)]
    x = 300
    for label, width in items:
        if label == active:
            builder.button(header, "Nav Active", label, x, 24, width, 34,
                           PALETTE["blush"], PALETTE["rose"], None, 11.5,
                           radius=17)
        else:
            builder.text(header, "Nav " + label, label, x, 31, width, 20,
                         size=11.5, weight="Medium", fill=PALETTE["muted"])
        x += width + 8
    chip = builder.frame(header, "User Chip", 1084, 18, 190, 44,
                         PALETTE["blush"] if profile_active else PALETTE["card"],
                         PALETTE["rose"] if profile_active else PALETTE["border"], 22)
    builder.circle(chip, "Avatar", 6, 6, 32, PALETTE["rose"], "R",
                   PALETTE["white"], 13)
    builder.text(chip, "User Name", "Ibu Rani", 46, 13, 130, 20, size=12,
                 weight="SemiBold",
                 fill=PALETTE["rose"] if profile_active else PALETTE["dark"])
    builder.text(chip, "User Role", "Ibu Pascasalin", 46, 29, 130, 15, size=9,
                 weight="Medium", fill=PALETTE["muted"])
    builder.button(header, "Logout", "Keluar", 1288, 22, 120, 38,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 12,
                   radius=19)


def screen_title(builder, screen, title, subtitle, y=115, action=None,
                 action_label=None):
    builder.text(screen, "Page Title", title, 80, y, 700, 48, size=32,
                 weight="Bold", fill=PALETTE["dark"], letter_spacing=-2.0)
    builder.text(screen, "Page Subtitle", subtitle, 80, y + 48, 820, 26,
                 size=13, weight="Regular", fill=PALETTE["muted"])
    if action and action_label:
        builder.button(screen, "Page Action", action_label, 1150, y + 4, 210,
                       46, PALETTE["rose"], PALETTE["white"], None, 13,
                       shadow_alpha=0.14)


def section_heading(builder, parent, kicker, title, subtitle, y=0, center=False):
    width = 1060
    x = 110 if center else 0
    builder.text(parent, "Kicker", kicker, x, y, width, 20, size=12,
                 weight="SemiBold", fill=PALETTE["rose"], align="center" if center else "left",
                 letter_spacing=8.0)
    builder.text(parent, "Heading", title, x, y + 28, width, 86, size=34,
                 weight="Bold", fill=PALETTE["dark"],
                 align="center" if center else "left", letter_spacing=-2.0)
    builder.text(parent, "Sub", subtitle, x, y + 120, width, 48, size=14,
                 weight="Regular", fill=PALETTE["muted"],
                 align="center" if center else "left", line_height=150.0)


def landing_page(builder, page):
    frame = builder.frame(page, "01 - Landing Page", 0, 0, 1440, 3940,
                          PALETTE["champagne"], None, 0, clip=True)
    landing_nav(builder, frame)

    hero = builder.frame(frame, "Hero", 0, 80, 1440, 780, None, None, 0,
                         clip=True)
    builder.circle(hero, "Hero Orb One", 1110, 20, 300, PALETTE["cherry"],
                   None, None, 0, stroke=None)
    builder.circle(hero, "Hero Orb Two", 660, 560, 160, PALETTE["sunset"],
                   None, None, 0, stroke=None)
    builder.pill(hero, "Hero Eyebrow", "RUANG AMAN UNTUK IBU BARU", 80, 92, 230,
                 32, PALETTE["white"], PALETTE["rose"], PALETTE["border"], 10.5)
    builder.text(hero, "Hero Title", "Rawat diri,\ntumbuh bersama si kecil.",
                 80, 148, 700, 150, size=50, weight="Bold",
                 fill=PALETTE["dark"], line_height=112.0, letter_spacing=-3.0)
    builder.text(hero, "Hero Body",
                 "Pendamping harian untuk memahami suasana hati, menulis jurnal,\n"
                 "menemukan jeda relaksasi, dan terhubung dengan tenaga profesional\n"
                 "yang tepat. Semua dalam satu ruang yang hangat dan privat.",
                 80, 332, 620, 96, size=15, weight="Regular",
                 fill=PALETTE["muted"], line_height=165.0)
    builder.button(hero, "Hero Primary", "Mulai Perjalanan", 80, 458, 210, 52,
                   PALETTE["rose"], PALETTE["white"], None, 14, radius=26,
                   shadow_alpha=0.18)
    builder.button(hero, "Hero Secondary", "Masuk ke Akun", 306, 458, 180, 52,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 14,
                   radius=26)
    avatars = [("RA", 80, PALETTE["rose"]), ("NS", 108, PALETTE["tickle"]),
               ("DP", 136, PALETTE["sunset"]), ("+2k", 164, PALETTE["dark"])]
    for label, ax, bg in avatars:
        builder.circle(hero, "Trust Avatar", ax, 546, 38, bg, label,
                       PALETTE["white"], 10, weight="Bold",
                       stroke=PALETTE["white"])
    builder.text(hero, "Trust Copy", "2.400+ ibu sudah menemukan ruang aman mereka di sini.",
                 214, 555, 430, 22, size=12, weight="Medium",
                 fill=PALETTE["muted"])
    builder.text(hero, "Safe Note",
                 "Privat, aman, dan bukan pengganti konsultasi medis profesional.",
                 80, 626, 560, 22, size=11.5, weight="Medium",
                 fill=PALETTE["muted"])

    visual = builder.frame(hero, "Hero Visual", 760, 118, 610, 610, None, None,
                           0, clip=False)
    builder.circle(visual, "Visual Orb", 430, -10, 210, PALETTE["blush"])
    main_card = builder.frame(visual, "Mood Mock", 34, 46, 520, 420,
                              PALETTE["white"], PALETTE["border"], 28,
                              shadow_alpha=0.16, shadow_radius=42)
    builder.text(main_card, "Mock Eyebrow", "MOOD CHECK-IN", 32, 28, 250, 18,
                 size=10.5, weight="SemiBold", fill=PALETTE["rose"],
                 letter_spacing=8.0)
    builder.text(main_card, "Mock Title", "Bagaimana perasaanmu hari ini, Ibu?",
                 32, 52, 400, 34, size=21, weight="Bold",
                 fill=PALETTE["dark"], line_height=125.0)
    builder.circle(main_card, "Mock Dot", 466, 30, 20, PALETTE["tickle"])
    moods = [("Tenang", 32, 110), ("Lelah", 134, 110), ("Cemas", 232, 110),
             ("Sedih", 330, 110)]
    for label, mx, my in moods:
        active = label == "Lelah"
        builder.pill(main_card, "Mood " + label, label, mx, my, 86, 34,
                     PALETTE["blush"] if active else PALETTE["card"],
                     PALETTE["rose"] if active else PALETTE["muted"],
                     PALETTE["border"], 11)
    chart = builder.frame(main_card, "Mood Chart", 32, 172, 456, 142, None, None,
                          0, clip=False)
    values = [46, 70, 52, 92, 64, 78, 58]
    for index, value in enumerate(values):
        bar_height = value * 1.2
        bx = index * 64
        builder.rect(chart, "Bar", bx, 130 - bar_height, 34, bar_height,
                     PALETTE["rose"] if index == 3 else PALETTE["cherry"],
                     radius=17)
    builder.text(main_card, "Chart Label", "Ritme emosi 7 hari", 32, 332, 200, 20,
                 size=11, weight="Medium", fill=PALETTE["muted"])
    builder.text(main_card, "Chart Value", "+14% lebih stabil", 332, 332, 156, 20,
                 size=11, weight="SemiBold", fill=PALETTE["rose"],
                 align="right")
    builder.line(main_card, "Mock Divider", 32, 310, 456)

    journal = builder.frame(visual, "Journal Mock", -52, 392, 360, 166,
                            PALETTE["white"], PALETTE["border"], 22,
                            shadow_alpha=0.14, shadow_radius=34)
    builder.text(journal, "Label", "DAILY JOURNAL", 24, 20, 240, 18, size=9.5,
                 weight="SemiBold", fill=PALETTE["rose"], letter_spacing=7.0)
    builder.text(journal, "Quote",
                 "\"Hari ini terasa panjang, tapi aku bangga\nsudah memberi jeda untuk diriku.\"",
                 24, 44, 304, 62, size=12, weight="Regular",
                 fill=PALETTE["dark"], line_height=150.0)
    builder.pill(journal, "Tag 1", "#lelah", 24, 116, 66, 24,
                 PALETTE["soft"], PALETTE["rose"], None, 9.5)
    builder.pill(journal, "Tag 2", "#bersyukur", 98, 116, 92, 24,
                 PALETTE["soft"], PALETTE["rose"], None, 9.5)

    relax = builder.frame(visual, "Relax Mock", 350, 476, 290, 112,
                          PALETTE["white"], PALETTE["border"], 20,
                          shadow_alpha=0.14, shadow_radius=34)
    builder.circle(relax, "Relax Icon", 18, 22, 44, PALETTE["blush"], "3",
                   PALETTE["rose"], 16)
    builder.text(relax, "Relax Title", "Pernapasan Tenang", 76, 26, 170, 22,
                 size=12.5, weight="SemiBold", fill=PALETTE["dark"])
    builder.text(relax, "Relax Sub", "03:00 menit", 76, 48, 120, 18, size=10,
                 weight="Medium", fill=PALETTE["muted"])
    builder.button(relax, "Play", "Mulai", 196, 66, 76, 28,
                   PALETTE["rose"], PALETTE["white"], None, 9.5, radius=14)

    proof = builder.frame(frame, "Proof Strip", 80, 860, 1280, 82,
                          PALETTE["white"], PALETTE["border"], 22,
                          shadow_alpha=0.06, shadow_radius=22)
    builder.text(proof, "Proof Label", "Dirancang bersama", 36, 30, 200, 22,
                 size=11, weight="Medium", fill=PALETTE["muted"])
    builder.text(proof, "Proof One", "Psikolog klinis perinatal", 260, 29, 250, 24,
                 size=12.5, weight="SemiBold", fill=PALETTE["dark"])
    builder.circle(proof, "Dot One", 540, 36, 8, PALETTE["tickle"])
    builder.text(proof, "Proof Two", "Bidan konselor laktasi", 575, 29, 250, 24,
                 size=12.5, weight="SemiBold", fill=PALETTE["dark"])
    builder.circle(proof, "Dot Two", 838, 36, 8, PALETTE["sunset"])
    builder.text(proof, "Proof Three", "Dokter spesialis obstetri", 873, 29, 260, 24,
                 size=12.5, weight="SemiBold", fill=PALETTE["dark"])

    features = builder.frame(frame, "Features", 0, 960, 1440, 900, None, None, 0)
    section_heading(builder, features, "SATU RUANG, BANYAK BENTUK DUKUNGAN",
                    "Pendampingan yang mengikuti ritme harimu.",
                    "Fitur sederhana yang dirancang untuk ibu baru: tidak menambah beban,\njustru membantu menemukan jeda.",
                    40, center=True)
    cards = [
        ("01", "Mood Check-In", "Kenali ritme emosi dan pemicunya lewat pencatatan singkat yang mudah diisi kapan saja.", "Coba mood check-in"),
        ("02", "Daily Journal", "Ruang privat untuk menuangkan cerita, rasa syukur, dan hal-hal yang sedang membebani pikiran.", "Mulai menulis"),
        ("03", "Micro-Relaxation", "Latihan pernapasan tiga menit untuk meredakan tegang bahu dan menenangkan pikiran yang penuh.", "Cari jeda sejenak"),
        ("04", "Edukasi Terpercaya", "Artikel pemulihan fisik dan kesehatan mental yang ditinjau tenaga medis, sesuai fase nifas.", "Baca panduan"),
        ("05", "Profesional Access", "Lihat profil, jadwal, dan ajukan sesi bersama psikolog, bidan, atau dokter terverifikasi.", "Lihat direktori"),
        ("06", "Profil & Privasi", "Atur informasi akun dan preferensi pendampingan. Catatan pribadi tetap tersimpan untukmu.", "Kelola profil"),
    ]
    for index, (number, title, body, link) in enumerate(cards):
        col = index % 3
        row = index // 3
        cx = 80 + col * 430
        cy = 260 + row * 310
        card = builder.frame(features, "Feature " + number, cx, cy, 400, 280,
                             PALETTE["white"], PALETTE["border"], 22,
                             shadow_alpha=0.07, shadow_radius=28)
        icon = builder.frame(card, "Icon", 26, 26, 48, 48, PALETTE["blush"],
                             None, 14)
        builder.text(icon, "Number", number, 0, 12, 48, 24, size=13,
                     weight="Bold", fill=PALETTE["rose"], align="center")
        builder.text(card, "Title", title, 26, 96, 340, 28, size=17,
                     weight="Bold", fill=PALETTE["dark"])
        builder.text(card, "Body", body, 26, 132, 344, 72, size=12,
                     weight="Regular", fill=PALETTE["muted"], line_height=160.0)
        builder.text(card, "Link", link + "  >", 26, 224, 260, 20, size=11.5,
                     weight="SemiBold", fill=PALETTE["rose"])

    how = builder.frame(frame, "How It Works", 0, 1860, 1440, 540, None, None, 0)
    section_heading(builder, how, "CARA KERJA", "Tiga langkah kecil, ruang yang terasa aman.",
                    "Mulai dari hal sederhana. Tidak perlu sempurna untuk merawat diri.",
                    35, center=True)
    builder.line(how, "Step Line", 150, 300, 1140)
    steps = [
        ("01", "Kenali dirimu", "Isi mood check-in singkat dan catat apa yang sedang terasa berat."),
        ("02", "Beri jeda", "Pilih latihan relaksasi tiga menit atau tulis jurnal tanpa penghakiman."),
        ("03", "Dapatkan dukungan", "Terhubung dengan tenaga profesional saat kamu membutuhkannya."),
    ]
    for index, (number, title, body) in enumerate(steps):
        sx = 150 + index * 400
        builder.circle(how, "Step Dot", sx + 140, 278, 44, PALETTE["rose"],
                       number, PALETTE["white"], 13)
        card = builder.frame(how, "Step Card " + number, sx, 355, 360, 140,
                             PALETTE["white"], PALETTE["border"], 20,
                             shadow_alpha=0.06, shadow_radius=24)
        builder.text(card, "Title", title, 24, 24, 310, 26, size=16,
                     weight="Bold", fill=PALETTE["dark"], align="center")
        builder.text(card, "Body", body, 24, 60, 312, 58, size=11.5,
                     weight="Regular", fill=PALETTE["muted"], align="center",
                     line_height=155.0)

    professional = builder.frame(frame, "Professional", 0, 2400, 1440, 430,
                                 None, None, 0)
    band = builder.frame(professional, "Professional Band", 80, 40, 1280, 330,
                         PALETTE["blush"], PALETTE["border"], 30)
    builder.pill(band, "Badge", "PENDUKUNG TERVERIFIKASI", 56, 48, 210, 30,
                 PALETTE["white"], PALETTE["rose"], None, 10)
    builder.text(band, "Title", "Tidak harus menjalani semuanya sendiri.",
                 56, 96, 550, 82, size=32, weight="Bold",
                 fill=PALETTE["dark"], line_height=118.0, letter_spacing=-2.0)
    builder.text(band, "Body",
                 "Bicara dengan psikolog perinatal, bidan konselor laktasi,\n"
                 "atau dokter spesialis obstetri yang siap mendengarkan.",
                 56, 184, 560, 60, size=13, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    builder.button(band, "CTA", "Jelajahi Direktori", 56, 252, 190, 46,
                   PALETTE["rose"], PALETTE["white"], None, 12.5, radius=23,
                   shadow_alpha=0.15)
    pro = builder.frame(band, "Professional Card", 750, 38, 470, 250,
                        PALETTE["white"], PALETTE["border"], 22,
                        shadow_alpha=0.12, shadow_radius=30)
    builder.circle(pro, "Pro Avatar", 28, 28, 56, PALETTE["rose"], "RK",
                   PALETTE["white"], 16)
    builder.text(pro, "Pro Name", "Rina Kusuma, M.Psi.", 100, 30, 320, 24,
                 size=14, weight="Bold", fill=PALETTE["dark"])
    builder.text(pro, "Pro Role", "Psikolog Klinis Perinatal", 100, 54, 280, 20,
                 size=11, weight="Medium", fill=PALETTE["muted"])
    builder.text(pro, "Pro Rating", "5.0  |  12 tahun pengalaman", 100, 78, 300, 18,
                 size=10.5, weight="SemiBold", fill=PALETTE["rose"])
    builder.pill(pro, "Tag One", "Kecemasan nifas", 28, 112, 138, 28,
                 PALETTE["soft"], PALETTE["rose"], None, 9.5)
    builder.pill(pro, "Tag Two", "Tidur & lelah", 174, 112, 116, 28,
                 PALETTE["soft"], PALETTE["rose"], None, 9.5)
    builder.text(pro, "Pro Schedule", "Jadwal tersedia minggu ini", 28, 158, 240, 20,
                 size=10.5, weight="Medium", fill=PALETTE["muted"])
    builder.button(pro, "Pro CTA", "Lihat Jadwal", 28, 190, 150, 38,
                   PALETTE["rose"], PALETTE["white"], None, 11.5, radius=19)

    testimonial = builder.frame(frame, "Testimonials", 0, 2830, 1440, 540,
                                None, None, 0)
    section_heading(builder, testimonial, "CERITA IBU",
                    "Ruang kecil yang membuat hari terasa lebih ringan.",
                    "Cerita nyata dari ibu yang menemukan jeda dan dukungan di sini.",
                    35, center=True)
    stories = [
        ("RA", "Rani, 29", "Ibu baru", "\"Awalnya saya merasa sendirian. Mood check-in membantu saya melihat pola dan berani mencari bantuan.\""),
        ("NS", "Nadia, 32", "Ibu dua anak", "\"Jurnal tiga menit setiap malam jadi ritual kecil yang saya tunggu. Rasanya seperti punya ruang untuk diri sendiri.\""),
        ("DP", "Dewi, 27", "Ibu menyusui", "\"Sesi dengan bidan konselor membuat saya jauh lebih tenang. Saya tidak merasa dihakimi sama sekali.\""),
    ]
    for index, (initials, name, role, quote) in enumerate(stories):
        tx = 80 + index * 430
        card = builder.frame(testimonial, "Story " + initials, tx, 185, 400, 280,
                             PALETTE["white"], PALETTE["border"], 22,
                             shadow_alpha=0.07, shadow_radius=28)
        builder.text(card, "Stars", "5.0", 26, 24, 100, 24, size=13,
                     weight="Bold", fill=PALETTE["rose"])
        builder.text(card, "Quote", quote, 26, 58, 344, 120, size=12,
                     weight="Regular", fill=PALETTE["dark"], line_height=160.0)
        builder.circle(card, "Avatar", 26, 204, 40, PALETTE["blush"], initials,
                       PALETTE["rose"], 11)
        builder.text(card, "Name", name, 78, 206, 180, 20, size=11.5,
                     weight="SemiBold", fill=PALETTE["dark"])
        builder.text(card, "Role", role, 78, 224, 180, 18, size=9.5,
                     weight="Medium", fill=PALETTE["muted"])

    cta = builder.frame(frame, "CTA", 0, 3370, 1440, 330, None, None, 0)
    band = builder.frame(cta, "CTA Band", 80, 40, 1280, 250, PALETTE["rose"],
                         None, 30)
    builder.circle(band, "CTA Orb One", 1030, -80, 260, PALETTE["tickle"],
                   None, None, 0, stroke=None)
    builder.circle(band, "CTA Orb Two", 1160, 120, 180, PALETTE["sunset"],
                   None, None, 0, stroke=None)
    builder.text(band, "CTA Title", "Mulai dengan satu napas hari ini.",
                 56, 54, 700, 56, size=32, weight="Bold", fill=PALETTE["white"],
                 letter_spacing=-2.0)
    builder.text(band, "CTA Body",
                 "Gratis untuk memulai. Ruang privat, tenang, dan selalu ada untukmu.",
                 56, 120, 650, 26, size=13, weight="Regular",
                 fill=PALETTE["blush"])
    builder.button(band, "CTA Primary", "Mulai Gratis", 56, 168, 180, 48,
                   PALETTE["white"], PALETTE["rose"], None, 13, radius=24)
    builder.button(band, "CTA Secondary", "Masuk", 250, 168, 120, 48,
                   PALETTE["rose"], PALETTE["white"], PALETTE["white"], 13,
                   radius=24)

    footer = builder.frame(frame, "Footer", 0, 3700, 1440, 240,
                           PALETTE["white"], PALETTE["border"], 0)
    logo(builder, footer, 80, 50)
    builder.text(footer, "Footer Copy",
                 "Pendamping emosional harian untuk ibu pascapersalinan.\n"
                 "Bukan pengganti diagnosis atau perawatan medis profesional.",
                 80, 118, 360, 52, size=11, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    columns = [("Produk", ["Fitur", "Cara Kerja", "Profesional"]),
               ("Dukungan", ["Pusat Bantuan", "Privasi", "Ketentuan"]),
               ("Tentang", ["Tentang Kami", "Kontak", "Blog"])]
    for index, (title, links) in enumerate(columns):
        fx = 620 + index * 220
        builder.text(footer, "Footer Title " + title, title, fx, 50, 160, 20,
                     size=12, weight="SemiBold", fill=PALETTE["dark"])
        for row, link in enumerate(links):
            builder.text(footer, "Footer Link " + link, link, fx, 82 + row * 26,
                         180, 20, size=10.5, weight="Regular",
                         fill=PALETTE["muted"])
    builder.line(footer, "Footer Line", 80, 190, 1280)
    builder.text(footer, "Copyright", "2026 Postpartum Care. Dibuat dengan hangat untuk ibu baru.",
                 80, 206, 600, 20, size=10, weight="Medium",
                 fill=PALETTE["muted"])
    builder.text(footer, "Footer Right", "Privat  |  Aman  |  Tidak menghakimi",
                 980, 206, 380, 20, size=10, weight="Medium",
                 fill=PALETTE["muted"], align="right")


def design_system(builder, page):
    frame = builder.frame(page, "00 - Design System", 0, -600, 1440, 520,
                          PALETTE["white"], PALETTE["border"], 20)
    builder.text(frame, "Title", "Postpartum Care - Clean & Modern", 40, 32, 800, 38,
                 size=24, weight="Bold", fill=PALETTE["rose"], letter_spacing=-2.0)
    builder.text(frame, "Subtitle",
                 "Design tokens, tipografi Poppins, dan komponen dasar untuk seluruh layar.",
                 40, 70, 1000, 24, size=13, weight="Regular", fill=PALETTE["muted"])
    swatches = [
        ("Champagne", PALETTE["champagne"], "#FBF4EB"),
        ("Blush", PALETTE["blush"], "#FBD9E5"),
        ("Cherry Blossom", PALETTE["cherry"], "#F7C5D7"),
        ("Tickle Me Pink", PALETTE["tickle"], "#F283AF"),
        ("Raspberry Rose", PALETTE["rose"], "#C43670"),
        ("Sunset", PALETTE["sunset"], "#F3CC97"),
        ("Text Dark", PALETTE["dark"], "#2E2228"),
        ("Text Muted", PALETTE["muted"], "#7A6670"),
    ]
    for index, (name, value, label) in enumerate(swatches):
        col = index % 4
        row = index // 4
        sx = 40 + col * 210
        sy = 125 + row * 150
        card = builder.frame(frame, "Swatch " + name, sx, sy, 190, 125, value,
                             PALETTE["border"], 14)
        dark = name in ("Raspberry Rose", "Text Dark", "Text Muted")
        builder.text(card, "Name", name, 14, 78, 160, 18, size=10.5,
                     weight="SemiBold",
                     fill=PALETTE["white"] if dark else PALETTE["dark"])
        builder.text(card, "Hex", label, 14, 96, 160, 16, size=9.5,
                     weight="Medium",
                     fill=PALETTE["blush"] if dark else PALETTE["muted"])
    builder.text(frame, "Type Label", "TIPOGRAFI POPPINS", 910, 125, 200, 18,
                 size=10, weight="SemiBold", fill=PALETTE["rose"],
                 letter_spacing=8.0)
    type_rows = [
        ("Display / 54", 54, "Rawat diri", 145),
        ("Heading / 32", 32, "Ruang aman", 215),
        ("Body / 15", 15, "Setiap hari membawa perubahan baru.", 264),
        ("Caption / 11", 11, "Privat dan tidak menghakimi", 298),
    ]
    for label, size, sample, ty in type_rows:
        builder.text(frame, label, label, 910, ty, 150, 16, size=9,
                     weight="Medium", fill=PALETTE["muted"])
        builder.text(frame, "Sample " + label, sample, 1040, ty - 8, 340, size * 1.5,
                     size=size, weight="Bold" if size > 20 else "Regular",
                     fill=PALETTE["dark"])
    builder.button(frame, "Sample Primary", "Mulai Perjalanan", 40, 435, 180, 46,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=23,
                   shadow_alpha=0.14)
    builder.button(frame, "Sample Secondary", "Masuk", 236, 435, 110, 46,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 12,
                   radius=23)
    builder.pill(frame, "Sample Pill", "MOOD CHECK-IN", 366, 443, 150, 30,
                 PALETTE["soft"], PALETTE["rose"], None, 9.5)
    input_box = builder.frame(frame, "Sample Input", 536, 435, 280, 46,
                              PALETTE["card"], PALETTE["border"], 12)
    builder.text(input_box, "Placeholder", "Tulis sesuatu yang hangat...", 16, 12,
                 240, 20, size=11, weight="Regular", fill=PALETTE["muted"])


def beranda(builder, page):
    screen = builder.frame(page, "02 - Beranda", 1600, 0, 1440, 1300,
                           PALETTE["champagne"], None, 0)
    app_header(builder, screen, "Beranda")
    banner = builder.frame(screen, "Welcome Banner", 80, 120, 1280, 300,
                           PALETTE["blush"], PALETTE["border"], 28)
    builder.pill(banner, "Badge", "RUANG AMAN & HANGAT IBU BARU", 48, 42, 240, 30,
                 PALETTE["white"], PALETTE["rose"], None, 10)
    builder.text(banner, "Greeting", "Halo, Ibu Rani!", 48, 86, 500, 48, size=34,
                 weight="Bold", fill=PALETTE["dark"], letter_spacing=-2.0)
    builder.text(banner, "Phase", "Hari ke-12 masa pascapersalinan - fase adaptasi awal",
                 48, 138, 560, 24, size=12, weight="SemiBold",
                 fill=PALETTE["rose"])
    builder.text(banner, "Body",
                 "Setiap hari membawa perubahan dan tantangan baru. Luangkan beberapa menit\n"
                 "untuk memeluk diri sendiri, menarik napas panjang, dan mendengarkan\n"
                 "kebutuhan tubuh serta hatimu.",
                 48, 178, 680, 72, size=12.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    quote = builder.frame(banner, "Daily Quote", 806, 40, 410, 220,
                          PALETTE["white"], PALETTE["border"], 20,
                          shadow_alpha=0.08, shadow_radius=22)
    builder.text(quote, "Quote Mark", "\"", 24, 12, 40, 40, size=40,
                 weight="Bold", fill=PALETTE["cherry"])
    builder.text(quote, "Quote",
                 "Merawat diri sendiri bukan tindakan egois;\nibu yang sejahtera adalah hadiah terbaik untuk si kecil.",
                 24, 58, 360, 100, size=13, weight="Medium",
                 fill=PALETTE["dark"], line_height=160.0)
    builder.text(quote, "Author", "Catatan Kebaikan Diri", 24, 178, 300, 20,
                 size=10, weight="SemiBold", fill=PALETTE["muted"])

    builder.text(screen, "Section Title", "Aktivitas Hari Ini", 80, 452, 500, 34,
                 size=22, weight="Bold", fill=PALETTE["dark"])
    actions = [
        ("Mood Check-In", "Bagaimana perasaanmu hari ini?", "Isi mood"),
        ("Daily Journal", "Tulis cerita dan rasa syukurmu.", "Mulai menulis"),
        ("Micro-Relaxation", "Beri jeda tiga menit untuk diri.", "Cari jeda"),
    ]
    for index, (title, body, action) in enumerate(actions):
        ax = 80 + index * 430
        card = builder.frame(screen, "Quick " + title, ax, 500, 400, 220,
                             PALETTE["white"], PALETTE["border"], 22,
                             shadow_alpha=0.07, shadow_radius=26)
        builder.circle(card, "Icon", 24, 24, 42, PALETTE["blush"],
                       str(index + 1), PALETTE["rose"], 14)
        builder.text(card, "Title", title, 24, 84, 340, 28, size=16,
                     weight="Bold", fill=PALETTE["dark"])
        builder.text(card, "Body", body, 24, 116, 330, 40, size=11.5,
                     weight="Regular", fill=PALETTE["muted"])
        builder.button(card, "Action", action, 24, 166, 120, 36,
                       PALETTE["rose"], PALETTE["white"], None, 11,
                       radius=18)

    progress = builder.frame(screen, "Weekly Progress", 80, 760, 780, 390,
                             PALETTE["white"], PALETTE["border"], 24,
                             shadow_alpha=0.06, shadow_radius=28)
    builder.text(progress, "Title", "Ritme Mingguanmu", 30, 28, 400, 30,
                 size=18, weight="Bold", fill=PALETTE["dark"])
    builder.text(progress, "Sub", "Mood check-in 5 dari 7 hari", 30, 60, 300, 20,
                 size=11, weight="Medium", fill=PALETTE["muted"])
    chart = builder.frame(progress, "Progress Chart", 30, 110, 720, 190, None, None, 0)
    values = [42, 64, 50, 82, 68, 90, 74]
    days = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
    for index, value in enumerate(values):
        bh = value * 1.45
        bx = index * 102 + 18
        builder.rect(chart, "Bar", bx, 170 - bh, 46, bh,
                     PALETTE["rose"] if index == 5 else PALETTE["cherry"],
                     radius=23)
        builder.text(chart, "Day", days[index], bx - 8, 182, 62, 18, size=9.5,
                     weight="Medium", fill=PALETTE["muted"], align="center")
    builder.text(progress, "Insight Label", "Insight", 30, 320, 100, 18, size=10,
                 weight="SemiBold", fill=PALETTE["rose"], letter_spacing=6.0)
    builder.text(progress, "Insight",
                 "Akhir pekan terasa lebih stabil. Pertahankan jeda relaksasi singkat.",
                 120, 318, 610, 22, size=11, weight="Regular",
                 fill=PALETTE["muted"])

    journal = builder.frame(screen, "Recent Journal", 890, 760, 470, 390,
                            PALETTE["white"], PALETTE["border"], 24,
                            shadow_alpha=0.06, shadow_radius=28)
    builder.text(journal, "Title", "Jurnal Terbaru", 28, 28, 300, 30,
                 size=18, weight="Bold", fill=PALETTE["dark"])
    builder.text(journal, "Date", "Hari ini, 20.15", 28, 60, 200, 18, size=10,
                 weight="Medium", fill=PALETTE["muted"])
    builder.text(journal, "Entry",
                 "\"Hari ini terasa panjang, tapi aku bangga\nsudah memberi jeda untuk diriku.\"",
                 28, 100, 400, 70, size=12, weight="Regular",
                 fill=PALETTE["dark"], line_height=160.0)
    builder.pill(journal, "Tag One", "#lelah", 28, 186, 70, 26, PALETTE["soft"],
                 PALETTE["rose"], None, 9.5)
    builder.pill(journal, "Tag Two", "#bersyukur", 106, 186, 92, 26,
                 PALETTE["soft"], PALETTE["rose"], None, 9.5)
    builder.button(journal, "Read", "Buka Jurnal", 28, 316, 140, 38,
                   PALETTE["rose"], PALETTE["white"], None, 11, radius=19)


def mood_screen(builder, page):
    screen = builder.frame(page, "03 - Mood Check-In", 3200, 0, 1440, 1200,
                           PALETTE["champagne"], None, 0)
    app_header(builder, screen, "Mood Check-In")
    screen_title(builder, screen, "Mood Check-In",
                 "Luangkan satu menit untuk mengenali apa yang kamu rasakan hari ini.")
    left = builder.frame(screen, "Mood Input", 80, 220, 620, 560,
                         PALETTE["white"], PALETTE["border"], 24,
                         shadow_alpha=0.07, shadow_radius=28)
    builder.text(left, "Question", "Bagaimana perasaanmu hari ini, Ibu?", 30, 28,
                 520, 30, size=18, weight="Bold", fill=PALETTE["dark"])
    builder.text(left, "Hint", "Tidak ada perasaan yang salah. Pilih yang paling dekat.",
                 30, 62, 520, 20, size=11, weight="Regular",
                 fill=PALETTE["muted"])
    moods = [("Tenang", 30), ("Bahagia", 210), ("Lelah", 390),
             ("Cemas", 30), ("Sedih", 210), ("Marah", 390)]
    for index, (label, mx) in enumerate(moods):
        my = 110 + (index // 3) * 82
        active = label == "Lelah"
        card = builder.frame(left, "Mood " + label, mx, my, 160, 64,
                             PALETTE["blush"] if active else PALETTE["card"],
                             PALETTE["rose"] if active else PALETTE["border"], 18)
        builder.circle(card, "Dot", 16, 16, 32,
                       PALETTE["rose"] if active else PALETTE["cherry"],
                       label[0], PALETTE["white"], 12)
        builder.text(card, "Label", label, 58, 20, 90, 22, size=11.5,
                     weight="SemiBold",
                     fill=PALETTE["rose"] if active else PALETTE["dark"])
    builder.text(left, "Intensity Label", "Seberapa kuat rasanya?", 30, 292, 300, 20,
                 size=11, weight="SemiBold", fill=PALETTE["dark"])
    builder.line(left, "Slider Track", 30, 336, 560, PALETTE["border"], 8)
    builder.circle(left, "Slider Knob", 330, 322, 36, PALETTE["rose"],
                   None, None, 0)
    builder.text(left, "Slider Low", "Ringan", 30, 350, 100, 18, size=9.5,
                 weight="Medium", fill=PALETTE["muted"])
    builder.text(left, "Slider High", "Sangat kuat", 490, 350, 100, 18, size=9.5,
                 weight="Medium", fill=PALETTE["muted"], align="right")
    note = builder.frame(left, "Note Field", 30, 392, 560, 78, PALETTE["card"],
                         PALETTE["border"], 16)
    builder.text(note, "Placeholder", "Ada yang ingin kamu catat? (opsional)",
                 18, 16, 500, 20, size=11, weight="Regular",
                 fill=PALETTE["muted"])
    builder.button(left, "Save Mood", "Simpan Mood Hari Ini", 30, 490, 190, 46,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=23,
                   shadow_alpha=0.14)

    right = builder.frame(screen, "Mood Insight", 740, 220, 620, 560,
                          PALETTE["white"], PALETTE["border"], 24,
                          shadow_alpha=0.07, shadow_radius=28)
    builder.text(right, "Title", "Ritme Emosi 7 Hari", 30, 28, 400, 30,
                 size=18, weight="Bold", fill=PALETTE["dark"])
    builder.text(right, "Sub", "Perasaanmu berubah, dan itu normal.", 30, 60, 400, 20,
                 size=11, weight="Regular", fill=PALETTE["muted"])
    chart = builder.frame(right, "Chart", 30, 104, 560, 220, None, None, 0)
    values = [52, 70, 48, 86, 62, 78, 66]
    labels = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
    for index, value in enumerate(values):
        bh = value * 1.55
        bx = index * 80 + 12
        builder.rect(chart, "Bar", bx, 200 - bh, 38, bh,
                     PALETTE["rose"] if index == 3 else PALETTE["cherry"],
                     radius=19)
        builder.text(chart, "Label", labels[index], bx - 8, 212, 54, 18,
                     size=9.5, weight="Medium", fill=PALETTE["muted"],
                     align="center")
    builder.line(right, "Divider", 30, 350, 560)
    builder.text(right, "Insight Title", "Yang kami lihat", 30, 374, 300, 24,
                 size=13, weight="SemiBold", fill=PALETTE["dark"])
    builder.text(right, "Insight",
                 "Kamu paling sering merasa lelah di sore hari.\nCoba jeda pernapasan tiga menit sebelum waktu tidur.",
                 30, 404, 540, 60, size=11.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    builder.button(right, "Open Relax", "Coba Relaksasi", 30, 486, 150, 40,
                   PALETTE["blush"], PALETTE["rose"], None, 11.5, radius=20)

    history = builder.frame(screen, "Mood History", 80, 810, 1280, 300,
                            PALETTE["white"], PALETTE["border"], 24,
                            shadow_alpha=0.06, shadow_radius=28)
    builder.text(history, "Title", "Riwayat Check-In", 30, 26, 400, 28, size=17,
                 weight="Bold", fill=PALETTE["dark"])
    rows = [("Hari ini, 08.10", "Lelah", "Tidur kurang, tapi masih bisa beristirahat siang."),
            ("Kemarin, 21.30", "Tenang", "Sempat jalan pagi dan merasa lebih ringan."),
            ("2 hari lalu, 19.45", "Cemas", "Banyak tugas rumah, perlu minta bantuan.")]
    for index, (date, mood, note_text) in enumerate(rows):
        ry = 76 + index * 66
        builder.line(history, "Row Line", 30, ry + 52, 1220)
        builder.text(history, "Date", date, 30, ry + 14, 180, 20, size=10.5,
                     weight="Medium", fill=PALETTE["muted"])
        builder.pill(history, "Mood " + mood, mood, 226, ry + 8, 90, 28,
                     PALETTE["soft"], PALETTE["rose"], None, 9.5)
        builder.text(history, "Note", note_text, 340, ry + 14, 860, 20, size=11,
                     weight="Regular", fill=PALETTE["dark"])


def journal_screen(builder, page):
    screen = builder.frame(page, "04 - Daily Journal", 4800, 0, 1440, 1100,
                           PALETTE["champagne"], None, 0)
    app_header(builder, screen, "Daily Journal")
    screen_title(builder, screen, "Daily Journal",
                 "Ruang privat untuk menuangkan cerita, rasa syukur, dan hal yang membebani.")
    editor = builder.frame(screen, "Journal Editor", 80, 220, 800, 680,
                           PALETTE["white"], PALETTE["border"], 24,
                           shadow_alpha=0.07, shadow_radius=28)
    builder.text(editor, "Date", "Jumat, 11 November 2026", 32, 28, 300, 20,
                 size=10.5, weight="SemiBold", fill=PALETTE["rose"])
    builder.text(editor, "Title", "Hari yang panjang, tapi aku bertahan.", 32, 58,
                 700, 36, size=22, weight="Bold", fill=PALETTE["dark"])
    builder.line(editor, "Divider", 32, 112, 736)
    builder.text(editor, "Body",
                 "Hari ini terasa panjang. Si kecil rewel karena tumbuh gigi, dan aku\n"
                 "hampir kehabisan tenaga. Tapi aku sempat duduk sebentar, minum teh\n"
                 "hangat, dan menarik napas panjang.\n\n"
                 "Aku bangga karena sudah meminta bantuan Mama untuk menjaga si kecil\n"
                 "selama satu jam. Ternyata memberi jeda bukan berarti menyerah.",
                 32, 136, 736, 260, size=13, weight="Regular",
                 fill=PALETTE["dark"], line_height=175.0)
    builder.text(editor, "Tag Label", "Tag perasaan", 32, 430, 200, 20, size=10.5,
                 weight="SemiBold", fill=PALETTE["muted"])
    tags = ["#lelah", "#bersyukur", "#butuh-bantuan"]
    for index, tag in enumerate(tags):
        builder.pill(editor, "Tag " + tag, tag, 32 + index * 110, 458, 100 if index < 2 else 140, 30,
                     PALETTE["soft"], PALETTE["rose"], None, 10)
    builder.button(editor, "Save Journal", "Simpan Jurnal", 32, 600, 160, 46,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=23,
                   shadow_alpha=0.14)
    builder.button(editor, "Cancel", "Batal", 208, 600, 100, 46,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 12,
                   radius=23)

    side = builder.frame(screen, "Journal Side", 920, 220, 440, 680, None, None, 0)
    prompts = builder.frame(side, "Prompts", 0, 0, 440, 360, PALETTE["blush"],
                            PALETTE["border"], 24)
    builder.text(prompts, "Title", "Butuh awalan?", 28, 26, 300, 28, size=17,
                 weight="Bold", fill=PALETTE["dark"])
    builder.text(prompts, "Sub", "Pilih pertanyaan yang terasa ringan.", 28, 58,
                 360, 20, size=11, weight="Regular", fill=PALETTE["muted"])
    prompt_items = ["Apa satu hal yang aku syukuri hari ini?",
                    "Apa yang paling menguras energiku?",
                    "Bantuan kecil apa yang bisa aku minta?"]
    for index, item in enumerate(prompt_items):
        py = 100 + index * 72
        box = builder.frame(prompts, "Prompt " + str(index), 28, py, 384, 58,
                            PALETTE["white"], PALETTE["border"], 14)
        builder.text(box, "Number", str(index + 1), 16, 18, 20, 20, size=11,
                     weight="Bold", fill=PALETTE["rose"])
        builder.text(box, "Text", item, 44, 16, 320, 28, size=10.5,
                     weight="Regular", fill=PALETTE["dark"])
    privacy = builder.frame(side, "Privacy Note", 0, 390, 440, 290,
                            PALETTE["white"], PALETTE["border"], 24,
                            shadow_alpha=0.06, shadow_radius=26)
    builder.circle(privacy, "Shield", 28, 28, 44, PALETTE["soft"], "P",
                   PALETTE["rose"], 16)
    builder.text(privacy, "Title", "Jurnal ini milikmu.", 88, 32, 300, 24,
                 size=14, weight="Bold", fill=PALETTE["dark"])
    builder.text(privacy, "Body",
                 "Catatan pribadi tidak dibagikan ke siapa pun.\n"
                 "Tenaga profesional hanya melihat ringkasan\n"
                 "yang kamu izinkan.",
                 28, 96, 380, 78, size=11, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    builder.text(privacy, "Small", "Terenkripsi dan bisa dihapus kapan saja.",
                 28, 210, 380, 20, size=10, weight="Medium",
                 fill=PALETTE["rose"])


def relaxation_screen(builder, page):
    screen = builder.frame(page, "05 - Micro-Relaxation", 6400, 0, 1440, 1040,
                           PALETTE["champagne"], None, 0)
    app_header(builder, screen, "Micro-Relaxation")
    screen_title(builder, screen, "Micro-Relaxation",
                 "Tiga menit untuk menurunkan bahu, melembutkan napas, dan kembali ke dirimu.")
    stage = builder.frame(screen, "Breathing Stage", 320, 220, 800, 520,
                          PALETTE["blush"], PALETTE["border"], 36)
    builder.text(stage, "Kicker", "PERNAPASAN TENANG", 0, 42, 800, 20, size=10.5,
                 weight="SemiBold", fill=PALETTE["rose"], align="center",
                 letter_spacing=8.0)
    builder.text(stage, "Title", "Tarik napas perlahan.", 0, 74, 800, 42,
                 size=30, weight="Bold", fill=PALETTE["dark"], align="center",
                 letter_spacing=-2.0)
    builder.circle(stage, "Breath Ring", 300, 138, 200, PALETTE["white"],
                   None, None, 0, stroke=PALETTE["cherry"])
    builder.circle(stage, "Breath Core", 340, 178, 120, PALETTE["tickle"],
                   "03:00", PALETTE["white"], 22)
    builder.text(stage, "Hint", "Ikuti lingkaran. Tidak perlu memaksakan napas.",
                 0, 354, 800, 20, size=11, weight="Regular",
                 fill=PALETTE["muted"], align="center")
    builder.button(stage, "Start", "Mulai Sesi", 320, 394, 160, 46,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=23,
                   shadow_alpha=0.14)
    builder.line(stage, "Progress", 140, 470, 520, PALETTE["cherry"], 8)
    builder.rect(stage, "Progress Fill", 140, 470, 210, 8, PALETTE["rose"], 4)

    sessions = [("Pernapasan 4-7-8", "Membantu tidur lebih tenang", "4 menit"),
                ("Body Scan Singkat", "Melepas tegang di bahu dan leher", "5 menit"),
                ("Jeda Syukur", "Menutup hari dengan hal baik", "3 menit")]
    for index, (title, body, duration) in enumerate(sessions):
        sx = 80 + index * 430
        card = builder.frame(screen, "Session " + str(index), sx, 790, 400, 170,
                             PALETTE["white"], PALETTE["border"], 22,
                             shadow_alpha=0.06, shadow_radius=26)
        builder.circle(card, "Number", 24, 24, 42, PALETTE["soft"],
                       str(index + 1), PALETTE["rose"], 14)
        builder.text(card, "Title", title, 24, 82, 300, 24, size=14,
                     weight="Bold", fill=PALETTE["dark"])
        builder.text(card, "Body", body, 24, 108, 330, 20, size=10.5,
                     weight="Regular", fill=PALETTE["muted"])
        builder.pill(card, "Duration", duration, 300, 24, 76, 26,
                     PALETTE["soft"], PALETTE["rose"], None, 9.5)


def education_screen(builder, page):
    screen = builder.frame(page, "06 - Edukasi", 8000, 0, 1440, 1100,
                           PALETTE["champagne"], None, 0)
    app_header(builder, screen, "Edukasi")
    screen_title(builder, screen, "Edukasi Terpercaya",
                 "Panduan pemulihan fisik dan mental yang disesuaikan dengan fase nifas.")
    featured = builder.frame(screen, "Featured Article", 80, 220, 780, 380,
                             PALETTE["blush"], PALETTE["border"], 28)
    builder.pill(featured, "Tag", "FASE ADAPTASI AWAL", 36, 32, 180, 30,
                 PALETTE["white"], PALETTE["rose"], None, 10)
    builder.text(featured, "Title", "Mengenali baby blues dan kapan perlu mencari bantuan.",
                 36, 84, 660, 84, size=28, weight="Bold", fill=PALETTE["dark"],
                 line_height=125.0, letter_spacing=-2.0)
    builder.text(featured, "Body",
                 "Perubahan emosi setelah melahirkan adalah hal yang umum. Pelajari\n"
                 "tanda-tandanya, cara merawat diri, dan kapan sebaiknya berbicara\n"
                 "dengan tenaga profesional.",
                 36, 190, 650, 76, size=12.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    builder.button(featured, "Read", "Baca Artikel", 36, 300, 150, 44,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=22,
                   shadow_alpha=0.14)
    builder.text(featured, "Meta", "6 menit baca  |  Ditinjau psikolog klinis", 206, 314,
                 360, 20, size=10, weight="Medium", fill=PALETTE["muted"])

    phase = builder.frame(screen, "Phase Picker", 900, 220, 460, 380,
                          PALETTE["white"], PALETTE["border"], 24,
                          shadow_alpha=0.07, shadow_radius=28)
    builder.text(phase, "Title", "Pilih Fase Pemulihan", 30, 28, 380, 28,
                 size=17, weight="Bold", fill=PALETTE["dark"])
    builder.text(phase, "Sub", "Konten akan disesuaikan dengan kebutuhanmu.",
                 30, 58, 380, 20, size=10.5, weight="Regular",
                 fill=PALETTE["muted"])
    phases = ["Minggu 1-2: Adaptasi", "Minggu 3-6: Pemulihan",
              "Bulan 2-3: Transisi", "Setelah 3 bulan"]
    for index, label in enumerate(phases):
        active = index == 1
        builder.button(phase, "Phase " + str(index), label, 30, 96 + index * 58,
                       400, 44, PALETTE["blush"] if active else PALETTE["card"],
                       PALETTE["rose"] if active else PALETTE["dark"],
                       PALETTE["border"], 11, radius=14)

    builder.text(screen, "Article Section", "Artikel untukmu", 80, 650, 400, 30,
                 size=20, weight="Bold", fill=PALETTE["dark"])
    articles = [("01", "Menjaga kualitas tidur di tengah jadwal menyusui", "Tidur 4 menit"),
                ("02", "Nutrisi sederhana untuk mendukung pemulihan", "5 menit"),
                ("03", "Bergerak lembut setelah persalinan", "4 menit")]
    for index, (number, title, duration) in enumerate(articles):
        ax = 80 + index * 430
        card = builder.frame(screen, "Article " + number, ax, 706, 400, 280,
                             PALETTE["white"], PALETTE["border"], 22,
                             shadow_alpha=0.06, shadow_radius=26)
        builder.circle(card, "Number", 24, 24, 42, PALETTE["blush"], number,
                       PALETTE["rose"], 12)
        builder.text(card, "Title", title, 24, 88, 340, 60, size=15,
                     weight="Bold", fill=PALETTE["dark"], line_height=150.0)
        builder.text(card, "Meta", "Ditinjau tenaga medis", 24, 166, 260, 20,
                     size=10, weight="Medium", fill=PALETTE["muted"])
        builder.text(card, "Duration", duration, 24, 224, 120, 20, size=10.5,
                     weight="SemiBold", fill=PALETTE["rose"])


def help_screen(builder, page):
    screen = builder.frame(page, "07 - Bantuan Profesional", 9600, 0, 1440, 1100,
                           PALETTE["champagne"], None, 0)
    app_header(builder, screen, "Bantuan Profesional")
    screen_title(builder, screen, "Bantuan Profesional",
                 "Temukan tenaga terverifikasi yang tepat untuk mendampingi perjalananmu.")
    professionals = [
        ("RK", "Rina Kusuma, M.Psi.", "Psikolog Klinis Perinatal", "Kecemasan nifas", "5.0"),
        ("AS", "Ayu Safitri, S.Tr.Keb.", "Bidan Konselor Laktasi", "Menyusui", "4.9"),
        ("BD", "dr. Bima Darma, Sp.OG", "Dokter Spesialis Obstetri", "Pemulihan fisik", "4.8"),
    ]
    for index, (initials, name, role, tag, rating) in enumerate(professionals):
        px = 80 + index * 430
        card = builder.frame(screen, "Professional " + initials, px, 220, 400, 430,
                             PALETTE["white"], PALETTE["border"], 24,
                             shadow_alpha=0.07, shadow_radius=28)
        builder.circle(card, "Avatar", 26, 26, 64, PALETTE["rose"], initials,
                       PALETTE["white"], 18)
        builder.text(card, "Name", name, 106, 30, 270, 24, size=14,
                     weight="Bold", fill=PALETTE["dark"])
        builder.text(card, "Role", role, 106, 56, 270, 20, size=10.5,
                     weight="Medium", fill=PALETTE["muted"])
        builder.text(card, "Rating", rating + "  |  Terverifikasi", 26, 112, 300, 20,
                     size=10, weight="SemiBold", fill=PALETTE["rose"])
        builder.pill(card, "Tag", tag, 26, 150, 150, 28, PALETTE["soft"],
                     PALETTE["rose"], None, 9.5)
        builder.line(card, "Divider", 26, 202, 348)
        builder.text(card, "Schedule Title", "Jadwal tersedia", 26, 226, 300, 22,
                     size=11.5, weight="SemiBold", fill=PALETTE["dark"])
        builder.text(card, "Schedule", "Senin - Jumat, 09.00 - 17.00", 26, 252, 320, 20,
                     size=10, weight="Regular", fill=PALETTE["muted"])
        builder.button(card, "Book", "Ajukan Sesi", 26, 310, 160, 42,
                       PALETTE["rose"], PALETTE["white"], None, 11.5,
                       radius=21)
        builder.button(card, "Profile", "Lihat Profil", 200, 310, 140, 42,
                       PALETTE["white"], PALETTE["rose"], PALETTE["border"], 11.5,
                       radius=21)

    info = builder.frame(screen, "Help Info", 80, 700, 1280, 260,
                         PALETTE["white"], PALETTE["border"], 24,
                         shadow_alpha=0.06, shadow_radius=28)
    builder.text(info, "Title", "Tidak yakin harus mulai dari mana?", 30, 28, 600, 30,
                 size=18, weight="Bold", fill=PALETTE["dark"])
    builder.text(info, "Body",
                 "Tim pendamping dapat membantumu memilih tenaga profesional yang sesuai.\n"
                 "Ceritakan kebutuhanmu dengan tenang, tanpa harus menjelaskan semuanya.",
                 30, 66, 760, 60, size=12, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    builder.button(info, "Match", "Cari Pendamping", 30, 164, 180, 44,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=22,
                   shadow_alpha=0.14)
    builder.text(info, "Note", "Respon dalam 1x24 jam kerja", 226, 176, 300, 20,
                 size=10, weight="Medium", fill=PALETTE["muted"])
    builder.text(info, "Emergency", "Jika ada kondisi darurat, segera hubungi layanan medis terdekat.",
                 790, 176, 460, 20, size=10, weight="Medium",
                 fill=PALETTE["rose"], align="right")


def profile_screen(builder, page):
    screen = builder.frame(page, "08 - Profil", 11200, 0, 1440, 1060,
                           PALETTE["champagne"], None, 0)
    app_header(builder, screen, active=None, profile_active=True)
    screen_title(builder, screen, "Profil Saya",
                 "Kelola informasi akun dan preferensi pendampinganmu.",
                 action=True, action_label="Edit Profil")
    left = builder.frame(screen, "Profile Card", 80, 220, 400, 540,
                         PALETTE["white"], PALETTE["border"], 24,
                         shadow_alpha=0.07, shadow_radius=28)
    builder.circle(left, "Avatar", 152, 36, 96, PALETTE["rose"], "RA",
                   PALETTE["white"], 30)
    builder.text(left, "Name", "Ibu Rani", 0, 148, 400, 30, size=20,
                 weight="Bold", fill=PALETTE["dark"], align="center")
    builder.text(left, "Email", "rani.anindita@email.com", 0, 180, 400, 20,
                 size=11, weight="Regular", fill=PALETTE["muted"],
                 align="center")
    builder.pill(left, "Phase Badge", "Hari ke-12 pemulihan", 112, 216, 176, 30,
                 PALETTE["soft"], PALETTE["rose"], None, 10)
    builder.line(left, "Divider", 30, 278, 340)
    stats = [("12", "Hari"), ("5/7", "Check-in"), ("8", "Jurnal")]
    for index, (value, label) in enumerate(stats):
        sx = 30 + index * 115
        builder.text(left, "Stat " + label, value, sx, 304, 100, 30, size=20,
                     weight="Bold", fill=PALETTE["rose"], align="center")
        builder.text(left, "Stat Label " + label, label, sx, 336, 100, 18,
                     size=9.5, weight="Medium", fill=PALETTE["muted"],
                     align="center")
    builder.line(left, "Divider Two", 30, 380, 340)
    builder.text(left, "Member", "Bergabung sejak Oktober 2026", 0, 410, 400, 20,
                 size=10, weight="Medium", fill=PALETTE["muted"],
                 align="center")
    builder.button(left, "Edit Profile", "Edit Profil", 30, 456, 340, 46,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=23,
                   shadow_alpha=0.14)

    right = builder.frame(screen, "Account Info", 510, 220, 850, 540,
                          PALETTE["white"], PALETTE["border"], 24,
                          shadow_alpha=0.07, shadow_radius=28)
    builder.text(right, "Title", "Informasi Akun", 32, 28, 400, 30, size=18,
                 weight="Bold", fill=PALETTE["dark"])
    builder.text(right, "Sub", "Data ini membantu kami menyesuaikan pendampingan.",
                 32, 60, 500, 20, size=10.5, weight="Regular",
                 fill=PALETTE["muted"])
    fields = [("Nama lengkap", "Ibu Rani"), ("Email", "rani.anindita@email.com"),
              ("Tanggal persalinan", "30 Oktober 2026"),
              ("Fase pemulihan", "Fase adaptasi awal (hari ke-12)")]
    for index, (label, value) in enumerate(fields):
        fy = 108 + index * 84
        builder.text(right, "Label " + label, label, 32, fy, 300, 20, size=10,
                     weight="SemiBold", fill=PALETTE["muted"])
        box = builder.frame(right, "Field " + label, 32, fy + 24, 786, 46,
                            PALETTE["card"], PALETTE["border"], 12)
        builder.text(box, "Value", value, 16, 12, 700, 20, size=12,
                     weight="Regular", fill=PALETTE["dark"])
    builder.button(right, "Save", "Simpan Perubahan", 32, 460, 180, 44,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=22,
                   shadow_alpha=0.14)
    builder.button(right, "Cancel", "Batal", 224, 460, 100, 44,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 12,
                   radius=22)

    privacy = builder.frame(screen, "Privacy", 80, 800, 1280, 180,
                            PALETTE["white"], PALETTE["border"], 24,
                            shadow_alpha=0.06, shadow_radius=26)
    builder.circle(privacy, "Shield", 30, 34, 44, PALETTE["soft"], "P",
                   PALETTE["rose"], 16)
    builder.text(privacy, "Title", "Privasi & Keamanan", 90, 34, 400, 26,
                 size=15, weight="Bold", fill=PALETTE["dark"])
    builder.text(privacy, "Body",
                 "Jurnal dan mood check-in hanya bisa dilihat olehmu.\n"
                 "Kamu dapat mengunduh atau menghapus data kapan saja.",
                 90, 66, 700, 48, size=11, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    builder.button(privacy, "Manage", "Kelola Privasi", 1030, 64, 190, 44,
                   PALETTE["blush"], PALETTE["rose"], None, 11.5, radius=22)

    modal_screen = builder.frame(page, "09 - Edit Profil Modal", 11200, 1100,
                                 1440, 800, PALETTE["dark"], None, 0)
    builder.nodes[str(modal_screen)]["fills"] = paint(PALETTE["dark"], 0.45)
    card = builder.frame(modal_screen, "Modal Card", 410, 70, 620, 660,
                         PALETTE["white"], PALETTE["border"], 28,
                         shadow_alpha=0.24, shadow_radius=50)
    builder.text(card, "Title", "Edit Profil", 32, 28, 400, 32, size=22,
                 weight="Bold", fill=PALETTE["dark"])
    builder.text(card, "Sub", "Perbarui informasi yang ingin kamu tampilkan.",
                 32, 64, 500, 20, size=11, weight="Regular",
                 fill=PALETTE["muted"])
    builder.button(card, "Close", "X", 548, 24, 36, 36, PALETTE["card"],
                   PALETTE["muted"], PALETTE["border"], 12, radius=18)
    fields = [("Nama lengkap", "Ibu Rani"), ("Email", "rani.anindita@email.com"),
              ("Tanggal persalinan", "30 Oktober 2026"),
              ("Fase pemulihan", "Fase adaptasi awal")]
    for index, (label, value) in enumerate(fields):
        fy = 112 + index * 92
        builder.text(card, "Label " + label, label, 32, fy, 300, 20, size=10,
                     weight="SemiBold", fill=PALETTE["muted"])
        box = builder.frame(card, "Input " + label, 32, fy + 24, 556, 48,
                            PALETTE["card"], PALETTE["border"], 12)
        builder.text(box, "Value", value, 16, 13, 500, 20, size=12,
                     weight="Regular", fill=PALETTE["dark"])
    builder.button(card, "Cancel", "Batal", 32, 540, 120, 46, PALETTE["white"],
                   PALETTE["rose"], PALETTE["border"], 12, radius=23)
    builder.button(card, "Save", "Simpan Profil", 168, 540, 180, 46,
                   PALETTE["rose"], PALETTE["white"], None, 12, radius=23,
                   shadow_alpha=0.14)


def login_screen(builder, page):
    screen = builder.frame(page, "10 - Login", 12800, 0, 1440, 1000,
                           PALETTE["champagne"], None, 0)
    left = builder.frame(screen, "Login Brand Panel", 0, 0, 620, 1000,
                         PALETTE["blush"], PALETTE["border"], 0)
    logo(builder, left, 56, 52)
    builder.pill(left, "Badge", "RUANG AMAN UNTUK IBU BARU", 56, 150, 240, 30,
                 PALETTE["white"], PALETTE["rose"], None, 10)
    builder.text(left, "Title", "Kembali ke\nruang yang tenang.", 56, 202, 500, 140,
                 size=46, weight="Bold", fill=PALETTE["dark"],
                 line_height=115.0, letter_spacing=-3.0)
    builder.text(left, "Body",
                 "Lanjutkan perjalanan kecilmu: catat mood,\n"
                 "tulis jurnal, dan temukan jeda yang kamu butuhkan.",
                 56, 370, 500, 70, size=13, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    features = ["Mood check-in harian", "Jurnal privat terenkripsi",
                "Relaksasi tiga menit", "Pendampingan profesional"]
    for index, label in enumerate(features):
        fy = 500 + index * 54
        builder.circle(left, "Check " + str(index), 56, fy, 28,
                       PALETTE["white"], str(index + 1), PALETTE["rose"], 9)
        builder.text(left, "Feature " + str(index), label, 98, fy + 4, 380, 22,
                     size=11.5, weight="Medium", fill=PALETTE["dark"])

    builder.text(screen, "Back", "< Kembali ke beranda", 1200, 40, 180, 20,
                 size=10.5, weight="SemiBold", fill=PALETTE["muted"],
                 align="right")
    card = builder.frame(screen, "Login Card", 760, 150, 600, 700,
                         PALETTE["white"], PALETTE["border"], 28,
                         shadow_alpha=0.10, shadow_radius=36)
    builder.text(card, "Title", "Masuk ke akunmu", 44, 38, 420, 34, size=24,
                 weight="Bold", fill=PALETTE["dark"], letter_spacing=-1.0)
    builder.text(card, "Sub", "Selamat datang kembali. Kami sudah menunggu.",
                 44, 76, 480, 20, size=11, weight="Regular",
                 fill=PALETTE["muted"])
    builder.text(card, "Role Label", "Masuk sebagai", 44, 118, 200, 20, size=10,
                 weight="SemiBold", fill=PALETTE["muted"])
    builder.button(card, "Role Ibu", "Ibu Pascasalin", 44, 142, 240, 42,
                   PALETTE["blush"], PALETTE["rose"], PALETTE["rose"], 11,
                   radius=21)
    builder.button(card, "Role Pro", "Tenaga Profesional", 300, 142, 240, 42,
                   PALETTE["white"], PALETTE["muted"], PALETTE["border"], 11,
                   radius=21)
    builder.text(card, "Email Label", "Alamat email", 44, 210, 200, 20, size=10,
                 weight="SemiBold", fill=PALETTE["muted"])
    email = builder.frame(card, "Email Input", 44, 234, 512, 48,
                          PALETTE["card"], PALETTE["border"], 12)
    builder.text(email, "Value", "rani.anindita@email.com", 16, 13, 460, 20,
                 size=12, weight="Regular", fill=PALETTE["dark"])
    builder.text(card, "Password Label", "Kata sandi", 44, 304, 200, 20, size=10,
                 weight="SemiBold", fill=PALETTE["muted"])
    password = builder.frame(card, "Password Input", 44, 328, 512, 48,
                             PALETTE["card"], PALETTE["border"], 12)
    builder.text(password, "Value", "............", 16, 13, 300, 20, size=12,
                 weight="Regular", fill=PALETTE["dark"])
    builder.text(card, "Forgot", "Lupa kata sandi?", 392, 386, 164, 20,
                 size=10, weight="SemiBold", fill=PALETTE["rose"],
                 align="right")
    builder.button(card, "Login", "Masuk", 44, 420, 512, 50,
                   PALETTE["rose"], PALETTE["white"], None, 13, radius=25,
                   shadow_alpha=0.18)
    builder.text(card, "Or", "atau coba akun demo", 0, 492, 600, 20, size=10,
                 weight="Medium", fill=PALETTE["muted"], align="center")
    builder.button(card, "Demo", "Isi Akun Demo", 44, 520, 512, 46,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 12,
                   radius=23)
    builder.text(card, "Register", "Belum punya akun?  Daftar gratis", 0, 606, 600,
                 20, size=11, weight="Medium", fill=PALETTE["muted"],
                 align="center")


def register_screen(builder, page):
    screen = builder.frame(page, "11 - Register", 14400, 0, 1440, 1100,
                           PALETTE["champagne"], None, 0)
    left = builder.frame(screen, "Register Brand Panel", 0, 0, 520, 1100,
                         PALETTE["blush"], PALETTE["border"], 0)
    logo(builder, left, 48, 48)
    builder.pill(left, "Badge", "MULAI DENGAN LEMBUT", 48, 150, 200, 30,
                 PALETTE["white"], PALETTE["rose"], None, 10)
    builder.text(left, "Title", "Mulai perjalanan\nkesejahteraanmu.", 48, 200, 420, 140,
                 size=40, weight="Bold", fill=PALETTE["dark"],
                 line_height=115.0, letter_spacing=-3.0)
    builder.text(left, "Body",
                 "Ruang aman untuk mencatat, beristirahat,\n"
                 "dan mendapatkan dukungan yang tepat.",
                 48, 356, 420, 70, size=12.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=160.0)
    features = [("01", "Mood Check-In", "Kenali ritme emosi harianmu."),
                ("02", "Daily Journal", "Ruang privat tanpa penghakiman."),
                ("03", "Relaksasi 3 Menit", "Jeda praktis di sela merawat bayi."),
                ("04", "Tenaga Terpercaya", "Psikolog, bidan, dan dokter.")]
    for index, (number, title, body) in enumerate(features):
        fy = 490 + index * 108
        card = builder.frame(left, "Feature " + number, 48, fy, 424, 88,
                             PALETTE["white"], PALETTE["border"], 14)
        builder.text(card, "Number", number, 16, 14, 30, 20, size=10,
                     weight="Bold", fill=PALETTE["rose"])
        builder.text(card, "Title", title, 56, 12, 340, 22, size=11.5,
                     weight="Bold", fill=PALETTE["dark"])
        builder.text(card, "Body", body, 56, 36, 340, 20, size=9.5,
                     weight="Regular", fill=PALETTE["muted"])

    builder.text(screen, "Back", "< Kembali ke beranda", 1200, 40, 180, 20,
                 size=10.5, weight="SemiBold", fill=PALETTE["muted"],
                 align="right")
    card = builder.frame(screen, "Register Card", 610, 70, 730, 960,
                         PALETTE["white"], PALETTE["border"], 28,
                         shadow_alpha=0.10, shadow_radius=36)
    builder.text(card, "Title", "Buat akun Postpartum Care", 44, 34, 500, 34,
                 size=24, weight="Bold", fill=PALETTE["dark"],
                 letter_spacing=-1.0)
    builder.text(card, "Sub", "Lengkapi data singkat untuk memulai pendampingan.",
                 44, 72, 560, 20, size=11, weight="Regular",
                 fill=PALETTE["muted"])
    builder.text(card, "Role Label", "Pilih peran", 44, 112, 200, 20, size=10,
                 weight="SemiBold", fill=PALETTE["muted"])
    builder.button(card, "Role Ibu", "Ibu Pascasalin", 44, 136, 300, 42,
                   PALETTE["blush"], PALETTE["rose"], PALETTE["rose"], 11,
                   radius=21)
    builder.button(card, "Role Pro", "Tenaga Profesional", 360, 136, 300, 42,
                   PALETTE["white"], PALETTE["muted"], PALETTE["border"], 11,
                   radius=21)
    fields = [("Nama lengkap", "Ibu Rani", 200),
              ("Alamat email", "rani.anindita@email.com", 284),
              ("Tanggal persalinan", "30 Oktober 2026", 368)]
    for label, value, fy in fields:
        builder.text(card, "Label " + label, label, 44, fy, 300, 20, size=10,
                     weight="SemiBold", fill=PALETTE["muted"])
        box = builder.frame(card, "Input " + label, 44, fy + 24, 618, 46,
                            PALETTE["card"], PALETTE["border"], 12)
        builder.text(box, "Value", value, 16, 12, 560, 20, size=12,
                     weight="Regular", fill=PALETTE["dark"])
    builder.text(card, "Password Label", "Kata sandi", 44, 452, 200, 20, size=10,
                 weight="SemiBold", fill=PALETTE["muted"])
    password = builder.frame(card, "Password Input", 44, 476, 300, 46,
                             PALETTE["card"], PALETTE["border"], 12)
    builder.text(password, "Value", "............", 16, 12, 240, 20, size=12,
                 weight="Regular", fill=PALETTE["dark"])
    builder.text(card, "Confirm Label", "Konfirmasi kata sandi", 360, 452, 240, 20,
                 size=10, weight="SemiBold", fill=PALETTE["muted"])
    confirm = builder.frame(card, "Confirm Input", 360, 476, 302, 46,
                            PALETTE["card"], PALETTE["border"], 12)
    builder.text(confirm, "Value", "............", 16, 12, 240, 20, size=12,
                 weight="Regular", fill=PALETTE["dark"])
    builder.text(card, "Agreement", "Saya menyetujui Ketentuan Layanan & Kebijakan Privasi.",
                 44, 548, 520, 20, size=10, weight="Regular",
                 fill=PALETTE["dark"])
    builder.button(card, "Register", "Daftar Akun Baru", 44, 590, 618, 50,
                   PALETTE["rose"], PALETTE["white"], None, 13, radius=25,
                   shadow_alpha=0.18)
    builder.text(card, "Login Link", "Sudah memiliki akun?  Masuk di sini", 0, 674,
                 730, 20, size=11, weight="Medium", fill=PALETTE["muted"],
                 align="center")
    builder.text(card, "Safety", "Data pribadi dijaga kerahasiaannya. Kamu bisa menghapus akun kapan saja.",
                 0, 850, 730, 20, size=9.5, weight="Regular",
                 fill=PALETTE["muted"], align="center")


def build():
    builder = Builder("Postpartum Care - Clean & Modern")
    page = builder.page_id
    design_system(builder, page)
    landing_page(builder, page)
    beranda(builder, page)
    mood_screen(builder, page)
    journal_screen(builder, page)
    relaxation_screen(builder, page)
    education_screen(builder, page)
    help_screen(builder, page)
    profile_screen(builder, page)
    login_screen(builder, page)
    register_screen(builder, page)
    builder.save("postpartum-care.figcraft")


if __name__ == "__main__":
    build()
