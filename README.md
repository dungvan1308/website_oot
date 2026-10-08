# Ocean One Technology

Django project foundation for the enterprise technology company website.

## Requirements

- Python 3.12+
- PostgreSQL 14+
- Node.js 20+ and npm

## Local setup

1. Create and activate a virtual environment.
2. Install Python dependencies: `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and set a private Django secret and PostgreSQL credentials.
4. Create the PostgreSQL database and user matching `.env`.
5. Install frontend dependencies with `npm install` and build Tailwind with `npm run css:build`.
6. Run `python manage.py migrate` and `python manage.py seed_site_content` to create the initial editable site content.
7. Create an admin login with `python manage.py createsuperuser`.
8. Start Django with `python manage.py runserver`.

Manage content at `/admin/`. Services, solutions, products, industries, technologies,
case studies, articles, contact requests, company profile, site settings and SEO values
are stored in PostgreSQL. `seed_site_content` is safe to rerun: it adds missing initial
records and leaves existing records unchanged. Uploads accept JPG, PNG and WebP images
up to 5 MB; production media delivery should be configured in Nginx.

## Production deployment

- Set `DJANGO_DEBUG=False`, a unique `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and `DJANGO_CSRF_TRUSTED_ORIGINS` in the deployment environment.
- Serve the site over HTTPS. Keep `DJANGO_SECURE_SSL_REDIRECT=True` and enable HSTS with `DJANGO_SECURE_HSTS_SECONDS=31536000` after HTTPS is working for the full site. Enable the HSTS subdomain or preload options only when every affected domain is HTTPS-ready.
- Run `python manage.py check --deploy` and `python manage.py collectstatic --noinput` during deployment. Serve `STATIC_ROOT` and uploaded `MEDIA_ROOT` through the web server or object storage.
- `/sitemap.xml` lists the public pages and `/robots.txt` points crawlers to the sitemap while disallowing `/admin/`.
- Public pages send a restrictive Content Security Policy and baseline security headers. The Django admin keeps its inline scripts and styles and receives the baseline headers.

The database connection is configured only through `POSTGRES_DB`, `POSTGRES_USER`,
`POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT`. Never commit `.env`.

## Project layout

- `config/`: settings, URL routing, and WSGI/ASGI entry points.
- `core/`: site-level Django app and initial route.
- `core/homepage.py`, `core/editorial.py`: initial catalog and editorial seed content; public pages read editable CMS records.
- `core/models.py`: CMS content models and contact requests captured from the public enquiry form.
- `core/views.py`, `core/urls.py`: homepage and the Services, Solutions, Products, Industries, Case Studies, Insights and Contact routes.
- `templates/base.html`: shared SEO-aware document shell and content blocks.
- `templates/components/`: reusable page components for CTAs, cards, buttons, headings, hero, and statistics.
- `templates/partials/`: shared navigation links, responsive header, and footer.
- `templates/pages/`: homepage, capability pages, case studies, insights, and contact form pages.
- `static/src/css/app.css`: Tailwind entry point and Deep Ocean design tokens/components.
- `static/src/js/site.js`: accessible mobile navigation behavior in vanilla JavaScript.
- `static/css/site.css`: generated, minified stylesheet served by Django.

Use `npm run css:watch` while editing templates and styles locally. The design system
provides ocean navy and blue foundations, aqua accents, typography and layout tokens,
shared button/card/section styles, keyboard focus states, and reduced-motion support.

## Testing and responsive QA

Run `python manage.py check` and `python manage.py test core` after changes. The test
database uses the configured PostgreSQL account, which needs permission to create a
temporary test database. The public page tests cover route rendering, SEO metadata,
sitemap and robots output, security headers, mobile navigation markup, and contact form
validation and submission.

For browser QA, check all public routes at widths 320, 375, 390, 430, 768, 1024, 1280,
1440, and 1920 pixels. Confirm there is no horizontal page scrolling, the mobile menu
opens and closes with its button and Escape key, and the contact form remains usable.
