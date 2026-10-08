Bạn là Senior Full-Stack Developer + UI/UX Designer. Hãy xây dựng website giới thiệu công ty công nghệ theo yêu cầu sau.

## 1. Công nghệ bắt buộc

- Backend: Django
- Frontend: Django Template
- CSS: Tailwind CSS, build bằng npm, KHÔNG dùng Tailwind CDN
- JS: Alpine.js / HTMX / Vanilla JS khi cần
- Database: PostgreSQL
- Web server: Nginx + Gunicorn
- OS production: Ubuntu
- Không sử dụng React / Next.js / Vue / Bootstrap.

## 2. Mục tiêu

Website phải:

- Đẹp, hiện đại, premium, chuyên nghiệp.
- Mang phong cách Enterprise Technology / Data / Cloud.
- Responsive hoàn chỉnh Mobile / Tablet / Laptop / Desktop / 2K / 4K.
- Mobile-first.
- UX đơn giản, rõ ràng.
- Animation nhẹ và tinh tế.
- Performance tốt.
- SEO tốt.
- Accessibility tốt.
- Code modular, dễ bảo trì.
- Có Django Admin để quản trị nội dung.

Không làm website theo kiểu template IT truyền thống hoặc quá nhiều hiệu ứng.

## 3. Phong cách thương hiệu

Concept:

"Deep Ocean + Data + Digital Technology"

Màu sắc lấy cảm hứng từ Đại Hải Thủy:

- Midnight Navy
- Deep Ocean Blue
- Azure
- Cyan / Aqua
- White
- Cool Gray

Màu chủ đạo: Deep Navy / Ocean Blue.

Cyan/Aqua chỉ dùng làm accent.

Không dùng vàng, đỏ, cam làm màu chủ đạo.

Visual có thể sử dụng:

- Digital waves
- Data streams
- Network nodes
- Cloud
- Data particles
- Digital grid

Thiết kế phải premium, tinh tế, không lạm dụng gradient hoặc animation.

Font ưu tiên:
- Inter
- Manrope
- Plus Jakarta Sans

Icon:
- Lucide hoặc Heroicons.

## 4. Định vị công ty

Định vị:

"Enterprise Technology & Data Transformation"

Các năng lực chính:

- Data Warehouse
- Data Lakehouse
- Business Intelligence / BI Reporting
- ERP
- HR Management
- CRM
- Core Banking Migration
- Oracle FLEXCUBE
- T24 / Temenos
- SBV Regulatory Reporting
- Cloud & Data Platform
- System Integration
- Digital Transformation

Công nghệ/ecosystem:

- Oracle
- IBM
- Microsoft
- Microsoft Azure
- AWS
- PostgreSQL
- Power BI
- SQL Server

Chỉ mô tả là "Technologies We Work With" hoặc "Technology Ecosystem", không tự nhận là đối tác chính thức nếu chưa có thông tin xác nhận.

## 5. Sitemap

Tạo các trang:

- Home
- About
- Services
- Solutions
- Products
- Industries
- Case Studies
- Insights / News
- Contact

URL dạng:

/
/about/
/services/
/solutions/
/products/
/industries/
/case-studies/
/insights/
/contact/

## 6. Homepage

Thiết kế Homepage gồm:

1. Header / Navigation
2. Hero
3. Company Introduction
4. Core Capabilities
5. Services
6. Solutions
7. Products
8. Industries
9. Technology Ecosystem
10. Featured Case Studies
11. Statistics
12. Insights / News
13. CTA
14. Footer

Hero cần có:

Headline mạnh về Enterprise Technology / Data Transformation.

Ví dụ:

"Engineering Data. Powering Enterprise Transformation."

Subheadline ngắn, chuyên nghiệp.

CTA:

"Explore Our Solutions"
"Talk to Our Experts"

Hero visual theo concept Deep Ocean + Data.

## 7. Services

Tạo các nhóm:

### Data Platform
- Enterprise Data Warehouse
- Data Lakehouse
- Data Engineering
- Data Integration
- Data Governance

### Business Intelligence
- Management BI
- Executive Dashboard
- KPI Reporting
- Operational Reporting
- Enterprise Reporting

### Enterprise Software
- ERP
- HR Management
- CRM
- Workflow
- Enterprise Applications

### Banking Technology
- Core Banking Migration
- FLEXCUBE Migration
- T24 / Temenos Migration
- Banking Data Platform
- SBV Reporting

