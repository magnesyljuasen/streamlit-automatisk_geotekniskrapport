from docx import Document
from docx.shared import Inches
from docx.enum.style import WD_STYLE_TYPE
import io

import streamlit as st

st.title("Automatisk rapport")
report_name = st.text_input("Sted", placeholder = "Trondheim")
report_text_1 = st.text_area("Avsnitt 1", value = """Viktige problemstillinger innen geoteknikk er vurdering av fundamenters bæreevne 
(lastkapasitet) og deres setning under belastning, jordtrykk mot støtte- og kjellermurer, 
stabilitet av veiskjæringer og naturlige skråninger, fundamentering av marine konstruksjoner og rørledninger. """)
c1, c2 = st.columns(2)
with c1:
    depth_to_bedrock = st.number_input("Dybde til fjell [m]", value=5, step=1)
with c2:
    loose_material = st.selectbox("Hva slags løsmasser?", options=["hav- og fjordavsetning", "elveavsetning", "breelvavsetning", "morene"])
report_text_2 = f"""Dybde til fjell var {depth_to_bedrock} m. Løsmassene er kartlagt som {loose_material}."""

document = Document()
styles = document.styles
style = styles.add_style('Citation', WD_STYLE_TYPE.PARAGRAPH)
document.add_heading(f"Geoteknisk rapport - {report_name}", 0)
document.add_paragraph(report_text_1)
document.add_paragraph(report_text_2)

bio = io.BytesIO()
document.save(bio)
if document:
    st.download_button(
        label="Last ned rapport",
        data=bio.getvalue(),
        file_name="Report.docx",
        mime="docx")