from lecMgt_auth.models import *


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            # num of lec
            lec = User.objects.filter(is_central=False, is_dean=False, is_dept=False, is_hod=False, is_staff=False).count()
            # num of dept
            dept = Department.objects.all().count()
            # num of promotion
            pro = Promotion.objects.all().count()
            # num of user
            users = User.objects.all().count()

            return {
                'lec': lec,
                'dept':dept,
                'pro' : pro,
                'users':users
            }

        elif request.user.is_dept:
            # num of lec
            lec = User.objects.filter(department=request.user.department).count()
            # num of notice
            notice = Notice.objects.filter(department=request.user.department).count()
            # num of approved promotion
            pro = Promotion.objects.filter(dept_approval=True).count()
            # num of approved leaves
            leaves = Leave.objects.filter(dept_approval=True).count()
            return {
                'lec':lec,
                'notice':notice,
                'pro':pro,
                'leaves':leaves
            }
        elif request.user.is_dean:
            # approved promotion
            a_pro = Promotion.objects.filter(dean_approval=True).count()
            # disapproved promotion
            d_pro = Promotion.objects.filter(dean_approval=False).count()
            # total promotion received
            t_pro = a_pro + d_pro

            return {
                'a_pro':a_pro,
                'd_pro':d_pro,
                't_pro':t_pro
            }

        elif request.user.is_hod:
            # approved promotion
            a_pro = Promotion.objects.filter(hod_approval=True).count()
            # disapproved promotion
            d_pro = Promotion.objects.filter(hod_approval=False).count()
            # total promotion received
            t_pro = a_pro + d_pro

            return {
                'a_pro':a_pro,
                'd_pro':d_pro,
                't_pro':t_pro
            }

        elif request.user.is_central:
            # approved promotion
            a_pro = Promotion.objects.filter(central_approval=True).count()
            # disapproved promotion
            d_pro = Promotion.objects.filter(central_approval=False).count()
            # total promotion received
            t_pro = a_pro + d_pro

            return {
                'a_pro':a_pro,
                'd_pro':d_pro,
                't_pro':t_pro
            }
        else:
            lec = LecturerProfile.objects.get(user_id=request.user.user_id)
            a_leave = Leave.objects.filter(user=lec.user_id, dept_approval=True).count()
            d_leave = Leave.objects.filter(user=lec.user_id, dept_approval=False).count()
            p_pro = Promotion.objects.filter(is_pending=True, lecturer=lec).count()
            a_pro = Promotion.objects.filter(is_pending=False, lecturer=lec).count()
            return {
                'a_leave': a_leave,
                'd_leave': d_leave,
                'p_pro': p_pro,
                'a_pro': a_pro,
            }

    return dict()
