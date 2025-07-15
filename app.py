import streamlit as st
from utils import split_sentences, read_pdf
from plagiarism import get_embeddings, compare_internal, search_web_ddg, compare_to_web

st.title("DeepDetect - Semantic Plagiarism Checker")

files = st.file_uploader("Upload .txt or .pdf", type=["txt", "pdf"], accept_multiple_files=True)
use_web = st.checkbox("Include Internet plagiarism check", value=True)
threshold = st.slider("Similarity threshold", 0.5, 0.95, 0.8)

if files:
    all_raw = []
    file_names = []
    for file in files:
        raw = ""
        if file.type == "application/pdf":
            raw = read_pdf(file)
        else:
            try:
                content = file.read()
                try:
                    raw = content.decode("utf-8")
                except UnicodeDecodeError:
                    raw = content.decode("ISO-8859-1")
            except Exception as e:
                st.error(f"Could not read or decode the uploaded file: {e}")
                continue
        if raw:
            all_raw.append(raw)
            file_names.append(file.name)
        else:
            st.warning(f"Uploaded file '{file.name}' is empty or couldn't be read.")
    if not all_raw:
        st.warning("No valid files uploaded.")
        st.stop()

    # Combine all texts, but keep track of sentence origins and indices
    sents = []
    sent_file_map = []
    sent_file_idx = []
    for idx, raw in enumerate(all_raw):
        these_sents = split_sentences(raw)
        sents.extend(these_sents)
        sent_file_map.extend([file_names[idx]] * len(these_sents))
        sent_file_idx.extend(list(range(1, len(these_sents) + 1)))

    if not sents:
        st.warning("No sentences could be extracted from the uploaded documents.")
        st.stop()

    st.write("📄 Uploaded content preview (first 500 chars of each file):")
    for name, raw in zip(file_names, all_raw):
        st.markdown(f"**{name}:**")
        st.code(raw[:500])

    emb = get_embeddings(sents)
    internal = compare_internal(emb, emb, threshold)

    web_matches = []
    if use_web:
        for i, sent in enumerate(sents):
            snippets_and_urls = search_web_ddg(sent)
            score, idx = compare_to_web(sent, snippets_and_urls, threshold)
            if score >= threshold and idx is not None:
                matched_snippet, matched_url = snippets_and_urls[idx]
                web_matches.append({
                    "File": sent_file_map[i],
                    "Sentence #": sent_file_idx[i],
                    "Sentence": sents[i],
                    "Matched Web Snippet": matched_snippet,
                    "Similarity": round(score, 3),
                    "Source": matched_url
                })

    total_matches = len(set([i for i,_,_ in internal] + [sents.index(wm["Sentence"]) for wm in web_matches]))
    st.metric("Plagiarized Sentences", f"{total_matches}/{len(sents)}")

    st.subheader("Matched Sentences")

    # --- Internal Matches Table ---
    if internal:
        st.markdown("### Internal (Within/Across Files) Matches")
        match_rows = []
        for i, j, score in internal:
            match_type = "Cross-file" if sent_file_map[i] != sent_file_map[j] else "Within-file"
            match_rows.append({
                "Match Type": match_type,
                "File A": sent_file_map[i],
                "Sentence #A": sent_file_idx[i],
                "Sentence A": sents[i],
                "File B": sent_file_map[j],
                "Sentence #B": sent_file_idx[j],
                "Sentence B": sents[j],
                "Similarity": round(score, 3)
            })
        st.dataframe(match_rows, use_container_width=True)
    else:
        st.info("No internal plagiarism detected.")

    # --- Web Matches Table (with clickable links) ---
    if web_matches:
        st.markdown("### Web Matches")
        # Table header
        st.markdown(
            """
            <style>
            .web-table th, .web-table td { padding: 0.2em 0.5em; border: 1px solid #ddd; }
            .web-table { border-collapse: collapse; width: 100%; font-size: 0.95em; }
            </style>
            <table class="web-table">
                <tr>
                    <th>File</th>
                    <th>Sentence #</th>
                    <th>Sentence</th>
                    <th>Matched Web Snippet</th>
                    <th>Similarity</th>
                    <th>Source</th>
                </tr>
            """,
            unsafe_allow_html=True
        )
        # Table rows
        for wm in web_matches:
            st.markdown(
                f"""
                <tr>
                    <td>{wm['File']}</td>
                    <td>{wm['Sentence #']}</td>
                    <td>{wm['Sentence']}</td>
                    <td>{wm['Matched Web Snippet']}</td>
                    <td>{wm['Similarity']}</td>
                    <td><a href="{wm['Source']}" target="_blank">Link</a></td>
                </tr>
                """,
                unsafe_allow_html=True
            )
        # Close table
        st.markdown("</table>", unsafe_allow_html=True)
    else:
        st.info("No web plagiarism detected.")
