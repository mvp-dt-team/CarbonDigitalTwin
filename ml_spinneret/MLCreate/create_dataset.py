from DatasetPreproccessing import DatasetPreProc
import pandas as pd

df1 = pd.read_csv('CORRECTED_g1-g24_.csv')
columns1 = list(df1.columns)

df2 = pd.read_csv('CORRECTED_g25-49_.csv')
columns2 = list(df2.columns)

df3 = pd.read_csv('CORRECTED_g50-g74_.csv')
columns3 = list(df3.columns)

df4 = pd.read_csv('CORRECTED_g75-92_.csv')
columns4 = list(df4.columns)

df5 = pd.read_csv('CORRECTED_g93-g118_.csv')
columns5 = list(df5.columns)
a = DatasetPreProc(['g1-g24_.csv', 'g25-49_.csv', 'g50-g74_.csv', 'g75-92_.csv', 'g93-g118_.csv'], 
                   columns=[columns1[2:], columns2[2:], columns3[2:], columns4[2:], columns5[2:]],
                   params={'STEP_X': [0.01, 0.01, 0.01, 0.01, 0.01], 'STEP_Y': [0.01, 0.01, 0.01, 0.01, 0.01]},
                   dataset_filename='DATASET.json')
a.action()