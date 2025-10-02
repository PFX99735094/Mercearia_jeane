from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.marca}"

# ----------------------------
# Novo: modelo de Pedido
# ----------------------------
class Pedido(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="Pendente")  # Pendente, Confirmado, Pago, Enviado
    cliente = models.CharField(max_length=100, blank=True, null=True)  # opcional

    def __str__(self):
        return f"Pedido #{self.id} - {self.status}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} ({self.quantidade}x)"
