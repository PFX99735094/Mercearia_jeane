from django.contrib import admin
from .models import Produto, Pedido, ItemPedido

# Registro de Produto
#usuario jeane1234  senha jeane1234
admin.site.register(Produto)

# Inline para mostrar itens dentro do pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ("produto", "quantidade", "subtotal")

# Registro de Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "criado_em", "total", "status")
    list_filter = ("status", "criado_em")
    inlines = [ItemPedidoInline]
    actions = ["marcar_confirmado", "marcar_pago", "marcar_enviado"]

    # Ações rápidas para mudar status
    @admin.action(description="Marcar como Confirmado")
    def marcar_confirmado(self, request, queryset):
        queryset.update(status="Confirmado")

    @admin.action(description="Marcar como Pago")
    def marcar_pago(self, request, queryset):
        queryset.update(status="Pago")

    @admin.action(description="Marcar como Enviado")
    def marcar_enviado(self, request, queryset):
        queryset.update(status="Enviado")
