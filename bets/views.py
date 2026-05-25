from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Aposta, Banca
from .forms import BancaForm, ApostaForm


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    bancas = Banca.objects.filter(usuario=request.user).prefetch_related('apostas')
    dados_bancas = []
    for banca in bancas:
        apostas = list(banca.apostas.all())
        lucro_total = sum(a.lucro_prejuizo for a in apostas)
        saldo_atual = banca.capital_inicial + lucro_total
        dados_bancas.append({
            'banca': banca,
            'saldo_atual': saldo_atual,
            'lucro_total': lucro_total,
            'total_apostas': len(apostas),
        })
    return render(request, 'bets/dashboard.html', {'dados_bancas': dados_bancas})


@login_required
def banca_criar(request):
    if request.method == 'POST':
        form = BancaForm(request.POST)
        if form.is_valid():
            banca = form.save(commit=False)
            banca.usuario = request.user
            banca.save()
            messages.success(request, f'Banca "{banca.nome}" criada com sucesso!')
            return redirect('dashboard')
    else:
        form = BancaForm()
    return render(request, 'bets/banca_form.html', {'form': form, 'titulo': 'Nova Banca'})


@login_required
def banca_detalhe(request, pk):
    banca = get_object_or_404(Banca, pk=pk, usuario=request.user)
    apostas = list(banca.apostas.all().order_by('-data'))

    lucro_total = sum(a.lucro_prejuizo for a in apostas)
    stake_total = sum(a.stake for a in apostas)
    saldo_atual = banca.capital_inicial + lucro_total

    apostas_resolvidas = [a for a in apostas if a.resultado != 'PENDENTE']
    ganhas = [a for a in apostas if a.resultado == 'GANHA']

    win_rate = (len(ganhas) / len(apostas_resolvidas) * 100) if apostas_resolvidas else 0
    roi_medio = (float(lucro_total) / float(stake_total) * 100) if stake_total else 0

    return render(request, 'bets/banca_detail.html', {
        'banca': banca,
        'apostas': apostas,
        'lucro_total': lucro_total,
        'saldo_atual': saldo_atual,
        'stake_total': stake_total,
        'win_rate': round(win_rate, 1),
        'roi_medio': round(roi_medio, 2),
        'total_apostas': len(apostas),
    })


@login_required
def banca_editar(request, pk):
    banca = get_object_or_404(Banca, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = BancaForm(request.POST, instance=banca)
        if form.is_valid():
            form.save()
            messages.success(request, f'Banca "{banca.nome}" atualizada com sucesso!')
            return redirect('dashboard')
    else:
        form = BancaForm(instance=banca)
    return render(request, 'bets/banca_form.html', {
        'form': form,
        'titulo': 'Editar Banca',
        'banca': banca,
    })


@login_required
def banca_deletar(request, pk):
    banca = get_object_or_404(Banca, pk=pk, usuario=request.user)
    if request.method == 'POST':
        nome = banca.nome
        banca.delete()
        messages.success(request, f'Banca "{nome}" excluída com sucesso.')
        return redirect('dashboard')
    return render(request, 'bets/banca_confirm_delete.html', {'banca': banca})


@login_required
def aposta_criar(request, banca_pk):
    banca = get_object_or_404(Banca, pk=banca_pk, usuario=request.user)
    if request.method == 'POST':
        form = ApostaForm(request.POST)
        if form.is_valid():
            aposta = form.save(commit=False)
            aposta.banca = banca
            aposta.save()
            messages.success(request, 'Aposta registrada com sucesso!')
            return redirect('banca_detalhe', pk=banca.pk)
    else:
        form = ApostaForm()
    return render(request, 'bets/aposta_form.html', {
        'form': form,
        'banca': banca,
        'titulo': 'Nova Aposta',
    })


@login_required
def aposta_editar(request, pk):
    aposta = get_object_or_404(Aposta, pk=pk, banca__usuario=request.user)
    if request.method == 'POST':
        form = ApostaForm(request.POST, instance=aposta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aposta atualizada com sucesso!')
            return redirect('banca_detalhe', pk=aposta.banca.pk)
    else:
        form = ApostaForm(instance=aposta)
    return render(request, 'bets/aposta_form.html', {
        'form': form,
        'banca': aposta.banca,
        'titulo': 'Editar Aposta',
        'aposta': aposta,
    })


@login_required
def aposta_deletar(request, pk):
    aposta = get_object_or_404(Aposta, pk=pk, banca__usuario=request.user)
    banca_pk = aposta.banca.pk
    if request.method == 'POST':
        aposta.delete()
        messages.success(request, 'Aposta excluída com sucesso.')
        return redirect('banca_detalhe', pk=banca_pk)
    return render(request, 'bets/aposta_confirm_delete.html', {'aposta': aposta})
