from django.shortcuts import render,redirect
from .forms import NoticiaForm, NoticiaFilterForm, CategoriaForm, CategoriaFilterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Noticia, Categoria
from django.db.models.functions import Lower
from django.core.paginator import Paginator

# Create your views here.
@login_required
def inicio_gerencia(request):
    return render(request, 'gerencia/inicio.html')

def listagem_noticia(request):
    formularioFiltro = NoticiaFilterForm(request.GET or None)
    
    noticias = Noticia.objects.filter(usuario=request.user)  # Filtra pelo usuário logado

    if formularioFiltro.is_valid():
        if formularioFiltro.cleaned_data['titulo']:
            noticias = noticias.filter(titulo__icontains=formularioFiltro.cleaned_data['titulo'])
        if formularioFiltro.cleaned_data['data_publicacao_inicio']:
            noticias = noticias.filter(data_publicacao__gte=formularioFiltro.cleaned_data['data_publicacao_inicio'])
        if formularioFiltro.cleaned_data['data_publicacao_fim']:
            noticias = noticias.filter(data_publicacao__lte=formularioFiltro.cleaned_data['data_publicacao_fim'])
        if formularioFiltro.cleaned_data['categoria']:
            noticias = noticias.filter(categoria=formularioFiltro.cleaned_data['categoria'])
    
    contexto = {
        'noticias': noticias,
        'formularioFiltro': formularioFiltro
    }
    return render(request, 'gerencia/listagem_noticia.html',contexto)


def cadastrar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)  # Cria instância sem salvar
            noticia.usuario = request.user  # Atribui o autor (usuário logado)
            noticia.save()  # Salva a notícia no banco
            return redirect('gerencia:listagem_noticia')  # Redireciona para página de sucesso
    else:
        form = NoticiaForm() 

    contexto = {'form': form}
    return render(request, 'gerencia/cadastro_noticia.html', contexto)

@login_required
def editar_noticia(request, id):
    noticia = Noticia.objects.get(id=id)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia_editada = form.save(commit=False)  # Não salva ainda
            noticia_editada.usuario = request.user 
            noticia_editada.save()  # Salva com o usuário intacto
            return redirect('gerencia:listagem_noticia')
    else:
        form = NoticiaForm(instance=noticia)
    
    contexto = {
        'form': form
    }
    return render(request, 'gerencia/cadastro_noticia.html',contexto)





@login_required(login_url="usuarios:login")
def listagem_categoria(request):
    formularioFiltro = CategoriaFilterForm(request.GET or None)
    categorias_lista = Categoria.objects.all().order_by(Lower('nome'))
    
    if formularioFiltro.is_valid():
        if formularioFiltro.cleaned_data['nome']:
            categorias_lista = categorias_lista.filter(nome__icontains=formularioFiltro.cleaned_data['nome'])
    
    paginator = Paginator(categorias_lista, 5)
    page = request.GET.get('page', 1)
    categorias = paginator.get_page(page)
    
    contexto = {
        'categorias': categorias,
        'formularioFiltro': formularioFiltro
    }
    return render(request, 'gerencia/listagem_categoria.html', contexto)
@login_required(login_url="usuarios:login")
def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            categoria = form.save(commit=False)  
            categoria.save()  # Salva a categoria no banco
            return redirect('gerencia:listagem_categoria')  # Redireciona para página de sucesso
    else:
        form = CategoriaForm() 

    contexto = {'form': form}
    return render(request, 'gerencia/cadastro_categoria.html', contexto)

@login_required(login_url="usuarios:login")
def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            categoria_editada = form.save(commit=False)  # Não salva ainda
            categoria_editada.usuario = request.user 
            categoria_editada.save()  # Salva com o usuário intacto
            return redirect('gerencia:listagem_categoria')
    else:
        form = CategoriaForm(instance=categoria)
    
    contexto = {
        'form': form
    }
    return render(request, 'gerencia/cadastro_categoria.html',contexto)

@login_required
def excluir_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('gerencia:listagem_categoria')





























def index(request):
    categoria_nome = request.GET.get('categoria')  # Obtém o parâmetro 'categoria' da URL
    search_query = request.GET.get('search')  # Obtém o parâmetro de busca

    # Filtra as notícias com base na categoria ou na busca
    noticias = Noticia.objects.all()
    if categoria_nome:
        categoria = Categoria.objects.filter(nome=categoria_nome).first()
        if categoria:
            noticias = noticias.filter(categoria=categoria)

    if search_query:
        noticias = noticias.filter(titulo__icontains=search_query)  # Filtra por título, ignorando maiúsculas/minúsculas

    categorias = Categoria.objects.all()  # Pega todas as categorias para exibir no template

    contexto = {
        'noticias': noticias,
        'categorias': categorias,
        'categoria_selecionada': categoria_nome,
        'search_query': search_query,
    }
    return render(request, 'gerencia/index.html', contexto)
