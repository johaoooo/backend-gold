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
        # Vérifier si l'utilisateur est un investisseur approuvé
        if request.user.role == 'investisseur' and not request.user.is_approved:
            return Response(
                {'error': 'Votre compte investisseur est en attente de validation par un administrateur.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
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
    
    # ... le reste reste identique

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

            # Vérifier si l'investisseur a déjà postulé
            if Investment.objects.filter(investisseur=request.user, projet=projet).exists():
                return Response({'error': 'Vous avez déjà postulé à ce projet.'}, status=status.HTTP_400_BAD_REQUEST)

            investment = serializer.save(investisseur=request.user, projet=projet, statut='en_attente')
            # NE PAS ajouter le montant immédiatement — il faut attendre acceptation
            return Response(InvestmentSerializer(investment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptInvestmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Le porteur accepte un investissement"""
        try:
            investment = Investment.objects.get(pk=pk, statut='en_attente')
        except Investment.DoesNotExist:
            return Response({'error': 'Investissement introuvable ou déjà traité.'}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier que l'utilisateur est le porteur du projet
        if request.user != investment.projet.porteur:
            return Response({'error': 'Seul le porteur du projet peut accepter les investissements.'}, status=status.HTTP_403_FORBIDDEN)

        investment.statut = 'accepte'
        investment.save()

        # Ajouter le montant au projet
        investment.projet.montant_actuel += investment.montant
        investment.projet.save()

        return Response(InvestmentSerializer(investment).data)


class RejectInvestmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Le porteur refuse un investissement"""
        try:
            investment = Investment.objects.get(pk=pk, statut='en_attente')
        except Investment.DoesNotExist:
            return Response({'error': 'Investissement introuvable ou déjà traité.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != investment.projet.porteur:
            return Response({'error': 'Seul le porteur du projet peut refuser les investissements.'}, status=status.HTTP_403_FORBIDDEN)

        investment.statut = 'refuse'
        investment.save()
        return Response(InvestmentSerializer(investment).data)


class MyInvestmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Investissements effectués par l'utilisateur (investisseur)"""
        if request.user.role == 'investisseur':
            investissements = Investment.objects.filter(investisseur=request.user)
            serializer = InvestmentSerializer(investissements, many=True)
            return Response(serializer.data)
        return Response({'error': 'Seul un investisseur peut voir ses investissements.'}, status=status.HTTP_403_FORBIDDEN)


class ProjectInvestmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Investissements reçus sur un projet (porteur uniquement)"""
        try:
            projet = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'error': 'Projet introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != projet.porteur:
            return Response({'error': 'Seul le porteur peut voir les investissements de son projet.'}, status=status.HTTP_403_FORBIDDEN)

        investissements = Investment.objects.filter(projet=projet)
        serializer = InvestmentSerializer(investissements, many=True)
        return Response(serializer.data)
