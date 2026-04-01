import os
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
import streamlit as st
from typing import Optional
from pipeline.runner import Runner

# ---------- CONFIG ----------
st.set_page_config(page_title="Analyse CV vs Offre", layout="wide")


# ---------- HELPERS ----------
def validate_inputs(cv_file, cv_text, job_url, job_text) -> Optional[str]:
    if not cv_file and not cv_text:
        return "Veuillez fournir un CV (upload ou texte)."
    if not job_url and not job_text:
        return "Veuillez fournir une offre (URL ou texte)."
    return None


def display_score(score_output):
    score = score_output.score
    st.subheader("📊 Score de compatibilité")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric(label="Score", value=f"{score}%")
    with col2:
        st.progress(score / 100)

    st.write(score_output.justification)


def display_gaps(gaps_output):
    st.subheader("⚠️ Gaps identifiés")

    for gap in gaps_output.gaps:
        if gap.criticality == "high":
            st.error(f"{gap.element} — {gap.advice}")
        elif gap.criticality == "medium":
            st.warning(f"{gap.element} — {gap.advice}")
        else:
            st.success(f"{gap.element} — {gap.advice}")


def display_strengths(strengths_output):
    st.subheader("💪 Points forts")

    for s in strengths_output.strengths:
        st.markdown(f"**{s.element}**")
        st.write(s.justification)


def display_keywords(keywords_output):
    st.subheader("🔑 Mots-clés")

    for kw in keywords_output.key_words:
        st.markdown(f"- **{kw.key_word}** : {kw.context}")


def display_rewording(rewording_output):
    st.subheader("✍️ Suggestions de reformulation")

    for r in rewording_output.rewordings:
        with st.expander(f"Suggestion pour : {r.origine[:60]}..."):
            st.markdown(f"**Original :** {r.origine}")
            st.markdown(f"**Suggestion :** {r.suggested}")
            st.markdown(f"**Pourquoi :** {r.reason}")


# ---------- SIDEBAR ----------
st.sidebar.header("📥 Inputs")

cv_file = st.sidebar.file_uploader("Upload CV (PDF/DOCX)", type=["pdf", "docx"])
cv_text = st.sidebar.text_area("Ou coller le CV")

job_url = st.sidebar.text_input("URL de l'offre")
job_text = st.sidebar.text_area("Ou coller l'offre")

run_button = st.sidebar.button("🚀 Analyser")


# ---------- MAIN ----------
st.title("Analyse CV vs Offre")

if run_button:
    error = validate_inputs(cv_file, cv_text, job_url, job_text)

    if error:
        st.error(error)
    else:
        try:
            runner = Runner()

            cv_path = None
            if cv_file:
                # sauvegarde temporaire
                import tempfile

                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(cv_file.read())
                    cv_path = tmp.name

            with st.spinner("Analyse en cours..."):
                results = runner.run_job(
                    cv_path=cv_path,
                    cv_content=cv_text if not cv_file else None,
                    job_content=job_text if not job_url else None,
                    job_url=job_url,
                )

            # ---------- DISPLAY ----------
            display_score(results["ScoreAgent"])
            display_gaps(results["GapsAgent"])
            display_strengths(results["StrengthsAgent"])
            display_keywords(results["KeywordsAgent"])
            display_rewording(results["RewordingAgent"])

        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {str(e)}")