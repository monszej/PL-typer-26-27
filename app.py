
import streamlit as st,pandas as pd
from datetime import datetime,timezone
from database import get_conn
from football_data import get_matches
from scoring import points

conn=get_conn()
st.set_page_config(page_title='Premier League Typer',layout='wide')
st.title('⚽ Premier League Typer 26/27')

menu=st.sidebar.radio('Menu',['Typowanie','Ranking'])
user=st.sidebar.text_input('Nick')

if menu=='Typowanie':
 st.header('Nadchodzące mecze')
 matches=get_matches('SCHEDULED')
 if not matches:
  st.warning('Brak danych API lub nie ustawiono klucza.')
 for m in matches[:20]:
  mid=m['id']
  home=m['homeTeam']['shortName']
  away=m['awayTeam']['shortName']
  kickoff=m['utcDate']
  st.write(f'**{home} vs {away}** ({kickoff})')
  c1,c2=st.columns(2)
  hp=c1.number_input('Home',0,20,0,key=f'h{mid}')
  ap=c2.number_input('Away',0,20,0,key=f'a{mid}')
  if st.button(f'Zapisz {mid}'):
   conn.execute('INSERT OR REPLACE INTO predictions VALUES (?,?,?,?)',(user,mid,hp,ap))
   conn.commit()
   st.success('Zapisano')

if menu=='Ranking':
 st.header('Ranking')
 finished=get_matches('FINISHED')
 preds=pd.read_sql_query('select * from predictions',conn)
 ranking={}
 for _,p in preds.iterrows():
  match=next((m for m in finished if m['id']==p['match_id']),None)
  if not match: continue
  rh=match['score']['fullTime']['home']
  ra=match['score']['fullTime']['away']
  ranking[p['username']]=ranking.get(p['username'],0)+points(p['home_pred'],p['away_pred'],rh,ra)
 df=pd.DataFrame(sorted(ranking.items(),key=lambda x:x[1],reverse=True),columns=['Gracz','Punkty'])
 st.dataframe(df,use_container_width=True)
