from fishr.forms import EmailSubscriptionForm

def subscription(request):
    return { 'email_form': EmailSubscriptionForm() }
