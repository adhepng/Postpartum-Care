from generate_figcraft_clean import (
    Builder,
    PALETTE,
    design_system,
    landing_page as clean_landing_page,
    logo,
    paint,
)


def header(builder, screen, active="Beranda", profile_active=False):
    bar = builder.frame(screen, "App Header", 0, 0, 1440, 80,
                        PALETTE["white"], PALETTE["border"], 0)
    logo(builder, bar, 80, 20, compact=True)
    items = [
        ("Beranda", 80),
        ("Mood Check-In", 104),
        ("Daily Journal", 98),
        ("Micro-Relaxation", 124),
        ("Edukasi", 78),
        ("Bantuan Profesional", 168),
    ]
    x = 300
    for label, width in items:
        if label == active:
            builder.button(bar, "Nav Active", label, x, 24, width, 34,
                           PALETTE["blush"], PALETTE["rose"], None, 11.5,
                           radius=17)
        else:
            builder.text(bar, "Nav " + label, label, x, 31, width, 20,
                         size=11.5, weight="Medium", fill=PALETTE["muted"])
        x += width + 10
    chip = builder.frame(bar, "User Chip", 1100, 20, 150, 40,
                         PALETTE["blush"] if profile_active else PALETTE["card"],
                         PALETTE["rose"] if profile_active else PALETTE["border"],
                         20)
    builder.circle(chip, "Avatar", 5, 5, 30, PALETTE["rose"], "R",
                   PALETTE["white"], 12)
    builder.text(chip, "User Name", "Ibu Rani", 42, 11, 100, 20, size=12,
                 weight="SemiBold",
                 fill=PALETTE["rose"] if profile_active else PALETTE["dark"])
    builder.button(bar, "Logout", "Keluar", 1262, 24, 118, 34,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 11,
                   radius=17)


def page_header(builder, screen, title, subtitle, y=112, center=False):
    x = 0 if center else 80
    width = 1440 if center else 1050
    builder.text(screen, "Page Title", title, x, y, width, 48, size=32,
                 weight="Bold", fill=PALETTE["rose"],
                 align="center" if center else "left", letter_spacing=-2.0)
    builder.text(screen, "Page Subtitle", subtitle, x, y + 46, width, 44,
                 size=12.5, weight="Regular", fill=PALETTE["muted"],
                 align="center" if center else "left", line_height=155.0)


def panel(builder, parent, name, x, y, w, h, radius=24, fill=None):
    return builder.frame(parent, name, x, y, w, h,
                         fill or PALETTE["white"], PALETTE["border"], radius,
                         shadow_alpha=0.06, shadow_radius=28)


def input_box(builder, parent, name, x, y, w, h, value, placeholder=False):
    box = builder.frame(parent, name, x, y, w, h, PALETTE["card"],
                        PALETTE["border"], 12)
    builder.text(box, "Value", value, 16, 12, w - 32, 22, size=11.5,
                 weight="Regular",
                 fill=PALETTE["muted"] if placeholder else PALETTE["dark"])
    return box


def chip(builder, parent, name, label, x, y, w, h=32, active=False):
    return builder.button(parent, name, label, x, y, w, h,
                          PALETTE["soft"] if active else PALETTE["card"],
                          PALETTE["rose"] if active else PALETTE["muted"],
                          PALETTE["rose"] if active else PALETTE["border"],
                          9.5, radius=h / 2.0)


def toggle(builder, parent, x, y, on):
    track = builder.frame(parent, "Switch", x, y, 44, 24,
                          PALETTE["rose"] if on else PALETTE["border"],
                          None, 12)
    builder.circle(track, "Knob", 24 if on else 2, 2, 20, PALETTE["white"])


def beranda(builder, page):
    screen = builder.frame(page, "02 - Beranda", 1600, 0, 1440, 1620,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, "Beranda")

    banner = builder.frame(screen, "Hero Banner", 80, 110, 1280, 380,
                           PALETTE["blush"], PALETTE["border"], 28)
    builder.pill(banner, "Hero Badge", "Ruang Aman & Hangat Ibu Baru", 48, 38,
                 250, 30, PALETTE["white"], PALETTE["rose"], None, 10)
    builder.text(banner, "Greeting", "Halo, Ibu Rani!", 48, 88, 500, 54,
                 size=40, weight="Bold", fill=PALETTE["rose"],
                 letter_spacing=-2.0)
    builder.text(banner, "Phase",
                 "Hari ke-12 Masa Pascapersalinan (Fase Adaptasi Awal)",
                 48, 150, 620, 24, size=13, weight="SemiBold",
                 fill=PALETTE["dark"])
    builder.text(banner, "Body",
                 "Setiap hari membawa perubahan dan tantangan baru. Luangkan beberapa menit\n"
                 "untuk memeluk diri sendiri, menarik napas panjang, dan mendengarkan\n"
                 "kebutuhan tubuh serta hatimu.",
                 48, 188, 620, 78, size=12.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=165.0)
    note = builder.frame(banner, "Disclaimer", 48, 292, 690, 54,
                         PALETTE["white"], PALETTE["border"], 14)
    builder.circle(note, "Shield", 14, 14, 26, PALETTE["soft"], "S",
                   PALETTE["rose"], 10)
    builder.text(note, "Disclaimer Text",
                 "Platform ini dirancang sebagai pendamping emosional & kesejahteraan diri,\n"
                 "bukan pengganti konsultasi atau diagnosis medis profesional.",
                 52, 10, 620, 38, size=10.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=150.0)

    quote = builder.frame(banner, "Daily Quote", 880, 196, 350, 170,
                          PALETTE["white"], PALETTE["border"], 18,
                          shadow_alpha=0.05, shadow_radius=18)
    builder.text(quote, "Quote Mark", chr(34), 20, 6, 36, 40, size=38,
                 weight="Bold", fill=PALETTE["cherry"])
    builder.text(quote, "Quote",
                 "Merawat diri sendiri bukanlah tindakan egois; ibu yang\n"
                 "sejahtera adalah hadiah terbaik untuk si kecil.",
                 20, 48, 310, 80, size=11, weight="Medium",
                 fill=PALETTE["dark"], line_height=160.0)
    builder.text(quote, "Author", "- Catatan Kebaikan Diri", 20, 138, 280, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["muted"])

    builder.text(screen, "Activity Title", "Aktivitas Hari Ini", 80, 535, 500, 32,
                 size=20, weight="Bold", fill=PALETTE["dark"])

    quick = [
        ("01", "Mood Check-In", "Belum Diisi Hari Ini",
         "Pantau ritme perasaanmu secara berkala untuk mengenali perubahan\nemosi dan kebutuhan jeda.",
         "S  N  L  C  S", "Catat Suasana Hati Sekarang", "mood"),
        ("02", "Micro-Relaxation", "Audio 3 Menit",
         "Latihan pernapasan terpandu untuk meredakan kaku otot bahu dan\nmenenangkan overthinking.",
         "Pernapasan Tenang Ibu (03:00)", "Putar Relaksasi Singkat", "relax"),
        ("03", "Daily Journal", "Privat & Aman",
         "Tuliskan segala hal yang sedang membebani pikiran atau momen\nbahagia yang ingin Ibu syukuri.",
         "Hari ini terasa panjang, tapi melihat si kecil tersenyum...",
         "Tulis Jurnal Harian", "journal"),
    ]
    for index, (num, title, status, desc, preview, action, kind) in enumerate(quick):
        x = 80 + index * 430
        box = panel(builder, screen, "Quick " + num, x, 575, 400, 330, 22)
        icon = builder.frame(box, "Icon Badge", 24, 22, 44, 44,
                             PALETTE["blush"], None, 12)
        builder.text(icon, "Icon", num, 0, 11, 44, 22, size=13,
                     weight="Bold", fill=PALETTE["rose"], align="center")
        builder.pill(box, "Status", status, 250, 28, 126, 26,
                     PALETTE["soft"], PALETTE["rose"], None, 8.5)
        builder.text(box, "Title", title, 24, 86, 340, 28, size=16,
                     weight="Bold", fill=PALETTE["dark"])
        builder.text(box, "Desc", desc, 24, 120, 350, 62, size=10.5,
                     weight="Regular", fill=PALETTE["muted"], line_height=155.0)
        preview_box = builder.frame(box, "Preview", 24, 196, 352, 58,
                                    PALETTE["card"], PALETTE["border"], 12)
        if kind == "mood":
            for dot in range(5):
                builder.circle(preview_box, "Mood Dot", 74 + dot * 40, 14, 30,
                               PALETTE["soft"] if dot != 2 else PALETTE["cherry"],
                               str(dot + 1), PALETTE["rose"], 9)
        elif kind == "relax":
            builder.circle(preview_box, "Pulse", 16, 20, 18, PALETTE["rose"])
            builder.text(preview_box, "Player Text", preview, 44, 18, 290, 22,
                         size=10, weight="Medium", fill=PALETTE["dark"])
        else:
            builder.text(preview_box, "Snippet", chr(34) + preview + chr(34),
                         14, 14, 324, 34, size=9.5, weight="Regular",
                         fill=PALETTE["muted"], line_height=150.0)
        builder.button(box, "Action", action, 24, 272, 352, 40,
                       PALETTE["rose"], PALETTE["white"], None, 10.5,
                       radius=20)

    builder.text(screen, "Article Title",
                 "Panduan Edukasi Terpercaya Sesuai Fase", 80, 958, 700, 30,
                 size=20, weight="Bold", fill=PALETTE["dark"])
    builder.text(screen, "Article Sub",
                 "Informasi terverifikasi mengenai pemulihan fisik dan kesehatan mental di minggu ke-2 pascasalin.",
                 80, 990, 880, 24, size=11.5, weight="Regular",
                 fill=PALETTE["muted"])
    builder.text(screen, "See All", "Lihat Semua Artikel  >", 1110, 965, 250, 24,
                 size=11, weight="SemiBold", fill=PALETTE["rose"],
                 align="right")

    articles = [
        ("Kesehatan Mental", "4 mnt baca  |  dr. Sarah Anindya, Sp.OG",
         "Mengenali Baby Blues vs Depresi Pascapersalinan (PPD)",
         "Kapan tangisan emosional di minggu awal merupakan proses adaptasi normal, dan kapan memerlukan konsultasi profesional?",
         PALETTE["blush"]),
        ("Pemulihan Fisik", "5 mnt baca  |  Bidan Nurul Aisyah",
         "Panduan Merawat Luka Jahitan Caesar & Normal di Rumah",
         "Tips menjaga higiene area luka, posisi tidur yang mengurangi rasa nyeri, serta tanda bahaya infeksi yang patut diwaspadai.",
         PALETTE["sunset"]),
        ("Perawatan Diri", "3 mnt baca  |  Rina Kusuma, M.Psi.",
         "Mengatasi Rasa Bersalah Ketika Merasa Kewalahan & Butuh Jeda",
         "Membedah fenomena overthinking ibu baru dan bagaimana mengajak pasangan terlibat tanpa merasa menjadi beban.",
         PALETTE["cherry"]),
    ]
    for index, (cat, meta, title, snippet, tint) in enumerate(articles):
        x = 80 + index * 430
        card = panel(builder, screen, "Article " + str(index), x, 1030, 400, 330, 20)
        thumb = builder.frame(card, "Thumb", 0, 0, 400, 94, tint, None, 20)
        builder.pill(thumb, "Category", cat, 20, 20, 130, 26,
                     PALETTE["white"], PALETTE["rose"], None, 8.5)
        builder.text(card, "Meta", meta, 20, 112, 360, 20, size=8.5,
                     weight="Medium", fill=PALETTE["muted"])
        builder.text(card, "Title", title, 20, 138, 360, 56, size=13.5,
                     weight="Bold", fill=PALETTE["dark"], line_height=140.0)
        builder.text(card, "Snippet", snippet, 20, 202, 360, 68, size=9.5,
                     weight="Regular", fill=PALETTE["muted"], line_height=155.0)
        builder.text(card, "Read", "Baca Panduan Lengkap  >", 20, 292, 250, 20,
                     size=9.5, weight="SemiBold", fill=PALETTE["rose"])

    pro = builder.frame(screen, "Professional Banner", 80, 1400, 1280, 160,
                        PALETTE["card"], PALETTE["border"], 22,
                        shadow_alpha=0.05, shadow_radius=22)
    builder.text(pro, "Badge", "Layanan Dukungan Terpercaya", 40, 26, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["rose"])
    builder.text(pro, "Title", "Butuh Teman Berbagi Cerita atau Bantuan Medis?",
                 40, 54, 650, 30, size=19, weight="Bold", fill=PALETTE["dark"])
    builder.text(pro, "Body",
                 "Jangan ragu menjangkau psikolog klinis, bidan, dan konselor laktasi kami yang\n"
                 "berpengalaman mendampingi ibu pascapersalinan.",
                 40, 92, 720, 46, size=10.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=155.0)
    builder.button(pro, "CTA", "Lihat Direktori & Jadwalkan Sesi  >", 1000, 55,
                   240, 48, PALETTE["rose"], PALETTE["white"], None, 11,
                   radius=24)


