class DBConfig:
    DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/Student"
    from_attributes = True  # This allows Pydantic to work with SQLAlchemy models directly
    # """Explanation: The UserResponse Pydantic model represents how you want to structure the response
    # that will be sent back to the client. The orm_mode = True config tells Pydantic to accept ORM model objects
    # (like SQLAlchemy's User model) and convert them to a dictionary format."""

class ORMConfig:
    from_attributes = True #Pydantic expects configuration for serialization
