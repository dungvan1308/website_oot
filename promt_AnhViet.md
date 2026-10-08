## 13. HỖ TRỢ ĐA NGÔN NGỮ

Website bắt buộc hỗ trợ 2 ngôn ngữ:

- Tiếng Việt (vi)
- English (en)

Sử dụng Django Internationalization (i18n) và Localization (l10n).

### Nguyên tắc

Không hard-code nội dung ngôn ngữ trực tiếp trong template nếu nội dung đó cần dịch.

Sử dụng Django translation:

- `{% translate %}`
- `{% blocktranslate %}`
- `gettext`
- `gettext_lazy`

Thiết lập:

```python
LANGUAGES = [
    ("vi", "Tiếng Việt"),
    ("en", "English"),
]
```

Ngôn ngữ mặc định:

```python
LANGUAGE_CODE = "vi"
```

Timezone:

```python
TIME_ZONE = "Asia/Ho_Chi_Minh"
```

### URL đa ngôn ngữ

Sử dụng URL có language prefix:

Tiếng Việt:

```text
/vi/
/vi/about/
/vi/services/
/vi/solutions/
/vi/products/
/vi/industries/
/vi/case-studies/
/vi/insights/
/vi/contact/
```

English:

```text
/en/
/en/about/
/en/services/
/en/solutions/
/en/products/
/en/industries/
/en/case-studies/
/en/insights/
/en/contact/
```

Sử dụng Django `i18n_patterns` hoặc cơ chế i18n chuẩn của Django.

### Language Switcher

Header phải có Language Switcher:

```text
VI | EN
```

Desktop:

```text
About
Services
Solutions
Products
Industries
Insights
Contact
[VI | EN]
```

Mobile:

Language Switcher phải nằm trong mobile menu.

Khi người dùng chuyển ngôn ngữ:

- Giữ nguyên trang hiện tại nếu có bản dịch.
- Không đưa người dùng về Homepage nếu không cần thiết.
- Giữ query parameters nếu phù hợp.
- URL phải thay đổi đúng language prefix.

### CMS đa ngôn ngữ

Các nội dung quản lý từ Django Admin phải hỗ trợ cả:

- Vietnamese
- English

Đặc biệt:

Company
Services
Solutions
Products
Industries
Case Studies
News / Articles
SEO

Ví dụ Service:

```text
Service
├── Vietnamese
│   ├── Name
│   ├── Short Description
│   └── Description
│
└── English
    ├── Name
    ├── Short Description
    └── Description
```

Không tạo nội dung tiếng Anh bằng cách dịch tự động tại runtime.

### Database

Thiết kế model để hỗ trợ nội dung song ngữ một cách rõ ràng.

Có thể sử dụng một trong hai phương án:

Phương án ưu tiên:

```text
Service
ServiceTranslation
```

Ví dụ:

```text
Service
- id
- slug
- icon
- image
- display_order
- is_active

ServiceTranslation
- id
- service_id
- language
- name
- short_description
- description
- seo_title
- seo_description
```

Áp dụng mô hình tương tự cho:

- Solution
- Product
- Industry
- CaseStudy
- Article
- CompanyProfile

Đảm bảo mỗi entity có thể có bản dịch `vi` và `en`.

### SEO đa ngôn ngữ

Mỗi ngôn ngữ phải có SEO riêng:

Vietnamese:

```text
Title
Meta Description
Canonical
```

English:

```text
Title
Meta Description
Canonical
```

Implement:

- `hreflang`
- canonical URL
- Open Graph
- language-specific sitemap nếu cần

Ví dụ:

```html
<link rel="alternate"
      hreflang="vi"
      href="https://example.com/vi/services/" />

<link rel="alternate"
      hreflang="en"
      href="https://example.com/en/services/" />
```

### Content fallback

Nếu một nội dung chưa có bản dịch English:

- Không hiển thị nội dung rỗng.
- Có thể fallback về Vietnamese.
- Admin phải có trạng thái Translation Status.

Ví dụ:

```text
Vietnamese: Published
English: Draft
```

### Admin

Trong Django Admin phải dễ nhận biết trạng thái dịch:

```text
Service
------------------------------------------------
Data Warehouse
VI: ✓ Published
EN: ✓ Published

Lakehouse
VI: ✓ Published
EN: ⚠ Missing

Business Intelligence
VI: ✓ Published
EN: Draft
```

Có filter:

- Vietnamese
- English
- Missing Translation
- Published
- Draft

### Static UI Translation

Các text giao diện cố định cũng phải hỗ trợ đa ngôn ngữ:

Ví dụ:

Vietnamese:

```text
Tìm hiểu thêm
Liên hệ với chúng tôi
Giải pháp
Dịch vụ
Sản phẩm
Tin tức
Xem chi tiết
```

English:

```text
Learn More
Contact Us
Solutions
Services
Products
Insights
View Details
```

Không hard-code các text này trong HTML.

### Date / Number / Currency

Sử dụng Django localization.

Ngày tháng phải hiển thị phù hợp với từng language.

Vietnamese:

```text
08/10/2026
```

English:

```text
Oct 8, 2026
```

Không hard-code format ngày tháng.

### Sitemap

Sitemap phải hỗ trợ URL của cả:

```text
/vi/
/en/
```

Các URL phải có `hreflang` tương ứng khi phù hợp.

### Accessibility

Language switcher phải:

- keyboard accessible
- có aria-label
- hiển thị language hiện tại
- có trạng thái active rõ ràng

Ví dụ:

```html
<button aria-label="Switch language">
    VI
</button>
```

### Kiểm thử

Phải kiểm tra:

1. `/vi/`
2. `/en/`
3. `/vi/about/`
4. `/en/about/`
5. `/vi/services/`
6. `/en/services/`
7. Language switcher
8. Mobile language switcher
9. SEO metadata
10. hreflang
11. Missing translation
12. Fallback content

Không được xảy ra:

- URL sai language
- mất trang khi chuyển language
- mất slug
- nội dung bị trống
- layout thay đổi hoặc vỡ khi đổi language
- text English dài làm vỡ UI

Đặc biệt phải kiểm tra responsive với English vì text tiếng Anh có thể dài khác tiếng Việt.