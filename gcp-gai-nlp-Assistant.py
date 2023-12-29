import os

import pandas as pd
from sqlalchemy import create_engine, text
from vertexai.language_models import CodeGenerationModel

df = pd.read_csv('penguins.csv')
temp_db = create_engine('sqlite:///:memory:', echo=True)
data = df.to_sql(name='Penguins',con=temp_db)

os.getcwd()
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='C:\\work\\projects\\GCP-GAI\\doc\\gai87546-4b61133715b1.json'

model_name = 'code-bison'
model = CodeGenerationModel.from_pretrained(model_name)

def create_prefix(query):
    #query = input("what is your question about penguin table?")
    prefix = f""" Return a SQL statement that answer the following query:
    {query}
    
    For a table called 'Penguins" with the following properties:
    #   Column             Non-Null Count  Dtype  
    ---  ------             --------------  -----  
     0   species            344 non-null    object 
     1   island             344 non-null    object 
     2   bill_length_mm     342 non-null    float64
     3   bill_depth_mm      342 non-null    float64
     4   flipper_length_mm  342 non-null    float64
     5   body_mass_g        342 non-null    float64
     6   sex                333 non-null    object 
     
    Example Rows:
    (0, 'Adelie', 'Torgersen', 39.1, 18.7, 181.0, 3750.0, 'MALE'),
    (1, 'Adelie', 'Torgersen', 39.5, 17.4, 186.0, 3800.0, 'FEMALE')
    
    Only return the SQL statement for the query.
    """  
    return prefix

def user_input(query):
    #query = input('Ask a question about the Penguins Table: ')
    return create_prefix(query)

def clean_sql(sqlText):
    return sqlText.replace('```sql','').replace("```","").replace('\n',' ')

def nlp_assistant():
    print("Hello, I am your AI database assistant")
    #print('\n')
    while True :
        query = ''
        query = input('Ask a question about the Penguins Table (type exit to close the chat): ')
        if query.lower() == 'end' or query.lower() == 'exit' :
            print("Thank you, have a nice day.")
            return
        prefix = user_input(query)
        result = model.predict(prefix=prefix)
        sql = clean_sql(result.text)
        with temp_db.connect() as conn:
            result = conn.execute(text(sql))
        print("Here are your results:")
        print(result.all())
     
nlp_assistant()
    


