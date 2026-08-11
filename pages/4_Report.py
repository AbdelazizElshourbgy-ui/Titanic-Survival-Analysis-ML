import streamlit as st

st.set_page_config(page_title="Titanic Report", page_icon="📝", layout="wide")

st.title("📝 Titanic Data-Driven Action Report")
st.caption("From analytical findings to practical safety decisions")

st.divider()

st.subheader("🎯 Executive Summary")
st.markdown("""
The Titanic analysis reveals clear differences in survival outcomes
across passenger groups.

Passenger class, gender, age and fare were associated with different
survival patterns. The results show that passengers were not exposed
to the same level of risk during the disaster.

The purpose of this report is to translate these findings into
practical actions that could improve emergency preparedness and
passenger safety.
""")

st.subheader("🔎 Key Findings")

c1,c2 = st.columns(2)

with c1:
    with st.container(border=True):
        st.markdown("### 01 — Passenger Class")
        st.write("Survival rates differed across passenger classes, with lower-class passengers facing greater risk.")

with c2:
    with st.container(border=True):
        st.markdown("### 02 — Gender")
        st.write("Female passengers showed considerably higher survival rates than male passengers.")

c1,c2 = st.columns(2)

with c1:
    with st.container(border=True):
        st.markdown("### 03 — Age")
        st.write("Survival outcomes were not evenly distributed across passenger age groups.")

with c2:
    with st.container(border=True):
        st.markdown("### 04 — Fare & Socioeconomic Factors")
        st.write("Fare and passenger class reveal socioeconomic differences associated with survival.")

st.subheader("🚨 Recommended Actions")

with st.container(border=True):
    st.markdown("### 🔵 Priority 01 — Improve Emergency Prioritization")
    st.write("Establish clear evacuation procedures and ensure vulnerable passengers receive immediate assistance.")

with st.container(border=True):
    st.markdown("### 🟢 Priority 02 — Equal Access to Safety Resources")
    st.write("Ensure emergency equipment, evacuation routes and safety information are accessible regardless of ticket class.")

with st.container(border=True):
    st.markdown("### 🟣 Priority 03 — Strengthen Emergency Training")
    st.write("Conduct regular evacuation drills and provide passengers with clear emergency instructions.")

with st.container(border=True):
    st.markdown("### 🟠 Priority 04 — Monitor High-Risk Groups")
    st.write("Identify passenger groups that may require additional assistance during emergency situations.")

st.subheader("🔄 Decision Framework")
st.info("ANALYZE  →  IDENTIFY RISK  →  PRIORITIZE  →  ACT  →  MONITOR")

st.markdown("""
**Analyze:** Understand passenger characteristics and historical patterns.

**Identify Risk:** Detect groups and conditions associated with higher risk.

**Prioritize:** Allocate safety resources where they can have the greatest impact.

**Act:** Implement improved evacuation procedures and emergency training.

**Monitor:** Continuously evaluate safety performance and update procedures.
""")

st.subheader("🏁 Final Conclusion")
st.markdown("""
Data analysis provides more than historical statistics. It helps
identify risk patterns, prioritize resources and support better decisions.

The Titanic analysis demonstrates how demographic and socioeconomic
factors can reveal important differences in survival outcomes.

### **The key lesson: Data should lead to action.**
""")

st.success("📝 Report Completed — From Data to Decision")
