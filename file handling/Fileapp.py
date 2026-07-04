"""
File Cabinet — a Streamlit front end for basic filesystem operations
(create, read, append, delete, rename files; create/delete folders).

Run with:
    streamlit run file_cabinet_app.py
"""

import os
from datetime import datetime
from pathlib import Path

import streamlit as st

# --------------------------------------------------------------------------
# Page setup
# --------------------------------------------------------------------------

st.set_page_config(page_title="File Cabinet", page_icon="🗂", layout="wide")

# --------------------------------------------------------------------------
# Style — a working archive: brass-tab drawers, ledger paper, stamped tags.
# Palette:  ink #1B1F27 / panel #232833 / paper #E9E4D8
#           brass #C6982F / rust #B24F3C / sage #5D8A72 / line #363C48
# Type:     Space Grotesk (headers) / Inter (body) / JetBrains Mono (data)
# --------------------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root{
        --ink:#1B1F27;
        --panel:#232833;
        --panel-raised:#2B303C;
        --paper:#E9E4D8;
        --brass:#C6982F;
        --rust:#B24F3C;
        --sage:#5D8A72;
        --line:#363C48;
        --text-dim:#9AA1AE;
    }

    .stApp{
        background:
            radial-gradient(1200px 500px at 15% -10%, rgba(198,152,47,0.08), transparent 60%),
            var(--ink);
        font-family:'Inter',sans-serif;
        color:var(--paper);
    }

    /* headers */
    h1, h2, h3, .cabinet-title{
        font-family:'Space Grotesk',sans-serif !important;
        letter-spacing:0.01em;
    }

    .cabinet-header{
        display:flex;
        align-items:baseline;
        justify-content:space-between;
        border-bottom:1px solid var(--line);
        padding-bottom:14px;
        margin-bottom:6px;
    }
    .cabinet-title{
        font-size:1.9rem;
        font-weight:700;
        color:var(--paper);
        margin:0;
    }
    .cabinet-title span{ color:var(--brass); }
    .cabinet-path{
        font-family:'JetBrains Mono',monospace;
        font-size:0.8rem;
        color:var(--text-dim);
        background:var(--panel);
        border:1px solid var(--line);
        border-radius:3px;
        padding:5px 10px;
    }

    /* sidebar = the drawer bank */
    section[data-testid="stSidebar"]{
        background:var(--panel);
        border-right:1px solid var(--line);
    }
    section[data-testid="stSidebar"] .block-container{ padding-top:2rem; }
    section[data-testid="stSidebar"] h3{
        font-size:0.72rem;
        letter-spacing:0.14em;
        text-transform:uppercase;
        color:var(--text-dim);
        margin-bottom:0.6rem;
    }

    div[role="radiogroup"] label{
        border:1px solid var(--line);
        border-left:3px solid var(--line);
        background:var(--panel-raised);
        border-radius:3px;
        padding:9px 12px !important;
        margin-bottom:6px;
        width:100%;
        transition:border-color 0.15s ease, background 0.15s ease;
    }
    div[role="radiogroup"] label:hover{
        border-left-color:var(--brass);
        background:#313746;
    }
    div[role="radiogroup"] label[data-checked="true"]{
        border-left-color:var(--brass);
        background:#313746;
    }
    div[role="radiogroup"] p{
        font-family:'JetBrains Mono',monospace !important;
        font-size:0.85rem !important;
        color:var(--paper) !important;
    }

    /* cards */
    .card{
        background:var(--panel);
        border:1px solid var(--line);
        border-radius:4px;
        padding:22px 24px;
    }
    .card h3{
        font-size:1.05rem;
        margin-top:0;
        margin-bottom:2px;
    }
    .card .sub{
        color:var(--text-dim);
        font-size:0.85rem;
        margin-bottom:18px;
    }

    /* inputs */
    .stTextInput input, .stTextArea textarea{
        font-family:'JetBrains Mono',monospace !important;
        background:var(--ink) !important;
        border:1px solid var(--line) !important;
        color:var(--paper) !important;
        border-radius:3px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus{
        border-color:var(--brass) !important;
        box-shadow:0 0 0 1px var(--brass) !important;
    }
    label p{ font-size:0.82rem !important; color:var(--text-dim) !important; }

    /* buttons */
    .stButton button{
        font-family:'Inter',sans-serif;
        font-weight:600;
        font-size:0.82rem;
        letter-spacing:0.03em;
        text-transform:uppercase;
        border-radius:3px;
        border:1px solid var(--brass);
        background:var(--brass);
        color:#1B1F27;
        padding:0.5rem 1rem;
        transition:filter 0.15s ease;
    }
    .stButton button:hover{ filter:brightness(1.12); }
    .stButton button[kind="secondary"]{
        background:transparent;
        color:var(--paper);
        border:1px solid var(--line);
    }

    /* status stamps */
    .stamp{
        display:inline-block;
        font-family:'JetBrains Mono',monospace;
        font-size:0.72rem;
        letter-spacing:0.08em;
        text-transform:uppercase;
        padding:2px 8px;
        border-radius:2px;
        border:1px solid currentColor;
    }
    .stamp-ok{ color:var(--sage); }
    .stamp-err{ color:var(--rust); }
    .stamp-dir{ color:var(--brass); }
    .stamp-file{ color:var(--text-dim); }

    /* ledger */
    .ledger{
        font-family:'JetBrains Mono',monospace;
        font-size:0.78rem;
        max-height:520px;
        overflow-y:auto;
        padding-right:4px;
    }
    .ledger-row{
        display:grid;
        grid-template-columns:64px 60px 1fr;
        gap:10px;
        padding:7px 0;
        border-bottom:1px solid var(--line);
        color:var(--paper);
    }
    .ledger-row:last-child{ border-bottom:none; }
    .ledger-time{ color:var(--text-dim); }
    .ledger-empty{ color:var(--text-dim); font-style:italic; font-size:0.82rem; }

    /* directory listing */
    .dir-row{
        display:flex;
        justify-content:space-between;
        align-items:center;
        font-family:'JetBrains Mono',monospace;
        font-size:0.8rem;
        padding:6px 0;
        border-bottom:1px solid var(--line);
    }
    .dir-row:last-child{ border-bottom:none; }

    hr{ border-color:var(--line) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------

if "log" not in st.session_state:
    st.session_state.log = []
if "confirm_target" not in st.session_state:
    st.session_state.confirm_target = None
if "confirm_kind" not in st.session_state:
    st.session_state.confirm_kind = None


def log_action(action: str, target: str, ok: bool, detail: str = ""):
    st.session_state.log.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M:%S"),
            "action": action,
            "target": target,
            "ok": ok,
            "detail": detail,
        },
    )


