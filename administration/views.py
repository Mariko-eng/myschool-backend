from .models import StudentClass, SubjectUnit
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def basic_setup(request):
    classes = [
        {"name": "Primary 1","level": "Lower"},
        {"name": "Primary 2","level": "Lower"},
        {"name": "Primary 3","level": "Lower"},
        {"name": "Primary 4","level": "Higher"},
        {"name": "Primary 5","level": "Higher"},
        {"name": "Primary 6","level": "Higher"},
        {"name": "Primary 7","level": "Higher"},
    ]
    subjects = [
        {"name": "Math","name_short_form": "MTC"},
        {"name": "English","name_short_form": "ENG"},
        {"name": "Christian Religious Education","name_short_form": "CRE"},
    ]
    if request.method == "GET":
        for c in classes:
            qs_exists = StudentClass.objects.filter(name = c["name"]).exists()
            if(qs_exists):
                obj = StudentClass.objects.get(name = c["name"])
            else:
                obj = StudentClass.objects.create(name= c["name"],level=c["level"])

        for sub in subjects:
            qs_exists = SubjectUnit.objects.filter(name = sub["name"]).exists()
            if(qs_exists):
                obj2 = SubjectUnit.objects.get(name = sub["name"])
            else:
                obj2 = SubjectUnit.objects.create(name= sub["name"],name_short_form=sub["name_short_form"])

        return Response({"data": "Successful"})