### Cloud & Digital Transformation
- AWS
- Azure
- Oracle
- IBM
- Cloud Migration
- Hybrid Cloud
- System Integration

## 8. Solutions

Tạo các solution:

- Enterprise Data Platform
- Lakehouse Platform
- Management BI Platform
- Enterprise Management Platform
- Banking Data & Reporting
- Core Banking Migration
- SBV Regulatory Reporting
- Cloud & Data Transformation

## 9. Products

Tạo Product showcase:

- Data Warehouse Platform
- Lakehouse Platform
- BI Reporting Platform
- ERP
- HR Management
- CRM
- Banking Data Platform
- SBV Reporting Solution

Mỗi product có:
- Logo/icon
- Description
- Features
- Technology
- Business Value
- Learn More

## 10. Case Studies

Thiết kế theo flow:

Challenge
→ Solution
→ Architecture
→ Technology
→ Implementation
→ Business Impact

Giao diện phải thể hiện được năng lực triển khai hệ thống enterprise lớn.

## 11. Django CMS

Sử dụng Django Admin để quản lý:

- Company
- Services
- Solutions
- Products
- Industries
- Technologies
- Case Studies
- News / Articles
- Partners
- Statistics
- Contact Requests
- SEO Settings
- Site Settings

Có:
- Search
- Filter
- Ordering
- Slug
- Publish status
- Display order
- Image
- Created / Updated date

Không hard-code nội dung website nếu nội dung đó cần thay đổi từ Admin.

## 12. Database

Sử dụng PostgreSQL.

Cấu hình bằng environment variables:

POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT

Tạo `.env.example`.

Không hard-code password, secret hoặc thông tin nhạy cảm.

## 13. Frontend architecture

Tạo:

templates/
├── base.html
├── components/
├── partials/
└── pages/

static/
├── src/
├── css/
├── js/
├── images/
└── fonts/

Tạo reusable components:

- navbar
- mobile menu
- hero
- section header
- button
- service card
- solution card
- product card
- case study card
- article card
- statistic
- CTA
- footer

Không tạo HTML duplicate.

## 14. Responsive

Thiết kế Mobile First.

Kiểm tra tối thiểu:

320px
375px
390px
430px
768px
1024px
1280px
1440px
1920px

Không được có:

- Horizontal scroll
- Layout vỡ
- Text overflow
- Image méo
- Button vỡ
- Navigation tràn màn hình

Mobile navigation phải có menu riêng, đẹp và dễ sử dụng.

## 15. SEO + Performance

Implement:

- Dynamic title
- Meta description
- Open Graph
- Canonical
- sitemap.xml
- robots.txt
- Semantic HTML
- H1/H2/H3 chuẩn
- Alt image
- Lazy loading
- WebP/AVIF khi phù hợp
- Tối ưu CSS/JS
- Không tải thư viện không cần thiết

## 16. Security

Production:

- DEBUG=False
- SECRET_KEY từ environment
- ALLOWED_HOSTS từ environment
- CSRF_TRUSTED_ORIGINS từ environment
- Secure cookies
- Security headers
- Validate file upload
- Giới hạn upload size

## 17. Quality

Ưu tiên theo thứ tự:

1. UI/UX
2. Responsive
3. Performance
4. Maintainability
5. SEO
6. Security
7. CMS usability

Website cuối cùng phải có cảm giác:

"Professional Enterprise Technology Company"

không phải "Basic Django Website".

## 18. Cách thực hiện

Trước khi code:

1. Kiểm tra source code hiện tại.
2. Không phá vỡ chức năng đang có.
3. Đề xuất cấu trúc nếu cần thay đổi.
4. Sau đó triển khai.

Thực hiện từng bước:

Phase 1 → Django + PostgreSQL + cấu trúc project.

Phase 2 → Tailwind + Design System.

Phase 3 → Base template + Components.

Phase 4 → Homepage.

Phase 5 → Services / Solutions / Products / Industries.

Phase 6 → Case Studies / Insights / Contact.

Phase 7 → Django Admin / CMS.

Phase 8 → SEO / Security / Performance.

Phase 9 → Testing + Responsive QA.

Sau mỗi phase phải chạy:

`python manage.py check`

và test các chức năng liên quan.

Không chuyển sang phase tiếp theo nếu phase hiện tại còn lỗi.

Bắt đầu bằng việc phân tích source code hiện tại và triển khai Phase 1.