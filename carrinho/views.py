from django.shortcuts import render, redirect
from mercearia.models import Produto, Pedido, ItemPedido
from urllib.parse import quote

# Adicionar ou atualizar produtos no carrinho
def atualizar_carrinho(request, produto_id, quantidade):
    carrinho = request.session.get("carrinho", {})
    carrinho[str(produto_id)] = int(quantidade)
    # remover do carrinho se quantidade <= 0
    if carrinho[str(produto_id)] <= 0:
        del carrinho[str(produto_id)]
    request.session["carrinho"] = carrinho
    return redirect("ver_carrinho")

# Ver carrinho
def ver_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    itens = []
    total = 0
    for produto_id, qtd in carrinho.items():
        produto = Produto.objects.get(id=int(produto_id))
        subtotal = produto.preco * int(qtd)
        total += subtotal
        itens.append({"produto": produto, "quantidade": qtd, "subtotal": subtotal})
    return render(request, "carrinho/ver_carrinho.html", {"itens": itens, "total": total})

# Checkout via WhatsApp
def checkout(request):
    carrinho = request.session.get("carrinho", {})
    if not carrinho:
        return redirect("ver_carrinho")

    if request.method == "POST":
        cliente_nome = request.POST.get("cliente_nome")
        cliente_telefone = request.POST.get("cliente_telefone")
        cliente_endereco = request.POST.get("cliente_endereco", "")

        total = 0
        itens = []
        mensagem = f"Olá, tenho um novo pedido do cliente {cliente_nome} ({cliente_telefone}):\n"
        if cliente_endereco:
            mensagem += f"Endereço: {cliente_endereco}\n"
        mensagem += "\nItens:\n"

        pedido = Pedido.objects.create(total=0, cliente=cliente_nome)

        for produto_id, qtd in carrinho.items():
            produto = Produto.objects.get(id=int(produto_id))
            subtotal = produto.preco * int(qtd)
            total += subtotal
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=int(qtd),
                subtotal=subtotal
            )
            mensagem += f"{produto.nome} ({qtd}x) - R$ {subtotal}\n"
            itens.append({"produto": produto, "quantidade": qtd, "subtotal": subtotal})

        pedido.total = total
        pedido.save()
        mensagem += f"\nTotal: R$ {total}"

        # codificar mensagem para URL do WhatsApp
        mensagem_url = quote(mensagem)
        numero_whatsapp = "5586988727233"  # substitua pelo número real do dono
        url_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensagem_url}"

        request.session["carrinho"] = {}  # limpar carrinho após gerar pedido

        return render(request, "carrinho/checkout.html", {
            "itens": itens,
            "total": total,
            "url_whatsapp": url_whatsapp,
            "cliente_nome": cliente_nome,
            "cliente_telefone": cliente_telefone,
            "cliente_endereco": cliente_endereco
        })

    return redirect("ver_carrinho")
