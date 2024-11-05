from ninja import Router, Query
from .schemas import LivrosSchema, AvaliacaoSchema, FiltrosSortear
from .models import Livros, categorias

livros_router = Router()

@livros_router.post('/')
def create_livro(request, Livro_schema: LivrosSchema):
    #print(Livro_schema.dict())
    nome = Livro_schema.dict()['nome']
    streaming = Livro_schema.dict()['streaming']
    categorias = Livro_schema.dict()['categorias']

    if streaming not in ['F', 'AK']:
        return 400, {'status': 'Erro, Streaming deve ser F ou AK' }
    livro = Livros(
        nome=nome,
        streaming=streaming
        #categorias=categorias não é possivel salvar campos manytomany, depois que os dois campos já existe.
    )
    livro.save()

    for categoria in categorias:
        categoria_temp = categorias.objetcts.get(id=categoria) # Obtém a categoria pelo ID
        livro.categorias.add(categoria_temp) # Adiciona a categoria à instância do livro

    return {'status': 'ok'}

@livros_router.put('/{livro_id}')
def avaliar_livro(request, livro_id: int, avaliacao_schema: AvaliacaoSchema):#precisamos da nota do livro e do comentário, desta forma precisamos de um esquema
    comentario = avaliacao_schema.dict()['comentarios']
    nota = avaliacao_schema.dict()['nota']
    if nota < 0 or nota > 5:
        return 400, {'status': 'Error: Nota deve ser entre 0 e5'}
    try:
        livro = Livros.objects.get(id=livro_id)
        livro.comentarios = comentario
        livro.nota = nota
        livro.save()

        return 200, {'status': 'Avaliação realizada com Sucesso'}
    except:
        return 500, {'status', 'Erro interno do servidor'}

@livros_router.delete('/{livro_id}')
def deleltar_livro(request, livro_id: int):
    livro = Livros.objects.get(id=livro_id)
    livro.delete()
    return livro_id

@livros_router.get('/sortear/', response={200: LivrosSchema, 404: dict})
def sortear_livro(request, filtros: Query[FiltrosSortear]):
    # print(filtros.dict())
    # return {'ok': 'ok'}
    nota_minima = filtros.dict()['nota_minima']
    categoria = filtros.dict()['categorias']
    reler = filtros.dict()['reler']

    livros = Livros.objects.all()

    if not reler:
        livros = livros.filter(nota=None)
    if nota_minima:
        livros = livros.filter(nota__gte=nota_minima)
    if categoria:
        livros = livros.filter(categorias__id=categoria)
    
    livro = livros.order_by('?').first()

    if livros.count() > 0:
        return 200, livro
    else:
        return 404, {'status': 'Livro não encontrado'}
