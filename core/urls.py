from django.urls import path

from core.views import about, case_studies, contact, home, industries, insights, products, services, solutions


urlpatterns = [path("", home, name="home"), path("about/", about, name="about")]
urlpatterns += [
    path("services/", services, name="services"),
    path("solutions/", solutions, name="solutions"),
    path("products/", products, name="products"),
    path("industries/", industries, name="industries"),
    path("case-studies/", case_studies, name="case-studies"),
    path("insights/", insights, name="insights"),
    path("contact/", contact, name="contact"),
]