def mood_screen(builder, page):
    screen = builder.frame(page, "03 - Mood Check-In", 3200, 0, 1440, 1320,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, "Mood Check-In")
    page_header(builder, screen, "Mood Check-In Harian",
                "Pencatatan sederhana dan cepat untuk memahami ritme emosi serta memetakan faktor pemicunya.")

    left = panel(builder, screen, "Mood Form", 80, 210, 680, 1010, 24)
    builder.text(left, "Step One", "1. Pilih Suasana Hati Saat Ini", 30, 28,
                 600, 28, size=17, weight="Bold", fill=PALETTE["rose"])
    builder.text(left, "Step One Sub",
                 "Bagaimana kondisi tubuh dan pikiran Ibu Rani saat ini?",
                 30, 60, 600, 20, size=10.5, weight="Regular",
                 fill=PALETTE["muted"])

    moods = [
        ("Senang / Tenang", "Pikiran jernih, merasa damai"),
        ("Cukup Netral", "Biasa saja, menjalani rutinitas"),
        ("Lelah / Kewalahan", "Kurang tidur, energi terkuras"),
        ("Cemas / Khawatir", "Banyak pikiran, overthinking"),
        ("Sedih / Rapuh", "Mudah menangis, butuh pelukan"),
    ]
    for index, (title, sub) in enumerate(moods):
        y = 100 + index * 78
        active = index == 2
        row = builder.frame(left, "Mood Row " + str(index), 30, y, 620, 68,
                            PALETTE["soft"] if active else PALETTE["card"],
                            PALETTE["rose"] if active else PALETTE["border"], 14)
        builder.circle(row, "Mood Icon", 16, 14, 40,
                       PALETTE["cherry"] if active else PALETTE["blush"],
                       str(index + 1), PALETTE["rose"], 11)
        builder.text(row, "Mood Title", title, 70, 13, 330, 22, size=11.5,
                     weight="SemiBold",
                     fill=PALETTE["rose"] if active else PALETTE["dark"])
        builder.text(row, "Mood Sub", sub, 70, 36, 400, 18, size=9.5,
                     weight="Regular", fill=PALETTE["muted"])
        if active:
            builder.text(row, "Selected", "Dipilih", 530, 24, 70, 20, size=9.5,
                         weight="SemiBold", fill=PALETTE["rose"],
                         align="right")

    builder.text(left, "Step Two", "2. Faktor Pemicu (Bisa Pilih Lebih dari Satu)",
                 30, 515, 620, 26, size=17, weight="Bold",
                 fill=PALETTE["rose"])
    factors = [
        ("Kurang Tidur", 150, 30, 548),
        ("Menyusui Sakit", 150, 190, 548),
        ("Dukungan Pasangan", 170, 350, 548),
        ("Nyeri Jahitan", 140, 30, 592),
        ("Bayi Kolik / Rewel", 165, 180, 592),
        ("Pekerjaan Rumah", 150, 355, 592),
        ("Tamu Berkunjung", 150, 30, 636),
    ]
    for index, (label, width, x, y) in enumerate(factors):
        chip(builder, left, "Factor " + str(index), label, x, y, width, 32,
             active=index in (0, 1, 4))

    builder.text(left, "Step Three", "3. Catatan Refleksi Singkat (Opsional)",
                 30, 690, 620, 26, size=17, weight="Bold",
                 fill=PALETTE["rose"])
    note = builder.frame(left, "Mood Note", 30, 726, 620, 130,
                         PALETTE["card"], PALETTE["border"], 12)
    builder.text(note, "Placeholder",
                 "Tuliskan jika ada momen spesifik atau keluhan fisik yang ingin Ibu ingat hari ini...",
                 16, 14, 580, 40, size=10.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=150.0)
    builder.button(left, "Save Mood", "Simpan Catatan Mood Hari Ini", 30, 886,
                   620, 50, PALETTE["rose"], PALETTE["white"], None, 11.5,
                   radius=25)

    right = panel(builder, screen, "Mood History", 800, 210, 560, 930, 24)
    builder.text(right, "History Title", "Riwayat 7 Hari Terakhir", 30, 28,
                 360, 30, size=17, weight="Bold", fill=PALETTE["rose"])
    builder.pill(right, "Week Badge", "Minggu ke-2", 410, 28, 120, 28,
                 PALETTE["soft"], PALETTE["rose"], None, 9)

    history = [
        ("Hari ini, 11 Nov", "14:20 WIB", "Lelah / Kewalahan",
         "Kurang Tidur, Bayi Kolik", "Terbangun 4 kali semalam, butuh tidur siang."),
        ("Kemarin, 10 Nov", "09:15 WIB", "Senang / Tenang",
         "Dukungan Pasangan", "Suami membantu menggendong saat subuh."),
        ("Senin, 09 Nov", "11:00 WIB", "Cukup Netral",
         "Menyusui Sakit", "Mulai mencoba posisi menyusui menyamping."),
        ("Minggu, 08 Nov", "21:30 WIB", "Cemas / Khawatir",
         "Bayi Kolik, Nyeri Jahitan", "Menangis tersedu-sedu karena bingung bayi menangis terus."),
        ("Sabtu, 07 Nov", "15:45 WIB", "Lelah / Kewalahan",
         "Pekerjaan Rumah, Tamu", "Terlalu banyak kerabat datang, energi terkuras habis."),
    ]
    for index, (date, time, mood, tags, note_text) in enumerate(history):
        y = 94 + index * 104
        row = builder.frame(right, "History " + str(index), 30, y, 500, 96,
                            PALETTE["card"], PALETTE["border"], 14)
        builder.text(row, "Date", date, 16, 10, 200, 18, size=9.5,
                     weight="SemiBold", fill=PALETTE["dark"])
        builder.text(row, "Time", time, 360, 10, 120, 18, size=8.5,
                     weight="Medium", fill=PALETTE["muted"], align="right")
        builder.text(row, "Mood", mood, 16, 30, 280, 18, size=9.5,
                     weight="SemiBold", fill=PALETTE["rose"])
        builder.text(row, "Tags", tags, 16, 50, 360, 16, size=8,
                     weight="Medium", fill=PALETTE["muted"])
        builder.text(row, "Note", note_text, 16, 68, 450, 20, size=7.5,
                     weight="Regular", fill=PALETTE["muted"])

    insight = builder.frame(right, "Insight Box", 30, 654, 500, 240,
                            PALETTE["card"], PALETTE["border"], 14)
    builder.circle(insight, "Insight Icon", 14, 14, 24, PALETTE["soft"], "i",
                   PALETTE["rose"], 10)
    builder.text(insight, "Insight Title", "Catatan Pola Kesejahteraan Ibu",
                 48, 18, 400, 20, size=10, weight="Bold",
                 fill=PALETTE["dark"])
    insights = [
        "Kelelahan tertinggi tercatat saat si kecil terbangun lebih dari 3 kali di malam hari.",
        "Tingkat kecemasan menurun signifikan ketika Ibu menyempatkan relaksasi napas 3 menit di siang hari.",
        "Tidak apa-apa meminta pasangan atau keluarga menggantikan menggendong bayi selama 30 menit.",
    ]
    for index, text in enumerate(insights):
        y = 50 + index * 58
        builder.circle(insight, "Dot", 18, y + 6, 5, PALETTE["rose"])
        builder.text(insight, "Insight " + str(index), text, 32, y, 448, 50,
                     size=8.5, weight="Regular", fill=PALETTE["muted"],
                     line_height=155.0)


