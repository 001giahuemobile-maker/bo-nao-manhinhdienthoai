---
name: viet-bai-dich-vu
description: Viết và đăng bài dịch vụ theo tên model cho giahuemobile.com với ít token nhất. Dùng khi bạn hiền chỉ gửi tên một model điện thoại, hoặc nói viết bài, đăng bài thay màn hình, ép kính, thay pin cho một model.
---

# Viết bài dịch vụ tiết kiệm token

Mỗi bài một phiên mới. AI viết **một file nguồn**, `production/cong-cu/bai.py` lo ảnh, các bản của bài, kiểm tra và gói đăng. Không mở các trang quy tắc khác, trừ khi trang này không đủ. Chi tiết gốc: `wiki/khai-niem/lenh-viet-bai-seo-dich-vu.md`.

**Mỗi lần bạn hiền yêu cầu sửa bài, ghi ngay yêu cầu đó thành luật trong skill này** (bạn hiền dặn 2026-11-04), kèm ngày và ví dụ câu bị chê nếu có, để bài sau không lặp lại lỗi. Chỉ đẩy lên khi bạn hiền bảo.

## 1. Lấy dữ liệu (một lệnh, không đọc cả file)

Với `X` là tên model, ví dụ `x60`:

```bash
ls "C:/Users/Dell/Downloads/Anh Website/vivo x60"; grep -n -i "x60" raw/google-drive/bang-gia.md | cut -c1-160; grep -n -i "x60" wiki/so-sanh/gia-website-*.md | cut -c1-200; grep -n -A1 "Góc đã dùng" wiki/khai-niem/lenh-viet-bai-seo-dich-vu.md | cut -c1-700; curl -s -o /dev/null -L -A 'Mozilla/5.0' -w "%{http_code} %{url_effective}\n" https://giahuemobile.com/san-pham/thay-man-hinh-vivo-x60/
```

- Thời gian lấy từ trang cùng dòng máy trong `raw/website/2026-10-30/text/`; ghi rõ ở `luu_y` nếu mượn.
- Thông số màn: tối đa 1 lần tìm trên mạng, ghi nguồn, ghi `luu_y`. Không chép thông số từ máy khác.
- **Không bịa** giá, thời gian, bảo hành. Thiếu dữ liệu quan trọng thì hỏi bạn hiền. Giá không có trong bảng thì để Liên hệ.
- **Giá trong bài để Liên hệ, toàn bộ** (bạn hiền yêu cầu 2026-11-04, bài Redmi K90 Pro Max): kể cả dịch vụ phụ nhắc trong bài như thay kính, ép kính. Bảng giá có số cũng không đưa vào bài; chỉ ghi số khi bạn hiền chốt số cho đúng bài đó. Ví dụ câu bị bỏ: "Thay kính Redmi K90 Pro Max có giá 1.000.000 đồng".
- **Bạn hiền gửi một giá cho model mà bài có hai loại màn thì ghi cho Màn Zin** (bạn hiền chốt 2026-11-05, 15 bài thay màn Xiaomi): dòng Màn Zin ghi số kèm "đã gồm công thay", Màn Cao Cấp để Liên hệ, ô giá sản phẩm điền số đó. Câu đầu phần giá và câu hỏi về tiền công cũng nêu số.
- **Dấu `/` trong bảng giá bạn hiền gửi là các model cùng mức giá** (bạn hiền dặn 2026-11-05): không suy ra hai máy dùng chung màn, không viết "lắp lẫn được". Ví dụ "Redmi Turbo 5/poco x8promax 2100k" là hai máy cùng giá 2.100.000 đồng.
- Dịch vụ chọn theo dữ liệu, không mặc định thay màn. Không rõ thì hỏi.
- **Ảnh ghép hai mặt màn hình trong một khung chỉ dùng làm ảnh đại diện, không đưa vào thân bài.** Ảnh tách riêng từng mặt cũng không đưa vào thân bài, chỉ thêm vào album ảnh đại diện (bạn hiền chốt 2026-11-05, bài Redmi 10C).
- **Cách thêm ảnh mặt trước, mặt sau của màn vào album ảnh đại diện.** `bai.py` chưa làm bước này. Sau khi đăng: xuất ảnh ra webp tên `<slug>-mat-truoc.webp`, `<slug>-mat-sau.webp`, không kèm dữ liệu ẩn, tải lên thư viện với alt có từ khóa, mở trang sửa sản phẩm, điền ID vào ô `#product_image_gallery` theo thứ tự trước rồi sau, bấm `#publish`, rồi kiểm tra trang công khai có đủ ảnh trong album. Không gắn khung vì thanh dưới của khung che mép màn.
- **Soát ảnh của bạn hiền một lần:** phóng to chữ trên màn. Thấy tên máy khác thì báo, alt không khẳng định là model đó.
- **Xóa dấu vết AI trong ảnh:** nhãn trong dữ liệu ẩn (C2PA, XMP) tự mất khi script xuất ảnh, bước `kiem` báo `LOI` nếu còn. Logo AI nhìn thấy ở góc ảnh thì che bằng `| che=x0,y0,x1,y1`. Dấu ẩn trong điểm ảnh không xóa được, không hứa với bạn hiền. Alt mô tả tình trạng máy, không viết là máy của khách. Bạn hiền gửi ảnh thì mặc định phải làm bước này, kể cả khi không nhắc. Ảnh có hình dáng khác hẳn model (tai thỏ trong khi máy dùng lỗ camera) thì không dùng và báo lại.

## 2. Viết file nguồn `production/<slug>-<YYYY-MM-DD>.md`

Mẫu về cách ghi file nguồn: `production/thay-man-hinh-oppo-reno-15c-2026-11-03.md`, chỉ học khung, không chép câu. Mẫu về nội dung: xem mục "Học từ bài mẫu Xiaomi Civi 1" bên dưới. Đầu file:

