// Chạy ở trang sửa sản phẩm ngay sau khi đăng, nhận biến s là phần bước 1 đã lưu.
// Điền Rank Math, lưu FAQPage rồi đọc lại trang công khai để kiểm tra.
const id = +document.querySelector('#post_ID')?.value;
const slug = document.querySelector('#editable-post-name-full')?.textContent;
if (!id || slug !== s.slug) return {dung: 'Khong dung trang', id, slug};
const nonce = await (await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {credentials: 'include'})).text();
const rm = await fetch('/wp-json/rankmath/v1/updateMeta', {method: 'POST', credentials: 'include', headers: {'X-WP-Nonce': nonce, 'Content-Type': 'application/json'}, body: JSON.stringify({objectType: 'post', objectID: id, meta: s.rank})});
const faq = await new (Object.getPrototypeOf(async function(){}).constructor)('g', s.js4)(s);
const r0 = await fetch(`/san-pham/${s.slug}/`, {cache: 'no-store'});
const d = new DOMParser().parseFromString(await r0.text(), 'text/html');
const box = d.querySelector('#tab-description');
const anh = [...box.querySelectorAll('img')];
const st = await Promise.all(anh.map(async u => (await fetch(u.getAttribute('data-src') || u.getAttribute('src'), {method: 'HEAD'})).status));
localStorage.removeItem('gh_sau_dang:' + s.slug);
return {id, faq, rm: rm.status, trang: r0.status, duong_dan: new URL(r0.url).pathname, title: d.title, h1: d.querySelector('h1')?.textContent?.trim(), mo_ta: d.querySelector('meta[name=description]')?.content?.length, anh_ok: st.filter(x => x === 200).length, anh_can: s.so_anh, chu_thich: box.querySelectorAll('figcaption,.wp-caption-text').length, ban_do: box.querySelectorAll('iframe').length, h2: box.querySelectorAll('h2').length, gia: d.querySelector('.summary .price')?.textContent?.trim(), og: d.querySelector('meta[property="og:image"]')?.content?.split('/').pop(), danh_muc: d.querySelector('.posted_in')?.textContent?.trim()};
