from app import *


'''
title = db.session.query(douban.title_Chinese).all()
n_title = db.session.query(IMDB.title).all()

print(title)
print(n_title)
'''
ge = '2010s'
ge = ge.rstrip('s')
print(ge)
movie= db.session.query(douban.title_Chinese,IMDB.n_title,douban.director,douban.country,douban.year,douban.genre,douban.rate,rate.imdb,rate.rottenTomatoes,IMDB.image)\
    .join(IMDB,douban.title_English==IMDB.title)\
    .join(rate,IMDB.id==rate.r_id)\
    .filter(douban.year >=ge).filter(douban.year <=str(int(ge)+10))
print(movie)
df = pd.DataFrame(movie, columns=['title','n_title','director','district','year','genre','douban_rate','imdb_rate','rT_rate','image'])
df.to_csv(ge+'.csv',mode='w',index=False,sep="\t")#部分电影名称包含逗号，所以使用tab作为分隔符
print(df)