def journal_screen(builder, page):
    screen = builder.frame(page, "04 - Daily Journal", 4800, 0, 1440, 1170,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, "Daily Journal")
    page_header(builder, screen, "Daily Journal (Ruang Curahan Hati Privat)",
                "Tempat yang sepenuhnya aman dan tertutup untuk mengekspresikan segala bentuk rasa lelah, haru, maupun cemas tanpa takut dihakimi.")

    left = panel(builder, screen, "Journal Editor", 80, 210, 720, 800, 24)
    lock = builder.frame(left, "Lock Indicator", 30, 26, 660, 38,
                         PALETTE["card"], PALETTE["border"], 12)
    builder.circle(lock, "Lock Icon", 12, 9, 20, PALETTE["soft"], "L",
                   PALETTE["rose"], 8)
    builder.text(lock, "Lock Text",
                 "Terenkripsi & Hanya Dapat Dilihat oleh Ibu Rani",
                 40, 10, 540, 18, size=9.5, weight="Medium",
                 fill=PALETTE["rose"])

    builder.text(left, "Title Label", "Judul Refleksi", 30, 86, 300, 20,
                 size=10, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, left, "Title Input", 30, 110, 660, 46,
              "Hari ke-12: Belajar melepaskan ekspektasi menjadi ibu sempurna")

    builder.text(left, "Tags Label", "Pilih Tag Perasaan", 30, 176, 300, 20,
                 size=10, weight="SemiBold", fill=PALETTE["dark"])
    tags = [
        ("#lelah", 78, 30, 200, True),
        ("#bersyukur", 96, 118, 200, True),
        ("#cemas", 76, 224, 200, False),
        ("#sayangBayi", 100, 310, 200, True),
        ("#kewalahan", 94, 420, 200, False),
        ("#butuhJeda", 94, 30, 238, True),
    ]
    for index, (label, width, x, y, active) in enumerate(tags):
        chip(builder, left, "Tag " + str(index), label, x, y, width, 30,
             active=active)

    builder.text(left, "Body Label", "Isi Curahan Hati", 30, 286, 300, 20,
                 size=10, weight="SemiBold", fill=PALETTE["dark"])
    body = builder.frame(left, "Body Field", 30, 310, 660, 320,
                         PALETTE["card"], PALETTE["border"], 12)
    builder.text(body, "Body Text",
                 "Hari ini tubuh terasa begitu lelah, tapi ketika melihat senyum kecil si bayi\n"
                 "saat digendong, ada rasa hangat yang susah dijelaskan.\n\n"
                 "Terkadang aku merasa bersalah saat ingin beristirahat sejenak dan menyerahkan\n"
                 "bayi ke suami, tapi aku perlahan belajar bahwa ibu yang bahagia dan cukup\n"
                 "istirahat adalah yang terbaik untuk bayi.\n\n"
                 "Hari ini aku berhasil makan siang tepat waktu dan melakukan relaksasi napas\n"
                 "3 menit. Kemajuan kecil yang patut dirayakan.",
                 16, 14, 620, 286, size=10.5, weight="Regular",
                 fill=PALETTE["dark"], line_height=170.0)
    builder.button(left, "Save Journal", "Simpan ke Jurnal Pribadi", 30, 660, 220,
                   48, PALETTE["rose"], PALETTE["white"], None, 11.5, radius=24)
    builder.button(left, "Reset Journal", "Batal / Reset", 266, 660, 160, 48,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 11.5,
                   radius=24)

    right = panel(builder, screen, "Journal List", 840, 210, 520, 880, 24)
    builder.text(right, "List Title", "Daftar Jurnal Tersimpan", 30, 28, 330, 28,
                 size=17, weight="Bold", fill=PALETTE["rose"])
    builder.pill(right, "Count", "3 Catatan", 390, 26, 100, 28,
                 PALETTE["soft"], PALETTE["rose"], None, 9)
    search = builder.frame(right, "Search", 30, 80, 460, 44,
                           PALETTE["card"], PALETTE["border"], 12)
    builder.circle(search, "Search Icon", 14, 12, 20, PALETTE["soft"], "?",
                   PALETTE["rose"], 8)
    builder.text(search, "Search Text", "Cari catatan atau tag perasaan...",
                 44, 12, 380, 20, size=10, weight="Regular",
                 fill=PALETTE["muted"])

    journals = [
        ("28 Okt 2026", "#cemas  #lelah",
         "Hari pertama sendirian menjaga bayi saat suami kerja",
         "Rasanya campur aduk dan panik saat bayi menangis tanpa henti. Tapi sore ini aku berhasil menenangkannya dengan gendongan samping..."),
        ("27 Okt 2026", "#lelah  #butuhJeda",
         "Malam yang panjang dan pelajaran tentang kesabaran",
         "Kurang tidur membuat kepalaku pusing. Untung ibu datang membawakan sup hangat dan membiarkanku tidur 2 jam..."),
        ("25 Okt 2026", "#bersyukur  #sayangBayi",
         "Kunjungan pertama ke dokter anak",
         "Berat badan si kecil naik dengan baik. Hati merasa sangat lega mendengar penjelasan dokter..."),
    ]
    for index, (date, tags_text, title, snippet) in enumerate(journals):
        y = 145 + index * 224
        card = builder.frame(right, "Journal Card " + str(index), 30, y, 460,
                             210, PALETTE["card"], PALETTE["border"], 14)
        builder.text(card, "Date", date, 16, 12, 160, 18, size=9,
                     weight="SemiBold", fill=PALETTE["rose"])
        builder.text(card, "Tags", tags_text, 220, 12, 220, 18, size=7.5,
                     weight="Medium", fill=PALETTE["muted"], align="right")
        builder.text(card, "Title", title, 16, 34, 420, 44, size=10,
                     weight="Bold", fill=PALETTE["dark"], line_height=145.0)
        builder.text(card, "Snippet", snippet, 16, 84, 420, 54, size=8.5,
                     weight="Regular", fill=PALETTE["muted"], line_height=155.0)
        builder.text(card, "Read", "Baca Penuh", 16, 174, 100, 18, size=8,
                     weight="SemiBold", fill=PALETTE["rose"])
        builder.text(card, "Delete", "Hapus", 122, 174, 70, 18, size=8,
                     weight="SemiBold", fill=PALETTE["muted"])