```
---
title: 55–70 ký tự, 1 lần từ khóa, có yếu tố hút khách (lấy ngay, giá rẻ...), không có từ bắt đầu bằng đ
meta: 150–160 ký tự, có từ khóa, không ghi số điện thoại
slug: thay-man-hinh-vivo-x60
tieu_de: Thay màn hình Vivo X60
tu_khoa: thay màn hình Vivo X60
tu_khoa_phu: ...
chu_anh_dai_dien: VIVO X60
anh_dai_dien: vivo x60/anh-dai-dien-vivo-x60.png
thoi_gian: 60–90 phút
bao_hanh: 6 tháng
danh_muc: 1872, 129
goc_viet: ...
nguon: ...
anh: ten-ngan = vivo x60/ten-file.png
anh: ten-ngan = xuong:<file trong production/anh/thay-man-hinh-huawei-mate-40-pro/goc>
anh: ten-ngan = vivo x60/ten-file.png | che=x0,y0,x1,y1   (làm mờ một vùng theo tọa độ ảnh gốc)
luu_y: điều còn chờ xác nhận (được phép nhiều dòng)
mo_ta: chỉ ghi khi không phải thay màn (nhiều dòng, thay mô tả ngắn mặc định)
---
```

Danh mục: Vivo `1872, 129`; OPPO `1871, 126`. Hãng khác thì tra trong trang admin.

Thân bài dùng: `## H2` (script tự đánh số và tô màu), `### H3`, `**đậm**`, `[chữ](url)`, `- `, `1. `, bảng `|`, `![alt có từ khóa](ten-ngan)`, `{{co-so}}` (hai địa chỉ và bản đồ).

**Luật viết:**
- **Ngôn từ thân thiện, dễ hiểu:** người không biết kỹ thuật đọc là hiểu ngay. Câu ngắn, tự nhiên. Thuật ngữ giải thích trong ngoặc: "cáp màn (dây nối màn với máy)". Viết "kỹ thuật viên", tránh tiếng nghề cụt lủn. Khi sửa để giảm trùng vẫn giữ câu tự nhiên.
- **Lời lịch sự, thu hút, không cộc hay suồng sã** (bạn hiền yêu cầu 2026-11-04). Không viết kiểu "bạn nghe giá rồi đổi ý thì cứ cầm máy về", "sau này chỉ cần đọc số điện thoại là tra được". Viết kiểu "Bạn thoải mái cân nhắc, chỉ sửa khi thấy phù hợp", "thông tin lưu trực tuyến nên bạn tra cứu rất dễ dàng". Tránh "cứ", "khỏi lo", "ca nặng", "không nghe lời", "ráp", "đem máy".
- **Câu từ có vần, thu hút, không cộc lốc** (bạn hiền yêu cầu 2026-11-04, bài Redmi Note 15 4G): câu có nhịp, đọc xuôi tai; dùng cụm cân đối ở chỗ cần nhấn, như "rõ lỗi, rõ giá", "xem tận mắt, ưng ý mới thay", "hợp nhu cầu, hợp túi tiền". Vần phải tự nhiên, không ép vần làm sai nghĩa hay thêm lời hứa ngoài não. Không để câu trả lời chỉ có vài chữ trống trơn, nối ý bằng lý do hoặc lợi ích cho khách.
- **SEO, AIO, GEO:** phần lớn H2 là câu hỏi khách hay tìm, có tên model. Câu đầu dưới mỗi H2 trả lời thẳng. Dùng bảng, danh sách, các bước đánh số. Câu hỏi FAQ có tên model, câu trả lời mở bằng kết luận và đọc riêng vẫn hiểu. Nêu rõ Gia Huệ Mobile, Hà Nội, thời gian, bảo hành. Thông số lấy từ ngoài thì dẫn link nguồn.
- **Viết để AI dễ đề xuất và trích dẫn** (bạn hiền yêu cầu 2026-11-04): câu đầu dưới mỗi H2, H3 và FAQ tách riêng vẫn đủ nghĩa, có tên model, không mở bằng "Có.", "Không.", "Chưa hẳn." rồi mới nói tiếp, không dùng "tại đây", "hiện tượng này", "như trong ảnh", "việc này". Có một bảng thông tin nhanh ở H2 đầu hoặc thứ hai: nơi làm, thời gian, kiểm tra máy, viết ngắn dưới bảng giá hoặc thành bảng riêng. Câu trả lời về giá, địa chỉ nêu rõ **Gia Huệ Mobile**, Hà Nội, con số thật; câu địa chỉ nêu 22 năm kinh doanh (đã xác nhận). Thông số viết kèm tên nguồn. Không tự khen "tốt nhất", "uy tín nhất".
- **Mở bài là sapo 3 đoạn, tổng 130–230 từ** (bạn hiền chốt 2026-11-04, mẫu Xiaomi Civi 3; nâng từ 180 lên 230 từ ngày 2026-11-05, theo mẫu bài OnePlus Ace 3 Pro), đứng trước ảnh đầu, không có câu hỏi, script báo `LOI` nếu sai. Đoạn 1: lỗi nào cần kiểm tra để xác định chính xác, trường hợp nào còn cứu được, chảy mực thì phải thay màn; kỹ thuật viên **Gia Huệ Mobile** kiểm tra trước để biết nguyên nhân. Đoạn 2: có từ khóa, mất bao lâu kèm điều kiện (máy không có lỗi khác; cửa hàng luôn có sẵn linh kiện), có key dịch vụ, khách theo dõi được lúc sửa. Đoạn 3: chi phí báo trước, bảo hành bao lâu và phạm vi. Học khung, không chép câu; số liệu lấy theo đúng model. Từ khóa không bắt buộc ở đầu sapo. Mỗi câu vẫn không quá 32 từ.
- **Sapo không dẫn khách tới chuyện thay màn mới ngay** (bạn hiền yêu cầu 2026-11-05, bài Redmi 13C): sọc, vỡ kính, liệt cảm ứng và các lỗi tương tự thì nói rõ cần kiểm tra để xác định chính xác nguyên nhân, kèm trường hợp còn cứu được, như vỡ kính mà hình còn rõ, cảm ứng còn nhạy có thể chỉ cần ép kính. **Riêng chảy mực thì nói rõ phải thay màn.** Ví dụ câu bị bỏ: "Khi màn chập chờn, tự bấm loạn hay nổi sọc khiến Redmi 13C khó dùng, bạn nên cân nhắc đổi màn." Lời thu hút, có nhịp, không cộc lốc. Không dùng câu hỏi, tổng sapo vẫn 130–230 từ. Luật này thay cho "máy bị dấu hiệu gì thì nên cân nhắc thay" ở khung sapo.
- **Sapo theo mẫu bạn hiền sửa tay** (bạn hiền gửi 2026-11-05, bài OnePlus Ace 3 Pro): mỗi bài nói khác lời nhưng giữ nguyên nghĩa của 3 đoạn dưới đây, đổi số liệu theo đúng model. Câu văn có vần, có nhịp, thu hút, không cộc lốc, không khó hiểu. Viết câu đủ ý, không rút gọn kiểu tiếng nghề. Ví dụ câu bị thay: "cần soi kỹ trước, vì mỗi lỗi một hướng xử lý" thành "cần kiểm tra kỹ trước, vì mỗi lỗi có một hướng xử lý riêng"; "Tiền sửa được báo từ đầu" thành "Chi phí được thông báo trước khi sửa". Mẫu gốc của bạn hiền:
  > Trên OnePlus Ace 3 Pro, sọc màn, nứt kính hay cảm ứng chập chờn đều cần kiểm tra kỹ trước, vì mỗi lỗi có một hướng xử lý riêng. Kính vỡ nhưng hình ảnh vẫn sáng đẹp, cảm ứng nhạy thì ép kính có thể đã đủ. Riêng trường hợp màn chảy mực thì cần thay màn. Kỹ thuật viên Gia Huệ Mobile kiểm tra, xác định nguyên nhân và giải thích rõ tình trạng máy ngay trước mặt bạn.
  > Khi thực sự cần thay, dịch vụ thay màn hình OnePlus Ace 3 Pro mất khoảng 45–60 phút, nếu có sẵn linh kiện và máy không phát sinh lỗi khác. Màn mới được test thử, bạn kiểm tra và hài lòng mới tiến hành thay. Sau khi hoàn tất, máy được dán đầy đủ keo kháng nước. Bạn có thể ngồi cạnh bàn sửa và theo dõi toàn bộ quá trình.
  > Chi phí được thông báo trước khi sửa, rõ tình trạng và rõ giá. Nếu phát hiện thêm lỗi trong quá trình làm, cửa hàng sẽ báo lại để bạn quyết định trước khi xử lý. Với lỗi phát sinh do quá trình sửa chữa, Gia Huệ Mobile chịu trách nhiệm bồi thường theo chính sách của cửa hàng. Máy được bảo hành lỗi cảm ứng 6 tháng, hỗ trợ tra cứu bảo hành trực tuyến.
  Mẫu ghi "keo kháng nước", còn key của skill là "dán đầy đủ keo tếp kháng nước": bài vẫn viết đủ key, cho tới khi bạn hiền chốt khác. Tổng sapo vẫn giữ 130–230 từ.
