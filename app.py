from __future__ import annotations
import base64,hashlib,os,json
from pathlib import Path
import streamlit as st
from data_model import load_workbook
from assistant import answer,optional_ai
from sql_lab import run_query,STARTERS

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='Elm · Customer intelligence',page_icon='✦',layout='wide',initial_sidebar_state='collapsed')
st.markdown('''<style>[data-testid="stHeader"],footer{display:none}.stMainBlockContainer{padding:0!important;max-width:none!important}.stMain{background:#f3f6fc}[data-testid="stVerticalBlock"]{gap:0}body{margin:0}</style>''',unsafe_allow_html=True)
@st.cache_data(show_spinner=False)
def read_data(raw):return load_workbook(raw)
@st.cache_data(show_spinner=False)
def asset_payload():
    result={}
    for p in (ROOT/'assets').iterdir():
        if p.suffix.lower() not in ['.svg','.png','.jpg','.jpeg','.woff2']:continue
        mime={'.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.woff2':'font/woff2'}[p.suffix.lower()]
        result[p.name]='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
    return result

st.session_state.setdefault('workbook_bytes',(ROOT/'data/customer_journey.xlsx').read_bytes())
st.session_state.setdefault('replies',[])
st.session_state.setdefault('ai_enabled',False)
st.session_state.setdefault('sql_reply',None)
raw=st.session_state.workbook_bytes
try:data=read_data(raw)
except ValueError as exc:st.error(str(exc));st.stop()
# Geography is optional. Demo mapping is used ONLY for the bundled demo workbook.
if hashlib.sha256(raw).digest()==b'@\x06,\x93\x05\x1f\x02\xa8\xaf&\xd9\xd5fLLe\x1f\x94jP\x9b\xa7V\x8b\xadQ\x17\xbf\x92o\xeb\x9c':
    data['Locations']=json.loads((ROOT/'data/demo_locations.json').read_text(encoding='utf-8'))
else:
    data['Locations']=[]
    for c in data['Customers']:
        try:
            lat,lon=float(c['latitude']),float(c['longitude'])
            if str(c['city']).strip() and -90<=lat<=90 and -180<=lon<=180:data['Locations'].append(dict(customer_id=c['customer_id'],city=str(c['city']),latitude=lat,longitude=lon,demo=False))
        except (KeyError,TypeError,ValueError):pass

workspace=st.components.v2.component('elm_page8_workspace',html='<div id="elm-app" aria-label="Elm customer intelligence"></div>',css=(ROOT/'frontend/styles.css').read_text(encoding='utf-8'),js='const MESSAGES='+ (ROOT/'frontend/locales.json').read_text(encoding='utf-8')+';\n'+(ROOT/'frontend/workspace.js').read_text(encoding='utf-8'))
result=workspace(key='elm_workspace',data={'dataset':data,'assets':asset_payload(),'version':hashlib.sha256(raw).hexdigest()[:16],'replies':st.session_state.replies,'ai':st.session_state.ai_enabled,'sqlReply':st.session_state.sql_reply,'sqlStarters':STARTERS,'outline':json.loads((ROOT/'data/saudi_outline.json').read_text(encoding='utf-8'))},default={'ask':None,'settings':None,'sql':None},on_sql_change=lambda:None,on_ask_change=lambda:None,on_settings_change=lambda:None,height='content')

if result.sql and result.sql.get('id')!=st.session_state.get('last_sql_id'):
    request=result.sql;st.session_state.last_sql_id=request['id']
    st.session_state.sql_reply={'id':request['id'],**run_query(data,str(request.get('query','')),request.get('context',{}))}
    st.rerun()

if result.ask and result.ask.get('id')!=st.session_state.get('last_question_id'):
    request=result.ask;st.session_state.last_question_id=request['id']
    response=answer(str(request.get('question',''))[:2000],data,request.get('context',{}))
    if st.session_state.ai_enabled:
        response=optional_ai(request['question'],response,os.getenv('OPENAI_API_KEY',''),os.getenv('OPENAI_MODEL','gpt-4.1-mini'))
    st.session_state.replies.append({'id':request['id'],'question':request['question'],'answer':response})
    st.session_state.replies=st.session_state.replies[-30:]
    st.rerun()

@st.dialog('Data & assistant',width='large')
def data_settings():
    ar=bool(result.settings and result.settings.get('language')=='ar')
    T=lambda en,arabic:arabic if ar else en
    st.write(T('The app starts with the included synthetic Excel workbook. Replace it with your own workbook using the same four-sheet schema.','يبدأ التطبيق بملف Excel تجريبي. يمكنك رفع ملفك بنفس أسماء الأوراق والأعمدة المطلوبة.'))
    upload=st.file_uploader(T('Excel workbook','ملف Excel'),type=['xlsx'])
    if upload:
        try:
            check=read_data(upload.getvalue())
            st.success(f"Validated: {len(check['Customers'])} customers, {len(check['Products'])} products.")
            if st.button(T('Use this workbook','استخدام هذا الملف'),type='primary'):
                st.session_state.workbook_bytes=upload.getvalue();st.session_state.replies=[];st.session_state.sql_reply=None;st.rerun()
        except Exception as exc:st.error(str(exc))
    st.download_button(T('Download current workbook','تنزيل ملف البيانات الحالي'),data=st.session_state.workbook_bytes,file_name='customer_journey.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.divider()
    st.caption('Local data assistant works without an API key. Optional AI wording sends only your question and the computed answer to OpenAI; enable only if permitted for your data.')
    st.checkbox(T('Use optional AI wording','استخدام إعادة الصياغة بالذكاء الاصطناعي — اختياري'),key='ai_enabled',disabled=not bool(os.getenv('OPENAI_API_KEY')))
    if not os.getenv('OPENAI_API_KEY'):st.caption('Optional: set OPENAI_API_KEY and OPENAI_MODEL in your server environment. No key is included in the project.')
    st.caption('Design reference: Figma MDM · page 8. This is a Streamlit app with an editable HTML/CSS/JS component for precise alignment. No Node.js build is required.')

if result.settings:data_settings()
