// Chạy ở trang wp-admin/post-new.php?post_type=product, nhận biến g là gói đăng.
// Tải ảnh, điền form, lưu việc còn lại cho bước 2, rồi bấm Đăng.
const nonce = await (await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {credentials: 'include'})).text();
const opt = {credentials: 'include', headers: {'X-WP-Nonce': nonce, 'Content-Type': 'application/json'}};
const lay = async u => (await fetch(u, opt)).json();
for (const st of ['any', 'trash']) {
  const co = await lay(`/wp-json/wp/v2/product?status=${st}&slug=${g.slug}&_fields=id,status`);
  if (co.length) return {dung: 'Trang da ton tai, chua dang', co};
}
const ids = {};
for (const a of g.anh) {
  const goc = a.ten.replace(/\.\w+$/, '');
  const co = await lay(`/wp-json/wp/v2/media?search=${encodeURIComponent(goc)}&per_page=10&_fields=id,source_url`);
  let m = co.find(x => x.source_url.endsWith('/' + a.ten));
  if (!m) {
    const bytes = Uint8Array.from(atob(a.b64), c => c.charCodeAt(0));
    const r = await fetch('/wp-json/wp/v2/media', {method: 'POST', credentials: 'include', headers: {'X-WP-Nonce': nonce, 'Content-Disposition': `attachment; filename="${a.ten}"`, 'Content-Type': a.mime}, body: bytes});
    if (!r.ok) return {dung: 'Loi tai anh', ten: a.ten, status: r.status};
    m = await r.json();
    m.source_url = m.source_url || m.guid.rendered;
  }
  await fetch('/wp-json/wp/v2/media/' + m.id, {method: 'POST', ...opt, body: JSON.stringify({alt_text: a.alt, title: a.alt})});
  ids[a.ten] = {id: m.id, url: m.source_url, dai_dien: !!a.dai_dien};
}
const c = g.noi_dung.replace(/<figure>\s*<img src="([^"]+)" alt="([^"]+)"[^>]*\/>\s*<figcaption>[\s\S]*?<\/figcaption>\s*<\/figure>/g, (s, ten, alt) => {
  const m = ids[ten];
  if (!m) throw new Error('Thieu anh ' + ten);
  return `[caption id="attachment_${m.id}" align="aligncenter" width="843"]<img class="size-full wp-image-${m.id}" src="${m.url}" alt="${alt}" width="843" height="623" /> ${alt}[/caption]`;
});
if (window.switchEditors) { switchEditors.go('content', 'html'); switchEditors.go('excerpt', 'html'); }
const t = document.querySelector('#title');
t.value = g.tieu_de;
t.dispatchEvent(new Event('input', {bubbles: true}));
document.querySelector('#content').value = c;
document.querySelector('#excerpt').value = g.mo_ta;
for (const v of g.danh_muc) {
  const i = document.querySelector(`#product_catchecklist input[value="${v}"]`);
  if (!i) return {dung: 'Khong thay danh muc ' + v};
  if (!i.checked) i.click();
}
const dd = Object.values(ids).find(x => x.dai_dien);
const dat = (n, v) => {
  const e = document.querySelector(`[name="${n}"]`);
  if (!e) return n;
  e.value = v;
  e.dispatchEvent(new Event('change', {bubbles: true}));
  return '';
};
const thieu = [dat('_hb_repair_time', g.thoi_gian), dat('_hb_warranty', g.bao_hanh), dat('_thumbnail_id', String(dd.id)), dat('rank_math_primary_product_cat', g.danh_muc[0])].filter(Boolean);
const so_anh = g.anh.length - 1;
const caps = (c.match(/\[caption/g) || []).length;
if (thieu.length || caps !== so_anh || /\{\{|<figure/.test(c)) return {dung: 'Form chua du', thieu, caps, so_anh};
localStorage.setItem('gh_sau_dang:' + g.slug, JSON.stringify({slug: g.slug, rank: g.rank, so_anh, js2: g.js2, faq: g.faq, js4: g.js4}));
document.querySelector('#tai-goi')?.remove();
window.onbeforeunload = null;
if (window.jQuery) jQuery(window).off('beforeunload');
setTimeout(() => document.querySelector('#publish').click(), 300);
return {da_bam_dang: true, anh: Object.values(ids).map(x => x.id), caps};
