from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Filial, Saldo
from django.contrib.messages import constants
from django.contrib import messages
from django.shortcuts import render, get_list_or_404, get_object_or_404


def cadastro_filial(request):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, "Para cadastrar filial, tem que estar logado."
        )
        return redirect("/usuarios/login")
    if request.method == "GET":
        context = {}
        return render(request, "cadastro_filial.html", context)
    elif request.method == "POST":
        nome = request.POST.get("nome")
        cnpj = request.POST.get("cnpj")
        rua = request.POST.get("rua")
        bairro = request.POST.get("bairro")
        numero = request.POST.get("numero")
        cidade = request.POST.get("cidade")
        foto = request.FILES.get("foto")
        if not nome:
            messages.add_message(
                request, constants.ERROR, "Nome da filial é obrigatório"
            )
            return redirect("/unidades/cadastro_filial")

        try:
            dados_filial = Filial(
                nome=nome,
                cnpj=cnpj,
                rua=rua,
                bairro=bairro,
                numero=numero,
                cidade=cidade,
                foto=foto,
                user=request.user,
            )
            dados_filial.save()
            messages.add_message(
                request, constants.SUCCESS, "Cadastro da Filial realizado com sucesso."
            )
            return redirect("/unidades/cadastro_filial")
        except:
            messages.add_message(request, constants.ERROR, "Erro ao salvar Medico.")
            return redirect("/unidades/cadastro_filial")


# Comentar  ---->  CTRL + K e C
# Descomentar -->  CTRL + K e U
def home(request):
    # usuario = request.user
    # usuario = User.is_authenticated
    # hoje = datetime.now().date()
    if request.method == "GET":
        filiais = Filial.objects.all()
        saldos = Saldo.objects.filter(
            data__range=[
                datetime.now().date() - timedelta(days=1),
                datetime.now().date() + timedelta(days=1),
            ]
        ).order_by("filial__id", "data")

        data_atual = str(datetime.now().date())

       

        tg = 0
        tm = 0
        soma = 0
        for i in saldos:
            tg += int(i.tergrasa)
            tm += int(i.termasa)
            soma += int(i.tergrasa) + int(i.termasa)
        context = {
            "data_atual":data_atual,
            "saldos": saldos,
            "filiais": filiais,
            "tg": tg,
            "tm": tm,
            "soma": soma,
        }
        return render(request, "home.html", context)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            messages.add_message(
                request, constants.ERROR, "Para incluir saldo, tem que estar logado."
            )
            return redirect("/usuarios/login")

        filial = request.POST.get("filial")
        if not filial:
            messages.add_message(request, constants.ERROR, "Filial não selecionada.")
            return redirect("/unidades/home")

        data = request.POST.get("data")
        tergrasa = request.POST.get("tergrasa")
        termasa = request.POST.get("termasa")
        if termasa == "":
            termasa = "0"
        if tergrasa == "":
            tergrasa = "0"
        soma = int(tergrasa) + int(termasa)

        try:
            saldos = Saldo.objects.filter(filial=filial, data=data)
        except:
            messages.add_message(
                request, constants.ERROR, "Confira as informações digitadas."
            )
            return redirect("/unidades/home")

        if not saldos:
            try:
                saldo = Saldo(
                    data=data,
                    tergrasa=tergrasa,
                    termasa=termasa,
                    total=str(soma),
                    filial_id=filial,
                )
                saldo.save()
                messages.add_message(request, constants.SUCCESS, "Salvo com sucesso.")
                return redirect("/unidades/home")
            except:
                messages.add_message(
                    request, constants.ERROR, "Confira as informações digitadas."
                )
                return redirect("/unidades/home")
        else:
            messages.add_message(request, constants.ERROR, "Data ja existe.")
            return redirect("/unidades/home")


def editar_saldo(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
            request, constants.ERROR, "Para editar o saldo, tem que estar logado  ."
        )
        return redirect("/usuarios/login")

    if request.method == "GET":
        saldo_editado = Saldo.objects.filter(id=id).first()
        saldos = Saldo.objects.filter(data__range=[datetime.now().date() - timedelta(days=1), datetime.now().date() + timedelta(days=1),]).order_by("filial__id", "data")

        
        tg = 0
        tm = 0
        soma = 0
        for i in saldos:
            tg += int(i.tergrasa)
            tm += int(i.termasa)
            soma += int(i.tergrasa) + int(i.termasa)

        context = {
           
            "idd": id,
            "saldos": saldos,
            "saldo_editado": saldo_editado,
            "tg": tg,
            "tm": tm,
            "soma": soma,
        }
        
        return render(request, "editar.html", context)

    elif request.method == "POST":
        tg = request.POST.get("tergrasa")
        tm = request.POST.get("termasa")
        if tm == "":
            tm = "0"
        if tg == "":
            tg = "0"
        soma = int(tg) + int(tm)

        saldo_editado = Saldo.objects.filter(id=id).first()
        saldo_editado.tergrasa = tg
        saldo_editado.termasa = tm
        saldo_editado.total = str(soma)
        saldo_editado.save()
        messages.add_message(request, constants.SUCCESS, "Salvo com sucesso.")
        return redirect("/unidades/home")

    else:
        messages.add_message(
            request, constants.ERROR, "Confira as informações digitadas."
        )
        return redirect("/unidades/home")


"""
https://www.youtube.com/watch?v=vxfouMYa9dM
__gte  maior ou iual

"""
