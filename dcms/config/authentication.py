from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


default_authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication)