def relaxation_screen(builder, page):
    screen = builder.frame(page, "05 - Micro-Relaxation", 6400, 0, 1440, 1260,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, "Micro-Relaxation")
    page_header(builder, screen, "Micro-Relaxation: Jeda 3 Menit Ibu",
                "Dirancang khusus untuk ibu pascapersalinan: singkat, mudah dilakukan di mana saja saat bayi tidur atau sedang menyusui.",
                108, center=True)

    player = builder.frame(screen, "Relaxation Player", 80, 230, 1280, 650,
                           PALETTE["white"], PALETTE["border"], 28,
                           shadow_alpha=0.06, shadow_radius=30)
    builder.pill(player, "Selected Badge", "Sesi Terpilih", 570, 34, 140, 28,
                 PALETTE["soft"], PALETTE["rose"], None, 9)
    builder.text(player, "Player Title",
                 "Pernapasan Tenang & Pelepasan Beban Pundak", 0, 76, 1280, 42,
                 size=27, weight="Bold", fill=PALETTE["rose"], align="center",
                 letter_spacing=-1.0)
    builder.text(player, "Player Meta",
                 "Audio panduan suara lembut dengan instrumen alam pengantar relaksasi",
                 0, 120, 1280, 22, size=10.5, weight="Regular",
                 fill=PALETTE["muted"], align="center")

    builder.circle(player, "Breath Outer", 510, 168, 260, PALETTE["white"],
                   None, None, 24, stroke=PALETTE["rose"])
    builder.circle(player, "Breath Inner", 540, 198, 200, PALETTE["soft"],
                   None, None, 0, stroke=PALETTE["cherry"])
    builder.text(player, "Breath Action", "Tarik Napas", 555, 250, 170, 28,
                 size=20, weight="SemiBold", fill=PALETTE["rose"],
                 align="center")
    builder.text(player, "Breath Timer", "4 Detik", 555, 284, 170, 24, size=13,
                 weight="Medium", fill=PALETTE["muted"], align="center")

    builder.text(player, "Current Time", "00:00", 540, 468, 80, 20, size=10,
                 weight="SemiBold", fill=PALETTE["muted"], align="right")
    builder.text(player, "Time Divider", "/", 632, 468, 20, 20, size=10,
                 weight="Medium", fill=PALETTE["muted"], align="center")
    builder.text(player, "Total Time", "03:00", 660, 468, 80, 20, size=10,
                 weight="SemiBold", fill=PALETTE["muted"])
    builder.rect(player, "Progress Track", 320, 502, 640, 8, PALETTE["border"], 4)
    builder.rect(player, "Progress Fill", 320, 502, 40, 8, PALETTE["rose"], 4)

    builder.button(player, "Rewind", "Mundur 10s", 500, 538, 110, 42,
                   PALETTE["card"], PALETTE["muted"], PALETTE["border"], 10,
                   radius=21)
    builder.circle(player, "Play Button", 620, 532, 54, PALETTE["rose"], ">",
                   PALETTE["white"], 20)
    builder.button(player, "Stop", "Stop", 690, 538, 100, 42,
                   PALETTE["card"], PALETTE["muted"], PALETTE["border"], 10,
                   radius=21)

    builder.text(screen, "Session Title", "Pilihan Sesi Relaksasi 3 Menit Lainnya",
                 80, 930, 700, 30, size=19, weight="Bold",
                 fill=PALETTE["dark"])
    sessions = [
        ("Sesi 1 - 3 Menit", "Pernapasan Tenang & Beban Pundak",
         "Fokus melepaskan ketegangan di area leher dan bahu akibat posisi menggendong.",
         "Sedang Dipilih", True),
        ("Sesi 2 - 3 Menit", "Afirmasi Kebaikan Diri Ibu Baru",
         "Kalimat penerimaan diri dan afirmasi hangat untuk meredakan rasa bersalah.",
         "Putar Sesi Ini", False),
        ("Sesi 3 - 3 Menit", "Relaksasi Menjelang Power Nap",
         "Menurunkan frekuensi gelombang otak agar tidur 30 menit terasa sangat menyegarkan.",
         "Putar Sesi Ini", False),
    ]
    for index, (badge_text, title, desc, action, active) in enumerate(sessions):
        x = 80 + index * 430
        card = builder.frame(screen, "Session " + str(index), x, 982, 400, 190,
                             PALETTE["white"], PALETTE["rose"] if active else PALETTE["border"],
                             20, shadow_alpha=0.05, shadow_radius=22)
        builder.pill(card, "Session Badge", badge_text, 20, 20, 116, 26,
                     PALETTE["soft"], PALETTE["rose"], None, 8)
        builder.text(card, "Session Title", title, 20, 58, 360, 40, size=13,
                     weight="Bold", fill=PALETTE["dark"], line_height=140.0)
        builder.text(card, "Session Desc", desc, 20, 106, 360, 46, size=9.5,
                     weight="Regular", fill=PALETTE["muted"], line_height=155.0)
        builder.text(card, "Session Action", ">  " + action, 20, 160, 300, 20,
                     size=9, weight="SemiBold", fill=PALETTE["rose"])


def education_screen(builder, page):
    screen = builder.frame(page, "06 - Edukasi", 8000, 0, 1440, 1180,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, "Edukasi")
    page_header(builder, screen, "Pusat Informasi & Edukasi Pascapersalinan",
                "Kumpulan artikel berbasis bukti medis dan literatur kesehatan perinatal yang disajikan dengan bahasa empatik dan mudah dipahami.")

    search = builder.frame(screen, "Article Search", 80, 208, 1280, 48,
                           PALETTE["white"], PALETTE["border"], 12,
                           shadow_alpha=0.04, shadow_radius=18)
    builder.circle(search, "Search Icon", 16, 14, 20, PALETTE["soft"], "?",
                   PALETTE["rose"], 8)
    builder.text(search, "Search Placeholder",
                 "Cari topik artikel (contoh: baby blues, luka jahitan, asi, overthinking)...",
                 46, 14, 1100, 20, size=10.5, weight="Regular",
                 fill=PALETTE["muted"])

    pills = [
        ("Semua Kategori", 140, 0, True),
        ("Kesehatan Mental", 160, 152, False),
        ("Pemulihan Fisik", 152, 324, False),
        ("Menyusui & Bayi", 150, 488, False),
        ("Perawatan Diri & Nutrisi", 190, 650, False),
    ]
    for index, (label, width, offset, active) in enumerate(pills):
        x = 80 + offset
        chip(builder, screen, "Category " + str(index), label, x, 270, width,
             34, active)

    articles = [
        ("Kesehatan Mental", "4 mnt baca  |  dr. Sarah Anindya, Sp.OG",
         "Mengenali Baby Blues vs Depresi Pascapersalinan (PPD)",
         "Kapan tangisan emosional di minggu awal merupakan proses adaptasi normal, dan kapan memerlukan konsultasi profesional?",
         PALETTE["blush"]),
        ("Pemulihan Fisik", "5 mnt baca  |  Bidan Nurul Aisyah",
         "Panduan Merawat Luka Jahitan Caesar & Normal di Rumah",
         "Tips menjaga higiene area luka, posisi tidur yang mengurangi rasa nyeri, serta tanda bahaya infeksi yang patut diwaspadai.",
         PALETTE["sunset"]),
        ("Kesehatan Mental", "3 mnt baca  |  Rina Kusuma, M.Psi.",
         "Mengatasi Rasa Bersalah Ketika Merasa Kewalahan & Butuh Jeda",
         "Membedah fenomena overthinking ibu baru dan bagaimana mengajak pasangan terlibat tanpa merasa menjadi beban.",
         PALETTE["cherry"]),
        ("Menyusui & Bayi", "4 mnt baca  |  Bidan Nurul Aisyah",
         "Posisi Menyusui yang Ergonomis & Nyaman untuk Punggung",
         "Mencegah puting lecet dan pegal pinggang dengan penopang bantal serta pelekatan mulut bayi yang tepat.",
         PALETTE["blush"]),
        ("Perawatan Diri & Nutrisi", "3 mnt baca  |  Tim Nutrisi Postpartum Care",
         "Pola Makan Pemulih Energi & Pelancar ASI Alami",
         "Kombinasi makanan kaya zat besi, protein, dan hidrasi optimal tanpa perlu diet ketat yang melelahkan.",
         PALETTE["sunset"]),
        ("Kesehatan Mental", "4 mnt baca  |  Rina Kusuma, M.Psi.",
         "Kapan Waktu yang Tepat Menghubungi Tenaga Profesional?",
         "Tolak ukur objektif kapan ibu perlu menjadwalkan konseling psikologis atau pemeriksaan medis lanjutan.",
         PALETTE["cherry"]),
    ]
    for index, (cat, meta, title, snippet, tint) in enumerate(articles):
        col = index % 3
        row = index // 3
        x = 80 + col * 430
        y = 340 + row * 375
        card = panel(builder, screen, "Article " + str(index), x, y, 400, 350, 20)
        thumb = builder.frame(card, "Thumb", 0, 0, 400, 106, tint, None, 20)
        builder.pill(thumb, "Category", cat, 20, 22, 150, 26,
                     PALETTE["white"], PALETTE["rose"], None, 8)
        builder.text(card, "Meta", meta, 20, 122, 360, 20, size=8.5,
                     weight="Medium", fill=PALETTE["muted"])
        builder.text(card, "Title", title, 20, 148, 360, 58, size=13.5,
                     weight="Bold", fill=PALETTE["dark"], line_height=140.0)
        builder.text(card, "Snippet", snippet, 20, 214, 360, 76, size=9.5,
                     weight="Regular", fill=PALETTE["muted"], line_height=155.0)
        builder.text(card, "Read", "Baca Panduan Lengkap  >", 20, 312, 250, 20,
                     size=9.5, weight="SemiBold", fill=PALETTE["rose"])


