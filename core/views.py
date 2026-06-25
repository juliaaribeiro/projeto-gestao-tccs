from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Count
from django.utils import timezone
import re
import unicodedata
from .models import UnidadeAcademica, Departamento, Curso, Aluno, Professor, TCC
from .serializers import (
    UnidadeAcademicaSerializer, DepartamentoSerializer, CursoSerializer,
    AlunoSerializer, ProfessorSerializer, TCCSerializer
)


def _slug_sigla(nome, tamanho=6):
    """Gera uma sigla a partir das primeiras letras das palavras do nome."""
    nome_sem_acento = ''.join(
        c for c in unicodedata.normalize('NFKD', nome) if not unicodedata.combining(c)
    )
    palavras = re.findall(r'[A-Za-z]+', nome_sem_acento)
    if not palavras:
        return 'GER'
    if len(palavras) == 1:
        return palavras[0][:tamanho].upper()
    sigla = ''.join(p[0] for p in palavras).upper()
    return sigla[:tamanho] if sigla else 'GER'


def _gerar_sigla_unica(model, nome):
    """Gera uma sigla única para o model (Curso/Departamento), evitando colisão."""
    base = _slug_sigla(nome)
    sigla = base
    contador = 1
    while model.objects.filter(sigla=sigla).exists():
        contador += 1
        sigla = f"{base[:8]}{contador}"
    return sigla


def _gerar_codigo_unico(model):
    """Gera um código numérico único baseado em timestamp + contador."""
    base = timezone.now().strftime('%Y%m%d')
    contador = model.objects.count() + 1
    codigo = f"{base}{contador:04d}"
    while model.objects.filter(codigo=codigo).exists():
        contador += 1
        codigo = f"{base}{contador:04d}"
    return codigo


def _gerar_matricula_unica():
    """Gera uma matrícula provisória única baseada em timestamp + contador."""
    base = timezone.now().strftime('%Y%m%d')
    contador = Aluno.objects.count() + 1
    matricula = f"{base}{contador:04d}"
    while Aluno.objects.filter(matricula=matricula).exists():
        contador += 1
        matricula = f"{base}{contador:04d}"
    return matricula


class UnidadeAcademicaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeAcademica.objects.all()
    serializer_class = UnidadeAcademicaSerializer

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'sigla']

    @action(detail=False, methods=['post'])
    def buscar_ou_criar(self, request):
        """
        Recebe {nome}. Se já existir um departamento com esse nome
        (case-insensitive), retorna ele. Caso contrário, cria um novo,
        gerando sigla automaticamente e usando a primeira unidade
        acadêmica cadastrada (ou criando uma padrão, se não houver nenhuma).
        """
        nome = (request.data.get('nome') or '').strip().upper()
        if not nome:
            return Response({'erro': 'Nome é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        existente = Departamento.objects.filter(nome__iexact=nome).first()
        if existente:
            return Response(DepartamentoSerializer(existente).data)

        unidade = UnidadeAcademica.objects.first()
        if not unidade:
            unidade = UnidadeAcademica.objects.create(nome='UNIDADE ACADÊMICA PADRÃO', sigla='UAP')

        sigla = _gerar_sigla_unica(Departamento, nome)
        serializer = DepartamentoSerializer(data={
            'nome': nome, 'sigla': sigla, 'unidade_academica': unidade.id
        })
        serializer.is_valid(raise_exception=True)
        departamento = serializer.save()
        return Response(DepartamentoSerializer(departamento).data, status=status.HTTP_201_CREATED)

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'sigla', 'codigo']

    @action(detail=False, methods=['post'])
    def buscar_ou_criar(self, request):
        """
        Recebe {nome}. Se já existir um curso com esse nome
        (case-insensitive), retorna ele. Caso contrário, cria um novo,
        gerando sigla e código automaticamente.
        """
        nome = (request.data.get('nome') or '').strip().upper()
        if not nome:
            return Response({'erro': 'Nome é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        existente = Curso.objects.filter(nome__iexact=nome).first()
        if existente:
            return Response(CursoSerializer(existente).data)

        sigla = _gerar_sigla_unica(Curso, nome)
        codigo = _gerar_codigo_unico(Curso)
        serializer = CursoSerializer(data={'nome': nome, 'sigla': sigla, 'codigo': codigo})
        serializer.is_valid(raise_exception=True)
        curso = serializer.save()
        return Response(CursoSerializer(curso).data, status=status.HTTP_201_CREATED)

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'matricula']

    @action(detail=False, methods=['post'])
    def buscar_ou_criar(self, request):
        """
        Recebe {nome, matricula?, curso_nome}. Se já existir um aluno com
        esse nome (case-insensitive), retorna ele. Caso contrário, cria
        um novo: o curso é resolvido/criado pelo NOME digitado (não precisa
        já estar cadastrado), e a matrícula é gerada automaticamente
        caso não seja informada.
        """
        nome = (request.data.get('nome') or '').strip().upper()
        if not nome:
            return Response({'erro': 'Nome é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        existente = Aluno.objects.filter(nome__iexact=nome).first()
        if existente:
            return Response(AlunoSerializer(existente).data)

        curso_nome = (request.data.get('curso_nome') or '').strip().upper()
        if not curso_nome:
            return Response(
                {'erro': 'Aluno novo: informe o curso.', 'novo': True},
                status=status.HTTP_400_BAD_REQUEST
            )

        curso = Curso.objects.filter(nome__iexact=curso_nome).first()
        if not curso:
            curso = Curso.objects.create(
                nome=curso_nome,
                sigla=_gerar_sigla_unica(Curso, curso_nome),
                codigo=_gerar_codigo_unico(Curso),
            )

        matricula = (request.data.get('matricula') or '').strip()
        if not matricula:
            matricula = _gerar_matricula_unica()

        serializer = AlunoSerializer(data={'nome': nome, 'matricula': matricula, 'curso': curso.id})
        serializer.is_valid(raise_exception=True)
        aluno = serializer.save()
        return Response(AlunoSerializer(aluno).data, status=status.HTTP_201_CREATED)

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    @action(detail=False, methods=['post'])
    def buscar_ou_criar(self, request):
        """
        Recebe {nome, departamento_nome}. Se já existir um professor com
        esse nome (case-insensitive), retorna ele. Caso contrário, cria
        um novo: o departamento é resolvido/criado pelo NOME digitado
        (não precisa já estar cadastrado).
        """
        nome = (request.data.get('nome') or '').strip().upper()
        if not nome:
            return Response({'erro': 'Nome é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        existente = Professor.objects.filter(nome__iexact=nome).first()
        if existente:
            return Response(ProfessorSerializer(existente).data)

        departamento_nome = (request.data.get('departamento_nome') or '').strip().upper()
        if not departamento_nome:
            return Response(
                {'erro': 'Professor novo: informe o departamento.', 'novo': True},
                status=status.HTTP_400_BAD_REQUEST
            )

        departamento = Departamento.objects.filter(nome__iexact=departamento_nome).first()
        if not departamento:
            unidade = UnidadeAcademica.objects.first()
            if not unidade:
                unidade = UnidadeAcademica.objects.create(nome='UNIDADE ACADÊMICA PADRÃO', sigla='UAP')
            departamento = Departamento.objects.create(
                nome=departamento_nome,
                sigla=_gerar_sigla_unica(Departamento, departamento_nome),
                unidade_academica=unidade,
            )

        serializer = ProfessorSerializer(data={'nome': nome, 'departamento': departamento.id})
        serializer.is_valid(raise_exception=True)
        professor = serializer.save()
        return Response(ProfessorSerializer(professor).data, status=status.HTTP_201_CREATED)

class TCCViewSet(viewsets.ModelViewSet):
    queryset = TCC.objects.all()
    serializer_class = TCCSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'resumo', 'aluno__nome', 'orientador__nome']

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        total_tccs = TCC.objects.count()
        
        # Agregações
        por_status = TCC.objects.values('status').annotate(total=Count('id'))
        por_tipo = TCC.objects.values('tipo').annotate(total=Count('id'))
        por_idioma = TCC.objects.values('idioma').annotate(total=Count('id'))
        por_semestre = TCC.objects.values('semestre_letivo_defesa').annotate(total=Count('id'))
        
        por_orientador = TCC.objects.values('orientador__nome').annotate(total=Count('id'))
        por_coorientador = TCC.objects.exclude(coorientador__isnull=True).values('coorientador__nome').annotate(total=Count('id'))
        por_curso = TCC.objects.values('aluno__curso__nome').annotate(total=Count('id'))
        por_departamento = TCC.objects.values('orientador__departamento__nome').annotate(total=Count('id'))
        por_unidade = TCC.objects.values('orientador__departamento__unidade_academica__nome').annotate(total=Count('id'))

        # Dicionários de mapeamento para os labels das escolhas (choices)
        status_map = dict(TCC.STATUS_CHOICES)
        tipo_map = dict(TCC.TIPO_CHOICES)
        idioma_map = dict(TCC.IDIOMA_CHOICES)

        return Response({
            'total_geral': total_tccs,
            'por_status': {status_map.get(item['status'], item['status']): item['total'] for item in por_status},
            'por_tipo': {tipo_map.get(item['tipo'], item['tipo']): item['total'] for item in por_tipo},
            'por_idioma': {idioma_map.get(item['idioma'], item['idioma']): item['total'] for item in por_idioma},
            'por_semestre': {item['semestre_letivo_defesa']: item['total'] for item in por_semestre if item['semestre_letivo_defesa']},
            'por_orientador': {item['orientador__nome']: item['total'] for item in por_orientador},
            'por_coorientador': {item['coorientador__nome']: item['total'] for item in por_coorientador},
            'por_curso': {item['aluno__curso__nome']: item['total'] for item in por_curso},
            'por_departamento': {item['orientador__departamento__nome']: item['total'] for item in por_departamento},
            'por_unidade_academica': {item['orientador__departamento__unidade_academica__nome']: item['total'] for item in por_unidade}
        })