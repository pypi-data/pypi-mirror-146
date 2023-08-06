def coef(data):
    matrix = np.zeros((data.shape[1], data.shape[1]))
    for i in range(data.shape[1]):
        for j in range(data.shape[1]):
            df01 = pd.DataFrame(zip(data.iloc[:,i], data.iloc[:,j]), columns=["x","y"])
            df01["yranks"] = df01["y"].rank()
            df01 = df01.sort_values("x")
            rank_series = df01["yranks"].reset_index(drop=True)
            #rank_series
            diff=[]
            for k in range(len(rank_series)-1):
                diff.append(abs(rank_series[k+1]-rank_series[k]))
            f=1-3*(sum(diff)/(df01.shape[0]**2-1))
            matrix[i,j] = f
    return matrix

a = coef(df)
    
df02 = pd.DataFrame(a, columns=df.columns, index=df.columns).round(3)
df02