// Chạy ở một trang wp-admin bất kỳ, nhận biến g là gói đăng. Sửa bài đã đăng theo gói: tải ảnh mới, thay nội dung, Rank Math, FAQPage.
const nonce = await (await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {credentials: 'include'})).text();
const opt = {credentials: 'include', headers: {'X-WP-Nonce': nonce, 'Content-Type': 'application/json'}};
const lay = async u => (await fetch(u, opt)).json();
const sp = (await lay(`/wp-json/wp/v2/product?status=publish,future&slug=${g.slug}&_fields=id`))[0];
if (!sp) return {dung: 'Khong thay trang ' + g.slug};
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
  }
  await fetch('/wp-json/wp/v2/media/' + m.id, {method: 'POST', ...opt, body: JSON.stringify({alt_text: a.alt, title: a.alt})});
  ids[a.ten] = {id: m.id, url: m.source_url};
}
const c = g.noi_dung.replace(/<figure>\s*<img src="([^"]+)" alt="([^"]+)"[^>]*\/>\s*<figcaption>[\s\S]*?<\/figcaption>\s*<\/figure>/g, (s, ten, alt) => {
  const m = ids[ten];
  if (!m) throw new Error('Thieu anh ' + ten);
  return `[caption id="attachment_${m.id}" align="aligncenter" width="843"]<img class="size-full wp-image-${m.id}" src="${m.url}" alt="${alt}" width="843" height="623" /> ${alt}[/caption]`;
});
const r = await fetch('/wp-json/wp/v2/product/' + sp.id, {method: 'POST', ...opt, body: JSON.stringify({content: c})});
const rm = await fetch('/wp-json/rankmath/v1/updateMeta', {method: 'POST', ...opt, body: JSON.stringify({objectType: 'post', objectID: sp.id, meta: g.rank})});
const faq = await new (Object.getPrototypeOf(async function(){}).constructor)('g', g.js4)(g);
const r0 = await fetch(`/san-pham/${g.slug}/?v=${Date.now()}`, {cache: 'no-store'});
const d = new DOMParser().parseFromString(await r0.text(), 'text/html');
const box = d.querySelector('#tab-description');
const anh = [...box.querySelectorAll('img')].map(u => u.getAttribute('data-src') || u.getAttribute('src'));
const st = await Promise.all(anh.map(async u => (await fetch(u, {method: 'HEAD'})).status));
return {id: sp.id, faq, luu: r.status, rm: rm.status, trang: r0.status, anh_ok: st.filter(x => x === 200).length, anh_can: g.anh.length - 1, anh_ten: anh.map(u => u.split('/').pop()), sapo: box.querySelector('p')?.textContent?.slice(0, 40), h2: box.querySelectorAll('h2').length, ban_do: box.querySelectorAll('iframe').length};
