from docx import Document
from docx.shared import Inches
from docx.enum.style import WD_STYLE_TYPE
import io
import datetime

import streamlit as st

st.title("Automatisk geoteknisk rapport")
#--
st.header("Dokumentinformasjon")
c1, c2 = st.columns(2)
with c1:
    forfatter = st.text_input("Forfatter", value="Ola Nordmann")
    oppdragsleder = st.text_input("Oppdragsleder", value="Kari Nordmann")
    oppdragsgiver = st.text_input("Oppdragsgiver", value = "Firma AS")
with c2:
    oppdragsnummer = st.text_input("Oppdragsnummer", value = "635960-01")
    sted = st.text_input("Sted", value = "Trondheim")
#--
st.markdown("---")
st.header("Innhenting av data")
st.caption("Folium / Geopandas | ArcGIS")
st.write("- Sted -> Oversiktskart")
st.write("- Sted -> Terrengprofil(?)")
st.write("- Sted -> Frost MET (klimadata) fra nærmeste værstasjon")
st.write("- Sted -> NGU-kart: løsmasser, marin grense, NADAG, GRANADA, ...")

#--
st.markdown("---")
st.header("Redigerbare avsnitt")
report_text_1 = st.text_area("Avsnitt 1", value = """Viktige problemstillinger innen geoteknikk er vurdering av fundamenters bæreevne 
(lastkapasitet) og deres setning under belastning, jordtrykk mot støtte- og kjellermurer, 
stabilitet av veiskjæringer og naturlige skråninger, fundamentering av marine konstruksjoner og rørledninger. """)
c1, c2 = st.columns(2)
with c1:
    depth_to_bedrock = st.number_input("Dybde til fjell [m]", value=5, step=1)
with c2:
    loose_material = st.selectbox("Hva slags løsmasser?", options=["hav- og fjordavsetning", "elveavsetning", "breelvavsetning", "morene"])
report_text_2 = f"""Dybde til fjell var {depth_to_bedrock} m. Løsmassene er kartlagt som {loose_material}."""
#--
document = Document("Notatmal.docx")
styles = document.styles
style = styles.add_style('Citation', WD_STYLE_TYPE.PARAGRAPH)
document.paragraphs[0].text = f"Oppdragsgiver: {oppdragsgiver}"
document.paragraphs[1].text = f"Oppdragsnavn: Geoteknisk rapport - {sted}"
document.paragraphs[2].text = f"Oppdragsnummer: {oppdragsnummer} - {sted}"
document.paragraphs[3].text = f"Utarbeidet av: {forfatter}"
document.paragraphs[4].text = f"Oppdragsleder: {oppdragsleder}"
document.paragraphs[5].text = f"Dato: {datetime.date.today()}"
document.paragraphs[6].text = f"Tilgjenglighet: Åpen"

document.paragraphs[7].text = f"Geoteknisk notat - {sted}"

document.add_picture('trondheim.png', width=Inches(1.25))
document.add_heading("Innledning", 1)
document.add_paragraph(report_text_1)
document.add_paragraph(report_text_2)
#--
st.markdown("---")
st.header("Last ned rapport")
bio = io.BytesIO()
document.save(bio)
if document:
    st.download_button(
        label="Last ned rapport i word-format",
        data=bio.getvalue(),
        file_name="Report.docx",
        mime="docx")