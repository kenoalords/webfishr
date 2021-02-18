from django.urls import path
import fishr.views as view
from django.conf import settings
from django.conf.urls.static import static
from fishr.views import is_user_loggedin
from django.views.generic import TemplateView

urlpatterns = [
    path('', view.IndexView.as_view(), name='index'),
    path('career/', view.CareerTemplateView.as_view(template_name="app/careers.html"), name='career'),
    path('contact/', view.CareerTemplateView.as_view(template_name="app/contact.html"), name='contact'),
    path('about/', view.AboutTemplateView.as_view(template_name="app/about.html"), name='about'),
    path('blog/<int:pk>/<str:slug>', view.BlogDetailView.as_view(), name='blog'),
    path('blog/', view.BlogPageListView.as_view(), name='blogs'),
    path('privacy-policy/', view.PolicyTemplateView.as_view(template_name="app/policy.html"), name='policy'),
    path('how-it-works/', view.HowItWorksTemplateView.as_view(template_name="app/how-it-works.html"), name='how-it-works'),
    path('signup/', view.OrderWizardView.as_view(), name="signup"),
    path('faq/', view.FaqTemplateView.as_view(), name="faq"),
    path('terms-condition/', TemplateView.as_view(template_name='app/terms.html'), name="terms"),
    path('order/<str:pk>/', view.OrderCompleteView.as_view(), name="order"),
    path('order/paystack/callback/', view.PaystackCallback.as_view(), name="paystack_callback"),
    path('website-design/', view.WebsiteThemeView.as_view(), name="themes"),
    path('pricing/', view.PricingView.as_view(), name="pricing"),
    path('website-design/theme/<slug:slug>/', view.WebsiteDesignPreviewView.as_view(), name="design"),
    path('dashboard/', view.DashboardTemplateView.as_view(), name="dashboard"),
    path('subscribe/', view.SubscribeEmail.as_view(), name="subscribe-email"),
    path('subscribe/<str:uuid>/success', view.SubscriptionSuccessful.as_view(), name="email_sub_successful"),
    path('subscribe/<str:uuid>/verify', view.SubscriptionVerify.as_view(), name="email_verify"),
    path('dashboard/blog/', view.BlogListView.as_view(), name="admin_blog"),
    path('dashboard/blog/add/', view.BlogAddTemplateView.as_view(), name="blog_add"),
    path('dashboard/blog/<int:pk>/edit/', view.BlogEditTemplateView.as_view(), name="blog_edit"),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
