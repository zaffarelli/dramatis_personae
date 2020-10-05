from collector.models.tourofduty import TourOfDutyRef
#  exec(open('scripts/check_tod.py').read())
all = TourOfDutyRef.objects.all()
for tod in all:
    tod.check_value()
    tod.save()
    if not tod.valid:
        print("[%2s] %30s has an error." % (tod.category, tod.reference))


