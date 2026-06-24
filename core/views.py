from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import UnidadeAcademica, Departamento, Curso, Aluno, Professor, TCC
from .serializers import (
    UnidadeAcademicaSerializer, DepartamentoSerializer, CursoSerializer,
    AlunoSerializer, ProfessorSerializer, TCCSerializer
)

class UnidadeAcademicaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeAcademica.objects.all()
    serializer_class = UnidadeAcademicaSerializer

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'sigla']

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'sigla', 'codigo']

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'matricula']

    @action(detail=False, methods=['post'])
    def buscar_ou_criar(self, request):
        """
        Recebe {nome, matricula?, curso?}. Se já existir um aluno com
        esse nome (case-insensitive), retorna ele. Caso contrário,
        cria um novo (matricula e curso são obrigatórios para criar).
        """
        nome = (request.data.get('nome') or '').strip().upper()
        if not nome:
            return Response({'erro': 'Nome é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        existente = Aluno.objects.filter(nome__iexact=nome).first()
        if existente:
            return Response(AlunoSerializer(existente).data)

        matricula = (request.data.get('matricula') or '').strip()
        curso_id = request.data.get('curso')

        if not matricula or not curso_id:
            return Response(
                {'erro': 'Aluno novo: matrícula e curso são obrigatórios.', 'novo': True},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AlunoSerializer(data={'nome': nome, 'matricula': matricula, 'curso': curso_id})
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
        Recebe {nome, departamento?}. Se já existir um professor com
        esse nome (case-insensitive), retorna ele. Caso contrário,
        cria um novo (departamento é obrigatório para criar).
        """
        nome = (request.data.get('nome') or '').strip().upper()
        if not nome:
            return Response({'erro': 'Nome é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        existente = Professor.objects.filter(nome__iexact=nome).first()
        if existente:
            return Response(ProfessorSerializer(existente).data)

        departamento_id = request.data.get('departamento')
        if not departamento_id:
            return Response(
                {'erro': 'Professor novo: departamento é obrigatório.', 'novo': True},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfessorSerializer(data={'nome': nome, 'departamento': departamento_id})
        serializer.is_valid(raise_exception=True)
        professor = serializer.save()
        return Response(ProfessorSerializer(professor).data, status=status.HTTP_201_CREATED)

class TCCViewSet(viewsets.ModelViewSet):
    queryset = TCC.objects.all()
    serializer_class = TCCSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'resumo']

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