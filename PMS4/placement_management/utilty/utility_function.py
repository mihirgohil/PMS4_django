from placement_management.models import CustomUser

def check_mail(email):
    usermailcheck = CustomUser.objects.filter(email=email).first()
    if usermailcheck != None:
        return True
    return False