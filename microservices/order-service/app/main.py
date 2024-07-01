import grpc
from concurrent import futures
from app import service, database
from app.proto import order_pb2_grpc

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(service.OrderService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Order service is running on port 50052.")
    server.wait_for_termination()

if __name__ == '__main__':
    database.init_db()
    serve()
