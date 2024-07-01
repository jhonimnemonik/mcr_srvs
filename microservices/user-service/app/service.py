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
            return user_pb2.UserResponse(user=self._user_to_proto(user))
        else:
            context.set_details('User not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_pb2.UserResponse()

    def UpdateUser(self, request, context):
        user = session.query(User).filter_by(email=request.email).first()
        if user:
            user.name = request.name
            user.age = request.age
            session.commit()
            return user_pb2.UserResponse(message="User updated successfully", user=self._user_to_proto(user))
        else:
            context.set_details('User not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_pb2.UserResponse()

    def _user_to_proto(self, user):
        return user_pb2.User(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age
        )
