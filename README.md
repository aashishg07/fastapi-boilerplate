# alembic migration command 
    alembic revision --autogenerate -m <"message">

# After running this command, execute the following command to apply the migration files and make actual changes to the database    
    alembic upgrade head