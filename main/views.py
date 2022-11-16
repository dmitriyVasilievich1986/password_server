from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import PasswordsSerializer
from rest_framework import status, mixins
from .models import Passwords, Field
from .secret_key import Key


def index_view(request):
    return render(request, "index.html")


class PasswordViewSet(GenericViewSet, mixins.DestroyModelMixin):
    serializer_class = PasswordsSerializer
    queryset = Passwords.objects.all()

    def list(self, request, *args, **kwargs) -> Response:
        data = [x.json() for x in Passwords.objects.all()]
        return Response(data)

    def create(self, request, *args, **kwargs):
        key = Key(password=request.data["key"])
        fields = {
            k: v
            for k, v in request.data.items()
            if k not in {"name", "description", "key"}
        }
        p = Passwords(
            description=request.data.get("description"),
            name=request.data["name"],
        )
        p.save()
        for k, v in fields.items():
            Field(name=k, value=key.encrypt(v), password=p).save()
        return Response(p.json(), status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def get(self, request, *args, **kwargs) -> Response:
        key = Key(password=request.data["key"])
        if "id" in request.data:
            p = get_object_or_404(Passwords, id=request.data["id"])
        else:
            p = Passwords.objects.filter(name__icontains=request.data["name"])[0]
        fields = {x.name: key.decrypt(x.value) for x in p.fields.all()}
        # fields = dict()
        # for x in p.fields.all():
        #     fields[x.name] = key.decrypt(x.value)
        return Response(fields)

    def partial_update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.description = request.data.get("description", instance.description)
        instance.name = request.data.get("name", instance.name)
        if "key" in request.data:
            key = Key(password=request.data["key"])
            for x in instance.fields.all():
                print(f"{x.name}: {x.name in request.data}")
                if x.name in request.data:
                    x.value = key.encrypt(request.data[x.name])
                    x.save()
        instance.save()
        return Response(instance.json(), status=status.HTTP_202_ACCEPTED)
