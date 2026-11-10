# Công cụ làm bài dịch vụ: AI chỉ viết một file nguồn, script lo phần lặp lại.
# Cách chạy: python production/cong-cu/bai.py production/<slug>-<ngày>.md [anh|dung|dung-faq|kiem|kiem-web]
# Không ghi lệnh thì chạy anh, dung, kiem. Lệnh kiem-web đối chiếu FAQPage trên trang đã đăng. Lệnh dung-faq tạo gói chỉ có FAQPage. Hướng dẫn: .claude/skills/viet-bai-dich-vu/SKILL.md
import sys, io, os, re, json, glob, base64, html, hashlib, urllib.request
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOL)
DL = os.environ.get('ANH_WEBSITE', r'C:\Users\Dell\Downloads\Anh Website')
GOC = os.path.join(ROOT, 'anh', 'thay-man-hinh-huawei-mate-40-pro', 'goc')
MAX_KB = 100
BANDO = [
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3724.909930723746!2d105.81337701184512!3d20.996247280564248!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3135ac9200cafca3%3A0xde5877234f0e689!2sGia%20Hue%20Mobile!5e0!3m2!1sen!2sus!4v1774344620210!5m2!1sen!2sus',
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3724.559683084036!2d105.8227862!3d21.010280299999998!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3135ab5f4cd90755%3A0x21386ca6879f6ce4!2zR2lhIEh14buHIE1vYmlsZSAyMiBUaMOhaSBIw6A!5e0!3m2!1svi!2s!4v1785382773384!5m2!1svi!2s',
]
TU_XUNG_SAI = ['bên mình', 'bên em', 'chúng tôi', 'chúng em', 'xưởng']
TU_HUT_KHACH = ['lấy ngay', 'lấy liền', 'giá rẻ', 'giá tốt', 'uy tín', 'bao mọi rủi ro', 'test ưng', 'test thử']
TU_CAM = ['top 1', 'số 1', 'tốt nhất', 'rẻ nhất', 'uy tín nhất', 'duy nhất', '100%', 'tuyệt đối', 'vĩnh viễn', 'hoàn hảo', 'vượt trội', 'đỉnh cao', 'chính hãng', 'chiêm tài', 'bao mọi', 'ip68', 'chống nước như mới']


def doc_nguon(path):
    s = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', s, flags=re.S)
    cfg = {'anh': [], 'luu_y': [], 'mo_ta': []}
    for l in m[1].split('\n'):
        k, _, v = l.partition(':')
        k, v = k.strip(), v.strip()
        if k in ('anh', 'luu_y', 'mo_ta'):
            cfg[k].append(v)
        elif k:
            cfg[k] = v
    cfg['ngay'] = re.search(r'(\d{4}-\d{2}-\d{2})\.md$', path)[1]
    # File nguồn mẫu cũ ghi slug là đường dẫn đầy đủ (/san-pham/ten-bai/), chỉ lấy phần cuối
    if 'slug' in cfg:
        cfg['slug'] = cfg['slug'].strip('/').split('/')[-1]
    return cfg, m[2].strip()


def nguon_anh(s, phan_xuong=0.96):
    # "xuong:ten.jpg" là ảnh xưởng (chỉ cắt nhẹ), còn lại là ảnh trong Downloads/Anh Website
    if s.startswith('xuong:'):
        im = Image.open(os.path.join(GOC, s[6:])).convert('RGB')
        w, h = im.width * phan_xuong, im.height * phan_xuong
        x0, y0 = (im.width - w) / 2, (im.height - h) / 2
        return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h)))
    return Image.open(os.path.join(DL, s)).convert('RGB')


