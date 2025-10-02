from django.urls import path
from . import views

urlpatterns = [
    path("carrinho/", views.ver_carrinho, name="ver_carrinho"),
    path("atualizar/<int:produto_id>/<int:quantidade>/", views.atualizar_carrinho, name="atualizar_carrinho"),
    path("checkout/", views.checkout, name="checkout"),
]