- **Thân bài có hai H2 riêng: khách lo gì và nhận được gì khi thay màn tại Gia Huệ Mobile** (bạn hiền yêu cầu 2026-11-05, bài Redmi 13C): H2 lo gì có bảng nỗi lo và việc cửa hàng làm; H2 nhận được gì nêu quyền lợi có trong não, đặt 3 đặc quyền và phần keo tếp thành H3 để giữ tổng 8–10 H2. Thân bài mới không tự thêm "lỗi 1 đổi 1", "hoàn tiền"; mô tả ngắn và bài cũ đang có hai cụm này thì giữ nguyên (bạn hiền chốt 2026-11-05).
- **Viết rõ chuyện phát sinh** (bạn hiền yêu cầu 2026-11-04): không viết chung chung "nếu có phát sinh cửa hàng sẽ hỏi lại bạn". Phải nói đủ hai ý: khi chưa làm, lúc kiểm tra thấy thêm lỗi thì cửa hàng báo lại cho khách; nếu lỗi do cửa hàng thì cửa hàng bồi thường. Đưa vào đoạn 3 của sapo và câu hỏi về giá phát sinh.
- **Xưng là "cửa hàng"** (bạn hiền yêu cầu 2026-11-04): không viết "bên mình", "bên em", "chúng tôi", "chúng em", "xưởng", kể cả trong alt ảnh; script báo `LOI`. Vẫn gọi khách là "bạn" và vẫn nêu tên **Gia Huệ Mobile**.
- **Mỗi bài 8–10 H2, có dấu hiệu và nguyên nhân** (bạn hiền yêu cầu 2026-11-04): phải có một H2 về dấu hiệu và một H2 về nguyên nhân hỏng, tên H2 ghi rõ hai chữ này. Ý phụ thì đưa xuống H3. Script báo `LOI` nếu sai.
- **Độ dài 1.500–2.500 từ** (bạn hiền chốt 2026-11-03, tính cả địa chỉ và dòng liên quan; script báo `LOI` ngoài khoảng này).
- **Mô tả SEO không ghi số điện thoại** (bạn hiền yêu cầu 2026-11-05, bài Xiaomi Mi 11 Ultra): ô meta chỉ giữ từ khóa, key và lợi ích. Ví dụ câu bị bỏ: "Gọi 0962 528 528." Hotline vẫn đặt trong thân bài theo luật CTA. Script chưa kiểm tra luật này, phải tự soát.
- **Tiêu đề SEO có yếu tố hút khách và luân phiên giữa các bài** (bạn hiền yêu cầu 2026-11-03, bổ sung 2026-11-05, bài Xiaomi 17 Pro Max): ghép tự nhiên sau từ khóa, đổi yếu tố giữa các bài, không lặp mãi "lấy ngay, giá rẻ". Các yếu tố: uy tín; bao mọi rủi ro khi thay; test ưng mới thay; giá tốt; lấy ngay. Ví dụ: "Thay màn hình Xiaomi 17 Pro Max uy tín, test Ưng mới thay tại Hà Nội". Không viết "uy tín nhất". Web tự viết hoa đầu mỗi chữ trong thẻ tiêu đề nhưng bỏ sót chữ mở đầu bằng "ư", nên trong file nguồn ghi "test Ưng mới thay" để web hiện đúng. Trước khi đặt tiêu đề, xem tiêu đề bài gần nhất bằng `grep -h "^title:" production/*.md | tail` để chọn cặp khác. Script báo `LOI` nếu thiếu yếu tố.
- **Link ngoài để nofollow, link nội bộ giahuemobile.com để dofollow** (bạn hiền yêu cầu 2026-11-03): viết link bình thường, script tự gắn và tự kiểm tra. Tiếp theo là các phần giúp khách biết **khi nào chưa cần thay**; giá, thời gian, bảo hành; quy trình; FAQ từ 6 câu (tên H2 có chữ "hỏi"); `{{co-so}}`; câu kết có từ khóa; dòng trang liên quan.
- **Cấu trúc link nội bộ 3-2-1** (bạn hiền yêu cầu 2026-11-05): 3 link dịch vụ liên quan cùng model hoặc dòng máy (ép kính, thay pin, model kế cận); 2 link bài cẩm nang phân biệt lỗi hoặc bảng giá tổng của hãng; 1 link trỏ về danh mục cha (dofollow, anchor text tự nhiên). Chỉ dùng trang đang hoạt động; thiếu loại trang nào thì không tự tạo đường dẫn, ghi vào `luu_y` và báo bạn hiền. Script chưa kiểm tra đủ cấu trúc này, phải tự soát.
- **Chốt chuyển đổi (CTA)** (bạn hiền yêu cầu 2026-11-05): chèn Hotline/Zalo 0962.528.528 ở 2 vị trí: ngay sau bảng giá và đoạn kết bài. Lời kêu gọi lịch sự, hướng khách mang máy kiểm tra miễn phí trước. Script chưa kiểm tra đủ hai vị trí này, phải tự soát.
- **Tên file ảnh** (bạn hiền yêu cầu 2026-11-05): toàn bộ viết thường, không dấu, ngăn cách bằng dấu gạch ngang, ví dụ `slug-chuan-seo.webp`.
- **Bảng giá thay màn chia theo loại màn** (bạn hiền yêu cầu 2026-11-04, bài Xiaomi 12): mỗi dòng một loại, Màn Zin và Màn Cao Cấp, bốn cột Loại màn, Giải thích, Bảo hành, Giá; cột giá ghi Liên hệ. Không để dòng "Cập nhật" hay "Tháng 11/2026" trong bảng.
- **Cửa hàng luôn có sẵn linh kiện** (bạn hiền xác nhận 2026-11-05, bài OnePlus Ace 5 Pro): nói thời gian kèm điều kiện máy không có lỗi khác, không viết "nếu có sẵn linh kiện", "khi đủ linh kiện". Luật này thay cho điều kiện "có sẵn linh kiện" ở khung sapo và mẫu sapo ở trên. Ví dụ câu bị thay: "45–60 phút khi linh kiện sẵn sàng" thành "45–60 phút khi máy không còn lỗi nào khác, nhờ cửa hàng luôn có sẵn linh kiện".
- **Tra cứu bảo hành ghi rõ hai đường** (bạn hiền bổ sung 2026-11-05, bài OnePlus Ace 5 Pro): thông tin bảo hành tra online qua phiếu hoặc trên website giahuemobile.com, mục Tra cứu bảo hành. Không chỉ viết chung chung "tra cứu trực tuyến"; nêu đủ hai đường ở phần quyền lợi và câu hỏi về bảo hành.
- **Bảo hành thay màn chỉ ghi lỗi cảm ứng 6 tháng** (bạn hiền chốt 2026-11-04): không viết "lỗi hiển thị và cảm ứng", kể cả khi trang cũ trên web đang ghi vậy; `bai.py` kiểm tra.
- **FAQ là thắc mắc thật của khách về dịch vụ** (bạn hiền yêu cầu 2026-11-04): ưu tiên điều khách lo trước khi giao máy, không viết câu để lấp cho đủ số. Luôn có câu "Thay màn hình <model> có mất dữ liệu không?" (đúng dịch vụ của bài); `bai.py` kiểm tra có chữ "dữ liệu" trong câu hỏi. Chọn thêm theo bài: có xem ảnh, tin nhắn không; giá đã gồm tiền công chưa; không sửa được có mất phí không; có được xem làm không; màn có kèm khung không; mất phiếu có được bảo hành không. Câu trả lời chỉ lấy từ não; não chưa có thì bỏ câu đó, không đoán. Không lặp lại H3 đã có ở H2 khác.
- **Nội dung phải khác biệt** (bạn hiền nhắc lại 2026-11-03): mỗi bài một góc và bố cục riêng: đổi tên, thứ tự H2, cách trình bày giá, quy trình, FAQ. Không chép câu từ bài trước. Chỉ giữ nguyên dữ liệu bắt buộc.
- **Mỗi ảnh đặt ngay dưới một H2 hoặc H3 có nội dung đúng với ảnh** (bạn hiền yêu cầu 2026-11-04), rồi mới tới câu trả lời. Không đặt ảnh giữa đoạn hay giữa danh sách, mỗi tiêu đề một ảnh; hai ảnh cùng phần thì thêm H3. Script báo `LOI` nếu sai.
- **Ảnh dãn đều theo các H2** (bạn hiền yêu cầu 2026-11-04): mỗi H2 nhiều nhất một ảnh, không dồn nhiều ảnh vào một H2, nhất là H2 đầu. Ảnh vẫn phải đúng nội dung của tiêu đề; bài ít ảnh hơn H2 thì để trống H2 đã có bảng hoặc FAQ. Script chưa kiểm tra luật này, phải tự soát.
- Từ 5 ảnh. Mật độ từ khóa 1–1,5%.
- **Bôi đậm từ khóa chính và Gia Huệ Mobile ở mọi lần xuất hiện trong đoạn văn, danh sách, bảng và câu trả lời FAQ** (bạn hiền yêu cầu 2026-11-05, bài Redmi 10X 5G); không bôi trong tiêu đề, alt ảnh, link và dòng trang liên quan. Script chưa kiểm tra luật này, phải tự soát.
- Key đúng dịch vụ: thay màn "dán đầy đủ keo tếp kháng nước"; thay pin "dùng thử miễn phí 1 tháng"; ép kính "test nhiệt" và "bao mọi xác suất, lỗi là đền". Không gắn nhầm, không mở rộng; keo không phải chống nước. **Viết đúng "keo tếp", không viết "keo tiếp"** (bạn hiền sửa 2026-11-05, bài Redmi 13C: "keo tếp nhé không phải keo tiếp"); `bai.py` đã kiểm tra theo chữ này.
- **Nhấn mạnh key và thương hiệu (bắt buộc, bạn hiền yêu cầu 2026-11-03):** key của dịch vụ phải có trong sapo và meta, bôi đậm đúng nguyên cụm từ 3 chỗ trở lên (sapo, quyền lợi hoặc quy trình, FAQ). Nên có một H2 hoặc đoạn riêng giải thích key đó giúp gì cho khách. **Gia Huệ Mobile** bôi đậm từ 3 chỗ. Với thay màn, script báo `LOI` nếu thiếu.
- **Khung ảnh đại diện giữ nguyên** (bạn hiền chốt 2026-11-05, bài Redmi K70 Pro): chữ in sẵn trên khung như "Bao mọi xác suất", "Không phát sinh chi phí", "Nguyên zin" không phải lỗi, không sửa và không hỏi lại. Luật key ở trên chỉ áp dụng cho phần chữ của bài.
- Từ cấm và lời hứa tuyệt đối: script tự dò. Không dùng tên, dữ liệu, câu chữ của web tham khảo.
- Không khẳng định "chắc chắn phải thay" khi chưa xem máy. Viết giọng người trong nghề, lời phổ thông.