def lam_anh(cfg):
    slug = cfg['slug']
    out_dir = os.path.join(ROOT, 'anh', slug)
    os.makedirs(out_dir, exist_ok=True)
    # Ảnh đại diện: chỉ đổi tên model và ảnh màn trên khung mẫu
    s16 = Image.open(os.path.join(ROOT, 'anh', 'thay-man-hinh-vivo-s16', 'anh-dai-dien-thay-man-hinh-vivo-s16.png')).convert('RGB')
    nen = Image.open(os.path.join(ROOT, 'anh', 'thay-man-hinh-oppo-reno-7-pro', 'nhap-anh-dai-dien-chua-co-man.png')).convert('RGB')
    W, H = nen.size
    ImageDraw.Draw(nen).rectangle([312, 108, 755, 148], fill=(255, 255, 255))
    px16 = s16.load()
    cols = {}
    for x in range(440, 620):
        c = min((px16[x, y] for y in range(112, 144)), key=lambda p: p[0])
        if c[0] < 120:
            cols[x] = c
    xs = sorted(cols)

    def color(x):
        x = max(xs[0], min(xs[-1], x))
        n = sorted(xs, key=lambda k: abs(k - x))[:5]
        return tuple(sum(cols[k][i] for k in n) // len(n) for i in range(3))
    k = 4
    f = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 31.75 * k)
    text = cfg['chu_anh_dai_dien']
    b = f.getbbox(text)
    tw, th = b[2] - b[0], b[3] - b[1]
    cx = (xs[0] + xs[-1]) / 2
    m = Image.new('L', (W * k, H * k), 0)
    ImageDraw.Draw(m).text((cx * k - tw / 2 - b[0], 127.5 * k - th / 2 - b[1]), text, font=f, fill=255)
    m = m.resize((W, H), Image.LANCZOS)
    g = Image.new('RGB', (W, H), (255, 255, 255))
    gp = g.load()
    for x in range(312, 756):
        c = color(x)
        for y in range(100, 160):
            gp[x, y] = c
    nen.paste(g, (0, 0), m)
    man = nguon_anh(cfg['anh_dai_dien'])
    w, h = man.size
    px = man.load()
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y * w + x] or not (min(px[x, y]) > 205 and max(px[x, y]) - min(px[x, y]) < 22):
            continue
        seen[y * w + x] = 1
        q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    mask = Image.frombytes('L', (w, h), bytes(0 if s else 255 for s in seen))
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    box = mask.point(lambda v: 255 if v > 128 else 0).getbbox()
    sc = 262 / (box[3] - box[1])
    size = (round((box[2] - box[0]) * sc), round((box[3] - box[1]) * sc))
    nen.paste(man.crop(box).resize(size, Image.LANCZOS), (round(530 - size[0] / 2), 430 - size[1]), mask.crop(box).resize(size, Image.LANCZOS))
    dd = os.path.join(out_dir, f'anh-dai-dien-{slug}.png')
    nen.save(dd, optimize=True)
    nen.save(dd[:-4] + '.webp', 'WEBP', quality=85, method=6)
    print('dai dien', os.path.getsize(dd) // 1024, 'KB')
    # Ảnh trong bài: đặt vào khung, nén WebP dưới MAX_KB
    frame = Image.open(os.path.join(ROOT, 'anh', 'khung', 'khung-anh-gia-hue-mobile.png')).convert('RGB')
    FW, FH = frame.size
    fill = frame.copy()
    ImageDraw.floodfill(fill, (FW // 2, FH // 2), (255, 0, 255), thresh=60)
    fm = fill.split()[1].point(lambda v: 0 if v == 0 else 255).filter(ImageFilter.MinFilter(3))
    _m, _f = fm.load(), frame.load()
    for y in range(0, 585):
        for x in range(FW):
            if min(_f[x, y]) > 200 and not (x < 195 and y < 90):
                _m[x, y] = 0
    ds = []
    for dong in cfg['anh']:
        ten, _, src = dong.partition('=')
        ten, src = ten.strip(), src.strip()
        src, _, che = src.partition('| che=')
        goc = nguon_anh(src.strip())
        if che:
            # làm mờ một vùng (x0,y0,x1,y1 theo ảnh gốc), mép mờ dần để không lộ vết
            bx = tuple(int(v) for v in che.split(','))
            mo = goc.filter(ImageFilter.GaussianBlur(16))
            mk = Image.new('L', goc.size, 0)
            ImageDraw.Draw(mk).rectangle(bx, fill=255)
            goc.paste(mo, (0, 0), mk.filter(ImageFilter.GaussianBlur(5)))
        im = ImageOps.fit(goc, (FW, FH), Image.LANCZOS)
        im.paste(frame, (0, 0), fm)
        for q_ in range(90, 30, -4):
            bf = io.BytesIO()
            im.save(bf, 'WEBP', quality=q_, method=6)
            if bf.tell() <= MAX_KB * 1024:
                break
        p = os.path.join(out_dir, f'{slug}-{ten}.webp')
        open(p, 'wb').write(bf.getvalue())
        ds.append(p)
        print(ten, bf.tell() // 1024, 'KB')
    # Một tấm gộp để xem một lần, đỡ tốn token hơn mở từng ảnh
    sheet = Image.new('RGB', (1260, 640), 'white')
    for i, p in enumerate(ds[:5]):
        sheet.paste(Image.open(p).convert('RGB').resize((420, 310)), ((i % 3) * 420, (i // 3) * 320))
    sheet.paste(nen.resize((420, 326)), (840, 314))
    sheet.save(os.path.join(out_dir, 'xem-nhanh.jpg'), quality=72)


def inline(s):
    def lk(m):
        u = html.escape(html.unescape(m[2]), quote=False)
        return f'<a href="{u}">{m[1]}</a>' if 'giahuemobile.com' in m[2] else f'<a href="{u}" target="_blank" rel="nofollow noopener">{m[1]}</a>'
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lk, s)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)


def co_so():
    ifr = lambda s: f'<iframe src="{s}" width="100%" height="250" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
    gm = 'https://www.google.com/maps/search/?api=1&amp;query=Gia+Huệ+Mobile+'
    return (f'<p><strong>Cơ sở 1:</strong> <a href="{gm}177+Vũ+Tông+Phan+Khương+Đình+Thanh+Xuân+Hà+Nội" target="_blank" rel="nofollow noopener">177 Vũ Tông Phan, Khương Đình, Thanh Xuân, Hà Nội</a> · Hotline <strong>0962 528 528</strong></p>\n{ifr(BANDO[0])}\n'
            f'<p><strong>Cơ sở 2:</strong> <a href="{gm}22+Thái+Hà+Trung+Liệt+Đống+Đa+Hà+Nội" target="_blank" rel="nofollow noopener">22 Thái Hà, Trung Liệt, Đống Đa, Hà Nội</a> · Hotline <strong>0986 980 802</strong></p>\n{ifr(BANDO[1])}')


def sang_html(than, slug):
    out, i, n_h2 = [], 0, 0
    ls = than.split('\n')
    while i < len(ls):
        l = ls[i].strip()
        i += 1
        if not l:
            continue
        if l == '{{co-so}}':
            out.append(co_so())
        elif l.startswith('### '):
            out.append(f'<h3>{inline(l[4:])}</h3>')
        elif l.startswith('## '):
            n_h2 += 1
            out.append(f'<h2><span style="color: #00aae7;">{n_h2}. {inline(l[3:])}</span></h2>')
        elif (m := re.match(r'!\[(.+)\]\((.+)\)$', l)):
            out.append(f'<figure>\n<img src="{slug}-{m[2]}.webp" alt="{m[1]}" width="843" height="623" />\n<figcaption>{m[1]}</figcaption>\n</figure>')
        elif l.startswith('|'):
            rows = [l]
            while i < len(ls) and ls[i].strip().startswith('|'):
                rows.append(ls[i].strip()); i += 1
            cell = lambda r: [c.strip() for c in r.strip('|').split('|')]
            t = '<table>\n<thead>\n<tr>' + ''.join(f'<th>{inline(c)}</th>' for c in cell(rows[0])) + '</tr>\n</thead>\n<tbody>\n'
            t += '\n'.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cell(r)) + '</tr>' for r in rows[2:])
            out.append(t + '\n</tbody>\n</table>')
        elif re.match(r'(- |\d+\. )', l):
            tag = 'ul' if l.startswith('- ') else 'ol'
            items = [l]
            while i < len(ls) and re.match(r'(- |\d+\. )', ls[i].strip()):
                items.append(ls[i].strip()); i += 1
            out.append(f'<{tag}>\n' + '\n'.join('<li>' + inline(re.sub(r'^(- |\d+\. )', '', x)) + '</li>' for x in items) + f'\n</{tag}>')
        else:
            out.append(f'<p>{inline(l)}</p>')
    return '\n'.join(out) + '\n'


def mo_ta_ngan(cfg):
    ds = cfg['mo_ta'] or [
        f"Thay lấy trong ngày, khoảng {cfg['thoi_gian']}, luôn có sẵn linh kiện",
        f"Bảo hành lỗi cảm ứng {cfg['bao_hanh']}, lỗi 1 đổi 1",
        'Báo giá trọn gói, không phát sinh chi phí',
        'Hoàn tiền nếu không hài lòng về linh kiện hoặc dịch vụ',
        'Được dán đầy đủ keo tếp kháng nước sau khi thay màn',
        'Miễn phí kiểm tra và vệ sinh thiết bị',
        'Hỗ trợ xuất hóa đơn VAT đầy đủ',
    ]
    return ds


def chu_faq(h):
    # Thẻ trong dòng bỏ hẳn để không sinh dấu cách thừa ("nước , song"), thẻ khối mới đổi thành cách
    h = re.sub(r'<figure.*?</figure>', ' ', h, flags=re.S)
    h = re.sub(r'</?(?:strong|em|b|i|a|span)\b[^>]*>', '', h)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def faq_tu_html(body):
    # Trả về (tên H2, [(câu hỏi, trả lời)]) của H2 có chữ "hỏi", "thắc mắc" hoặc "FAQ" và nhiều H3 nhất
    ten, tot = '', ''
    for m in re.finditer(r'(<h2>.*?</h2>)(.*?)(?=<h2>|\Z)', body, flags=re.S):
        if re.search(r'hỏi|thắc mắc|FAQ', m[1], flags=re.I) and m[2].count('<h3>') > tot.count('<h3>'):
            ten, tot = re.sub(r'^(\d+\.\s*)+', '', chu_faq(m[1])), m[2]
    p = re.split(r'<h3>(.*?)</h3>', tot, flags=re.S)
    return ten, [(chu_faq(q), chu_faq(a)) for q, a in zip(p[1::2], p[2::2])]


def faq_schema(body, slug):
    # Đúng khuôn mẫu FAQ của Rank Math, đọc từ mẫu "FAQ" trên web ngày 2026-11-04
    ten, ds = faq_tu_html(body)
    return {'@type': 'FAQPage', 'name': ten, 'url': '%url%',
            'metadata': {'title': 'FAQ', 'type': 'template', 'isPrimary': '', 'shortcode': 's-faq-' + hashlib.md5(slug.encode()).hexdigest()[:12]},
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in ds]}


def kiem_web(cfg, than):
    # Đọc trang công khai, đối chiếu FAQPage với file nguồn và với chữ hiện trên trang
    slug, loi = cfg['slug'], []
    body = sang_html(than, slug)

    def xet(ok, ten, gt=''):
        print(('OK  ' if ok else 'LOI ') + ten + (f': {gt}' if gt != '' else ''))
        if not ok:
            loi.append(ten)
    u = f'https://giahuemobile.com/san-pham/{slug}/?v={os.urandom(4).hex()}'
    trang = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=25).read().decode('utf-8')
    nut = []
    for x in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', trang, flags=re.S):
        j = json.loads(x)
        nut += j.get('@graph', [j])
    kieu = lambda n: n.get('@type') if isinstance(n.get('@type'), list) else [n.get('@type')]
    f = [n for n in nut if 'FAQPage' in kieu(n)]
    xet(len(f) == 1, 'Trang có đúng 1 FAQPage', len(f))
    xet(any('Product' in kieu(n) for n in nut), 'Vẫn còn Product')
    if f:
        khoa = lambda t: re.sub(r'\s+', ' ', re.sub('[“”„]', '"', re.sub('[‘’]', "'", html.unescape(t)))).strip()
        chu = khoa(chu_faq(re.sub(r'<script.*?</script>', ' ', trang, flags=re.S)))
        tren_web = [(q.get('name', ''), q.get('acceptedAnswer', {}).get('text', '')) for q in f[0].get('mainEntity', [])]
        _, nguon = faq_tu_html(body)
        xet(len(tren_web) >= 6, 'FAQPage từ 6 câu', len(tren_web))
        xet([(khoa(q), khoa(a)) for q, a in tren_web] == [(khoa(q), khoa(a)) for q, a in nguon], 'FAQPage khớp file nguồn')
        lech = [q for q, a in tren_web if khoa(q) not in chu or khoa(a) not in chu]
        xet(not lech, 'Mỗi câu hỏi, câu trả lời có nguyên văn trên trang', lech[:3] or '')
        xet(not any(re.search(r'<[a-z/]|&[a-z]+;|%[a-z_]+%', q + a) for q, a in tren_web), 'Không còn thẻ, mã ký tự hay biến chưa thay')
    print('KET QUA:', 'dat' if not loi else f'{len(loi)} loi')


def dung_faq(cfg, than):
    # Gói chỉ có FAQPage, không ghi đè bản bài và ảnh. Dùng cho file nguồn mẫu cũ, vốn không chạy được lệnh dung
    slug = cfg['slug']
    goi = {'slug': slug, 'faq': faq_schema(sang_html(than, slug), slug), 'js4': open(os.path.join(TOOL, 'dang-faq.js'), encoding='utf-8').read()}
    gp = os.path.join(ROOT, 'dang', f'{slug}-faq-goi.txt')
    json.dump(goi, open(gp, 'w', encoding='utf-8'), ensure_ascii=False)
    print('goi faq', len(goi['faq']['mainEntity']), 'cau ->', gp)


def dung(cfg, than, nguon_path):
    thieu = [k for k in ('tieu_de', 'tu_khoa', 'thoi_gian', 'bao_hanh', 'danh_muc') if k not in cfg]
    if thieu:
        sys.exit(f'File nguon mau cu, thieu {thieu}: lenh dung se ghi de ban bai. Chi them FAQPage thi dung lenh dung-faq.')
    slug, ngay = cfg['slug'], cfg['ngay']
    body = sang_html(than, slug)
    goc = os.path.join(ROOT, f'{slug}-{ngay}')
    open(goc + '-ma-wordpress.html', 'w', encoding='utf-8').write(body)
    out_dir = os.path.join(ROOT, 'anh', slug)
    emb = lambda m: 'src="data:image/webp;base64,' + base64.b64encode(open(os.path.join(out_dir, m[1]), 'rb').read()).decode() + '"'
    prev = re.sub(r'src="([^"]+\.webp)"', emb, body)
    dd = os.path.join(out_dir, f'anh-dai-dien-{slug}.png')
    fe = base64.b64encode(open(dd, 'rb').read()).decode()
    css = 'body{max-width:843px;margin:0 auto;padding:16px;font:17px/1.6 Arial,sans-serif;color:#222;background:#fff}img{max-width:100%;height:auto;display:block}figure{margin:16px 0}figcaption{font-size:14px;color:#555;text-align:center;margin-top:6px}table{border-collapse:collapse;width:100%;margin:12px 0}th,td{border:1px solid #ccc;padding:8px;text-align:left}th{background:#f2f8fb}h1{font-size:28px}h3{margin-bottom:4px}'
    open(goc + '.html', 'w', encoding='utf-8').write(f'<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{cfg["title"]}</title><meta name="description" content="{cfg["meta"]}"><style>{css}</style></head><body><figure><img src="data:image/png;base64,{fe}" alt="{cfg["tieu_de"]} tại Gia Huệ Mobile"><figcaption>Ảnh đại diện</figcaption></figure><h1>{cfg["tieu_de"]}</h1>{prev}</body></html>')
    ds = mo_ta_ngan(cfg)
    nd = [f'# Nội dung điền khi đăng: {cfg["tieu_de"]}', '', f'Nguồn: `{os.path.basename(nguon_path)}`. Bài: `{slug}-{ngay}-ma-wordpress.html`. Ảnh: `anh/{slug}/`.', '', '## Mô tả ngắn', '']
    nd += [f'- {x}' for x in ds]
    nd += ['', '## Thông tin bổ sung', '', f'- Thời gian (_hb_repair_time): {cfg["thoi_gian"]}', f'- Bảo hành (_hb_warranty): {cfg["bao_hanh"]}', '- Giá: để trống, web hiện "Liên hệ"', f'- Danh mục: {cfg["danh_muc"]} (mã đầu là danh mục chính)', '', '## Rank Math', '', f'- **Thẻ tiêu đề ({len(cfg["title"])} ký tự):** {cfg["title"]}', f'- **Mô tả ({len(cfg["meta"])} ký tự):** {cfg["meta"]}', f'- **Đường dẫn:** {slug}', f'- **Từ khóa chính:** {cfg["tu_khoa"]}', '']
    if cfg['luu_y']:
        nd += ['## Còn chờ xác nhận', ''] + [f'- ⚠️ {x}' for x in cfg['luu_y']] + ['']
    open(os.path.join(ROOT, f'{slug}-noi-dung-dang-web.md'), 'w', encoding='utf-8').write('\n'.join(nd))
    # Gói đăng: một file duy nhất tải lên Chrome, kèm luôn cả mã đăng bài
    dd_webp = dd[:-4] + '.webp'
    imgs = [{'ten': os.path.basename(dd_webp), 'mime': 'image/webp', 'b64': base64.b64encode(open(dd_webp, 'rb').read()).decode(), 'alt': f'{cfg["tieu_de"]} tại Gia Huệ Mobile', 'dai_dien': True}]
    alts = dict((m[1], m[0]) for m in re.findall(r'!\[(.+)\]\((.+)\)', than))
    for dong in cfg['anh']:
        ten = dong.partition('=')[0].strip()
        p = os.path.join(out_dir, f'{slug}-{ten}.webp')
        imgs.append({'ten': os.path.basename(p), 'mime': 'image/webp', 'b64': base64.b64encode(open(p, 'rb').read()).decode(), 'alt': alts[ten]})
    goi = {'slug': slug, 'tieu_de': cfg['tieu_de'], 'noi_dung': body, 'mo_ta': '<ul>\n' + '\n'.join(f'<li>{x}</li>' for x in ds) + '\n</ul>',
           'danh_muc': [x.strip() for x in cfg['danh_muc'].split(',')], 'thoi_gian': cfg['thoi_gian'], 'bao_hanh': cfg['bao_hanh'], 'anh': imgs,
           'rank': {'rank_math_title': cfg['title'], 'rank_math_description': cfg['meta'], 'rank_math_focus_keyword': cfg['tu_khoa']},
           'faq': faq_schema(body, slug),
           'js1': open(os.path.join(TOOL, 'dang-buoc-1.js'), encoding='utf-8').read(), 'js2': open(os.path.join(TOOL, 'dang-buoc-2.js'), encoding='utf-8').read(), 'js3': open(os.path.join(TOOL, 'dang-cap-nhat.js'), encoding='utf-8').read(), 'js4': open(os.path.join(TOOL, 'dang-faq.js'), encoding='utf-8').read()}
    os.makedirs(os.path.join(ROOT, 'dang'), exist_ok=True)
    gp = os.path.join(ROOT, 'dang', f'{slug}-goi.txt')
    json.dump(goi, open(gp, 'w', encoding='utf-8'), ensure_ascii=False)
    print('goi dang', os.path.getsize(gp) // 1024, 'KB ->', gp)


def chu_thuan(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<iframe.*?</iframe>', ' ', h, flags=re.S))).strip()


def nam_tu(s):
    s = re.sub(r'(oppo reno ?\d+( pro)?|vivo [a-z]+ ?\d+\w*( pro)?|huawei mate ?\d+( pro)?|\b[svx]\d{2}\b( pro)?|reno ?\d+( pro)?)', 'MAY', s.lower())
    w = re.findall(r'\w+', s)
    return {' '.join(w[i:i + 5]) for i in range(len(w) - 4)}


def kiem(cfg, than):
    slug, ngay, kw = cfg['slug'], cfg['ngay'], cfg['tu_khoa'].lower()
    body = open(os.path.join(ROOT, f'{slug}-{ngay}-ma-wordpress.html'), encoding='utf-8').read()
    vis = chu_thuan(body)
    words, n = len(vis.split()), vis.lower().count(kw)
    sapo_doan = re.findall(r'<p>(.*?)</p>', body[:body.index('<figure')], flags=re.S)
    sapo_chu = ' '.join(chu_thuan(d) for d in sapo_doan)
    loi = []

    def xet(ok, ten, gt=''):
        print(('OK  ' if ok else 'LOI ') + ten + (f': {gt}' if gt != '' else ''))
        if not ok:
            loi.append(ten)
    xet(55 <= len(cfg['title']) <= 70, 'Tiêu đề 55–70 ký tự', len(cfg['title']))
    xet(cfg['title'].lower().count(kw) == 1, 'Tiêu đề có 1 lần từ khóa')
    xet(any(k in cfg['title'].lower() for k in TU_HUT_KHACH), 'Tiêu đề có yếu tố hút khách', TU_HUT_KHACH)
    xet(150 <= len(cfg['meta']) <= 160, 'Mô tả 150–160 ký tự', len(cfg['meta']))
    xet(1 <= cfg['meta'].lower().count(kw) <= 3, 'Mô tả có từ khóa')
    xet(not re.search(r'(^|\s)đ\w*', cfg['title'].split(':')[-1], flags=re.I), 'Tiêu đề không có từ bắt đầu bằng đ')
    xet(1500 <= words <= 2500, 'Độ dài 1.500–2.500 từ', words)
    xet(1.0 <= n / words * 100 <= 1.5, 'Mật độ từ khóa 1–1,5%', f'{n}/{words} = {n / words * 100:.2f}%')
    xet(len(sapo_doan) == 3, 'Sapo đủ 3 đoạn trước ảnh đầu bài', len(sapo_doan))
    xet(130 <= len(sapo_chu.split()) <= 230, 'Sapo 130–230 từ', len(sapo_chu.split()))
    xet(kw in sapo_chu.lower() and '?' not in sapo_chu, 'Sapo có từ khóa, không có câu hỏi')
    xet(body.index('<p>') < body.index('<figure'), 'Sapo đứng trước ảnh đầu bài')
    xet(body.count('<img') >= 5, 'Từ 5 ảnh trở lên', body.count('<img'))
    anh_lac = len(re.findall(r'<figure', body)) - len(re.findall(r'</h[23]>\s*<figure', body))
    xet(anh_lac == 0, 'Mỗi ảnh nằm ngay dưới H2 hoặc H3', anh_lac)
    alts = re.findall(r'alt="([^"]+)"', body)
    xung = [t for t in TU_XUNG_SAI if t in (vis + ' ' + ' '.join(alts)).lower()]
    xet(not xung, 'Xưng là cửa hàng', xung or '')
    xet(all(kw in a.lower() for a in alts), 'Alt nào cũng có từ khóa')
    xet(len(set(alts)) == len(alts), 'Alt không trùng nhau')
    _, faq = faq_tu_html(body)
    xet(len(faq) >= 6, 'FAQ từ 6 câu', len(faq))
    xet(all(q.endswith('?') for q, a in faq), 'Câu FAQ kết thúc bằng dấu hỏi', [q[:50] for q, a in faq if not q.endswith('?')][:3] or '')
    xet(any('dữ liệu' in q.lower() for q, a in faq), 'FAQ có câu khách lo mất dữ liệu')
    xet(all(a for q, a in faq), 'Câu FAQ nào cũng có trả lời', [q[:50] for q, a in faq if not a][:3] or '')
    xet(not any(re.search(r'%[a-z_]+%', q + a) for q, a in faq), 'FAQ không có chữ dạng biến Rank Math')
    xet(body.count('{{') == 0, 'Không còn ký hiệu chờ')
    cau = [c.strip() for c in re.split(r'[.!?;:]\s', chu_thuan(' '.join(re.findall(r'<(?:p|li)>.*?</(?:p|li)>', body, flags=re.S))))]
    dai = [c for c in cau if len(c.split()) > 32 and 'Hotline' not in c and 'Trang liên quan' not in c]
    xet(not dai, 'Câu không quá 32 từ', [c[:50] for c in dai][:3] or '')
    h2 = re.findall(r'<h2>.*?</h2>', body)
    xet(8 <= len(h2) <= 10, 'Bài có 8–10 H2', len(h2))
    xet(any('dấu hiệu' in x.lower() for x in h2) and any('nguyên nhân' in x.lower() for x in h2), 'Có H2 về dấu hiệu và H2 về nguyên nhân')
    xet(sum('?' in x for x in h2) >= len(h2) - 2, 'Phần lớn H2 là câu hỏi khách hay tìm', f"{sum('?' in x for x in h2)}/{len(h2)}")
    xet(body.count('<iframe') == 2 and '177 Vũ Tông Phan' in body and '22 Thái Hà' in body, 'Đủ 2 cơ sở và bản đồ')
    xet('0962 528 528' in vis, 'Có hotline')
    the_a = re.findall(r'<a [^>]*>', body)
    sai = [t for t in the_a if ('giahuemobile.com' in t) == ('nofollow' in t)]
    xet(the_a and not sai, 'Link ngoài nofollow, link nội bộ dofollow', sai[:3] or '')
    if 'màn hình' in kw:
        xet(not re.search(r'lỗi hiển thị và cảm ứng|bảo hành[^.]{0,60}lỗi hiển thị', vis, flags=re.I), 'Bảo hành màn chỉ ghi lỗi cảm ứng, không ghi lỗi hiển thị')
        xet(len(re.findall(r'<strong>[^<]*dán đầy đủ keo tếp kháng nước[^<]*</strong>', body, flags=re.I)) >= 3, 'Key: bôi đậm "dán đầy đủ keo tếp kháng nước" từ 3 chỗ')
        xet('dán đầy đủ keo tếp kháng nước' in sapo_chu.lower(), 'Key: có trong sapo')
    if 'pin' in kw:
        xet('dùng thử miễn phí 1 tháng' in vis.lower(), 'Key: dùng thử pin miễn phí 1 tháng')
    if 'ép kính' in kw:
        xet('test nhiệt' in vis.lower(), 'Key: test nhiệt')
    xet(len(re.findall(r'<strong>[^<]*Gia Huệ Mobile[^<]*</strong>', body)) >= 3, 'Thương hiệu Gia Huệ Mobile bôi đậm từ 3 chỗ')
    co = [t for t in TU_CAM if t in vis.lower()]
    xet(not co, 'Không có từ cấm', co or '')
    for p in glob.glob(os.path.join(ROOT, 'anh', slug, f'{slug}-*.webp')):
        im = Image.open(p)
        xet(os.path.getsize(p) <= MAX_KB * 1024 and im.size == (843, 623), f'Ảnh {os.path.basename(p)[len(slug) + 1:]}', f'{os.path.getsize(p) // 1024} KB {im.size[0]}x{im.size[1]}')
    # Ảnh đầu ra không còn nhãn AI trong dữ liệu ẩn (C2PA, XMP, EXIF)
    vet = [os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'anh', slug, f'*{slug}*.*'))
           if any(k in open(p, 'rb').read() for k in (b'c2pa', b'C2PA', b'jumb', b'caBX', b'trainedAlgorithmicMedia', b'<x:xmpmeta'))]
    xet(not vet, 'Ảnh không còn nhãn AI trong dữ liệu ẩn', vet or '')
    me = nam_tu(vis)
    tr = []
    for p in glob.glob(os.path.join(ROOT, '*-ma-wordpress.html')):
        if slug in p:
            continue
        kia = nam_tu(chu_thuan(open(p, encoding='utf-8').read()))
        tr.append((len(me & kia) * 100 // max(len(me), 1), os.path.basename(p).split('-20')[0].replace('thay-man-hinh-', '')))
    tr.sort(reverse=True)
    xet(not tr or tr[0][0] < 15, 'Trùng 5 từ dưới 15%', tr[:3])
    for u in sorted(set(re.findall(r'href="(https://giahuemobile[^"]+)"', body))):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=25)
            xet(r.status == 200 and r.url.rstrip('/') == u.rstrip('/'), 'Link', u.split('.com')[1])
        except Exception as e:
            xet(False, 'Link', f'{u.split(".com")[1]} {e}')
    print('KET QUA:', 'dat' if not loi else f'{len(loi)} loi')


if __name__ == '__main__':
    path = sys.argv[1]
    lenh = sys.argv[2] if len(sys.argv) > 2 else 'tat-ca'
    cfg, than = doc_nguon(path)
    if lenh in ('anh', 'tat-ca'):
        lam_anh(cfg)
    if lenh in ('dung', 'tat-ca'):
        dung(cfg, than, path)
    if lenh in ('kiem', 'tat-ca'):
        kiem(cfg, than)
    if lenh == 'dung-faq':
        dung_faq(cfg, than)
    if lenh == 'kiem-web':
        kiem_web(cfg, than)
