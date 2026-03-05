from django.contrib import admin
from .models import Banca, Aposta
# Register your models here.

@admin.register(Banca)
class BancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'capital_inicial', 'ativo', 'criado_em')
    search_fields = ('nome',)

@admin.register(Aposta)
class ApostaAdmin(admin.ModelAdmin):

    list_display = ('data', 'esporte', 'competicao', 'mercado', 'stake', 'odd', 'resultado', 'mostrar_lucro')
    list_filter = ('resultado', 'esporte', 'banca')
    
    # pesquisa
    search_fields = ('competicao', 'mercado', 'anotacao')
    
    ordering = ('-data',)

    # funcao auxiliar para mostrar o lucro calculado na lista
    def mostrar_lucro(self, obj):
        return obj.lucro_prejuizo
    mostrar_lucro.short_description = "Lucro/Prejuízo"