import grpc
from concurrent import futures
from app import service, database
from app.proto import user_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(service.UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("User service running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    database.init_db()
    serve()
