import pandas as pd
from sqlalchemy.engine import create_engine



def main():
    conex = create_engine("mysql+pymysql://root:Rugby_777@localhost/dublinbikes")
    
    df = pd.read_sql_table("data", conex)
    
    print(df)
    
    


        
        