def stamp(ok: bool) -> str:
    return '<span class="stamp stamp-ok">done</span>' if ok else '<span class="stamp stamp-err">failed</span>'


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------

st.markdown(
    f"""
    <div class="cabinet-header">
        <div class="cabinet-title">File <span>Cabinet</span></div>
        <div class="cabinet-path">{Path.cwd()}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Sidebar — drawer selection + live directory listing
# --------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### Drawers")
    operation = st.radio(
        "Choose an operation",
        [
            "Create file",
            "Read file",
            "Append to file",
            "Rename file",
            "Delete file",
            "Create folder",
            "Delete folder",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Current directory")
    entries = sorted(Path.cwd().iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    if not entries:
        st.markdown('<div class="ledger-empty">Empty.</div>', unsafe_allow_html=True)
    else:
        rows = ""
        for e in entries:
            tag = '<span class="stamp stamp-dir">dir</span>' if e.is_dir() else '<span class="stamp stamp-file">file</span>'
            rows += f'<div class="dir-row"><span>{e.name}</span>{tag}</div>'
        st.markdown(rows, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Main layout
# --------------------------------------------------------------------------

col_main, col_ledger = st.columns([2.1, 1], gap="large")

with col_main:

    # ---------------- Create file ----------------
    if operation == "Create file":
        st.markdown('<div class="card"><h3>Create file</h3><div class="sub">Writes a brand new file. Refuses to overwrite one that already exists.</div>', unsafe_allow_html=True)
        name = st.text_input("File name", placeholder="notes.txt")
        content = st.text_area("Content", placeholder="Whatever goes in the file...", height=140)
        if st.button("Create file", key="create_file_btn"):
            if not name.strip():
                st.warning("Give the file a name first.")
            else:
                path = Path(name)
                if path.exists():
                    st.error(f"'{name}' already exists — nothing was overwritten.")
                    log_action("Create", name, False, "already exists")
                else:
                    path.write_text(content)
                    st.success(f"'{name}' created.")
                    log_action("Create", name, True)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Read file ----------------
    elif operation == "Read file":
        st.markdown('<div class="card"><h3>Read file</h3><div class="sub">Shows the current contents of a file.</div>', unsafe_allow_html=True)
        name = st.text_input("File name", placeholder="notes.txt")
        if st.button("Read file", key="read_file_btn"):
            path = Path(name)
            if not name.strip():
                st.warning("Enter a file name.")
            elif not path.exists():
                st.error(f"'{name}' does not exist.")
                log_action("Read", name, False, "not found")
            elif path.is_dir():
                st.error(f"'{name}' is a folder, not a file.")
                log_action("Read", name, False, "is a folder")
            else:
                st.code(path.read_text() or "(empty file)", language=None)
                log_action("Read", name, True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Append to file ----------------
    elif operation == "Append to file":
        st.markdown('<div class="card"><h3>Append to file</h3><div class="sub">Adds text to the end of an existing file.</div>', unsafe_allow_html=True)
        name = st.text_input("File name", placeholder="notes.txt")
        content = st.text_area("Content to add", height=140)
        if st.button("Append", key="append_btn"):
            path = Path(name)
            if not name.strip():
                st.warning("Enter a file name.")
            elif not path.exists():
                st.error(f"'{name}' does not exist.")
                log_action("Append", name, False, "not found")
            else:
                with open(path, "a") as f:
                    f.write(content)
                st.success(f"Content added to '{name}'.")
                log_action("Append", name, True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Rename file ----------------
    elif operation == "Rename file":
        st.markdown('<div class="card"><h3>Rename file</h3><div class="sub">Changes a file\'s name in place.</div>', unsafe_allow_html=True)
        old = st.text_input("Current name", placeholder="notes.txt")
        new = st.text_input("New name", placeholder="notes-final.txt")
        if st.button("Rename", key="rename_btn"):
            old_path = Path(old)
            if not old.strip() or not new.strip():
                st.warning("Fill in both names.")
            elif not old_path.exists():
                st.error(f"'{old}' does not exist.")
                log_action("Rename", old, False, "not found")
            elif Path(new).exists():
                st.error(f"'{new}' already exists.")
                log_action("Rename", old, False, "target exists")
            else:
                os.rename(old, new)
                st.success(f"'{old}' → '{new}'.")
                log_action("Rename", f"{old} → {new}", True)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Delete file ----------------
    elif operation == "Delete file":
        st.markdown('<div class="card"><h3>Delete file</h3><div class="sub">Permanently removes a file. This cannot be undone.</div>', unsafe_allow_html=True)
        name = st.text_input("File name", placeholder="notes.txt")
        if st.button("Delete file", key="delete_file_btn"):
            path = Path(name)
            if not name.strip():
                st.warning("Enter a file name.")
            elif not path.exists():
                st.error(f"'{name}' does not exist.")
                log_action("Delete", name, False, "not found")
            elif path.is_dir():
                st.error(f"'{name}' is a folder — use Delete folder instead.")
            else:
                st.session_state.confirm_kind = "file"
                st.session_state.confirm_target = name

        if st.session_state.confirm_kind == "file" and st.session_state.confirm_target:
            target = st.session_state.confirm_target
            st.warning(f"Delete '{target}' permanently?")
            c1, c2 = st.columns(2)
            if c1.button("Confirm delete", key="confirm_del_file"):
                Path(target).unlink()
                st.success(f"'{target}' deleted.")
                log_action("Delete", target, True)
                st.session_state.confirm_target = None
                st.session_state.confirm_kind = None
                st.rerun()
            if c2.button("Cancel", key="cancel_del_file"):
                st.session_state.confirm_target = None
                st.session_state.confirm_kind = None
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Create folder ----------------
    elif operation == "Create folder":
        st.markdown('<div class="card"><h3>Create folder</h3><div class="sub">Makes a new, empty folder.</div>', unsafe_allow_html=True)
        name = st.text_input("Folder name", placeholder="archive")
        if st.button("Create folder", key="create_folder_btn"):
            path = Path(name)
            if not name.strip():
                st.warning("Give the folder a name.")
            elif path.exists():
                st.error(f"'{name}' already exists.")
                log_action("Create folder", name, False, "already exists")
            else:
                os.mkdir(name)
                st.success(f"Folder '{name}' created.")
                log_action("Create folder", name, True)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Delete folder ----------------
    elif operation == "Delete folder":
        st.markdown('<div class="card"><h3>Delete folder</h3><div class="sub">Permanently removes an empty folder. This cannot be undone.</div>', unsafe_allow_html=True)
        name = st.text_input("Folder name", placeholder="archive")
        if st.button("Delete folder", key="delete_folder_btn"):
            path = Path(name)
            if not name.strip():
                st.warning("Enter a folder name.")
            elif not path.exists():
                st.error(f"'{name}' does not exist.")
                log_action("Delete folder", name, False, "not found")
            elif not path.is_dir():
                st.error(f"'{name}' is a file — use Delete file instead.")
            elif any(path.iterdir()):
                st.error(f"'{name}' is not empty — remove its contents first.")
                log_action("Delete folder", name, False, "not empty")
            else:
                st.session_state.confirm_kind = "folder"
                st.session_state.confirm_target = name

        if st.session_state.confirm_kind == "folder" and st.session_state.confirm_target:
            target = st.session_state.confirm_target
            st.warning(f"Delete folder '{target}' permanently?")
            c1, c2 = st.columns(2)
            if c1.button("Confirm delete", key="confirm_del_folder"):
                os.rmdir(target)
                st.success(f"Folder '{target}' deleted.")
                log_action("Delete folder", target, True)
                st.session_state.confirm_target = None
                st.session_state.confirm_kind = None
                st.rerun()
            if c2.button("Cancel", key="cancel_del_folder"):
                st.session_state.confirm_target = None
                st.session_state.confirm_kind = None
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Ledger — running record of every operation, most recent first
# --------------------------------------------------------------------------

with col_ledger:
    st.markdown('<div class="card"><h3>Ledger</h3><div class="sub">Every operation this session, in order.</div>', unsafe_allow_html=True)
    if not st.session_state.log:
        st.markdown('<div class="ledger-empty">Nothing logged yet.</div>', unsafe_allow_html=True)
    else:
        rows = '<div class="ledger">'
        for entry in st.session_state.log:
            rows += (
                '<div class="ledger-row">'
                f'<span class="ledger-time">{entry["time"]}</span>'
                f'{stamp(entry["ok"])}'
                f'<span>{entry["action"]} — {entry["target"]}'
                + (f' <span style="color:var(--text-dim)">({entry["detail"]})</span>' if entry["detail"] else "")
                + "</span></div>"
            )
        rows += "</div>"
        st.markdown(rows, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)