### Viết chạm insight khách hàng cuối (bạn hiền yêu cầu 2026-11-04)

Người đọc là **người dùng điện thoại đang có máy hỏng**, không phải cửa hàng hay đại lý. Viết như đang nói chuyện với một người đang lo cho chiếc máy của mình, để họ thấy "đúng cái mình đang lo" và muốn mang máy đến.

**Mỗi nỗi lo thật phải được gỡ bằng một việc Gia Huệ thật sự làm, có trong não:**

| Khách lo | Gỡ bằng |
|---|---|
| Bị tráo linh kiện | Khách ký lên linh kiện, ngồi xem sửa, nhận lại linh kiện cũ |
| Bị vẽ thêm bệnh, báo sai lỗi | Kiểm tra trước mặt khách, ghi phiếu, khách đồng ý mới sửa |
| Giá phát sinh khi đã mở máy | Báo giá trọn gói trước khi sửa; lúc kiểm tra thấy thêm lỗi thì báo lại cho khách; lỗi do cửa hàng thì cửa hàng bồi thường |
| Mất dữ liệu, ảnh, tài khoản | Trả lời thẳng có mất hay không, khi nào nên sao lưu |
| Thay xong màn kém, mất tính năng | Thử linh kiện trước khi lắp, khách tự thử lại trước khi nhận |
| Phải để máy lại, không có máy dùng | Nói rõ thời gian, có lấy trong ngày hay không |
| Sửa xong lỗi lại, khó đòi bảo hành | Bảo hành điện tử tra bằng số điện thoại, nói rõ phạm vi |
| Tốn tiền oan khi chưa cần thay | Nói thật lúc nào chưa cần thay, phương án rẻ hơn nếu có |