def help_screen(builder, page):
    screen = builder.frame(page, "07 - Bantuan Profesional", 9600, 0, 1440, 1280,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, "Bantuan Profesional")
    page_header(builder, screen, "Direktori Bantuan & Konsultasi Profesional",
                "Akses langsung ke tenaga profesional terverifikasi: psikolog klinis perinatal, dokter spesialis obstetri, dan bidan konselor laktasi.")

    alert = builder.frame(screen, "Empathy Alert", 80, 200, 1280, 110,
                          PALETTE["card"], PALETTE["sunset"], 16)
    builder.circle(alert, "Alert Icon", 32, 34, 38, PALETTE["soft"], "!",
                   PALETTE["rose"], 16)
    builder.text(alert, "Alert Title",
                 "Ibu Tidak Sendirian: Meminta Bantuan adalah Tanda Kasih & Kekuatan",
                 88, 26, 1120, 24, size=12, weight="Bold",
                 fill=PALETTE["dark"])
    builder.text(alert, "Alert Body",
                 "Jika perasaan sedih, cemas, atau hampa berlangsung lebih dari 2 minggu dan mengganggu aktivitas sehari-hari,\n"
                 "berkonsultasi dengan profesional adalah langkah tepat dan terlindungi kerahasiaannya.",
                 88, 54, 1120, 42, size=10, weight="Regular",
                 fill=PALETTE["muted"], line_height=155.0)

    left = panel(builder, screen, "Professional List", 80, 335, 680, 690, 24)
    builder.text(left, "List Title", "Daftar Tenaga Profesional Berlisensi",
                 30, 28, 560, 28, size=17, weight="Bold", fill=PALETTE["rose"])
    builder.text(left, "List Sub",
                 "Silakan pilih tenaga profesional untuk melihat jadwal dan melakukan reservasi.",
                 30, 60, 600, 20, size=10, weight="Regular",
                 fill=PALETTE["muted"])

    professionals = [
        ("RK", "Rina Kusuma, M.Psi., Psikolog", "Rp 200.000 / sesi",
         "Psikolog Klinis Perinatal & Manajemen Kecemasan Pascasalin",
         "SIP: 1029/PSI/2020  |  Pengalaman 8 Tahun",
         "Video Call   Chat Intensif", "Dipilih", True),
        ("NA", "Bidan Nurul Aisyah, S.Tr.Keb", "Rp 150.000 / sesi",
         "Konselor Laktasi & Perawatan Luka Pemulihan Nifas",
         "KTA IBI: 8841/DKI  |  Pengalaman 12 Tahun",
         "Video Call   Chat WhatsApp", "Pilih", False),
        ("SA", "dr. Sarah Anindya, Sp.OG", "Rp 250.000 / sesi",
         "Konsultasi Kesehatan Fisik Reproduksi & Pasca-Operasi",
         "STR: 3121002341  |  RSUP Fatmawati",
         "Video Call", "Pilih", False),
    ]
    for index, (initials, name, fee, spec, lic, media, action, selected) in enumerate(professionals):
        y = 100 + index * 174
        card = builder.frame(left, "Pro " + str(index), 30, y, 620, 160,
                             PALETTE["soft"] if selected else PALETTE["card"],
                             PALETTE["rose"] if selected else PALETTE["border"],
                             14)
        builder.circle(card, "Avatar", 18, 20, 52,
                       PALETTE["blush"] if selected else PALETTE["card"],
                       initials, PALETTE["rose"], 12,
                       stroke=PALETTE["border"])
        builder.text(card, "Name", name, 84, 16, 330, 22, size=11,
                     weight="Bold", fill=PALETTE["dark"])
        builder.text(card, "Fee", fee, 380, 16, 220, 22, size=9.5,
                     weight="SemiBold", fill=PALETTE["rose"], align="right")
        builder.text(card, "Spec", spec, 84, 42, 500, 20, size=9,
                     weight="Medium", fill=PALETTE["muted"])
        builder.text(card, "Lic", lic, 84, 62, 500, 18, size=8.5,
                     weight="Regular", fill=PALETTE["muted"])
        builder.text(card, "Media", media, 84, 94, 310, 18, size=8,
                     weight="Medium", fill=PALETTE["dark"])
        builder.button(card, "Action", action, 470, 100, 130, 36,
                       PALETTE["rose"] if selected else PALETTE["white"],
                       PALETTE["white"] if selected else PALETTE["rose"],
                       None if selected else PALETTE["border"], 9,
                       radius=18)

    right = panel(builder, screen, "Booking Form", 800, 335, 560, 900, 24)
    builder.text(right, "Form Title", "Formulir Permintaan Sesi Konsultasi",
                 30, 28, 500, 28, size=17, weight="Bold", fill=PALETTE["rose"])
    builder.text(right, "Form Sub", "Konfirmasi jadwal dan topik yang ingin didiskusikan.",
                 30, 60, 500, 20, size=10, weight="Regular",
                 fill=PALETTE["muted"])
    chosen = builder.frame(right, "Chosen Professional", 30, 96, 500, 76,
                           PALETTE["card"], PALETTE["border"], 12)
    builder.text(chosen, "Label", "Tenaga Terpilih:", 16, 12, 200, 18, size=8.5,
                 weight="Medium", fill=PALETTE["muted"])
    builder.text(chosen, "Name", "Rina Kusuma, M.Psi., Psikolog", 16, 30, 460,
                 20, size=9.5, weight="Bold", fill=PALETTE["rose"])
    builder.text(chosen, "Spec", "Psikolog Klinis Perinatal", 16, 50, 400, 18,
                 size=8.5, weight="Regular", fill=PALETTE["muted"])

    builder.text(right, "Date Label", "Pilih Tanggal Sesi", 30, 192, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, right, "Date Input", 30, 216, 500, 46, "12 / 11 / 2026")
    builder.text(right, "Time Label", "Pilih Jam Konsultasi", 30, 282, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    slots = [("10:00 WIB", 30, 110, False), ("14:00 WIB", 152, 110, True),
             ("16:30 WIB", 274, 110, False), ("19:30 WIB", 396, 104, False)]
    for index, (label, x, width, active) in enumerate(slots):
        chip(builder, right, "Time " + str(index), label, x, 306, width, 36,
             active)
    builder.text(right, "Media Label", "Media Komunikasi", 30, 362, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, right, "Media Input", 30, 386, 500, 46,
              "Google Meet (Panggilan Video)")
    builder.text(right, "Notes Label", "Keluhan atau Topik yang Ingin Disampaikan",
                 30, 452, 480, 20, size=9.5, weight="SemiBold",
                 fill=PALETTE["dark"])
    notes = builder.frame(right, "Booking Notes", 30, 476, 500, 100,
                          PALETTE["card"], PALETTE["border"], 12)
    builder.text(notes, "Placeholder",
                 "Contoh: Merasa sangat cemas setiap kali menjelang malam dan kesulitan membagi waktu istirahat...",
                 16, 14, 460, 48, size=9.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=150.0)
    builder.button(right, "Submit Booking", "Kirim Permintaan Sesi Konsultasi",
                   30, 600, 500, 48, PALETTE["rose"], PALETTE["white"], None,
                   10.5, radius=24)

    builder.text(right, "Status Title", "Status Permintaan Sesi Terkini", 30, 680,
                 400, 24, size=11.5, weight="Bold", fill=PALETTE["dark"])
    status = builder.frame(right, "Booking Status", 30, 712, 500, 154,
                           PALETTE["card"], PALETTE["border"], 12)
    builder.pill(status, "Status Badge", "Menunggu Konfirmasi", 14, 14, 150, 26,
                 PALETTE["soft"], PALETTE["rose"], None, 8)
    builder.text(status, "Status Date", "12 Nov 2026 - 14:00 WIB", 250, 18, 230,
                 18, size=8.5, weight="Medium", fill=PALETTE["muted"],
                 align="right")
    builder.text(status, "Status Name", "Rina Kusuma, M.Psi., Psikolog", 14, 50,
                 460, 20, size=9.5, weight="Bold", fill=PALETTE["rose"])
    builder.text(status, "Status Desc",
                 "Media: Google Meet Video Call. Tenaga profesional akan mengonfirmasi\n"
                 "sesi dalam waktu maksimal 2 jam.",
                 14, 78, 460, 40, size=8.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=155.0)


def profile_screen(builder, page):
    screen = builder.frame(page, "08 - Profil", 11200, 0, 1440, 1120,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, active=None, profile_active=True)
    page_header(builder, screen, "Profil Saya",
                "Kelola informasi akun, preferensi pendampingan, dan pengaturan privasi Anda.")

    left = panel(builder, screen, "Profile Summary", 80, 210, 320, 520, 22)
    builder.circle(left, "Avatar XL", 118, 36, 84, PALETTE["rose"], "RA",
                   PALETTE["white"], 26)
    builder.text(left, "Name", "Rani Anindita", 0, 136, 320, 26, size=17,
                 weight="Bold", fill=PALETTE["dark"], align="center")
    builder.text(left, "Role", "Ibu Pascasalin", 0, 166, 320, 20, size=10.5,
                 weight="Regular", fill=PALETTE["muted"], align="center")
    builder.pill(left, "Phase", "Hari ke-12 Pemulihan", 80, 194, 160, 28,
                 PALETTE["soft"], PALETTE["rose"], None, 8.5)
    builder.line(left, "Divider", 30, 246, 260)
    stats = [("12", "Hari nifas"), ("7", "Jurnal"), ("5", "Mood log")]
    for index, (value, label) in enumerate(stats):
        x = 30 + index * 87
        builder.text(left, "Stat " + str(index), value, x, 268, 80, 26, size=18,
                     weight="Bold", fill=PALETTE["rose"], align="center")
        builder.text(left, "Stat Label " + str(index), label, x, 296, 80, 18,
                     size=8, weight="Medium", fill=PALETTE["muted"],
                     align="center")
    builder.line(left, "Divider Two", 30, 334, 260)
    builder.button(left, "Edit Profile", "Edit Profile", 30, 356, 260, 46,
                   PALETTE["rose"], PALETTE["white"], None, 11, radius=23)
    builder.text(left, "Privacy Note",
                 "Data profil dan catatan pribadi Anda tersimpan secara privat.",
                 24, 412, 272, 34, size=8.5, weight="Regular",
                 fill=PALETTE["muted"], align="center", line_height=150.0)

    info = panel(builder, screen, "Account Info", 430, 210, 930, 430, 22)
    builder.text(info, "Info Title", "Informasi Akun", 30, 26, 400, 28,
                 size=17, weight="Bold", fill=PALETTE["rose"])
    builder.text(info, "Info Sub",
                 "Detail dasar yang digunakan untuk pendampingan harian Anda.",
                 30, 58, 500, 20, size=10, weight="Regular",
                 fill=PALETTE["muted"])
    builder.button(info, "Change", "Ubah", 800, 28, 100, 34,
                   PALETTE["white"], PALETTE["rose"], PALETTE["border"], 9,
                   radius=17)
    fields = [
        ("Nama Lengkap", "Rani Anindita", 30, 100),
        ("Alamat Email", "rani.anindita@email.com", 470, 100),
        ("Peran Akun", "Ibu Pascasalin", 30, 212),
        ("Tanggal Persalinan", "30 Oktober 2026", 470, 212),
        ("Fase Pemulihan", "Fase Adaptasi Awal", 30, 324),
        ("Bergabung Sejak", "November 2026", 470, 324),
    ]
    for index, (label, value, x, y) in enumerate(fields):
        box = builder.frame(info, "Info " + str(index), x, y, 430, 88,
                            PALETTE["card"], PALETTE["border"], 12)
        builder.text(box, "Label", label, 16, 20, 380, 18, size=9,
                     weight="Medium", fill=PALETTE["muted"])
        builder.text(box, "Value", value, 16, 44, 380, 24, size=11,
                     weight="SemiBold", fill=PALETTE["dark"])

    pref = panel(builder, screen, "Preferences", 430, 670, 455, 350, 22)
    builder.text(pref, "Title", "Preferensi Pendampingan", 26, 24, 400, 26,
                 size=15, weight="Bold", fill=PALETTE["rose"])
    builder.text(pref, "Sub",
                 "Sesuaikan pengingat dan pengalaman yang paling nyaman untuk Anda.",
                 26, 54, 400, 36, size=9.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=150.0)
    prefs = [
        ("Pengingat mood check-in", "Setiap hari pukul 19.00 WIB", True),
        ("Pengingat jurnal harian", "Setiap hari pukul 21.00 WIB", True),
        ("Ringkasan mingguan", "Rekap mood dan jurnal setiap Minggu", False),
    ]
    for index, (title, sub, on) in enumerate(prefs):
        y = 104 + index * 78
        builder.text(pref, "Pref Title " + str(index), title, 26, y, 330, 20,
                     size=9.5, weight="SemiBold", fill=PALETTE["dark"])
        builder.text(pref, "Pref Sub " + str(index), sub, 26, y + 20, 350, 18,
                     size=8.5, weight="Regular", fill=PALETTE["muted"])
        toggle(builder, pref, 382, y + 4, on)
        if index < 2:
            builder.line(pref, "Pref Line", 26, y + 58, 404)

    privacy = panel(builder, screen, "Privacy", 905, 670, 455, 350, 22)
    builder.text(privacy, "Title", "Privasi & Keamanan", 26, 24, 400, 26,
                 size=15, weight="Bold", fill=PALETTE["rose"])
    builder.text(privacy, "Sub", "Kendali penuh atas data dan akses akun Anda.",
                 26, 54, 400, 20, size=9.5, weight="Regular",
                 fill=PALETTE["muted"])
    rows = [
        ("Jurnal privat", "Hanya Anda yang dapat membaca catatan jurnal.",
         "Aktif", "pill"),
        ("Verifikasi dua langkah", "Tambahkan lapisan keamanan ekstra pada akun.",
         "Atur", "button"),
        ("Unduh data saya", "Minta salinan data mood dan jurnal Anda.",
         "Minta", "button"),
    ]
    for index, (title, sub, action, kind) in enumerate(rows):
        y = 104 + index * 78
        builder.text(privacy, "Privacy Title " + str(index), title, 26, y, 280,
                     20, size=9.5, weight="SemiBold", fill=PALETTE["dark"])
        builder.text(privacy, "Privacy Sub " + str(index), sub, 26, y + 20, 320,
                     18, size=8.5, weight="Regular", fill=PALETTE["muted"])
        if kind == "pill":
            builder.pill(privacy, "Privacy Pill " + str(index), action, 370, y,
                         70, 26, PALETTE["soft"], PALETTE["rose"], None, 8)
        else:
            builder.button(privacy, "Privacy Action " + str(index), action, 370,
                           y, 70, 32, PALETTE["white"], PALETTE["rose"],
                           PALETTE["border"], 8.5, radius=16)
        if index < 2:
            builder.line(privacy, "Privacy Line", 26, y + 58, 404)


def edit_profile_modal(builder, page):
    screen = builder.frame(page, "09 - Edit Profile Modal", 11200, 1120, 1440,
                           780, PALETTE["dark"], None, 0)
    builder.nodes[str(screen)]["fills"] = paint(PALETTE["dark"], 0.45)
    card = builder.frame(screen, "Modal Card", 440, 90, 560, 580,
                         PALETTE["white"], PALETTE["border"], 24,
                         shadow_alpha=0.24, shadow_radius=50)
    builder.text(card, "Modal Category", "Profil Pengguna", 32, 28, 400, 20,
                 size=9, weight="SemiBold", fill=PALETTE["rose"])
    builder.text(card, "Modal Title", "Edit Profile", 32, 52, 400, 34, size=23,
                 weight="Bold", fill=PALETTE["dark"], letter_spacing=-1.0)
    builder.text(card, "Modal Sub",
                 "Perbarui informasi akun Anda. Perubahan akan langsung terlihat di halaman profil.",
                 32, 90, 470, 38, size=10, weight="Regular",
                 fill=PALETTE["muted"], line_height=150.0)
    builder.button(card, "Close", "X", 500, 26, 32, 32, PALETTE["card"],
                   PALETTE["muted"], PALETTE["border"], 10, radius=16)

    builder.text(card, "Name Label", "Nama Lengkap", 32, 146, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, card, "Name Input", 32, 170, 496, 46, "Rani Anindita")
    builder.text(card, "Email Label", "Alamat Email", 32, 236, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, card, "Email Input", 32, 260, 496, 46,
              "rani.anindita@email.com")
    builder.text(card, "Birth Label", "Tanggal Persalinan", 32, 326, 230, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, card, "Birth Input", 32, 350, 234, 46, "30 / 10 / 2026")
    builder.text(card, "Phase Label", "Fase Pemulihan", 294, 326, 230, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, card, "Phase Input", 294, 350, 234, 46,
              "Fase Adaptasi Awal")
    builder.button(card, "Cancel", "Batal", 32, 444, 150, 46, PALETTE["white"],
                   PALETTE["rose"], PALETTE["border"], 11, radius=23)
    builder.button(card, "Save", "Simpan Perubahan", 198, 444, 200, 46,
                   PALETTE["rose"], PALETTE["white"], None, 11, radius=23)


def login_screen(builder, page):
    screen = builder.frame(page, "10 - Login", 12800, 0, 1440, 1040,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, active=None)

    left = builder.frame(screen, "Auth Brand", 80, 120, 560, 740,
                         PALETTE["blush"], None, 24)
    builder.pill(left, "Badge", "Ruang Pendamping Pribadi", 36, 34, 220, 30,
                 PALETTE["white"], PALETTE["rose"], None, 9)
    builder.text(left, "Title", "Selamat Datang\nKembali,\nIbu Hebat.", 36, 92,
                 470, 150, size=36, weight="Bold", fill=PALETTE["dark"],
                 line_height=112.0, letter_spacing=-2.0)
    builder.text(left, "Body",
                 "Masa pascapersalinan adalah perjalanan berharga. Masuk ke akunmu\n"
                 "untuk melanjutkan pencatatan suasana hati, menulis curahan jurnal,\n"
                 "dan mengakses panduan pemulihan harian.",
                 36, 250, 480, 90, size=11, weight="Regular",
                 fill=PALETTE["muted"], line_height=165.0)
    quote = builder.frame(left, "Auth Quote", 36, 374, 480, 196,
                          PALETTE["white"], PALETTE["border"], 16,
                          shadow_alpha=0.04, shadow_radius=18)
    builder.text(quote, "Quote",
                 chr(34) + "Ibu tidak perlu menjadi sempurna untuk menjadi ibu yang luar biasa bagi si kecil.\n"
                 "Rawatlah dirimu sebagaimana engkau merawat buah hatimu." + chr(34),
                 20, 20, 440, 100, size=10.5, weight="Regular",
                 fill=PALETTE["dark"], line_height=165.0)
    builder.text(quote, "Author", "- Komunitas Postpartum Care", 20, 148, 420,
                 20, size=8.5, weight="SemiBold", fill=PALETTE["rose"])
    trust = [
        "Data jurnal refleksi dan mood 100% tersimpan privat",
        "Seluruh informasi edukasi ditinjau oleh tenaga medis",
        "Kepatuhan penuh pada UU Pelindungan Data Pribadi",
    ]
    for index, text in enumerate(trust):
        y = 606 + index * 36
        builder.circle(left, "Trust Dot " + str(index), 38, y + 3, 18,
                       PALETTE["white"], str(index + 1), PALETTE["rose"], 8)
        builder.text(left, "Trust " + str(index), text, 68, y, 440, 24, size=9,
                     weight="Medium", fill=PALETTE["muted"])

    card = builder.frame(screen, "Auth Form", 680, 120, 660, 740,
                         PALETTE["white"], PALETTE["border"], 24,
                         shadow_alpha=0.06, shadow_radius=30)
    builder.text(card, "Auth Title", "Masuk ke Akun Anda", 36, 34, 500, 34,
                 size=24, weight="Bold", fill=PALETTE["rose"],
                 letter_spacing=-1.0)
    builder.text(card, "Auth Sub",
                 "Pilih peran akun dan masukkan kredensial terdaftar.",
                 36, 72, 500, 20, size=10.5, weight="Regular",
                 fill=PALETTE["muted"])
    builder.text(card, "Role Label", "Masuk sebagai", 36, 108, 200, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    roles = [("Ibu Pascasalin", 36, 130, True), ("Tenaga Medis", 228, 130, False),
             ("Admin", 420, 130, False)]
    for index, (label, x, y, active) in enumerate(roles):
        builder.button(card, "Role " + str(index), label, x, y, 180, 42,
                       PALETTE["soft"] if active else PALETTE["white"],
                       PALETTE["rose"] if active else PALETTE["muted"],
                       PALETTE["rose"] if active else PALETTE["border"], 9.5,
                       radius=21)

    builder.text(card, "Email Label", "Alamat Email", 36, 198, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, card, "Login Email", 36, 222, 588, 46,
              "ibu.rani@postpartum.id")
    builder.text(card, "Password Label", "Kata Sandi", 36, 286, 200, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    builder.text(card, "Forgot", "Lupa kata sandi?", 420, 286, 204, 20,
                 size=9, weight="SemiBold", fill=PALETTE["rose"],
                 align="right")
    input_box(builder, card, "Login Password", 36, 310, 588, 46,
              "............")
    builder.circle(card, "Remember", 36, 378, 18, PALETTE["rose"], "v",
                   PALETTE["white"], 8)
    builder.text(card, "Remember Text", "Ingat saya di perangkat desktop ini",
                 62, 378, 400, 20, size=9, weight="Regular",
                 fill=PALETTE["muted"])
    builder.button(card, "Submit Login", "Masuk ke Akun Sekarang  >", 36, 414,
                   588, 50, PALETTE["rose"], PALETTE["white"], None, 11,
                   radius=25)
    builder.text(card, "Switch", "Belum memiliki akun Postpartum Care?  Daftar Akun Baru",
                 36, 486, 588, 20, size=9.5, weight="Medium",
                 fill=PALETTE["muted"], align="center")
    demo = builder.frame(card, "Demo Box", 36, 522, 588, 190,
                         PALETTE["card"], PALETTE["sunset"], 14)
    builder.text(demo, "Demo Title", "Akses Cepat Demo (Pengujian Kebutuhan FR-01):",
                 18, 12, 520, 20, size=9, weight="Bold", fill=PALETTE["dark"])
    demos = ["Demo Akun: Ibu Rani (Hari ke-12)",
             "Demo Akun: Rina Kusuma, M.Psi. (Psikolog)",
             "Demo Akun: Administrator Sistem"]
    for index, label in enumerate(demos):
        builder.button(demo, "Demo " + str(index), label, 18, 40 + index * 44,
                       552, 36, PALETTE["white"], PALETTE["muted"],
                       PALETTE["border"], 8.5, radius=10)


def register_screen(builder, page):
    screen = builder.frame(page, "11 - Register", 14400, 0, 1440, 1040,
                           PALETTE["champagne"], None, 0)
    header(builder, screen, active=None)

    left = builder.frame(screen, "Register Brand", 80, 120, 560, 760,
                         PALETTE["blush"], None, 24)
    builder.pill(left, "Badge", "Mulai Langkah Pertama", 36, 34, 200, 30,
                 PALETTE["white"], PALETTE["rose"], None, 9)
    builder.text(left, "Title", "Daftar Akun\nPostpartum Care", 36, 92, 480,
                 100, size=36, weight="Bold", fill=PALETTE["dark"],
                 line_height=112.0, letter_spacing=-2.0)
    builder.text(left, "Body",
                 "Bergabunglah untuk mendapatkan sarana pendampingan harian yang\n"
                 "memprioritaskan pemulihan fisik dan kesejahteraan mental Ibu.",
                 36, 214, 480, 62, size=11, weight="Regular",
                 fill=PALETTE["muted"], line_height=165.0)
    benefits = [
        ("01", "Mood Check-In & Tren Emosi",
         "Identifikasi faktor pemicu kelelahan harian dan pantau grafik pemulihan."),
        ("02", "Daily Journal Pribadi",
         "Curahkan perasaan secara privat dengan tag emosi tanpa takut dihakimi."),
        ("03", "Micro-Relaxation 3 Menit",
         "Latihan pernapasan sederhana yang ramah waktu bagi ibu menyusui."),
        ("04", "Akses Konsultasi Terverifikasi",
         "Kemudahan reservasi sesi dengan psikolog perinatal dan bidan."),
    ]
    for index, (num, title, body) in enumerate(benefits):
        y = 330 + index * 98
        card = builder.frame(left, "Benefit " + str(index), 36, y, 488, 86,
                             PALETTE["white"], PALETTE["border"], 14)
        builder.circle(card, "Number", 16, 20, 36, PALETTE["soft"], num,
                       PALETTE["rose"], 9)
        builder.text(card, "Benefit Title", title, 66, 14, 380, 22, size=10,
                     weight="Bold", fill=PALETTE["dark"])
        builder.text(card, "Benefit Body", body, 66, 38, 390, 38, size=8.5,
                     weight="Regular", fill=PALETTE["muted"],
                     line_height=150.0)

    card = builder.frame(screen, "Register Form", 680, 120, 660, 760,
                         PALETTE["white"], PALETTE["border"], 24,
                         shadow_alpha=0.06, shadow_radius=30)
    builder.text(card, "Auth Title", "Buat Akun Baru", 36, 34, 500, 34,
                 size=24, weight="Bold", fill=PALETTE["rose"],
                 letter_spacing=-1.0)
    builder.text(card, "Auth Sub", "Lengkapi formulir di bawah ini untuk memulai.",
                 36, 72, 500, 20, size=10.5, weight="Regular",
                 fill=PALETTE["muted"])
    builder.text(card, "Role Label", "Daftar Sebagai:", 36, 108, 200, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    builder.button(card, "Reg Ibu", "Ibu Pascasalin (Utama)", 36, 132, 288, 42,
                   PALETTE["soft"], PALETTE["rose"], PALETTE["rose"], 9.5,
                   radius=21)
    builder.button(card, "Reg Pro", "Tenaga Profesional", 336, 132, 288, 42,
                   PALETTE["white"], PALETTE["muted"], PALETTE["border"], 9.5,
                   radius=21)

    builder.text(card, "Name Label", "Nama Lengkap", 36, 198, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, card, "Reg Name", 36, 222, 588, 46, "Rani Anindita")
    builder.text(card, "Email Label", "Alamat Email", 36, 286, 300, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, card, "Reg Email", 36, 310, 588, 46,
              "rani.anindita@email.com")
    builder.text(card, "Birth Label", "Tanggal Persalinan / Kelahiran Bayi", 36,
                 374, 450, 20, size=9.5, weight="SemiBold",
                 fill=PALETTE["dark"])
    input_box(builder, card, "Reg Birth", 36, 398, 588, 46, "30 / 10 / 2026")
    builder.text(card, "Password Label", "Kata Sandi", 36, 462, 250, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    builder.text(card, "Confirm Label", "Ulangi Kata Sandi", 336, 462, 250, 20,
                 size=9.5, weight="SemiBold", fill=PALETTE["dark"])
    input_box(builder, card, "Reg Password", 36, 486, 276, 46, "............")
    input_box(builder, card, "Reg Confirm", 336, 486, 288, 46, "............")
    builder.circle(card, "Agree", 36, 552, 18, PALETTE["rose"], "v",
                   PALETTE["white"], 8)
    builder.text(card, "Agree Text",
                 "Saya menyetujui Syarat & Ketentuan serta Kebijakan Privasi platform Postpartum Care.",
                 62, 550, 550, 34, size=8.5, weight="Regular",
                 fill=PALETTE["muted"], line_height=150.0)
    builder.button(card, "Submit Register", "Daftar Akun Baru Sekarang  >", 36,
                   596, 588, 50, PALETTE["rose"], PALETTE["white"], None, 11,
                   radius=25)
    builder.text(card, "Switch", "Sudah memiliki akun?  Masuk di Sini", 36, 668,
                 588, 20, size=9.5, weight="Medium", fill=PALETTE["muted"],
                 align="center")


def child_by_name(builder, parent, name):
    for child_id in builder.nodes[str(parent)]["children"]:
        node = builder.nodes[str(child_id)]
        if node.get("name") == name:
            return child_id
    return None


def patch_text(builder, page, path, value):
    current = page
    for name in path:
        current = child_by_name(builder, current, name)
        if current is None:
            return
    node = builder.nodes[str(current)]
    if node.get("type") == "text":
        node["characters"] = value


def refine_landing(builder, page):
    base = ["01 - Landing Page"]
    patch_text(builder, page, base + ["How It Works", "Heading"],
               "Tiga langkah kecil untuk mulai merasa didampingi.")
    patch_text(builder, page, base + ["How It Works", "Sub"],
               "Mulai dari hal sederhana. Tidak perlu sempurna untuk merawat diri.")
    steps = [
        ("Step Card 01", "Daftar dengan tenang",
         "Buat akun dan tentukan fase pemulihan agar panduan yang muncul lebih relevan untukmu."),
        ("Step Card 02", "Ceritakan harimu",
         "Isi mood check-in atau tulis jurnal sebanyak yang kamu mau. Tidak ada penilaian di sini."),
        ("Step Card 03", "Ambil jeda yang tepat",
         "Pilih relaksasi, baca edukasi, atau hubungi profesional ketika kamu butuh dukungan lebih."),
    ]
    for card, title, body in steps:
        patch_text(builder, page, base + ["How It Works", card, "Title"], title)
        patch_text(builder, page, base + ["How It Works", card, "Body"], body)

    patch_text(builder, page, base + ["Professional", "Professional Band", "Title"],
               "Kamu tidak harus menjalani semuanya sendirian.")
    patch_text(builder, page, base + ["Professional", "Professional Band", "Body"],
               "Terhubung dengan psikolog klinis perinatal, bidan konselor laktasi,\n"
               "dan dokter spesialis obstetri yang berpengalaman.")
    patch_text(builder, page, base + ["Professional", "Professional Band", "Professional Card", "Pro Rating"],
               "8 tahun pengalaman  |  Video call  |  Chat intensif")

    stories = [
        ("Story RA", "Rani A.", "Ibu 1 anak - Hari ke-12",
         "\"Mood check-in bikin aku lebih sadar pola lelahku. Ternyata yang aku butuh bukan jadi ibu sempurna, tapi tidur cukup.\""),
        ("Story NS", "Nadia S.", "Ibu 2 anak - Hari ke-34",
         "\"Jurnalnya terasa seperti teman yang tidak menghakimi. Aku bisa menuangkan rasa cemas tanpa takut dianggap lemah.\""),
        ("Story DP", "Dewi P.", "Ibu 1 anak - Hari ke-48",
         "\"Sesi dengan psikolog perinatal membantu banget. Prosesnya jelas, privat, dan aku merasa benar-benar didengar.\""),
    ]
    for card, name, role, quote in stories:
        patch_text(builder, page, base + ["Testimonials", card, "Quote"], quote)
        patch_text(builder, page, base + ["Testimonials", card, "Name"], name)
        patch_text(builder, page, base + ["Testimonials", card, "Role"], role)

    patch_text(builder, page, base + ["CTA", "CTA Band", "CTA Title"],
               "Hari ini, beri dirimu ruang untuk bernapas.")
    patch_text(builder, page, base + ["CTA", "CTA Band", "CTA Body"],
               "Gratis untuk memulai. Catatanmu privat. Kamu bisa berhenti kapan saja.")
    patch_text(builder, page, base + ["CTA", "CTA Band", "CTA Primary", "Label"],
               "Buat Akun Gratis")


def build():
    builder = Builder("Postpartum Care - HTML Match")
    page = builder.page_id
    design_system(builder, page)
    clean_landing_page(builder, page)
    refine_landing(builder, page)
    beranda(builder, page)
    mood_screen(builder, page)
    journal_screen(builder, page)
    relaxation_screen(builder, page)
    education_screen(builder, page)
    help_screen(builder, page)
    profile_screen(builder, page)
    edit_profile_modal(builder, page)
    login_screen(builder, page)
    register_screen(builder, page)
    builder.save("postpartum-care.figcraft")


if __name__ == "__main__":
    build()
