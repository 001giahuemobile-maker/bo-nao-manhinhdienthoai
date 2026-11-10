---
tieu_de: Hướng dẫn dùng bộ kiến thức website cho các phiên sau
loai: khai-niem
ngay_tao: 2026-10-30
ngay_cap_nhat: 2026-10-30
nguon: [yêu cầu của bạn hiền ngày 2026-10-30, website-giahuemobile-com-2026-10-30]
tags: [huong-dan, website, quy-trinh-ai]
---

# Hướng dẫn dùng bộ kiến thức website

Dành cho AI ở các phiên sau khi bạn hiền giao việc **viết bài, sửa nội dung, phân tích SEO, làm FAQ, viết trang dịch vụ, tư vấn kỹ thuật** cho giahuemobile.com.

## Bộ tài liệu (10 phần theo yêu cầu ngày 2026-10-30)

| # | Phần | Trang |
|---|---|---|
| 1 | Tổng quan doanh nghiệp và thương hiệu | [[gia-hue-mobile]], [[thong-tin-doanh-nghiep-tren-website]] |
| 2 | Danh sách URL đã kiểm tra | [[danh-sach-url-website]] |
| 3 | Danh mục dịch vụ, nhóm sản phẩm | [[he-thong-dich-vu-website]] |
| 4 | Dịch vụ theo hãng và model | [[gia-website-iphone]], [[gia-website-ipad-va-apple-watch]], [[gia-website-samsung]], [[gia-website-xiaomi]], [[gia-website-oppo-realme-oneplus]], [[gia-website-vivo-huawei]] |
| 5 | Lỗi và cách sửa | [[co-so-du-lieu-loi-va-cach-sua]], [[kien-thuc-ky-thuat-man-hinh]] |
| 6 | Giá, thời gian, bảo hành | 6 bảng ở mục 4, [[chinh-sach-bao-hanh-website]], [[bang-gia-dich-vu-le]] |
| 7 | Quy trình và cam kết | [[quy-trinh-sua-chua-website]], [[cam-ket-va-bao-hanh]] |
| 8 | Giọng văn, cách viết SEO | [[phong-cach-noi-dung-website]], [[quy-chuan-bai-seo]], [[seo-website-hien-trang]], khung bài [[phuong-phap-viet-hoc-tu-web-tham-khao]] (chỉ học cách viết, không dùng dữ liệu web tham khảo) |
| 9 | Thiếu, mâu thuẫn, cần xác minh | [[mau-thuan-du-lieu-website]] |
| 10 | Hướng dẫn này | trang này |

**Bạn hiền chỉ gửi tên model** → làm theo [[lenh-viet-bai-seo-dich-vu]] (lệnh ngày 2026-10-30).

## Thứ tự làm việc

1. Đọc `CLAUDE.md` rồi [[index]].
2. Xác định model và dịch vụ, mở **đúng dòng** trong bảng `gia-website-<hãng>` để lấy URL trang dịch vụ.
3. Cần chắc chắn thì **mở lại trang web đó** (dữ liệu quét ngày 2026-10-30 có thể đã cũ).
4. Giá báo khách: tra `raw/google-drive/bang-gia.md` qua [[bang-gia-dich-vu-le]]. Giá web chỉ để đối chiếu.
5. Bảo hành: theo [[chinh-sach-bao-hanh-website]]. Điểm đã chốt trong [[xac-nhan-cua-ban-hien]] được ưu tiên.
6. Thông số màn hình của model: lấy từ chính trang của model đó. **Không lấy từ model khác**, kể cả cùng dòng.
7. Viết theo [[phong-cach-noi-dung-website]] và [[quy-chuan-bai-seo]]. Trước khi viết bài mới, kiểm tra [[co-so-du-lieu-loi-va-cach-sua]] phần 2 để không viết trùng bài đã có.
8. Gặp điểm nằm trong [[mau-thuan-du-lieu-website]]: không tự chọn, hỏi bạn hiền.
9. Sản phẩm làm ra đặt ở `production/`, ghi một dòng vào [[log]].

## Không làm

- Không bịa giá, thời gian, loại linh kiện, bảo hành. Thiếu thì ghi "⚠️ Chưa có dữ liệu trong não" hoặc "Chưa tìm thấy thông tin".
- Không thêm cam kết mới (ví dụ "bảo hành vĩnh viễn", "chống nước như mới") nếu chính sách chưa có.
- Không hỏi lại bạn hiền những gì đã có trong các trang trên.

## Cập nhật bản quét

Website đổi hằng ngày (tháng 10/2026 có 93 bài mới). Nên quét lại khoảng mỗi tháng *(đề xuất)*: đọc `sitemap_index.xml`, so URL mới với [[danh-sach-url-website]], rồi chỉ đọc trang mới hoặc trang có ngày sửa (lastmod) mới hơn. Mỗi lần quét ghi một dòng vào [[log]] và cập nhật [[website-giahuemobile-com-2026-10-30]] (hoặc tạo trang tóm tắt mới theo ngày quét).
