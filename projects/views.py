from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Project, Investment
from .serializers import ProjectSerializer, InvestmentSerializer


class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        secteur = request.query_params.get('secteur')
        localisation = request.query_params.get('localisation')
        montant_min = request.query_params.get('montant_min')
        montant_max = request.query_params.get('montant_max')

        projets = Project.objects.filter(statut='ouvert')

        if secteur:
            projets = projets.filter(secteur=secteur)
        if localisation:
            projets = projets.filter(localisation__icontains=localisation)
        if montant_min:
            projets = projets.filter(montant_cible__gte=montant_min)
        if montant_max:
            projets = projets.filter(montant_cible__lte=montant_max)

        serializer = ProjectSerializer(projets, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'porteur':
            return Response(
                {'error': 'Seul un porteur de projet peut créer un projet.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(porteur=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            projet = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'error': 'Projet introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(projet)
        return Response(serializer.data)


class InvestmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'investisseur':
            return Response(
                {'error': 'Seul un investisseur peut postuler à un projet.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = InvestmentSerializer(data=request.data)
        if serializer.is_valid():
            projet_id = serializer.validated_data['projet_id']
            try:
                projet = Project.objects.get(pk=projet_id, statut='ouvert')
            except Project.DoesNotExist:
                return Response({'error': 'Projet introuvable ou fermé.'}, status=status.HTTP_404_NOT_FOUND)

            investment = serializer.save(investisseur=request.user, projet=projet)
            projet.montant_actuel += investment.montant
            projet.save()
            return Response(InvestmentSerializer(investment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyInvestmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        investissements = Investment.objects.filter(investisseur=request.user)
        serializer = InvestmentSerializer(investissements, many=True)
        return Response(serializer.data)
