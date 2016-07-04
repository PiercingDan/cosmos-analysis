

colnames = ['ch1', 'J', 'V', 'zpband']
mat = balogh_data2['ultravista_match'] 
for name in colnames:
    data = ultravista[name][mat]
    col = Column(data=data, name=name)
    balogh_data2.add_column(col)
    
    
    