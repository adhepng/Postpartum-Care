// ============================================================
// POSTPARTUM CARE — SHARED DATA & STATE
// ============================================================

const MOOD_OPTIONS = {
  senang: { label: 'Senang / Tenang', detail: 'Pikiran jernih, merasa damai' },
  netral: { label: 'Cukup Netral', detail: 'Biasa saja, menjalani rutinitas' },
  lelah: { label: 'Lelah / Kewalahan', detail: 'Kurang tidur, energi terkuras' },
  cemas: { label: 'Cemas / Khawatir', detail: 'Banyak pikiran, overthinking' },
  sedih: { label: 'Sedih / Rapuh', detail: 'Mudah menangis, butuh pelukan' }
};

const MOOD_ORDER = ['senang', 'netral', 'lelah', 'cemas', 'sedih'];

const MOOD_SCORES = { senang: 5, netral: 4, lelah: 3, cemas: 2, sedih: 1 };

const state = {
  selectedMood: MOOD_OPTIONS.lelah.label,
  selectedMoodKey: 'lelah',
  moodHistory: [
    { date: 'Hari ini, 11 Nov', time: '14:20 WIB', moodKey: 'lelah', tags: 'Kurang Tidur, Bayi Kolik', note: 'Terbangun 4 kali semalam, butuh tidur siang.', color: '#F3CC97' },
    { date: 'Kemarin, 10 Nov', time: '09:15 WIB', moodKey: 'senang', tags: 'Dukungan Pasangan', note: 'Suami membantu menggendong saat subuh.', color: '#FBD9E5' },
    { date: 'Senin, 09 Nov', time: '11:00 WIB', moodKey: 'netral', tags: 'Menyusui Sakit', note: 'Mulai mencoba posisi menyusui menyamping.', color: '#FBF4EB' },
    { date: 'Minggu, 08 Nov', time: '21:30 WIB', moodKey: 'cemas', tags: 'Bayi Kolik, Nyeri Jahitan', note: 'Menangis tersedu-sedu karena bingung bayi menangis terus.', color: '#F7C5D7' },
    { date: 'Sabtu, 07 Nov', time: '15:45 WIB', moodKey: 'lelah', tags: 'Pekerjaan Rumah, Tamu', note: 'Terlalu banyak kerabat datang, energi terkuras habis.', color: '#F3CC97' }
  ],
  journals: [
    {
      id: 1,
      date: '28 Okt 2026',
      title: 'Hari pertama sendirian menjaga bayi saat suami kerja',
      tags: ['#cemas', '#lelah'],
      snippet: 'Rasanya campur aduk dan panik saat bayi menangis tanpa henti. Tapi sore ini aku berhasil menenangkannya dengan gendongan samping...',
      full: 'Rasanya campur aduk dan panik saat bayi menangis tanpa henti. Tapi sore ini aku berhasil menenangkannya dengan gendongan samping. Aku sadar tidak semua hal bisa sempurna, dan itu wajar.'
    },
    {
      id: 2,
      date: '27 Okt 2026',
      title: 'Malam yang panjang dan pelajaran tentang kesabaran',
      tags: ['#lelah', '#butuhJeda'],
      snippet: 'Kurang tidur membuat kepalaku pusing. Untung ibu datang membawakan sup hangat dan membiarkanku tidur 2 jam...',
      full: 'Kurang tidur membuat kepalaku pusing. Untung ibu datang membawakan sup hangat dan membiarkanku tidur 2 jam. Meminta bantuan ternyata melegakan, bukan tanda kegagalan.'
    },
    {
      id: 3,
      date: '25 Okt 2026',
      title: 'Kunjungan pertama ke dokter anak',
      tags: ['#bersyukur', '#sayangBayi'],
      snippet: 'Berat badan si kecil naik dengan baik. Hati merasa sangat lega mendengar penjelasan dokter...',
      full: 'Berat badan si kecil naik dengan baik. Hati merasa sangat lega mendengar penjelasan dokter. Perjuanganku menyusui berjam-jam ternyata tidak sia-sia.'
    }
  ],
  articles: [
    {
      id: 0,
      title: 'Mengenali Baby Blues vs Depresi Pascapersalinan (PPD)',
      category: 'Mental',
      catLabel: 'Kesehatan Mental',
      author: 'dr. Sarah Anindya, Sp.OG',
      readTime: '4 mnt baca',
      snippet: 'Kapan tangisan emosional di minggu awal merupakan proses adaptasi normal, dan kapan memerlukan konsultasi profesional?',
      content: `
        <p>Setelah melahirkan, hampir 80% ibu mengalami apa yang disebut <strong>Baby Blues</strong>. Kondisi ini dipicu oleh penurunan drastis hormon estrogen dan progesteron setelah persalinan, ditambah dengan kelelahan fisik luar biasa dan penyesuaian peran baru.</p>
        <h4>Ciri Khas Baby Blues:</h4>
        <p>• Muncul pada hari ke-3 hingga ke-5 setelah persalinan.<br>
        • Ditandai dengan suasana hati yang mudah berubah, menangis tiba-tiba tanpa sebab jelas, rasa cemas, dan lelah.<br>
        • <em>Penting:</em> Gejala ini biasanya mereda secara alami dalam 10 hingga 14 hari seiring tubuh beradaptasi dan ibu mendapat istirahat yang cukup.</p>
        <h4>Kapan Disebut Postpartum Depression (PPD)?</h4>
        <p>Jika perasaan sedih mendalam, kehilangan minat, rasa bersalah berlebih, atau ketakutan bahwa diri sendiri tidak mampu mengurus bayi bertahan <strong>lebih dari 2 minggu</strong>, kondisi ini mengarah pada Depresi Pascapersalinan. Ini adalah kondisi medis nyata yang dapat diobati, bukan kelemahan iman atau kegagalan menjadi seorang ibu.</p>
        <p><em>Rekomendasi:</em> Jangan ragu mengkomunikasikan apa yang Ibu rasakan kepada pasangan, keluarga, atau membuat janji temu dengan psikolog perinatal melalui direktori bantuan kami.</p>
      `
    },
    {
      id: 1,
      title: 'Panduan Merawat Luka Jahitan Caesar & Normal di Rumah',
      category: 'Fisik',
      catLabel: 'Pemulihan Fisik',
      author: 'Bidan Nurul Aisyah, S.Tr.Keb',
      readTime: '5 mnt baca',
      snippet: 'Tips menjaga higiene area luka, posisi tidur yang mengurangi rasa nyeri, serta tanda bahaya infeksi yang patut diwaspadai.',
      content: `
        <p>Proses penyembuhan luka pascapersalinan, baik robekan perineum (persalinan normal) maupun sayatan operasi caesar, membutuhkan waktu rata-rata 4 hingga 6 minggu untuk pemulihan jaringan secara optimal.</p>
        <h4>Perawatan Luka Caesar:</h4>
        <p>• Jaga luka sayatan tetap bersih dan kering. Hindari menggosok area jahitan saat mandi.<br>
        • Gunakan pakaian longgar berbahan katun lembut yang tidak menekan garis luka.<br>
        • Topang perut dengan bantal kecil saat batuk atau tertawa untuk mengurangi tarikan pada otot dinding perut.</p>
        <h4>Perawatan Luka Normal (Perineum):</h4>
        <p>• Bersihkan dengan air bersih hangat dari arah depan ke belakang setiap selesai buang air.<br>
        • Keringkan perlahan dengan cara ditepuk-tepuk memakai kain kassa atau handuk bersih lembut.<br>
        • Ganti pembalut nifas secara teratur setiap 3-4 jam untuk mencegah kelembapan berlebih.</p>
        <h4>Tanda Bahaya yang Harus Segera Diperiksakan:</h4>
        <p>Segera hubungi bidan atau dokter jika terdapat demam >38°C, kemerahan yang meluas, nanah atau cairan berbau tajam keluar dari luka, atau nyeri perut hebat yang tidak mereda dengan obat pereda nyeri.</p>
      `
    },
    {
      id: 2,
      title: 'Mengatasi Rasa Bersalah Ketika Merasa Kewalahan & Butuh Jeda',
      category: 'Mental',
      catLabel: 'Kesehatan Mental',
      author: 'Rina Kusuma, M.Psi., Psikolog',
      readTime: '3 mnt baca',
      snippet: 'Membedah fenomena overthinking ibu baru dan bagaimana mengajak pasangan terlibat tanpa merasa menjadi beban.',
      content: `
        <p>Salah satu beban paling berat yang sering dipikul diam-diam oleh ibu baru adalah <em>mom guilt</em> atau rasa bersalah. Rasa bersalah muncul saat merasa lelah menggendong, ingin mandi lebih dari 5 menit, atau merasa belum bisa mencintai bayi secara instan.</p>
        <h4>Mengapa Rasa Bersalah Muncul?</h4>
        <p>Ekspektasi sosial di media sering kali melukiskan masa nifas sebagai momen yang selalu bahagia dan estetik. Padahal, realitanya penuh dengan darah nifas, kurang tidur, puting lecet, dan kekacauan jadwal.</p>
        <h4>Langkah Praktis Melepaskan Beban:</h4>
        <p>1. <strong>Ubah Pola Pikir:</strong> Mengambil jeda 15 menit bukan berarti menelantarkan bayi, melainkan mengisi ulang energimu agar tidak kelelahan mental.<br>
        2. <strong>Bagi Tugas Secara Spesifik:</strong> Alih-alih berkata "bantu aku dong", katakan pada pasangan: "Tolong gendong bayi selama 30 menit ke depan, aku butuh tidur sejenak". Pasangan sering kali ingin membantu tetapi bingung apa yang harus dilakukan.<br>
        3. <strong>Praktikkan Self-Compassion:</strong> Katakan pada dirimu: "Aku sedang belajar menjadi ibu baru, sama seperti bayiku yang sedang belajar hidup di dunia ini."</p>
      `
    },
    {
      id: 3,
      title: 'Posisi Menyusui yang Ergonomis & Nyaman untuk Punggung',
      category: 'Laktasi',
      catLabel: 'Menyusui & Bayi',
      author: 'Bidan Nurul Aisyah, S.Tr.Keb',
      readTime: '4 mnt baca',
      snippet: 'Mencegah puting lecet dan pegal pinggang dengan penopang bantal serta pelekatan mulut bayi yang tepat.',
      content: `
        <p>Nyeri punggung bawah dan leher kaku adalah keluhan paling sering dialami ibu menyusui karena posisi membungkuk saat menyodorkan payudara ke mulut bayi.</p>
        <h4>Kunci Utama Pelekatan & Ergonomi:</h4>
        <p>• <strong>Bawa Bayi ke Payudara, Bukan Payudara ke Bayi:</strong> Gunakan bantal menyusui atau tumpukan bantal di bawah lengan agar tinggi bayi sejajar dengan puting susu tanpa Ibu perlu membungkuk.<br>
        • <strong>Sandaran Punggung yang Kokoh:</strong> Selalu duduk di kursi atau tempat tidur dengan punggung tertopang tegak dan kaki menapak lantai atau bangku kecil.<br>
        • <strong>Posisi Side-Lying (Berbaring Miring):</strong> Posisi ini sangat dianjurkan untuk menyusui di malam hari atau bagi ibu yang baru menjalani operasi caesar, karena tidak memberikan beban pada luka perut.</p>
      `
    },
    {
      id: 4,
      title: 'Pola Makan Pemulih Energi & Pelancar ASI Alami',
      category: 'Nutrisi',
      catLabel: 'Perawatan Diri & Nutrisi',
      author: 'Tim Nutrisi Postpartum Care',
      readTime: '3 mnt baca',
      snippet: 'Kombinasi makanan kaya zat besi, protein, dan hidrasi optimal tanpa perlu diet ketat yang melelahkan.',
      content: `
        <p>Masa nifas dan menyusui membutuhkan tambahan kalori sekitar 450–500 kkal per hari serta nutrisi padat untuk meregenerasi sel darah merah yang hilang saat melahirkan.</p>
        <h4>Asupan Wajib Harian:</h4>
        <p>• <strong>Zat Besi & Protein:</strong> Telur, daging tanpa lemak, ikan gabus/lele, tahu, tempe, dan bayam.<br>
        • <strong>Hidrasi Cukup:</strong> Minum minimal 2,5 hingga 3 liter air putih hangat per hari. Selalu sediakan botol air di samping tempat menyusui.<br>
        • <strong>Serat Mencegah Sembelit:</strong> Buah pepaya, pisang, gandum utuh (oatmeal), dan sayuran hijau sangat penting agar BAB tidak perlu mengejan dan menekan jahitan.</p>
      `
    },
    {
      id: 5,
      title: 'Kapan Waktu yang Tepat Menghubungi Tenaga Profesional?',
      category: 'Mental',
      catLabel: 'Kesehatan Mental',
      author: 'Rina Kusuma, M.Psi., Psikolog',
      readTime: '4 mnt baca',
      snippet: 'Tolak ukur objektif kapan ibu perlu menjadwalkan konseling psikologis atau pemeriksaan medis lanjutan.',
      content: `
        <p>Banyak ibu menunda mencari bantuan profesional karena takut dianggap lemah atau merasa masalahnya sepele. Mengetahui batasan kemampuan diri adalah tanda kecerdasan emosional.</p>
        <h4>Indikator Segera Konsultasi:</h4>
        <p>• Merasa mati rasa (numbness) dan sama sekali tidak bisa merasakan keterikatan emosi dengan bayi.<br>
        • Serangan panik (jantung berdebar, napas tercekat) saat mendengar tangisan bayi.<br>
        • Kesulitan tidur sama sekali bahkan ketika bayi sedang tidur lelap.<br>
        • Muncul pikiran berulang yang menakutkan tentang melukai diri sendiri atau bayi.</p>
        <p><em>Ingat:</em> Penanganan dini membuat proses pemulihan jauh lebih cepat dan mencegah gangguan berkembang menjadi kronis.</p>
      `
    }
  ]
};
