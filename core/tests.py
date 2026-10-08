from django.test import TestCase
from django.urls import reverse

from core.models import ContactRequest


class PublicPageTests(TestCase):
    public_pages = (
        "home",
        "about",
        "services",
        "solutions",
        "products",
        "industries",
        "case-studies",
        "insights",
        "contact",
    )

    def test_public_pages_render_and_include_seo_metadata(self):
        for page_name in self.public_pages:
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'rel="canonical"')
                self.assertContains(response, 'property="og:title"')
                self.assertContains(response, 'name="twitter:card"')

    def test_sitemap_and_robots_routes(self):
        sitemap_response = self.client.get(reverse("sitemap"))
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertEqual(sitemap_response.content.count(b"<url>"), len(self.public_pages))

        robots_response = self.client.get(reverse("robots"))
        self.assertEqual(robots_response.status_code, 200)
        self.assertContains(robots_response, "Disallow: /admin/")
        self.assertContains(robots_response, "/sitemap.xml")

    def test_public_security_headers_and_admin_compatibility(self):
        public_response = self.client.get(reverse("home"))
        self.assertEqual(public_response["X-Content-Type-Options"], "nosniff")
        self.assertIn("frame-ancestors 'none'", public_response["Content-Security-Policy"])

        admin_response = self.client.get("/admin/login/")
        self.assertEqual(admin_response.status_code, 200)
        self.assertNotIn("Content-Security-Policy", admin_response)
        self.assertEqual(admin_response["X-Frame-Options"], "DENY")

    def test_mobile_navigation_and_responsive_shell_are_present(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'data-menu-toggle')
        self.assertContains(response, 'data-mobile-navigation')
        self.assertContains(response, 'class="container-site')


class ContactFormTests(TestCase):
    valid_payload = {
        "name": "  Alex   Example ",
        "email": "alex@example.com",
        "company": "Example Corp",
        "phone": "+1 555 0100",
        "interest": ContactRequest.Interest.DATA_PLATFORM,
        "message": "We would like to discuss a new enterprise data platform.",
        "consent_to_contact": "on",
    }

    def test_invalid_contact_request_is_not_saved(self):
        payload = {**self.valid_payload, "message": "Too short"}
        response = self.client.post(reverse("contact"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactRequest.objects.count(), 0)

    def test_valid_contact_request_is_saved_and_redirects(self):
        response = self.client.post(reverse("contact"), self.valid_payload)
        self.assertRedirects(response, reverse("contact"))
        request = ContactRequest.objects.get()
        self.assertEqual(request.name, "Alex Example")
        self.assertEqual(request.email, self.valid_payload["email"])
        self.assertTrue(request.consent_to_contact)
