import grpc
from app.proto import order_pb2, order_pb2_grpc, user_pb2, user_pb2_grpc
from app.models import Order, session

USER_SERVICE_HOST = os.getenv('USER_SERVICE_HOST', 'user-service')
USER_SERVICE_PORT = os.getenv('USER_SERVICE_PORT', '50051')

class OrderService(order_pb2_grpc.OrderServiceServicer):

    def AddOrder(self, request, context):
        with grpc.insecure_channel(f'{USER_SERVICE_HOST}:{USER_SERVICE_PORT}') as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            try:
                response = stub.GetUser(user_pb2.UserRequest(email=request.user_id))
                if not response.user.email:
                    context.set_details('User does not exist')
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return order_pb2.OrderResponse()
            except grpc.RpcError as e:
                context.set_details('Error connecting to user service')
                context.set_code(grpc.StatusCode.INTERNAL)
                return order_pb2.OrderResponse()

        new_order = Order(title=request.title, description=request.description, user_id=request.user_id)
        session.add(new_order)
        session.commit()
        return order_pb2.OrderResponse(message="Order added successfully", order=self._order_to_proto(new_order))

    def GetOrder(self, request, context):
        order = session.query(Order).filter_by(id=request.id).first()
        if order:
            return order_pb2.OrderResponse(order=self._order_to_proto(order))
        else:
            context.set_details('Order not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return order_pb2.OrderResponse()

    def UpdateOrder(self, request, context):
        order = session.query(Order).filter_by(id=request.id).first()
        if order:
            order.title = request.title
            order.description = request.description
            session.commit()
            return order_pb2.OrderResponse(message="Order updated successfully", order=self._order_to_proto(order))
        else:
            context.set_details('Order not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return order_pb2.OrderResponse()

    def _order_to_proto(self, order):
        return order_pb2.Order(
            id=order.id,
            title=order.title,
            description=order.description,
            user_id=order.user_id
        )
