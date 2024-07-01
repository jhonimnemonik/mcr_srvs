import grpc
from app.proto import user_pb2, user_pb2_grpc
from app.models import User, session


class UserService(user_pb2_grpc.UserServiceServicer):
    def AddUser(self, request, context):
        new_user = User(name=request.name, email=request.email, age=request.age)
        session.add(new_user)
        session.commit()
        return user_pb2.UserResponse(message="User added successfully", user=self._user_to_proto(new_user))

    def GetUser(self, request, context):
        user = session.query(User).filter_by(email=request.email).first()
        if user:
            return  user_pb2.UserResponse(user=self._user_to_proto(user))
        else:
            context.set_details('User not found')
        context.set_code(grpc.StatusCode.NOT_FOUND)
        return
    def UpdateUser