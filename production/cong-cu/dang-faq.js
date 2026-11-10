// Chạy ở một trang wp-admin bất kỳ, nhận biến g có slug và faq (dữ liệu FAQPage do bai.py tạo).
// Lưu FAQPage qua Rank Math rồi đọc lại trang công khai để đối chiếu. Chạy lại không sinh bản trùng.
const nonce = await (await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {credentials: 'include'})).text();
const opt = {credentials: 'include', headers: {'X-WP-Nonce': nonce, 'Content-Type': 'application/json'}};
if (!g.faq?.mainEntity?.length) return {dung: 'Goi khong co FAQ'};
const sp = (await (await fetch(`/wp-json/wp/v2/product?status=publish,future&slug=${g.slug}&_fields=id`, opt)).json())[0];
if (!sp) return {dung: 'Khong thay trang ' + g.slug};
const h = await (await fetch(`/wp-admin/post.php?post=${sp.id}&action=edit`, {credentials: 'include'})).text();
const vt = h.search(/var rankMath\s*=/);
if (vt < 0) return {dung: 'Khong doc duoc rankMath', id: sp.id};
const cu = JSON.parse(h.slice(vt).split('\n')[0].replace(/^var rankMath\s*=\s*/, '').replace(/;\s*$/, '')).schemas || {};
const faq_cu = Object.keys(cu).filter(k => cu[k]['@type'] === 'FAQPage');
if (faq_cu.length > 1) return {dung: 'Da co nhieu FAQPage, can xem tay', id: sp.id, faq_cu};
// Rank Math chỉ xuất schema mặc định khi bài chưa lưu schema nào, nên phải lưu kèm schema sản phẩm mặc định (khóa new-…).
const gui = {};
for (const [k, v] of Object.entries(cu)) if (k.startsWith('new-')) gui[k] = v;
gui[faq_cu[0] || 'new-faq'] = g.faq;
const r = await fetch('/wp-json/rankmath/v1/updateSchemas', {method: 'POST', ...opt, body: JSON.stringify({objectID: sp.id, objectType: 'post', schemas: gui})});
if (!r.ok) return {dung: 'Loi luu schema', status: r.status, id: sp.id};
// Đối chiếu trên trang công khai
const r0 = await fetch(`/san-pham/${g.slug}/?v=${Date.now()}`, {cache: 'no-store'});
const d = new DOMParser().parseFromString(await r0.text(), 'text/html');
const khoa = t => (t || '').replace(/[“”„]/g, '"').replace(/[‘’]/g, "'").replace(/\s+/g, ' ').trim();
const nut = [...d.querySelectorAll('script[type="application/ld+json"]')].flatMap(x => { const j = JSON.parse(x.textContent); return j['@graph'] || [j]; });
const kieu = n => [].concat(n['@type']);
const f = nut.filter(n => kieu(n).includes('FAQPage'));
const chu = khoa(d.querySelector('#tab-description')?.textContent);
const sai = (f[0]?.mainEntity || []).filter(q => !chu.includes(khoa(q.name)) || !chu.includes(khoa(q.acceptedAnswer?.text))).map(q => q.name);
return {id: sp.id, luu: r.status, trang: r0.status, so_faq: f.length, cau: f[0]?.mainEntity?.length, cau_can: g.faq.mainEntity.length, cau_lech: sai, product: nut.filter(n => kieu(n).includes('Product')).length, cac_kieu: nut.map(n => kieu(n).join('+'))};