**Cách viết:**
- Bắt đầu từ tình huống đời thường của đúng model: rơi máy, màn sọc giữa lúc cần liên lạc, ảnh gia đình còn trong máy. Không dùng tình huống hay câu chuyện khách hàng tự nghĩ ra rồi kể như có thật.
- Nói về lợi ích cho khách trước, tính năng dịch vụ sau: "bạn biết rõ số tiền trước khi sửa" thay vì "chính sách báo giá minh bạch".
- Thu hút bằng sự thật và sự yên tâm. Không hù dọa, không hối thúc, không hứa quá dữ liệu trong não.
- Mỗi lần nêu lo lắng thì có câu gỡ ngay sau đó. Sapo không có câu hỏi; phần chạm nỗi lo đặt ở thân bài và câu hỏi thường gặp.
- Câu kết mời hành động nhẹ, dễ làm: mang máy đến kiểm tra trước, thấy hợp lý mới sửa, gọi hoặc nhắn Zalo.

### Hai phần bạn hiền dặn phải chú ý (2026-11-04)

**Mẫu chung thay màn (bạn hiền gửi 2026-11-04):** bài thay màn phải có thông điệp "test thử, ưng ý mới thay", 3 đặc quyền (test thử màn trước khi lắp; giữ dữ liệu, lấy máy nhanh; bảo hành tra cứu trực tuyến) và quy trình 4 bước (kiểm tra và báo giá; thay màn; kiểm tra sau khi lắp; khách nghiệm thu, nhận bảo hành). Đổi thông số, vân tay, thời gian, bảo hành theo đúng model, viết lại lời mỗi bài. Chi tiết và bản gốc: `wiki/khai-niem/mau-chung-thay-man-theo-model.md`, chỉ cần mở trang này khi bài là thay màn. Không lấy "40 phút" của Vivo X90 Pro cho máy khác.

