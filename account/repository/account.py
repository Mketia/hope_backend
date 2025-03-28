from django.db import IntegrityError
from account.models import Visitor
from account.serializer import VisitorSerializer
from base.utils.response import RepositoryResponse
from django.db import transaction

class VisitorRepository:
    @staticmethod
    def create_visitor(user, phone_number):
        try:
            with transaction.atomic():
                if Visitor.objects.filter(user=user).exists():
                    return RepositoryResponse(
                        success=False,
                        data=None,
                        message="Visitor already exists"
                        )
    
                visitor = Visitor.objects.create(
                    user=user,
                    phone_number=phone_number,
                )
                if not visitor:
                    return RepositoryResponse(
                        success=False,
                        data=None,
                        message="Failed to create visitor"
                        )
                visitor_serializer = VisitorSerializer(visitor).data
                return RepositoryResponse(
                    success=True,
                    data=visitor_serializer,
                    message="Visitor created successfully"
                    )
        except IntegrityError as e:
            return RepositoryResponse(
                success=False,
                data=None,
                message="database integrity error:" + str(e)
                )
        except Exception as e:
            return RepositoryResponse(
                success=False,
                data=None,
                message="Error creating author:" + str(e)
                )


    @staticmethod
    def get_visitor_by_id(visitor_id):
        try:
            visitor=Visitor.objects.filter(id=visitor_id).exists()
            if visitor:
                visitor_serializer = VisitorSerializer(visitor).data
                return RepositoryResponse(
                    success=True,
                    data=visitor_serializer,
                    message="Visitor found successfully"
                    )
            return RepositoryResponse(
                success=False,
                data=None,
                message="visitor not found"
                )
        except Exception as e:
            return RepositoryResponse(
                success=False,
                data=None,
                message="Error retrieving visitor:" + str(e)
                ) 


    @staticmethod
    def get_all_visitors():
        try:
            visitor=Visitor.objects.all()
            if visitor:
                return RepositoryResponse(
                    success=True,
                    data=None,
                    message="No visitors found"
    
                )
            visitor_serializer = VisitorSerializer(visitor, many=True).data
            return RepositoryResponse(
                success=True,
                data=visitor_serializer,
                message="Visitors retrieved successfully"
                )

        except Exception as e:
            return RepositoryResponse(
                success=False,
                data=None,
                message="Error retrieving visitors:" + str(e)
                )

    # @staticmethod
    # def update_visitor(visitor_id, data):
    #     try:
    #         with transaction.atomic():
    #             visitor = Visitor.objects.filter(id=visitor_id).first()
    #             if not visitor:
    #                 return RepositoryResponse(False, None, message="Visitor not found")                
