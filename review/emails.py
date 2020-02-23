from django.conf import settings
from django.shortcuts import reverse
from django.template import Context, engines
from django.core.mail import send_mail

CONFIRM_USER_HTML = 'review/emails_templates/confirmation_email.html'


class EmailTemplateContext(Context):

    @staticmethod
    def make_link(path):
        return settings.DOMAIN_LINK + path

    def __init__(self, profile, dict_ = None, **kwargs):
        if dict_ is None:
            dict_ = {}
        email_ctx = self.common_context(profile)
        email_ctx.update(dict_)
        super().__init__(email_ctx, **kwargs)

    def common_context(self, profile):
        profile_pk = {'pk' : profile.idConform}
        return {
            'profile' : profile,
        }

def send_confirmation_email(profile):
    confirmation_link = EmailTemplateContext.make_link(
        reverse('user:confirmUser', kwargs = {'pk': profile.idConform})
    )
    context = EmailTemplateContext(profile, {'confirmation_link' : confirmation_link})
    subject = '{} this is your confirmation email'.format(profile.user.username)

    dt_engine = engines['django'].engine

    html_body_template = dt_engine.get_template(CONFIRM_USER_HTML)
    html_body = html_body_template.render(context = context)

    send_mail(
        subject = subject,
        message = "This is the txt file",
        from_email = 'arrowatom@gamil.com',
        recipient_list = (profile.user.email, ),
        html_message = html_body,
    )