**Quy trình:** lấy từ bản 5 bước trong `wiki/khai-niem/quy-trinh-sua-chua-website.md` (bản mới nhất trên web), kết hợp bước riêng của dịch vụ, viết lại lời cho mỗi bài. Các ý cần có khi đúng với dịch vụ: kiểm tra 12 điểm trước mặt khách và hai bên ký phiếu; phân đúng thợ theo lỗi; khách ký lên linh kiện và được ngồi xem sửa; thử linh kiện mới trước khi lắp; trưởng nhóm kiểm tra trước khi bàn giao; khách thử lại máy; bảo hành điện tử tra bằng số điện thoại; linh kiện cũ giao lại cho khách. Không viết "100%" vì là từ cấm. Không tự thêm bước hay cam kết ngoài nguồn.

**Key kinh doanh:** trước khi chạy `bai.py`, tự soát key đúng dịch vụ (luật "Key đúng dịch vụ" và "Nhấn mạnh key" ở trên). `bai.py` chỉ kiểm tra bôi đậm với thay màn, còn thay pin và ép kính phải tự soát đủ sapo, meta, 3 chỗ bôi đậm. ⚠️ Bài ép kính: `bai.py` coi "bao mọi" là từ cấm trong khi key lại có "bao mọi xác suất, lỗi là đền". Không bỏ key để cho hết `LOI`, hãy báo bạn hiền.

