import  pandas as pd
import matplotlib.pylab as plt
import  numpy as np
import pickle
rootPath = '../../../'

class ProjDataDump():
    def __init__(self):
        self.inputDataPath = rootPath + 'Data/RawData'
        self.outputDataPath = rootPath + 'API/FeatureExtraction/NetworkAnlaysis/'
        self.mainDataList = self.loadData()
        self.averaged_df = self.makeAverage_df()
        self.fileDump()


    def loadData(self):
        resultLst = []
        period = [2015,2016,2017]
        for year in period:
            filename = self.inputDataPath + '/HR__' + str(year) + '_EvalCap.csv'
            df = pd.read_csv(filename, engine='python',header=None, skiprows=1)
            df.columns = ['emp_id', 'var1','var2','var3','var4','var5','var6','var7','var8','var9','var10']
            df = df.set_index('emp_id')
            resultLst.append(df)
        return resultLst

    def makeAverage_df(self):
        empList =[]
        for lst in self.mainDataList:
            empList = empList + list(lst.index)
        empList = list(set(empList))
        df_main = pd.DataFrame([],columns=['var1','var2','var3','var4','var5','var6','var7','var8','var9','var10','Num'])
        for lst in self.mainDataList:
            for row in lst.iterrows():
                row[1]['Num'] = 1
                if row[0] not in list(df_main.index):
                    df_main = df_main.append(row[1])
                else:
                    df_main.loc[row[0]]  = df_main.loc[row[0]] + row[1]
        colNameList = list(df_main.columns)
        colNameList.pop()
        for col in colNameList:
            df_main[col] = df_main[col] / df_main['Num']
        df_main = df_main.drop(['Num'], axis=1)
        return df_main

    def fileDump(self):
        filename = self.outputDataPath + 'EvalCap_df.obj'
        f = open(filename,'wb')
        pickle.dump(self.averaged_df,f)
        f.close()


def Main():
    instance = ProjDataDump()


if __name__ == '__main__':
    Main()