**Ảnh nhân viên:** thư mục Drive "TVC ảnh" (https://drive.google.com/drive/folders/10aNiriLfnGITtOKL-pr3KF90YH6A3H4s), gồm 3 thư mục `Gia Hue Mobie`, `VTP`, `TH`; **lựa ảnh trong cả 3 thư mục này** (bạn hiền dặn 2026-11-05), chọn ảnh đúng với đoạn đang viết và đổi ảnh giữa các bài, không dùng lại mãi vài ảnh đã tải. Trên máy, ảnh đã tải nằm ở `production/anh/thay-man-hinh-huawei-mate-40-pro/goc`; chưa có ảnh phù hợp thì tải thêm từ Drive. **Lấy nguyên ảnh, chỉ thêm khung Gia Huệ Mobile** (bạn hiền chốt 2026-11-04): không che, không làm mờ mặt, không chỉnh sửa gì khác. Ảnh nào không đạt thì bỏ ảnh đó, không sửa. Ảnh ghép hai mặt màn hình chỉ dùng làm ảnh đại diện, gắn vào khung ảnh đại diện. Soát trước khi dùng: đúng việc đang nói trong đoạn, không lộ thông tin khách, không ghi tên nhân viên trong alt nếu bạn hiền chưa cho phép. Không dùng ảnh có biển địa chỉ cũ (179 Vũ Tông Phan, 45/76 Mai Dịch; xem `wiki/khai-niem/xac-nhan-cua-ban-hien.md` mục 17). Tiêu chí ảnh chung: `wiki/khai-niem/quy-chuan-hinh-anh-va-prompt.md`.

**Ảnh phần địa chỉ (bạn hiền yêu cầu 2026-11-04):** dưới H2 địa chỉ dùng ảnh toàn thể nhân viên đứng trước cửa hàng: `anh: toan-the-nhan-vien = xuong:toan-the-nhan-vien-dsc00012.jpg`. Dòng 179 Vũ Tông Phan, 45/76 Mai Dịch trong ảnh này nằm trên biển quán bên cạnh, không phải biển Gia Huệ. Không dùng DSC00017 vì biển LED ghi "Bảo hành 12 tháng".

### Học từ bài mẫu Xiaomi Civi 1

Bạn hiền chọn bài mẫu ngày 2026-11-04: https://giahuemobile.com/san-pham/thay-man-hinh-xiaomi-civi-1/. Phần cần học đã rút ở đây, **không cần mở lại trang**. Chỉ học cách viết, không chép câu chữ, thời gian, bảo hành, thông số.

**Câu trả lời đi trước (Answer-First), để AI dễ trích dẫn:**
- Mỗi H2 và mỗi H3 dạng câu hỏi: câu đầu trả lời luôn, như "Có, nếu màn thay thế hỗ trợ đúng...", "Thông thường không.", "Chưa thể kết luận chỉ dựa vào...". Sau đó 1–3 câu nói lý do và trường hợp ngoại lệ.
- Câu trả lời tách riêng khỏi bài vẫn hiểu: nhắc tên model, không viết "như trên", "lỗi này".
- Không kêu gọi thay ngay. Nói thật lúc nào chưa cần thay, và chỗ nào phải kiểm tra máy mới biết.

**Các nhóm nội dung nên có** (thay màn; dịch vụ khác đổi cho phù hợp). Giữ đủ ý, nhưng đổi tên và thứ tự H2 theo từng bài để không trùng nhau:
1. Khi nào cần thay, khi nào chưa: mỗi dấu hiệu một H3 (sọc, chảy mực, mất hiển thị, lỗi cảm ứng), viết theo thứ tự dấu hiệu → nguyên nhân có thể → nên làm gì; phân biệt với ép kính.
2. Có mấy loại màn, nên chọn loại nào: bảng so theo tiêu chí, có dòng "phù hợp với ai", rồi một kết luận chọn theo nhu cầu. Chỉ viết khi có dữ liệu.
3. Thay xong có ảnh hưởng gì không: H3 câu hỏi về tần số quét, vân tay, dữ liệu. Chỉ hỏi tính năng mà đúng model đó có.
4. Mất bao lâu, có lấy ngay không, có được ngồi xem sửa không.
5. Quy trình theo bước: tên mỗi bước nói rõ việc làm, có bước thử màn mới trước khi lắp.
6. Giá: bảng theo dịch vụ, cùng các câu hỏi giá bao nhiêu, đã gồm công chưa, bảo hành bao lâu.
7. Câu hỏi thường gặp.
8. Địa chỉ, vài lợi ích ngắn, câu kết mời khách chưa rõ lỗi mang máy đến kiểm tra trước.

**Chỗ không theo mẫu, vẫn giữ luật của skill này và của `bai.py`:**
- Sapo 3 đoạn theo khung mẫu Xiaomi Civi 3, tổng 130–230 từ, có key.
- Bài 1.500–2.500 từ (mẫu khoảng 3.450 từ). FAQ từ 6 câu (mẫu 3 câu).
- Thuật ngữ phải giải thích trong ngoặc (mẫu để nguyên "socket", "tấm nền OLED").
- Key viết đúng "dán đầy đủ keo tếp kháng nước" (bạn hiền chốt 2026-11-05; mẫu có chỗ ghi "keo tép" là sai).
- In đậm vừa phải (mẫu hơn 100 chỗ, tính cả tiêu đề và bảng).
- Tiêu đề, mô tả và thân bài phải nói cùng một thời gian (mẫu: mô tả ghi "30p", thân bài ghi 40–60 phút).

## 3. Chạy công cụ

```bash
python production/cong-cu/bai.py production/<file-nguon>.md | grep -E "LOI|KET|KB"
```

Xem **một lần** `production/anh/<slug>/xem-nhanh.jpg`. Có `LOI` thì sửa file nguồn rồi chạy lại `dung` và `kiem`, không chạy lại `anh` nếu ảnh không đổi. Trùng cao thì tìm câu trùng và viết lại chính các câu đó.

## 4. Đăng qua Claude in Chrome (khi bạn hiền đã bảo đăng)

Trong `ToolSearch`, tải một lần các công cụ: `tabs_context_mcp`, `navigate`, `javascript_tool`, `find`, `file_upload`. Mở `https://giahuemobile.com/wp-admin/post-new.php?post_type=product`, **chờ kết quả navigate rồi** chạy:

```js
const i=document.createElement('input');i.type='file';i.id='tai-goi';i.setAttribute('aria-label','tai goi dang bai');document.body.prepend(i);location.pathname
```

`find` ô `aria-label "tai goi dang bai"`, dùng `file_upload` tải `production/dang/<slug>-goi.txt`, rồi chạy bước 1:

```js
const g=JSON.parse(await document.querySelector('#tai-goi').files[0].text()); const AF=Object.getPrototypeOf(async function(){}).constructor; JSON.stringify(await new AF('g',g.js1)(g))
```

Có `da_bam_dang: true` thì chạy bước 2. Có `dung` thì dừng, đọc lý do, không ép đăng (trang đã tồn tại hoặc nằm trong thùng rác thì hỏi bạn hiền).

```js
const k=document.querySelector('#editable-post-name-full')?.textContent; const s=JSON.parse(localStorage.getItem('gh_sau_dang:'+k)||'null'); if(!s) {'khong co goi: '+k} else {const AF=Object.getPrototypeOf(async function(){}).constructor; JSON.stringify(await new AF('s',s.js2)(s))}
```

**Mỗi bài đặt thời gian xuất bản cách bài trước 1,5–3 tiếng** (bạn hiền dặn 2026-11-06, bài Vivo Z1x; nới từ cố định 3 tiếng thành 1,5–3 tiếng ngày 2026-11-06, bài Realme GT 5: "thời gian bạn để cách nhau 1,5-3 tiếng nhé không cần cố định 3 tiếng"). Chọn khoảng cách khác nhau giữa các bài, giờ phút lẻ cho tự nhiên. Lấy ngày của sản phẩm mới nhất, tính cả bài đã hẹn giờ: `fetch('/wp-json/wp/v2/product?status=publish,future&orderby=date&order=desc&per_page=1&_fields=id,date,status')`, cộng 1,5–3 tiếng. Chỗ nào dưới đây ghi "3 tiếng" thì hiểu là khoảng 1,5–3 tiếng. Giờ đó đã qua (bài trước cách hiện tại từ 3 tiếng trở lên) thì giữ giờ đăng thực tế, không lùi ngày (bài Vivo Z1x: bài trước 17:12 ngày 05/11, đăng 10:27 ngày 06/11 nên giữ nguyên). Bước 1 vẫn đăng ngay để bước 2, album ảnh và `kiem-web` chạy được trên trang công khai; làm xong hết mới đổi `date` qua REST (`POST /wp-json/wp/v2/product/<id>` với `date` và `status: 'future'` nếu giờ đó chưa tới), rồi kiểm tra lại trạng thái. Báo bạn hiền giờ hẹn.

**Không hẹn giờ đăng từ 22:00 tới 05:00** (bạn hiền dặn 2026-11-06, bài Vivo Y200 GT: "không cài bài vào những khoảng thời gian như: từ 22h đổ lên và 5h đổ xuống"). Giờ cộng 3 tiếng rơi vào khoảng này thì dời sang 05:30 sáng hôm sau, bài kế tiếp tính 3 tiếng từ giờ mới. Ví dụ: bài trước 20:27 thì bài sau hẹn 05:30 hôm sau, không phải 23:27. Đăng ngay mà giờ thực tế rơi vào khoảng này thì cũng chuyển sang hẹn 05:30.

Gói tạm lưu riêng theo đường dẫn của bài (`gh_sau_dang:<slug>`), nên nhiều phiên đăng song song trên cùng trình duyệt không đè nhau (sửa 2026-11-05). Báo `khong co goi` thì đọc đường dẫn trong thông báo: nếu khác slug trong gói (WordPress thêm `-2` chẳng hạn) thì dừng và hỏi bạn hiền, không ép chạy. Tên model có dấu `+` thì viết thành "Plus" trong toàn bài: tiêu đề, meta, H1, thân bài, alt, chữ trên ảnh đại diện (bạn hiền yêu cầu 2026-11-06, bài Vivo X50 Pro+: "đổi toàn bộ + thành plus"). Nếu vẫn gặp dấu `+` (gặp 2026-11-06, bài Vivo X50 Pro+): WordPress đặt đường dẫn từ tiêu đề, bỏ dấu `+` nên trùng bài cùng dòng và thêm `-2`; khi chắc là bài vừa tạo, đổi `slug` của bài đó qua REST cho khớp gói, mở lại trang sửa rồi chạy bước 2.

Bước 2 đã kiểm tra trang công khai; cần `anh_ok` bằng `anh_can`, `trang` 200, `rm` 200, trong `faq` có `so_faq` 1, `cau` bằng `cau_can`, `cau_lech` rỗng, `product` 1. Không chụp màn hình nếu các số đã đúng. Đóng tab đã mở. Rồi chạy `python production/cong-cu/bai.py production/<file-nguon>.md kiem-web`, cần `KET QUA: dat`.

**FAQPage (dữ liệu có cấu trúc cho phần câu hỏi):** `bai.py` lấy các câu H3 trong H2 câu hỏi của bài đưa vào gói, bước 2 và mã sửa bài lưu qua đường `updateSchemas` của Rank Math, không nhét thẻ script vào nội dung. Trên trang, Rank Math gộp thành một nút `ItemPage` + `FAQPage`, đó là đúng. Sửa câu FAQ thì phải chạy lại để FAQPage khớp chữ trên trang.

## Sửa bài đã đăng

Sửa file nguồn, đổi tên ngắn của ảnh nào có thay đổi, rồi chạy `bai.py`. Mở trang sửa sản phẩm, thêm ô tải file và tải gói như mục 4, rồi chạy mã dưới. Không xóa ảnh cũ trong thư viện, báo bạn hiền nếu cần xóa.

**Bài có đuôi 5G mà web đã có trang cùng tên không đuôi** (bạn hiền chốt 2026-11-06, bài Vivo V29 5G: "tạo trang mới vì có bản 4g nữa mà"): tạo trang mới có đuôi 5G, giữ nguyên trang cũ, ghi vào `luu_y` rằng hai trang có thể tranh từ khóa.

**Thay trang cũ đã có sẵn** (bạn hiền chốt 2026-11-04, bài Xiaomi 12: "thay giúp tôi và chỉnh lên ngày mới nhất"): hỏi trước khi thay, lưu HTML trang cũ vào `production/dang/<slug>-trang-cu-<ngày>.html`, giữ đường dẫn. Mã sửa bài chỉ đổi nội dung, Rank Math và FAQPage, nên phải tự làm thêm: đưa `featured_media`, `excerpt` (lấy `g.mo_ta`), `date` lên ngày mới nhất qua REST; rồi mở trang sửa, xóa `#_regular_price` nếu bài để Liên hệ, sửa ô `_hb_repair_time` cho khớp bài, bấm `#publish`.

```js
const g=JSON.parse(await document.querySelector('#tai-goi').files[0].text()); document.querySelector('#tai-goi').remove(); const AF=Object.getPrototypeOf(async function(){}).constructor; JSON.stringify(await new AF('g',g.js3)(g))
```

**Bài đang hẹn giờ** (bạn hiền dặn 2026-11-06: "tìm cả bài đang lên kế hoạch"): `js3` và `js4` đã tìm cả bài `status=publish,future`, không phải sửa chuỗi nữa; `kiem-web` báo 404 vì trang chưa công khai, kiểm tra trong trình duyệt đã đăng nhập thay cho bước này. Ảnh album đặt ở `production/anh/<slug>/album/`, không để chung thư mục ảnh bài vì `kiem` báo `LOI` kích thước.

**Bài có giá cụ thể** (bạn hiền chốt giá Redmi Note 10 JE 2026-11-04): `bai.py` không điền ô giá sản phẩm, trang vẫn hiện Liên hệ. Sửa số trong file nguồn và cập nhật bài trước, rồi **mở lại trang sửa** để form có nội dung mới, điền `#_regular_price` (ví dụ 550000) và bấm `#publish`. Sau đó kiểm tra trang công khai: giá, mô tả, số ảnh. Giá bạn hiền chốt mà bảng giá chưa có thì ghi vào `wiki/khai-niem/xac-nhan-cua-ban-hien.md`.

Chỉ thêm hoặc cập nhật FAQPage, không đụng nội dung và ảnh (chỉ làm với bài cũ khi bạn hiền đã đồng ý): chạy `bai.py <file-nguon> dung`, tải gói như trên, chạy mã dưới, rồi chạy `kiem-web`. Chạy lại không sinh bản trùng. File nguồn mẫu cũ (`slug: /san-pham/.../`, thiếu `tieu_de`) hoặc thiếu ảnh đại diện thì `dung` không chạy được: dùng `bai.py <file-nguon> dung-faq`, tạo gói `dang/<slug>-faq-goi.txt` chỉ có FAQPage và không ghi đè bản bài. Mã báo "Khong thay trang" thì slug trên web khác file nguồn (Redmi Note 13 Pro 5G trên web không có `xiaomi-`): đổi `g.slug` theo trang thật rồi chạy lại.

```js
const g=JSON.parse(await document.querySelector('#tai-goi').files[0].text()); document.querySelector('#tai-goi').remove(); const AF=Object.getPrototypeOf(async function(){}).constructor; JSON.stringify(await new AF('g',g.js4)(g))
```

## 5. Ghi sổ (một lệnh)

- Thêm góc của bài vào dòng "Góc đã dùng" ở `wiki/khai-niem/lenh-viet-bai-seo-dich-vu.md`.
- Thêm một dòng vào `wiki/log.md`: đường dẫn, ID sản phẩm, ID ảnh.
- Ghi điều còn chờ vào `wiki/so-sanh/mau-thuan-du-lieu-website.md`.
- Báo bạn hiền đường dẫn và những `luu_y`. Không đọc lại toàn bộ `log.md`.
