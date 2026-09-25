import streamlit as st
import pandas as pd
import math
import os
import json
import hashlib
import base64
from pathlib import Path
from datetime import date
from fpdf import FPDF
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import numpy as np
import requests as _req
import secrets as _sec
try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_OK = True
except ImportError:
    CANVAS_OK = False


# ─── NOVALINK BRAND ──────────────────────────────────────────────────────────
SYCOMMS_LOGO_B64 = "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"
st.set_page_config(
    page_title="Quotation Tool",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── EARLY CONFIG LOAD (needed for branding before login renders) ────────────
def _early_load_branding():
    """Minimal config load just to get branding for the login screen."""
    try:
        if Path("config.json").exists():
            with open("config.json") as _f:
                _c = json.load(_f)
            return _c.get("branding", {})
    except Exception:
        pass
    return {}

_early_brand = _early_load_branding()
_CO       = _early_brand.get("company_name",    "SY Comms")
_CO_LEGAL = _early_brand.get("company_legal",   "SY Comms Ltd")
_CO_TAG   = _early_brand.get("company_tagline", "SY Comms Pricing Tool")
_CO_CAP   = _early_brand.get("login_caption",   f"Authorised {_CO} users only.")
_CO_FOOT  = _early_brand.get("pdf_footer",      "SY Comms | All figures exclude VAT | This document is confidential")
_CO_PKG   = _early_brand.get("customer_pkg_label", "Your SY Comms Package")
_CO_FILE  = _early_brand.get("proposal_filename_prefix", "SYComms_Proposal")


# ─── MULTI-BRAND CONFIG ───────────────────────────────────────────────────────
BRAND_CONFIGS = {
    "SY Comms": {
        "name":       "SY Comms",
        "legal":      "SY Comms Ltd",
        "tagline":    "SY Comms Quotation Tool",
        "caption":    "Authorised SY Comms users only.",
        "footer":     "SY Comms | All figures exclude VAT | This document is confidential",
        "pkg_label":  "Your SY Comms Package",
        "file_prefix":"SYComms_Proposal",
        "accent":     "#00b5a3",
        "logo_key":   "SYCOMMS_LOGO_B64",
        "header":     "<span style=\'color:#00b5a3\'>SY</span>&middot;COMMS",
        "pw_key":     "APP_PASSWORD",
        "address":    "Suite C Jupiter House, Sitka Drive, Shrewsbury Business Park, Shrewsbury SY2 6LG",
        "email":      "hello@sycomms.co.uk",
        "phone":      "01743 667419",
        "website":    "www.sycomms.co.uk",
        "about":      "SY Comms is a locally owned and operated telecoms and IT services company ",
    },
    "SY Plus": {
        "name":       "SY Plus",
        "legal":      "SY Plus Ltd",
        "tagline":    "SY Plus Quotation Tool",
        "caption":    "Authorised SY Plus users only.",
        "footer":     "SY Plus | All figures exclude VAT | This document is confidential",
        "pkg_label":  "Your SY Plus Package",
        "file_prefix":"SYPlus_Proposal",
        "accent":     "#0084c8",
        "logo_key":   None,
        "header":     "<span style=\'color:#0084c8\'>SY</span>&middot;PLUS",
        "pw_key":     "APP_PASSWORD_SYPLUS",
        "address":    "Suite C Jupiter House, Sitka Drive, Shrewsbury Business Park, Shrewsbury SY2 6LG",
        "email":      "hello@syplus.co.uk",
        "phone":      "01743 667419",
        "website":    "www.syplus.co.uk",
        "about":      "SY Plus is a locally owned and operated telecoms and IT services company ",
    },
    "SW Comms": {
        "name":       "SW Comms",
        "legal":      "SW Comms Ltd",
        "tagline":    "SW Comms Quotation Tool",
        "caption":    "Authorised SW Comms users only.",
        "footer":     "SW Comms | All figures exclude VAT | This document is confidential",
        "pkg_label":  "Your SW Comms Package",
        "file_prefix":"SWComms_Proposal",
        "accent":     "#e67e22",
        "logo_key":   None,
        "header":     "<span style=\'color:#e67e22\'>SW</span>&middot;COMMS",
        "pw_key":     "APP_PASSWORD_SWCOMMS",
        "address":    "Suite C Jupiter House, Sitka Drive, Shrewsbury Business Park, Shrewsbury SY2 6LG",
        "email":      "hello@swcomms.co.uk",
        "phone":      "01743 667419",
        "website":    "www.swcomms.co.uk",
        "about":      "SW Comms is a locally owned and operated telecoms and IT services company ",
    },
}

# ─── APP LOGIN GATE ──────────────────────────────────────────────────────────
# Brand passwords — add to Streamlit secrets:
#   APP_PASSWORD         = "..."   (SY Comms)
#   APP_PASSWORD_SYPLUS  = "..."   (SY Plus)
#   APP_PASSWORD_SWCOMMS = "..."   (SW Comms)
# Falls back to hardcoded default if secret not set.
_FALLBACK_PW = "SYComms2026!!"

def _get_brand_pw(pw_key):
    try:
        return st.secrets[pw_key]
    except Exception:
        return _FALLBACK_PW

if "app_authenticated" not in st.session_state:
    st.session_state.app_authenticated = False
if "selected_brand" not in st.session_state:
    st.session_state.selected_brand = "SY Comms"

if not st.session_state.app_authenticated:
    _sel_brand = st.session_state.selected_brand
    _bc        = BRAND_CONFIGS[_sel_brand]
    _accent    = _bc["accent"]
    _logo_src  = f'data:image/jpeg;base64,{SYCOMMS_LOGO_B64}'
    _logo_html = (f'<img src="{_logo_src}" style="width:90px;margin-bottom:0.8rem;border-radius:8px;"><br>'
                  if _bc["logo_key"] else '')

    login_html = (
        '<style>'
        '.login-wrap{max-width:440px;margin:4vh auto 0;background:linear-gradient(160deg,#1f1450 0%,#2d1f6e 100%);border-radius:20px;padding:2.5rem 2.5rem 2rem;box-shadow:0 20px 60px rgba(0,0,0,0.4);text-align:center;border:1px solid rgba(0,181,163,0.2)}.'
        'login-wrap h1{font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#fff;margin:0 0 0.2rem}.'
        'login-wrap p{color:rgba(255,255,255,0.45);font-size:0.85rem;margin:0 0 1.2rem}.'
        f'.login-accent{{color:{_accent}}}</style>'
        f'<div class="login-wrap">{_logo_html}'
        f'<h1>{_bc["header"]}</h1>'
        f'<p>{_bc["tagline"]}</p></div>'
    )
    st.markdown(login_html, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown("###")
        # Brand selector
        brand_choice = st.selectbox(
            "Company", list(BRAND_CONFIGS.keys()),
            index=list(BRAND_CONFIGS.keys()).index(_sel_brand),
            key="brand_selector",
            label_visibility="collapsed",
        )
        if brand_choice != _sel_brand:
            st.session_state.selected_brand = brand_choice
            st.rerun()

        entered = st.text_input("", type="password",
                                placeholder=f"Enter {brand_choice} password...",
                                label_visibility="collapsed",
                                key="login_pw_input")
        if st.button("Sign In →", use_container_width=True, type="primary"):
            _correct_pw = _get_brand_pw(_bc["pw_key"])
            if entered == _correct_pw:
                st.session_state.app_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password - please try again.")
        st.markdown("")
        st.caption(_bc["caption"])

    st.stop()   # ← nothing below renders until authenticated

# ─── CONFIG SYSTEM ───────────────────────────────────────────────────────────
CONFIG_FILE = "config.json"
_DEFAULT_PWD_HASH = hashlib.sha256(b"araconnect").hexdigest()

def _default_config():
    return {
        "meta": {"version": "1.0", "password_hash": _DEFAULT_PWD_HASH},
        "email": {
            "smtp_host":    "smtp.office365.com",
            "smtp_port":    587,
            "username":     "sales@sycomms.co.uk",
            "password":     "ltvkqbxtjukvrzdm",
            "from_name":    "SY Comms",
            "reply_to":     "sales@sycomms.co.uk",
        },
        "branding": {
            "company_name":    "SY Comms",
            "company_legal":   "SY Comms Ltd",
            "company_tagline": "SY Comms Quotation Tool",
            "login_caption":   "Authorised SY Comms users only.",
            "pdf_footer":      "SY Comms | All figures exclude VAT | This document is confidential",
            "customer_pkg_label": "Your SY Comms Package",
            "proposal_filename_prefix": "SYComms_Proposal",
        },
        "handsets_desktop": [
            {"name": "Grandstream GRP2612W",      "buy": 42.00,  "poe": True,  "cat": "Desktop"},
            {"name": "Grandstream GRP2615",       "buy": 95.00,  "poe": True,  "cat": "Desktop"},
            {"name": "Grandstream GRP2650",       "buy": 98.00,  "poe": True,  "cat": "Desktop"},
            {"name": "Grandstream GXV3350",       "buy": 130.00, "poe": True,  "cat": "Desktop"},
            {"name": "Grandstream GXV3470",       "buy": 223.00, "poe": True,  "cat": "Desktop"},
            {"name": "Grandstream GXV3480",       "buy": 243.00, "poe": True,  "cat": "Desktop"},
            {"name": "Yealink T88 Pro",           "buy": 239.00, "poe": True,  "cat": "Desktop"},
            {"name": "Grandstream WP836 (Wi-Fi)", "buy": 88.00,  "poe": False, "cat": "Desktop"},
        ],
        "handsets_cordless": [
            {"name": "Grandstream DP720",              "buy": 35.00, "bogof": False, "cat": "DECT"},
            {"name": "Grandstream DP735 (Rugged)",     "buy": 59.00, "bogof": False, "cat": "DECT"},
            {"name": "Grandstream Dect Base Station",  "buy": 34.00, "bogof": False, "cat": "DECT"},
            {"name": "Grandstream DP760 Repeater",     "buy": 70.00, "bogof": False, "cat": "DECT"},
        ],
        "headsets": [
            {"name": "Poly Blackwire 3210 (Mono, Wired)",   "buy": 19.54},
            {"name": "Poly Blackwire 3220 (Stereo, Wired)", "buy": 29.31},
            {"name": "Yealink WH62 (Mono, Wireless)",       "buy": 97.39},
            {"name": "Yealink WH62 (Stereo, Wireless)",     "buy": 115.99},
        ],
        "other_hardware": [
            {"name": "GWN7660 WiFi AP (WiFi6)",      "buy": 58.00},
            {"name": "GWN7664E Outdoor WiFi AP",     "buy": 95.00},
            {"name": "GWN7604 Compact Switch",       "buy": 44.00},
            {"name": "Grandstream 4 Port ATA",       "buy": 80.00},
            {"name": "Grandstream 8 Port ATA",       "buy": 117.00},
            {"name": "Grandstream 24 Port ATA",      "buy": 300.00},
            {"name": "Door Entry System",            "buy": 55.00},
            {"name": "Intercom System",              "buy": 90.00},
            {"name": "PBX Unit",                     "buy": 150.00},
            {"name": "Loud Speaker",                 "buy": 140.00},
            {"name": "CAT5 Socket & Cabling (ea)",   "buy": 65.00},
            {"name": "Broadband Router",             "buy": 65.00},
            {"name": "Bluetooth Headset",            "buy": 110.00},
            {"name": "Conference Unit (GAC250)",       "buy": 130.00, "sell": 390.00},
            {"name": "Call Scope AI Setup (one-off)",  "buy": 1000.00,"sell": 2500.00},
            {"name": "Call Answer (500 mins)",            "buy": 100.00, "sell": 149.00},
            {"name": "Website Widget",                    "buy": 30.00,  "sell": 50.00},
            {"name": "Call Scope Platform Setup",         "buy": 300.00, "sell": 500.00},
            {"name": "TP Link NX200 (4G/5G Standalone)",  "buy": 210.00, "sell": 630.00},
            {"name": "HIK Vision Turret 8MP",          "buy": 125.00, "sell": 427.50},
            {"name": "HIK Vision Dome 8MP",            "buy": 125.00, "sell": 400.00},
            {"name": "HIK Vision 24TB NVR",            "buy": 750.00, "sell": 1875.00},
        ],
        "switches": [
            {"name": "5-Port (4x POE)",   "buy": 29.00,  "poe_ports": 4,  "total_ports": 5},
            {"name": "8-Port (4x POE)",   "buy": 34.00,  "poe_ports": 4,  "total_ports": 8},
            {"name": "8-Port (8x POE)",   "buy": 57.00,  "poe_ports": 8,  "total_ports": 8},
            {"name": "16-Port (8x POE)",  "buy": 80.00,  "poe_ports": 8,  "total_ports": 16},
            {"name": "16-Port (16x POE)", "buy": 152.00, "poe_ports": 16, "total_ports": 16},
            {"name": "24-Port (24x POE)", "buy": 172.00, "poe_ports": 24, "total_ports": 24},
            {"name": "48-Port (32x POE)", "buy": 344.00, "poe_ports": 32, "total_ports": 48},
        ],
        "routers": [
            {"name": "Grandstream GWN7062E (FTTP)", "buy": 65.00, "sell": 200.00},
            {"name": "Draytek Vigor 2927 (FTTP/SoGEA)", "buy": 195.00},
            {"name": "Draytek 2927LAC (FTTP/Leased Line)", "buy": 386.40},
            {"name": "Zyxel DX Series (FTTP)",          "buy": 64.95},
            {"name": "TP Link NX200 (4G/5G)",           "buy": 210.00},
        ],
        "lease_rates": [
            {"months": 24, "label": "2 Year (1+23)", "rate": 46.94},
            {"months": 36, "label": "3 Year (1+35)", "rate": 35.32},
            {"months": 48, "label": "4 Year (1+47)", "rate": 27.62},
            {"months": 60, "label": "5 Year (1+59)", "rate": 23.31},
            {"months": 72, "label": "6 Year (1+71)", "rate": 19.11},
            {"months": 84, "label": "7 Year (1+83)", "rate": 18.25},
        ],
        "broadband": [
            {"provider": "SY", "package": "FTTP 40/10 Unlimited",   "cost": 22.45, "sell": 35.00, "install": 100.00},
            {"provider": "SY", "package": "FTTP 80/20 Unlimited",   "cost": 29.00, "sell": 35.00, "install": 100.00},
            {"provider": "SY", "package": "FTTP 115/20 Unlimited",  "cost": 25.20, "sell": 35.00, "install": 100.00},
            {"provider": "SY", "package": "FTTP 160/30 Unlimited",  "cost": 26.48, "sell": 36.00, "install": 100.00},
            {"provider": "SY", "package": "FTTP 220/30 Unlimited",  "cost": 26.72, "sell": 37.00, "install": 100.00},
            {"provider": "SY", "package": "FTTP 330/50 Unlimited",  "cost": 34.66, "sell": 39.00, "install": 100.00},
            {"provider": "SY", "package": "FTTP 550/75 Unlimited",  "cost": 34.66, "sell": 45.00, "install": 100.00},
            {"provider": "SY", "package": "FTTP 1000/115 Unlimited","cost": 38.61, "sell": 55.00, "install": 100.00},
            {"provider": "SY", "package": "SOGEA 40/10 Unlimited",  "cost": 27.49, "sell": 30.00, "install": 122.50},
            {"provider": "SY", "package": "SOGEA 80/20 Unlimited",  "cost": 28.12, "sell": 32.00, "install": 122.50},
            {"provider": "SY", "package": "Leased Line / Other",    "cost": 0.00,   "sell": 0.00,  "install": 0.00},
        ],
        "constants": {
            "vc_cost_per_seat":    2.95,   # Professional Bundle buy cost per user/mo
            "vc_sell_per_seat":   12.00,   # Professional Bundle fixed sell price per user/mo
            "wallboard_sell":     99.00,   # Live HTML Wallboard sell price
            "wallboard_cost":      5.00,   # Live HTML Wallboard buy cost
            "default_service_uplift_pct": 40,
            "hw_uplift_pct":     200,      # SY Comms use 3x (200% uplift) on hardware
            "commission_unit_size": 4000,
            "commission_per_unit":  1000,
            "install_engineer":  450.00,   # On-site installation
            "install_remote":     50.00,   # Remote installation
        }
    }

def _load_config():
    """Load config from config.json, restore images into session state, merge defaults."""
    if Path(CONFIG_FILE).exists():
        try:
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
            # Restore product images into session state if saved in config
            if "product_images" in cfg:
                imgs = {k: base64.b64decode(v) for k, v in cfg.pop("product_images").items()}
                st.session_state.uploaded_images = imgs
            # Merge with defaults so new keys are always present
            defaults = _default_config()
            for k, v in defaults.items():
                if k not in cfg:
                    cfg[k] = v
            if "constants" in defaults:
                for k, v in defaults["constants"].items():
                    cfg.setdefault("constants", {}).setdefault(k, v)
            # Merge new hardware items from defaults into existing lists
            # (so newly added catalogue items appear even with old config.json)
            for hw_key in ("handsets_desktop", "handsets_cordless", "headsets", "other_hardware", "routers"):
                if hw_key in defaults and hw_key in cfg:
                    existing_names = {d["name"] for d in cfg[hw_key] if "name" in d}
                    for item in defaults[hw_key]:
                        if item.get("name") and item["name"] not in existing_names:
                            cfg[hw_key].append(item)
            return cfg
        except Exception:
            pass
    return _default_config()

def _cfg_to_json(cfg):
    return json.dumps(cfg, indent=2, default=str)

# Persist config and images in session state
if "active_config" not in st.session_state:
    st.session_state.active_config = _load_config()
if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False
if "consultant_unlocked" not in st.session_state:
    st.session_state.consultant_unlocked = False
if "c_desired_rental" not in st.session_state:
    st.session_state.c_desired_rental = 0.0
if "c_svc_disc" not in st.session_state:
    st.session_state.c_svc_disc = 0
if "c_svc_disc_w" not in st.session_state:
    st.session_state.c_svc_disc_w = 0
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = {}

cfg = st.session_state.active_config
C   = cfg["constants"]   # shorthand for constants dict
hw_uplift_override         = C.get("hw_uplift_pct", 50)          # from admin panel
hw_uplift_upfront_override = C.get("hw_uplift_upfront_pct", 20)  # upfront purchase uplift

# ── Early rental estimate so sidebar caption is never one-rerun stale ─────────
# Reads current widget values from session state BEFORE sidebar renders.
# Mirrors the P&L cos_ex formula; keeps sidebar in sync with termination cost etc.
def _early_rental_estimate():
    """Quick rental estimate using session-state widget values (no UI needed)."""
    _term     = float(st.session_state.get("q_termination", 0))
    _lease    = int(st.session_state.get("q_lease_term", 36))
    _lr_map   = {24: 46.94, 36: 39.45, 48: 31.00, 60: 26.26, 72: 21.90, 84: 20.58}
    _sr       = _lr_map.get(_lease, 39.45)
    # Use stored hw_buy/sell from previous run to avoid rebuilding catalogues
    _cos_full = float(st.session_state.get("_prev_cos_full", 0))
    _base     = float(st.session_state.get("_prev_base_rental", 0))
    if _base > 0 and _cos_full > 0:
        # Adjust previous rental by change in termination cost
        _prev_term = float(st.session_state.get("_prev_termination_cost", 0))
        _delta     = _term - _prev_term
        return round(_base + (_sr / 1000.0) * _delta, 2)
    return _base

_early_est = _early_rental_estimate()
if _early_est > 0:
    st.session_state["_prev_base_rental"] = _early_est
# Store current termination cost so next rerun can compute delta
st.session_state["_prev_termination_cost"] = float(st.session_state.get("q_termination", 0))
_no_switch = False  # default - overridden by sidebar switch radio button
switch_quantities = {}  # for manual multi-switch mode
cctv_turret_qty = cctv_dome_qty = cctv_nvr_qty = 0  # CCTV defaults
mobile_rows = []   # default - overridden by sidebar
# Current customer cost defaults (overridden by sidebar)
current_calls = current_lines = current_bb = current_system = 0.0
current_support = current_hosted = current_onhold = current_other = current_it = 0.0
current_mobile = current_total = 0.0
commission_pct      = C.get("commission_pct", 25)   # fallback %
commission_unit_size = C.get("commission_unit_size", 4000)  # £GP per unit
commission_per_unit  = C.get("commission_per_unit", 1000)   # £ per unit
# Override with appointment type rate if set
_appt_rates = {"Self Gen": 1000, "Base Deal": 600, "Acquisition": 500, "Telemarketer": 650}
commission_per_unit  = _appt_rates.get(st.session_state.get("q_appt_type", "Self Gen"), commission_per_unit)
B   = cfg.get("branding", {})     # shorthand for branding dict
# Branding helpers - refresh from full config (overrides early load)
# Apply selected brand overrides first, then let config.json further customise
_sb   = BRAND_CONFIGS.get(st.session_state.get("selected_brand", "SY Comms"), BRAND_CONFIGS["SY Comms"])
_CO       = _sb["name"]
_CO_LEGAL = _sb["legal"]
_CO_TAG   = _sb["tagline"]
_CO_CAP   = _sb["caption"]
_CO_FOOT  = _sb["footer"]
_CO_PKG   = _sb["pkg_label"]
_CO_FILE  = _sb["file_prefix"]
# Brand contact details shorthand (used throughout UI and PDFs)
_BRAND    = BRAND_CONFIGS.get(st.session_state.get("selected_brand", "SY Comms"), BRAND_CONFIGS["SY Comms"])
_CO_EMAIL = _BRAND["email"]
_CO_PHONE = _BRAND["phone"]
_CO_WEB   = _BRAND["website"]
_CO_ABOUT = _BRAND["about"]
# Let config.json further override ONLY for SY Comms (it's SY Comms-specific)
if st.session_state.get("selected_brand", "SY Comms") == "SY Comms":
    _CO       = B.get("company_name",                _CO)
    _CO_LEGAL = B.get("company_legal",               _CO_LEGAL)
    _CO_TAG   = B.get("company_tagline",             _CO_TAG)
    _CO_CAP   = B.get("login_caption",               _CO_CAP)
    _CO_FOOT  = B.get("pdf_footer",                  _CO_FOOT)
    _CO_PKG   = B.get("customer_pkg_label",          _CO_PKG)
    _CO_FILE  = B.get("proposal_filename_prefix",    _CO_FILE)

# Keys captured when saving a quote
QUOTE_KEYS = [
    "q_comp_name","q_comp_reg","q_biz_type","q_contact","q_phone",
    "q_dir_email","q_bill_email","q_address","q_employees",
    "q_deal_type","q_lease_term","q_install_type","q_num_sites",
    "q_bb_provider","q_bb_package","q_bb_care","q_second_fttp","q_ll_cost","q_ll_sell","q_ll_install",
    "q_bank_name","q_acc_holder","q_acc_no","q_sort_code",
    "q_bogof","q_darkweb","q_proactive","q_ooh","q_moh","q_website",
    "q_appt_type","q_svc_discount","c_svc_disc","cs_mypa","cs_website","cs_call_answer","cs_AI Integration - Portal","cs_AI Integration - CRM","cs_Manager Dashboard","cs_Call Score","cs_mins_AI Integration - Portal","cs_mins_AI Integration - CRM","sec_Bronze Security","sec_Silver Security","sec_Gold Security","q_termination","q_curr_calls","q_curr_lines","q_curr_bb","q_curr_system",
    "q_curr_support","q_curr_hosted","q_curr_onhold","q_curr_other",
    "q_rep_name","q_rep_position",
    "c_svc_disc",
]
# Hardware quantity keys added dynamically after catalogues load
def _hw_quote_keys():
    keys = []
    for n in HANDSETS_DESKTOP:  keys.append(f"desk_{n}")
    for n in HANDSETS_CORDLESS: keys.append(f"cord_{n}")
    for n in HEADSETS:          keys.append(f"hs_{n}")
    for n in OTHER_HARDWARE:    keys.append(f"oth_{n}")
    keys += ["standalone_softphones_key","wallboard_users_key",
             "auto_switch_key","manual_switch_key","router_type_key",
             "add_router_key","hw_fund_key","wired_ports_key"]
    return keys


# ─── BUNDLED PRODUCT IMAGES (base64 JPEG, embedded for zero-config deployment) ─
BUNDLED_IMAGES = {
    'Fanvil V66 Pro': ('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', 'jpeg'),
    'Fanvil V67': ('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', 'jpeg'),
    'Fanvil V62 Pro': ('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', 'jpeg'),
    'Fanvil V62W': ('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', 'jpeg'),
    'Yealink T85w': ('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', 'jpeg'),
    'Yealink T87w': ('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', 'jpeg'),
    'Linkvil W610W': ('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', 'jpeg'),
    'Linkvil W620W (Rugged)': ('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', 'jpeg'),
    'Yealink AX83H': ('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', 'jpeg'),
    'Yealink AX86R (Rugged)': ('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', 'jpeg'),
    'Yealink W57R (Rugged)': ('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', 'jpeg'),
    'Yealink W73H': ('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', 'jpeg'),
    'Yealink W70B (Base)': ('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', 'jpeg'),
# ─── NEW: PBX / Mobile App / CCTV product images ───
    '__CS_AI__': ('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', 'jpeg'),
    '__MYPA__': ('/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCADIAMgDASIAAhEBAxEB/8QAHAABAAICAwEAAAAAAAAAAAAAAAYHBAUCAwgB/8QASBAAAQMDAgMFBAYGBwYHAAAAAQACAwQFEQYhBxJBEzFRYXEIIoGRFBUyYqGxI0JDdLLRNjdScpLB4RYXJCdEolNVY4KUw/H/xAAbAQEAAgMBAQAAAAAAAAAAAAAAAQIDBAUGB//EADgRAAIBAgMFBQYEBgMAAAAAAAABAgMRBCExBRJBUWETInGBoSMyQpGx0QYUUsEVJFNikrJy4fD/2gAMAwEAAhEDEQA/AKyREWifdwiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIDPtdnuV2c9tqt9ZWujALxTwukLR4kAdy+19lulvB+n22tpcd/bU72fmF8tV4udpe91quFXROkADzTzOjLgD3HHRSOh4mawo3ZjvtTKOrZ+WUH/ECpy4mlVeKUvZKLXVtP6MhqKw266s15Aj1fpahnJ2NZbh9Gnb5kDZx8tlxqtCUd5p31mgbo26Ma3mfb5wI6uMf3dg8eYx4DKW5GP8/2btiYOHXWPzWnnYr5F21EEtNO+GojfHKxxa5jwQ5pHQg7grqUHQTvmgiIhIREQBERAEREAREQBERAEREAREQBERAEREBvtK6puemZZ5LUYAZ2hrxNC2QEA5HePNSMcSG1nuX/AEtp+4szu5tP2Evwc3+SjelrzQWiWd1xsdHd2ygBrahxHZ4zkgjqc/gpKLrw+u2GV9guFjkO3b0FSZ2g+Ja/p6BWTdtTj4ulSdRynQb/ALo2v6NS+RyFt0NqYEWqtn01cD9mnr3drTOO2wk72+pUcvtgvujrlA6rjlpZQeenqoH+4/wcx479vQjyW3uugJ30Mtz0nXQX+1x5LzTjlmhH34j73y/BdOkNavtdK60XunF205McS0cpyY/vRHva4eAPy7w8SlKc1Fyw0u0itYy95ebzv0lrzRvKO72viJDHbtUSRUGpGjkpLuBysnPSOcd2T0d/+GBX2z11iuk9uukDoKqF3K5p7iO8EHqMb5Gy3uuNLRWhtPdLLUmv07XE/RqnG7T1jeOjxv03wfAgSCzys4iabFlrXg6ptsTnW6oed6uIDJgcT3uG+P8ALclrk9SKVWOGiq1F+xeq/Q+a5JP3lw1WV0Vii5SMcx7mPa5rmnDmkYIK4qp207hERCQiIgCIiAIiIAiIgCIiAIiIAiIgCl+k+HepNURie3UPJSO7qmod2bD5jq74Aqb8D+G8V6Db/foO0t7SRTU7htO4HBc7xaCMY6nPQYN3XQ6ijudPHZYbQLWISJDUOeJGP6crWjBaNtvxCywp3V2eS2t+JPy9V4bC2clq3ounV/uUpDwAuxjzNeaFsmO5kb3D57KLXXhXeaeeoitVXbLzJBntYaGpBmjx4sOD8BlbHWutdS2KCr0Y24xPjo3mOWthY5kswd7xBJOw94jbwxkjvrm1GoFypfoT6hlUZGiN1PntA4nA5cHOd+7ZVlu6JG5gY7SnB1qtaNn7vdya5vRq64GTa7jddN3cVFDNPQV8Di1wwWuHi1wI3HkVN7tSUfECz1N8stNHS6jo2mS40EIw2oZ1njHj4j/P7Vv8Q+H1LrWwQ1lPE6mvscDXRSys5HP2H6OUfh1IPlkHzfYrpcNJ6mhrIA+GtopS2SN2xODhzHDwxkFTKO5k9DHhMbT2pB18P3a0NVz6PnF+jzN7w31BTU0lRp+/nn09dsRzA/sJO5szfAg4yfD0AWou9DctE6vkg7Qx11vnD45W5AcBu1w8iMbeZBWy4o2mkob7DcbQ3Fou8ArqYYxy832meRBzt0BCz9Zc2oNAae1Gfeq6VxtNY4bl3KOaJx8+XOc95Kr05G3CpDtIV4ruVcpJ/qtlfrk4vrY6uKlLBWVFv1VbY2x0N8iMr2DujqG7St+e+epJUDVh6ZP13ws1JaJPentcjLpTDqG/ZkHwHTzVeFQ+ZtbPbjGVB/A7eVrx9Gl4oIiKDoBERAEREAREQBERAEREBl19vrLf9HFdTSwGoibPF2jcc8bu5w8QcFYisLjGeefSUrQQx+n6Ut/7v9FXqlqzsauDruvRjUkrNhZdpopLldaOhhP6WqmZA31c4AfmsRSPhxIyLX2nXyEBor4ck/3gAi1MmIm6dKU46pN+h610xW2f6vfbrLUxuhtLvocrBsYXM2w75Hfrutbetf2C32S53CmuNPW/QQ1r2U7xIed/2Bsepzv5HwVIaa1VRaS1/q6kv8E8lvr5p6ecRbkHtHYOM7jDnb5zuuzUGjbLqmhoazht+leJGUstFsx8Lfe/Sycx5jk437sbdCs/aO2R88/gVGGIviZS3HZqVlZ3zab4cUirblW1Fyr562tldLUzvMkj3HJJPere9mu2fSrrdqmejpp6SKONvPKA5zJObLeUYPgcnpgKJai4VassjGPfbnVsTv1qHM2D5jHMPXGFk8ItfM0Pca5tfTzTUFU0B7IgOdsjc8pGcDG5B3656LFHuyW8er2lJY7Z84YFqTsrWfX7aHrNeXfaKs0du1vHWwM5WXGASvx/4jctd+HL8yr/AND6qo9YWQXO3xzRRiR0TmTABzXDB6EjqPmqg9qOSM1mnYhjtWsnc70JYB+IKzVLOFzxn4aVXDbUVGSs8014K/1RC60fWXBa3VDjzS2m6yUoz0jlaH/LmTRRFbw31xb379iyCui8i1+HfhslsBj4J3h7jhst3hjZ6hnMfwThoeTTWupHZ5BaSw+rnYCw8UexqZUKqXw1E1/lF/Vs+8E8zasqrf3tuFuqaVw8QWZ/yVfHI2Kn/Aof8zbW8nDY2TvcfIRPUBf9okeKjgjoUcsbVX9sH6z+yPiIiqdAIiIAiIgCIiAIiIAg7/JEQFga5H0/h7om6s37OCW3y/dMbvdHyyq/VhaOJv8Aw/1Fpwe9V0pF2o2nqWDEoHnynYDvyVXpVnzOfs/udpQfwyfyl3l9beQXZBM+CeOaJxbJG4Oa4dCDkFdaKpvtXyZPuKNNHdHUOsLe0Ciu7AJw39jVNGHsPrjIJ791JPZnq6KHVVxp6hoFbUU2Kd58GnL2+p90/wDtKg2jNUR2dlVbrtSG4WGuAbU0vNggjukYejx49fLYjfU+jqyCsp79w+rzeaankEoZA7s6uDG5a9nf3bbZz4YV4vPeR57F0ksJPAVnupq0ZcLcE3wa0z1WnFL1evMntDzWIahpqO00dPFcYueSumhYG8xfghrsfad3knzVs8TdZTWLScMtrpap9yuTC2maIzzQ5bkvcMZBbkbePxXny16D1PfZJKuopJaWnJ55q65OMLACd3Oc7c+ORkrLVlfuo83+GcGqEnjsRPdirpK9rvTzty5+BZXszX7DLjYHQPILjWsmaMtbkNaWu8O5uPioBxp1LFqTW9RJSP56OjaKWJwOQ7lJLnenMTv4ALvrr/bdI2assukKp1ZXVrQyvu2CxpaP2cI6Dcgu9cdMa/h3puC6VE93vbuw07awJayUjaQ9IW+LnHG3h6hY220onoKOFpUMVV2pNNJ5JcX1trdvJL0zMzWObLw80xYXkipqS+7VDD+rzjlj/wC0HvXKyg2rg7fqt+GyXithoovHljy9xHzIWh1Hc67W2sJKhkJdUVkrYqenb+q3ZrGflv45K3XFOeC3yWvSlBI2SnskJZM9vdJUv96U/Pbfu3Vb6s2VTlalh5+9J78ulnvf7WS6HZwi/wCDk1Len5DLdaZi0/8AqPHK0fmq+PmrDqSNPcIYKY5bXajqRO9vcRTRH3c+rsEeRKrxHwRuYL2lWrW4N2XhHL/a4REVTohERAEREAREQBERAEREBudI32o03qKhutKOZ1O/LmdHsIw5p9QStzxK0/Ba7jBdLOe0sN2aamjkAwG5PvRnwLTtjwx5qGqc6Gv9BLbp9K6oe4WSsfzw1HeaGfuEg+74j/VSs8jnYqEqVRYqmr2ykucenVarpdashMUb5pGRxMc+R5DWtaMkk9wA6pKx0cj2SMcx7XYLXDBBHQqQaisl30TqGJkrnRTxOE1LVwn3ZADkPY7qFKX1li4i4+tZaexapIx9MIxS1p+//Yf5934ALEzxu6o1YreptarO3W3LwzXgVmu6kqqiknbNSTSwTN+y+J5a5voRuFt9T6VvOmajs7xQyQtJwyYDmjePuuGx23/NaJQbcKlOvDeg04vzRLIuIur4owxuoLgWjq5/Mfmd1qLper1f5mNuNfW17ycNZJI5+D5NzgLJ0tebdZ31L7lYqW79o0CMVDy0RkHcjHf3jw7lIn8ULjSsczTtps1jBGO0o6UGQjzc7P5K2urOfKm6VT+Xw6vzyS9E36HCz8P309G2661qvqK1d7WSDNTUfdjj78+Z7vArA1pq1t3pqa02ak+rdO0RPYUgdlz3dZJD+s4/hk79Tg0dFqPW11PYsrbrWOIDpHEuDR5uOzR67KWR01g4duE1e+mv+qGbx0sZ5qWjd4vd+u4HoOvhsU4ZaGGctyqnWfaVeEVouvT/AJS8raH2xwM4d2IX65RtOpa6Mi10jwM0zCMGoeOhxnAP88RrQ+nptW6j7OpldHSR81TX1TztHGN3OJPU9y6Y2X3XuqOUdpXXSrdkk7BrR1P9lgHwUh1fdaHTlifo/TU7agOcHXW4M/6mQfs2/cb+fxJfQhqpBunF3rVNXwivsuHN3fO2h4hahZqPUctTSx9lboGNpqOHuDIWDDRjp1PkSo0iKG7nXo0Y0Kapw0WQREUGUIiIAiIgCIiAIiIAiIgCIiAm+mdY0/1U3T+rqZ9xsPNmJzXYnoz/AGoien3e78jzvvD6pbQm7aVqm3+yn9rTt/TReUkfeD8PkoKtjZbzcbHWCrtFZNSVA25onYz5EdR5FTfgznVMJOnJ1MLLdb1T91/Z9V5pm505rvUGn4DSU9UKigxyuoqxglhI8MHcD0wtpJqvSdyJdd9FwwSnvltlU6Ef4D7q5ya+oL1trHTVDcJTsaykJppyfEluzj5bLiKPhxX4MN1v1qce9tTTtnaPizdW6XNOcKak51aMoyerhfP/ABab80cPpfDY7/VupgfAVEX8lybqTRdAQ626NdVSg7SXGtc8D1Y3Yr6dLaG3I4gADwNomz+a+m28OKIk1F+vdzx+rR0Yhz8ZEz6ehW9CWXtZdLVF+yMC+8RL9dKT6FDLBa7d3Ckt0Ygjx4HG59CcL7prQFyulL9ZXOSOzWNmC+urfdBH3GndxPTGB0ys5mtbHZTnSmlaWOdvdWXN5qZfIhuwafRRbUWpLvqOr+kXqumqngnlDjhrP7rRsFDa1eZnpUq27uYemqUebs5fJXV+rb8CU3nV9BZ7VNYdCxyU9HMOWruUoxUVfl9xnkN/TJzX6IobudDD4aGHTUdXq3q3zb/9bgERFBsBERAEREAREQBERAEREAREQBFvdJ6Vu2q6yamskLZpYY+0e10gZgZA6nfcrK1boa+6UpoKi90rIYp3mNjmytfkgZ6HbZTZ2uazxlBVewc1v8rq/wAiMIt1pXTV01TcJKKywNmqGRmVwc8NAaCBnJ2/WCz9WaEv+lKKGqvVLHDDLJ2bHNla/LsE4wM9AUs7XEsZQjVVFzW++F1f5EWREUGyMoizrLbKq83Smt9AwPqqh4ZG0uDQT6nYdyFZyUIuUnZIwUVi/wC5nWv/AJfB/wDKj/mtbfeGWrLLRvq6y1OdTsGXvgkbLyjxIByB54wrbr5GlDauCnJRjVi2+qIYidVNrFwx1TfLTTXK30MbqWoaXRudOxpIBIzglQk3obFfE0cNFSrSUV1diEou2ohkpp5YJmlksbixzT3tIO4+YK6lBmTvmgiIhIREQBERAEREAREQBERAXL7MX9KLv+5D+Nqm3Gbl1Bw3vEjWgzWm4YIHTldy/wAMmVCfZi/pRd/3IfxtU404WXm+cTdNSEYnmL2A+MkfIT82tWePu25ngNqez2rPEf09yXldJ/UiPs/sZaNOap1HMBiFghjJ8WtLiPiSxSP2k2tdpmytmfyMNeA5+M8o5HZOOvitHURHTvAC3UzwWVF1q4+0B2PvSc38LAFuvad/opav37/63JpCxF+22vTxH6pyS8IpL7lb8QOFtRpLT8V3Zc4q+nfK2M8kRZgOBIdnJyMgD4rA4acPKnXIuDoq1lHFScg5nxl/OXZ2G46D8Qrc0jL/ALd8Dai2vPaVlPA6l37+ePDoj8uT8ViaGlGieBdVeThlXVB88fjzvPJF8NgfiVXcV78Dce18XDDVKDleupqCdlx0dtODKEvtDHbbzW0MFQKqOmlfEJg3lD+UkZAzsNlv+Ev9Y+nv3pv5FRJxLiSSSSdypbwl/rH09+9N/IrGtUemxqawdRSd3uv6Fz8dNaX3SlXZ2WKqZA2ojkdIDE1+S0tx3g+JXbwM11edWSXWmvZjmdTNZIyZkYYRzEjlIG3TI+K3fE2v0VRz28a0pmTSuY805dC+TABHNuO7ooqOKuh9MWqWHSdve+R55hFDB2LHOxj33Hc+uCthu0rt5HgKNFYnZ0aFHCt1H8dklr+rwyKp1pp9r+KlfY7SxrRPXCOJre5nPg49ASfkvTX1pbtOXDTmmY24NVE+Kn3A5WxMB39f5qmOBVFUan4hXPU1yw99PzSk4wO2kyAB5BvN6bKXa/0bqq8cRKG/WmSiFNb+y+jtlmLSeU8zsjlOMkkemFWF0nJI3dryhXr08DiKiSpwzbes2sv2fzKt48WP6n4gVUsbOWnr2irZjuydn/HmBPxCrtemfaNsP1hpCG6xMzPbZQXHr2b8Aj/Fy/ivMyx1FaR6T8PYz83gYN6x7r8v+rBERUO4EREAREQBERAEREAREQFq+z5ebbZdQ3Oa7VtPRxSUnI10zw0E84ON/ILaaY1Vbbfx0vNe+407LXW9rH9JLx2ZGGuac93e3GfNUsispNJLkcevsalXq1aspP2kd19OvoXXx41Va7rPp+hstbS1FJTvdNKYHBzWnIDRt5ByzvaD1JZb3pu3Q2m6UlZKyr53NhkDiG8jhk49R81QyKXNu/Ux0dhUqPYOMn7K9uu9zLi9mu9/RNTVlolfiOui54wesjN/4S75Lce0ndYqWis2naPljjGal8TdgGgFjB6fa+SwuE960Bpmx0l1uU4ZqMMkbJ7sj3NBc7AaAOUEtxv/AKqs9e6jk1TqmtusgcyOVwbCx36kbRho9cfiSrb1oWuc6lgnidsyxO44xhzVk5LK65q2dyPKT8NKynoNeWSqrZmQU8VSHPlkdhrRg7kqMIsZ6ivSVanKm/iTXzLg9oe+2q91lkdaLhTVrYo5Q8wPDuXJbjOPHBVP9URJPedzBgMHHBYeOHg7qPPxueheFOotO6Q4bSST3WhddJBJVvphKDIXYwxmPHDRt4kqqXcStYFxP1/WjO+A4DH4KIZRS5NpI1KGxqFOrUrVFvubvmk7dEekdB64s9+4dy27WF6po62QS00xqpA172nPK7fydjPkvOdTEIKmWISNkDHFoew5a7BxkHw8F1ZRJScrGTA7Mp4GpUnSeU3e3BeAREVTphERAEREAREQBERAEREAREQBERAMoiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiA//Z', 'jpeg'),
    '__GWN7062E__': ('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', 'jpeg'),
    '__CS_DASH__': ('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', 'jpeg'),
    '__CS_LOGO__': ('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', 'jpeg'),
# Paste these lines inside your existing BUNDLED_IMAGES = { ... } dict,
# just above the closing '}'. Keys match the exact product names used
# in other_quantities / the Customer View cards, so they'll be picked up
# automatically by get_product_image_b64() - no other code changes needed.

    'PBX Unit': ('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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH/2Q==', 'jpeg'),
    'Mobile App / Softphone Users': ('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', 'jpeg'),
    'HIK Vision Turret 8MP': ('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', 'jpeg'),
    'HIK Vision Dome 8MP': ('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', 'jpeg'),
    'HIK Vision 24TB NVR': ('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', 'jpeg'),}

# ─── PRODUCT IMAGE MAPPING ───────────────────────────────────────────────────
# Place product images in an "images/" subfolder in the repo.
# Filenames below - add matching files to unlock real photos.
PRODUCT_IMAGES = {
    # ── Switches ─────────────────────────────────────────────────────────────
    "Switch: 5-Port (4x POE)":       "images/switch_5port.jpg",
    "Switch: 8-Port (4x POE)":       "images/switch_8port_4poe.jpg",
    "Switch: 8-Port (8x POE)":       "images/switch_8port_8poe.jpg",
    "Switch: 16-Port (8x POE)":      "images/switch_16port_8poe.jpg",
    "Switch: 16-Port (16x POE)":     "images/switch_16port_16poe.jpg",
    "Switch: 24-Port (24x POE)":     "images/switch_24port.jpg",
    "Switch: 48-Port (32x POE)":     "images/switch_48port.jpg",
    # ── Routers ──────────────────────────────────────────────────────────────
    "Draytek Vigor 2927 (FTTP/SoGEA)":      "images/draytek_vigor_2927.jpg",
    "Draytek 2927LAC (FTTP/Leased Line)":   "images/draytek_2927lac.jpg",
    "Zyxel DX Series (FTTP)":               "images/zyxel_dx.jpg",
    "TP Link NX200 (4G/5G)":                "images/tplink_nx200.jpg",
    # ── Software add-ons ──────────────────────────────────────────────────────
    "Mobile App / Softphone Users":  "images/mobile_app.jpg",
    "SY Comms Studio":               "images/sy_comms_studio.jpg",
    "Call Recording":                "images/call_recording.jpg",
    "Call Scope AI Agent":               "images/crm_ai.jpg",
    "ACD Light Agent":               "images/acd_light.jpg",
    "Click to Dial":                 "images/teams_integration.jpg",
    "HTML Wallboard":                "images/html_wallboard.jpg",
    # ── Grandstream Desktop ───────────────────────────────────────────────────
    "Grandstream GRP2601P":    "images/grp2601p.jpg",
    "Grandstream GRP2602P":    "images/grp2602p.jpg",
    "Grandstream GRP2603P":    "images/grp2603p.jpg",
    "Grandstream GRP2615":     "images/grp2615.jpg",
    "Grandstream GRP2616":     "images/grp2616.jpg",
    "Grandstream GXV3350":     "images/gxv3350.jpg",
    "Grandstream GXV3470":     "images/gxv3470.jpg",
    "Grandstream GXV3480":     "images/gxv3480.jpg",
    # ── Grandstream DECT ──────────────────────────────────────────────────────
    "Grandstream DP720":        "images/dp720.jpg",
    "Grandstream DP722":        "images/dp722.jpg",
    "Grandstream DP730":        "images/dp730.jpg",
    "Grandstream DP750 (Base)": "images/dp750.jpg",
    "Grandstream DP752 (Base)": "images/dp752.jpg",
    "Poly Blackwire 3210 (Mono, Wired)":   "images/poly_bw3210.jpg",
    "Poly Blackwire 3220 (Stereo, Wired)": "images/poly_bw3220.jpg",
    "Yealink WH62 (Mono, Wireless)":       "images/yealink_wh62_mono.jpg",
    "Yealink WH62 (Stereo, Wireless)":     "images/yealink_wh62_stereo.jpg",
}

PRODUCT_ICONS = {
    "Desktop":    "🖥️",
    "Conference": "🎙️",
    "Wi-Fi":      "📶",
    "DECT":       "📞",
    "Wired":      "🎧",
    "Wireless":   "🎧",
}

def _norm(s):
    """Normalise a string for fuzzy image matching."""
    return "".join(c for c in s.lower() if c.isalnum())

def _image_alias(name):
    """Map product/service names to a shared bundled image.
    Order matters - most specific rules first."""
    n = (name or "").lower()
    if "my pa" in n:                              return "__MYPA__"      # Call Answer - My PA (any bundle)
    if "gwn7062e" in n:                           return "__GWN7062E__"  # Grandstream GWN7062E router
    if "manager dashboard" in n:                  return "__CS_DASH__"   # Call Scope Manager Dashboard
    if "ai integration" in n or "call scope ai" in n:
        return "__CS_AI__"                                            # AI Portal / AI CRM / minutes / AI setup
    if "call scope" in n or "call score" in n or "website widget" in n:
        return "__CS_LOGO__"                                          # everything else Call Scope
    return None


def get_product_image_b64(name):
    """Return (b64_data, ext) - checks bundled, then session upload, then images/ dir."""
    # 1. Bundled images - exact name first, then shared alias images
    if name in BUNDLED_IMAGES:
        return BUNDLED_IMAGES[name]
    _alias = _image_alias(name)
    if _alias and _alias in BUNDLED_IMAGES:
        return BUNDLED_IMAGES[_alias]
    # 2. Session-state uploaded images (fuzzy match)
    name_norm = _norm(name)
    best, best_score = None, 0
    for key, data in st.session_state.get("uploaded_images", {}).items():
        if name_norm in key or key in name_norm:
            score = len(key) / max(len(name_norm), 1)
            if score > best_score:
                best, best_score = (data, "jpeg"), score
    if best and best_score > 0.4:
        b64 = base64.b64encode(best[0]).decode()
        return b64, best[1]
    # 3. Explicit PRODUCT_IMAGES dict path
    img_path = PRODUCT_IMAGES.get(name)
    if img_path and Path(img_path).exists():
        try:
            with open(img_path, "rb") as f_:
                b64 = base64.b64encode(f_.read()).decode()
            return b64, img_path.rsplit(".", 1)[-1]
        except Exception:
            pass
    # 4. Auto-scan images/ directory with fuzzy name matching
    #    Matches any file whose name contains a key word from the product name
    img_dir = Path("images")
    if img_dir.exists():
        name_words = [w.lower() for w in name.replace("-","").replace("(","").replace(")","").split() if len(w) > 2]
        best_file, best_hits = None, 0
        for f_ in img_dir.iterdir():
            if f_.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                fname_lower = f_.stem.lower()
                hits = sum(1 for w in name_words if w in fname_lower)
                if hits > best_hits:
                    best_file, best_hits = f_, hits
        if best_file and best_hits >= 1:
            try:
                with open(best_file, "rb") as f_:
                    b64 = base64.b64encode(f_.read()).decode()
                return b64, best_file.suffix.lstrip(".")
            except Exception:
                pass
    return None, None

def product_card_html(name, info, qty=0, show_qty=False, img_height=80):
    """Render a product card - real image if available, styled placeholder if not."""
    b64, ext = get_product_image_b64(name)
    if b64:
        img_html = f'<img src="data:image/{ext};base64,{b64}" style="width:100%;height:{img_height}px;object-fit:contain;border-radius:6px;margin-bottom:4px;">' 
    else:
        cat = info.get("cat", "Desktop")
        icon = PRODUCT_ICONS.get(cat, "📱")
        img_html = f'<div style="height:{img_height}px;background:linear-gradient(135deg,#2d1f6e,#3b2882);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:4px">{icon}</div>'
    
    qty_badge = f'<div style="background:#00b5a3;color:white;border-radius:10px;padding:1px 7px;font-size:0.7rem;font-weight:700;display:inline-block">x{qty}</div>' if show_qty and qty > 0 else ""
    return f"""
    <div style="border:1px solid #e8e8f0;border-radius:10px;padding:8px;background:#fff;text-align:center">
      {img_html}
      <div style="font-size:0.72rem;font-weight:600;color:#333;line-height:1.2">{name}</div>
      {qty_badge}
    </div>"""

# ─── FULL PRODUCT CATALOGUE (from Excel NEW MECHANICS sheets) ────────────────

# ─── PRODUCT CATALOGUES - loaded from config (editable via Admin Panel) ────────
def _build_catalogues(cfg):
    hd = {i["name"]: {k:v for k,v in i.items() if k!="name"} for i in cfg["handsets_desktop"]}
    hc = {i["name"]: {k:v for k,v in i.items() if k!="name"} for i in cfg["handsets_cordless"]}
    hs = {i["name"]: {"buy": i["buy"]}                         for i in cfg["headsets"]}
    oh = {i["name"]: {"buy": i["buy"], "sell": i.get("sell", i["buy"]*3)} for i in cfg["other_hardware"]}
    sw = cfg["switches"]
    rt = {i["name"]: i["buy"]                                  for i in cfg["routers"]}
    lr  = {i["months"]: i["rate"]                              for i in cfg["lease_rates"]}
    ltr = {i["months"]: i.get("true_rate", i["rate"]*0.8)     for i in cfg["lease_rates"]}
    ll  = {i["months"]: i["label"]                             for i in cfg["lease_rates"]}
    bb = {}
    for row in cfg["broadband"]:
        bb.setdefault(row["provider"], {})[row["package"]] = {
            "cost": row["cost"], "sell": row.get("sell", 0), "install": row["install"]
        }
    # "None / Customer Supplied" - zero cost/sell, appears first in selector
    bb["None / Customer Supplied"] = {
        "Customer keeps existing broadband": {"cost": 0.0, "sell": 0.0, "install": 0.0}
    }
    return hd, hc, hs, oh, sw, rt, lr, ltr, ll, bb

HANDSETS_DESKTOP, HANDSETS_CORDLESS, HEADSETS, OTHER_HARDWARE, SWITCHES, ROUTERS, LEASE_RATES, TRUE_LEASE_RATES, LEASE_TERM_LABELS, BROADBAND = _build_catalogues(cfg)

MOBILE_NETWORKS = {
    "EE": {
        "EE Unlimited Voice & Data":  {"cost": 7.88,  "sell": 15.00},
        "EE Data Only (Unlimited)":   {"cost": 10.35, "sell": 20.00},
    },
    "Three": {
        "3 Unlimited Voice & Data":   {"cost": 4.73,  "sell": 15.00},
        "3 Data Only (Unlimited)":    {"cost": 4.28,  "sell": 10.00},
    },
    "Vodafone": {
        "Vodafone Unlimited V&D":     {"cost": 17.00, "sell": 22.00},
        "Vodafone Data Only":         {"cost": 17.00, "sell": 22.00},
    },
    "O2": {
        "O2 Unlimited Voice & Data":  {"cost": 10.80, "sell": 15.00},
        "O2 Data Only (300GB)":       {"cost": 11.25, "sell": 15.00},
    },
}

_IT_SERVICES_DEFAULT = {
    "Microsoft 365": {
        "M365 Business Premium":             {"cost": 17.24},
        "M365 Business Standard + Copilot":  {"cost": 18.47},
        "M365 Business Premium + Copilot":   {"cost": 25.10},
    },
    "Exclaimer": {
        "Exclaimer Starter":  {"cost": 0.60},
        "Exclaimer Standard": {"cost": 0.71},
        "Exclaimer Pro":      {"cost": 0.73},
    },
    "Support": {
        "Support (per user)": {"cost": 25.00, "sell": 35.00},
    },
}
IT_SERVICES = st.session_state.active_config.get("it_services", _IT_SERVICES_DEFAULT)

IT_UPLIFT_PCT = 15.0  # % markup on cost price

HARDWARE_FUNDS = {"Bronze": 500, "Silver": 1000, "Gold": 1500}
SERVICE_UPLIFT = 0.40

# ─── STYLING ─────────────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  .main-header {
    background: linear-gradient(135deg, #1f1450 0%, #2d1f6e 50%, #3b2882 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
  }
  .main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,181,163,0.15) 0%, transparent 70%);
    pointer-events: none;
  }
  .main-header h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
  }
  .main-header p {
    color: rgba(255,255,255,0.55);
    margin: 0.3rem 0 0;
    font-size: 0.95rem;
    font-weight: 300;
  }
  .brand-accent { color: #00b5a3; }

  .metric-card {
    background: #ffffff !important;
    border: 1px solid #e8e8f0 !important;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    color: #1f1450 !important;
  }
  .metric-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #666666 !important;
    margin-bottom: 0.4rem;
  }
  .metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #1f1450 !important;
    line-height: 1;
  }
  .metric-value.green { color: #00a854 !important; }
  .metric-value.red { color: #008078 !important; }
  .metric-value.amber { color: #f57c00 !important; }
  .metric-sub {
    font-size: 0.75rem;
    color: #888888 !important;
    margin-top: 0.3rem;
  }

  .section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #1f1450;
    margin: 1.5rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #f0f0f0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .override-badge {
    background: #fff3e0;
    border: 1px solid #ffb74d;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: #e65100;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .line-item-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f5f5f5;
    font-size: 0.9rem;
  }
  .line-item-name { color: #333; flex: 1; }
  .line-item-qty { color: #666; min-width: 40px; text-align: center; }
  .line-item-price { font-weight: 600; color: #1f1450; min-width: 90px; text-align: right; }

  .promo-tag {
    background: linear-gradient(90deg, #00b5a3, #009e8e);
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.15rem 0.5rem;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-left: 0.5rem;
  }

  .pat-good { color: #00a854 !important; }
  .pat-warn { color: #f57c00 !important; }
  .pat-bad  { color: #008078 !important; }

  .tab-content { padding: 1rem 0; }

  div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f1450 0%, #2d1f6e 100%);
  }
  div[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
  div[data-testid="stSidebar"] .stSelectbox label,
  div[data-testid="stSidebar"] .stNumberInput label,
  div[data-testid="stSidebar"] .stTextInput label,
  div[data-testid="stSidebar"] .stTextArea label { color: rgba(255,255,255,0.6) !important; font-size: 0.8rem !important; }
  div[data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #00b5a3 !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    padding-bottom: 0.4rem !important;
    margin-top: 1.2rem !important;
  }

  .stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
  }

  .stButton > button {
    background: linear-gradient(135deg, #00b5a3, #008078);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.6rem 1.5rem;
    width: 100%;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #33c4b5, #006058);
  }

  .stDownloadButton > button {
    background: linear-gradient(135deg, #1f1450, #2d1f6e);
    color: white !important;
    border: 1px solid rgba(0,181,163,0.4);
    border-radius: 8px;
    font-weight: 600;
    width: 100%;
  }

  .warning-box {
    background: #fff8e1;
    border-left: 4px solid #ffc107;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #5d4037;
    margin: 0.5rem 0;
  }
  .success-box {
    background: #e8f5e9;
    border-left: 4px solid #43a047;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #1b5e20;
    margin: 0.5rem 0;
  }
  .info-box {
    background: #e3f2fd;
    border-left: 4px solid #1976d2;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #0d47a1;
    margin: 0.5rem 0;
  }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
_show_logo = st.session_state.get("selected_brand", "SY Comms") == "SY Comms"
_logo_img  = (f'<img src="data:image/jpeg;base64,{SYCOMMS_LOGO_B64}" style="height:56px;border-radius:8px;flex-shrink:0;" alt="{_CO}"/>'
              if _show_logo else "")
st.markdown(f"""
<div class="main-header" style="display:flex;align-items:center;gap:1.2rem;">
  {_logo_img}
  <div>
    <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.7rem;color:#fff;line-height:1.1">
      {_BRAND["header"]}
    </div>
    <div style="color:rgba(255,255,255,0.5);font-size:0.88rem;margin-top:0.2rem">{_CO_TAG} &nbsp;·&nbsp; Build, price &amp; generate paperwork</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Apply any pending quote load (must happen before widgets render) ────────────
if "_pending_quote" in st.session_state:
    _pq = st.session_state.pop("_pending_quote")
    for _k, _v in _pq.items():
        st.session_state[_k] = _v
    st.session_state["_quote_ready"] = False

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
    # ── Appointment Type — affects commission rate ────────────────────────────
    APPT_RATES = {"Self Gen": 1000, "Base Deal": 600, "Acquisition": 500, "Telemarketer": 650}
    appt_type = st.selectbox(
        "📋 Appointment Type",
        list(APPT_RATES.keys()),
        key="q_appt_type",
        help="Sets commission rate per unit for this deal"
    )
    _appt_rate = APPT_RATES[appt_type]
    st.markdown("---")
    st.markdown("### 🏢 Customer Details")
    comp_name       = st.text_input("Company Name", placeholder="Acme Ltd", key="q_comp_name")
    comp_reg        = st.text_input("Company Reg. No.", placeholder="12345678", key="q_comp_reg")
    biz_type        = st.selectbox("Entity Type", ["Limited Company", "Sole Trader", "Partnership", "Other"], key="q_biz_type")
    contact_name    = st.text_input("Signatory Name & Position", placeholder="Jane Smith - Director", key="q_contact")
    company_phone   = st.text_input("Company Phone Number", key="q_phone")
    director_email  = st.text_input("Director's Email", key="q_dir_email")
    billing_email   = st.text_input("Billing Email", key="q_bill_email")
    install_address = st.text_area("Installation Address", height=80, key="q_address")
    num_employees   = st.number_input("No. of Employees", min_value=1, value=5, step=1, key="q_employees")

    st.markdown("### 📋 Deal Configuration")
    # Deal type derived from payment model selection below
    # (set after payment_model widget is rendered)
    lease_term = st.selectbox("Service Agreement Term", list(LEASE_TERM_LABELS.keys()),
                              format_func=lambda x: LEASE_TERM_LABELS[x], index=5, key="q_lease_term")
    install_type = st.selectbox("Installation Type", ["Engineer Install", "Remote Install", "Self Install"], key="q_install_type")
    payment_model = st.selectbox(
        "Hardware Payment Model",
        ["Lease (spread over contract term)", "Upfront Purchase (one-off payment)"],
        key="q_payment_model",
        help="Lease: hardware cost spread across monthly payments. Upfront: customer pays all hardware at start."
    )
    num_sites    = st.number_input("Number of Sites", min_value=1, value=1, key="q_num_sites")

    st.markdown("### 🌐 Broadband")
    _bb_providers = ["None / Customer Supplied"] + [k for k in BROADBAND.keys() if k != "None / Customer Supplied"]
    bb_provider  = st.selectbox("Provider", _bb_providers, key="q_bb_provider")
    bb_package   = st.selectbox("Package", list(BROADBAND[bb_provider].keys()), key="q_bb_package")
    if bb_provider != "None / Customer Supplied":
        bb_free_year = st.checkbox("\U0001f381 Free for first 12 months",
                                   key="q_bb_free_year",
                                   help="Shows £0/mo on customer docs then full price from month 13")
    else:
        bb_free_year = False
    # Bespoke price for Leased Line / Other
    if bb_package == "Leased Line / Other":
        _ll_col1, _ll_col2 = st.columns(2)
        with _ll_col1:
            ll_cost = st.number_input("Leased Line Cost (£/mo)", min_value=0.0, step=1.0,
                                      value=float(st.session_state.get("q_ll_cost", 0.0)),
                                      key="q_ll_cost", format="%.2f")
        with _ll_col2:
            ll_sell = st.number_input("Leased Line Sell (£/mo)", min_value=0.0, step=1.0,
                                      value=float(st.session_state.get("q_ll_sell", 0.0)),
                                      key="q_ll_sell", format="%.2f")
        ll_install = st.number_input("Install / Setup (£ one-off)", min_value=0.0, step=10.0,
                                     value=float(st.session_state.get("q_ll_install", 0.0)),
                                     key="q_ll_install", format="%.2f")
    else:
        ll_cost = ll_sell = ll_install = 0.0
    bb_care      = st.selectbox("Care Level", ["Standard (FOC)", "Business (+£8/mo)"], key="q_bb_care")
    second_fttp  = st.checkbox("Add 2nd Broadband Line", key="q_second_fttp")
    second_fttp_pkg = None
    if second_fttp:
        second_fttp_pkg = st.selectbox("2nd Line Package", list(BROADBAND[bb_provider].keys()), key="bb2")

    st.markdown("### 💰 Pricing Controls")
    def _sync_sidebar_to_cons():
        st.session_state["c_svc_disc"] = st.session_state["q_svc_discount"]
    service_discount_pct = st.slider(
        "Service Discount %", 0, 40,
        value=int(st.session_state.get("c_svc_disc", 0)),
        step=5,
        help="Syncs with Consultant tab. Floor protection keeps minimum 5% uplift on all items.",
        key="q_svc_discount", on_change=_sync_sidebar_to_cons
    )
    # Silent floor: effective uplift never drops below 5% regardless of discount level
    service_uplift_pct = max(40 - service_discount_pct, 5)

    st.markdown("")
    st.markdown("**Desired Lease Rental**")
    # Only sync from consultant side when flag is set
    if st.session_state.pop("_sync_rental_to_sidebar", False):
        st.session_state["q_sidebar_rental"] = float(
            st.session_state.get("c_desired_rental") or
            st.session_state.get("_prev_base_rental", 0.0))
    _sidebar_rental = st.number_input(
        "Target Rental (£/mo)",
        min_value=0.0,
        step=10.0,
        key="q_sidebar_rental",
        help="Enter target monthly rental, then click Apply. 0 = use calculated figure."
    )
    _sr_col1, _sr_col2 = st.columns(2)
    with _sr_col1:
        if st.button("✅ Apply", key="btn_apply_rental", use_container_width=True):
            st.session_state["c_desired_rental"]      = _sidebar_rental
            st.session_state["_sync_rental_to_cons"]  = True
            st.rerun()
    with _sr_col2:
        if st.button("✖ Clear", key="btn_clear_rental", use_container_width=True):
            st.session_state["c_desired_rental"]      = 0.0
            st.session_state["_sync_rental_to_cons"]  = True
            st.rerun()
    _active_rental = st.session_state.get("c_desired_rental", 0.0)
    _prev_units    = st.session_state.get("_prev_commission_units", 0.0)
    _calc_rental  = st.session_state.get("_prev_base_rental", 0.0)
    _true_rate_ss = st.session_state.get("_prev_true_rate", 0.0)
    _cos_full_ss  = st.session_state.get("_prev_cos_full", 0.0)
    # Compute units live from whatever rental is in the box right now
    _display_rental = _active_rental if _active_rental > 0 else _calc_rental
    if _true_rate_ss > 0:
        _live_units = ((_display_rental / _true_rate_ss) * 1000 - _cos_full_ss) / 4000
    else:
        _live_units = _prev_units
    if _active_rental > 0 and abs(_active_rental - _calc_rental) > 0.01:
        st.caption(f"Override: £{_active_rental:.2f}/mo  ·  ~{_live_units:.2f} units")
    else:
        st.caption(f"Calculated: £{_calc_rental:.2f}/mo  ·  ~{_live_units:.2f} units")

    st.markdown("### 🔒 Deal Adjustments (Internal Only)")
    termination_cost = st.number_input(
        "Buyout / Termination Cost (£)",
        min_value=0.0, value=0.0, step=50.0,
        key="q_termination",
        help="Cost to exit the customer's existing contract. Added to the lease spread - not shown to customer."
    )

    # SW Add-ons moved to Licences & Add-ons expander in right column

    with st.expander("📊 Current Customer Costs", expanded=False):
        st.caption("Fill in what the customer currently pays - used in the comparison view.")
        curr_col1, curr_col2 = st.columns(2)
        with curr_col1:
            current_bb      = st.number_input("Broadband / Lines (£/mo)", 0.0, step=5.0, key="q_curr_bb")
            current_system  = st.number_input("Phone System (£/mo)",      0.0, step=5.0, key="q_curr_system")
            current_calls   = st.number_input("Call Charges (£/mo)",      0.0, step=5.0, key="q_curr_calls")
            current_it      = st.number_input("IT Services / M365 (£/mo)", 0.0, step=5.0, key="q_curr_it")
        with curr_col2:
            current_hosted  = st.number_input("Hosted User Licences (£/mo)", 0.0, step=5.0, key="q_curr_hosted")
            current_mobile  = st.number_input("Mobile (£/mo)",            0.0, step=5.0, key="q_curr_mobile")
            current_support = st.number_input("Support / Maintenance (£/mo)", 0.0, step=5.0, key="q_curr_support")
            current_other   = st.number_input("Other / Misc (£/mo)",      0.0, step=5.0, key="q_curr_other")
        current_total = current_bb + current_system + current_calls + current_mobile + current_support + current_other + current_it + current_hosted

    st.markdown("### 🏦 Bank Details")
    bank_name  = st.text_input("Bank Name", key="q_bank_name")
    acc_holder = st.text_input("Account Holder", key="q_acc_holder")
    acc_no     = st.text_input("Account Number", max_chars=8, key="q_acc_no")
    sort_code  = st.text_input("Sort Code", max_chars=6, key="q_sort_code")

    # Promos removed - always recurring, no BOGOF or add-on promos



# Hardcoded values (features/promos removed - must stay defined for PDF/CV references)
# Current customer cost defaults (0 unless consultant fills in)

bogof_active    = False
dark_web_mon    = False
proactive_bb    = False
ooh_support     = False
music_on_hold   = False
website_promo   = False
rental_discount = 0.0
hw_fund         = "None"
is_recurring    = True
# Software add-on defaults (overridden by sidebar widgets above)
sw_studio_qty = sw_callrec_qty = sw_crm_qty = 0
_sw_studio_on = False
sw_acd_qty = 0
sw_ctd_qty = sw_wallboard_qty = 0

# ─── QUOTE SAVE / LOAD ───────────────────────────────────────────────────────
with st.expander("💾 Save / Load Quote", expanded=False):
    ql_col1, ql_col2, ql_col3 = st.columns(3)

    with ql_col1:
        st.markdown("**💾 Save current quote**")
        st.caption("Downloads a JSON file with all current inputs - share with manager or reload later.")
        if st.button("📥 Prepare Quote for Download", use_container_width=True, key="prep_save"):
            st.session_state["_quote_ready"] = True
        if st.session_state.get("_quote_ready"):
            snapshot = {k: st.session_state.get(k) for k in QUOTE_KEYS if k in st.session_state}
            # Also capture hardware quantities
            for n in list(HANDSETS_DESKTOP.keys()) + list(HANDSETS_CORDLESS.keys()):
                key = f"desk_{n}" if n in HANDSETS_DESKTOP else f"cord_{n}"
                if key in st.session_state:
                    snapshot[key] = st.session_state[key]
            for n in HEADSETS:
                if f"hs_{n}" in st.session_state: snapshot[f"hs_{n}"] = st.session_state[f"hs_{n}"]
            for n in OTHER_HARDWARE:
                if f"oth_{n}" in st.session_state: snapshot[f"oth_{n}"] = st.session_state[f"oth_{n}"]
            import json as _json
            quote_name = (st.session_state.get("q_comp_name") or "quote").replace(" ", "_")
            st.download_button(
                f"📥 Download quote - {quote_name}.json",
                data=_json.dumps(snapshot, indent=2, default=str),
                file_name=f"{quote_name}_{date.today()}.json",
                mime="application/json",
                use_container_width=True,
                key="dl_quote_btn"
            )

    with ql_col2:
        st.markdown("**📂 Load previous quote**")
        st.caption("Upload a previously saved quote JSON to restore all inputs.")
        _qu_key = f"quote_uploader_{st.session_state.get('_qu_reset', 0)}"
        loaded_quote_file = st.file_uploader("Upload quote JSON", type=["json"],
                                             key=_qu_key, label_visibility="collapsed")
        if loaded_quote_file:
            try:
                import json as _json
                q_data = _json.load(loaded_quote_file)
                # Store in temp key — applied BEFORE widgets render on next run
                # Increment reset counter to force file uploader to clear
                st.session_state["_qu_reset"] = st.session_state.get("_qu_reset", 0) + 1
                st.session_state["_pending_quote"] = q_data
                st.success(f"✅ Quote loaded — refreshing...")
                st.rerun()
            except Exception as e:
                st.error(f"Could not load quote: {e}")

    with ql_col3:
        st.markdown("**⚙️ Load config**")
        st.caption("Upload a config.json (downloaded from Admin panel) to restore pricing & catalogue.")
        loaded_cfg_file = st.file_uploader("Upload config JSON", type=["json"],
                                           key="cfg_uploader", label_visibility="collapsed")
        if loaded_cfg_file:
            try:
                import json as _json
                cfg_data = _json.load(loaded_cfg_file)
                if "product_images" in cfg_data:
                    imgs = {k: base64.b64decode(v) for k, v in cfg_data.pop("product_images").items()}
                    st.session_state.uploaded_images = imgs
                st.session_state.active_config = cfg_data
                n_imgs = len(st.session_state.get("uploaded_images", {}))
                st.success(f"✅ Config loaded! Pricing, catalogue and {n_imgs} image(s) restored.")
                st.rerun()
            except Exception as e:
                st.error(f"Could not load config: {e}")

# ─── HARDWARE BUILDER (main area) ────────────────────────────────────────────

st.markdown('<div class="section-header">📦 Hardware Builder</div>', unsafe_allow_html=True)

col_hw1, col_hw2 = st.columns([3, 2])

# ─── SYSTEM HARDWARE BUILDER ─────────────────────────────────────────────────
with col_hw1:
    st.markdown("**🖥️ System Desk Phones**")
    desktop_quantities = {}
    desk_cols = st.columns(3)
    for i, (name, info) in enumerate(HANDSETS_DESKTOP.items()):
        with desk_cols[i % 3]:
            st.markdown(product_card_html(name, info), unsafe_allow_html=True)
            qty = st.number_input(
                f"{'PoE ' if info['poe'] else ''}{name}",
                min_value=0, value=0, step=1, key=f"desk_{name}",
                label_visibility="collapsed"
            )
            if qty > 0:
                desktop_quantities[name] = qty

    # PBX fills the empty column after the last phone card
    _desk_count = len(HANDSETS_DESKTOP)
    _pbx_col_idx = _desk_count % 3  # which column position PBX lands in
    _pbx_col_idx = _desk_count % 3
    with desk_cols[_pbx_col_idx]:
        st.markdown(product_card_html("PBX Unit", {"buy": 150.0, "sell": 500.0, "cat": "Other"}),
                    unsafe_allow_html=True)
        pbx_qty = st.number_input("PBX Unit", min_value=0, value=0, step=1,
                                   key="oth_PBX Unit", label_visibility="collapsed")

    st.markdown("**📞 DECT & Wireless Phones**")
    cordless_quantities = {}
    cord_cols = st.columns(3)
    for i, (name, info) in enumerate(HANDSETS_CORDLESS.items()):
        with cord_cols[i % 3]:
            st.markdown(product_card_html(name, info), unsafe_allow_html=True)
            qty = st.number_input(
                name, min_value=0, value=0, step=1, key=f"cord_{name}",
                label_visibility="collapsed"
            )
            if qty > 0:
                cordless_quantities[name] = qty
with col_hw2:
    # ── PBX & CCTV - prominent quick-select ───────────────────────────────────
    st.markdown("<div style='margin-top:2.6rem'></div>", unsafe_allow_html=True)
    with st.expander("📹 CCTV, Security & Access", expanded=False):
        _cctv_col1, _cctv_col2, _cctv_col3 = st.columns(3)
        with _cctv_col1:
            cctv_turret_qty = st.number_input("HIK Vision Turret 8MP", min_value=0, value=0, step=1,
                                               key="cctv_turret", help="buy £125 / sell £427.50")
            cctv_dome_qty   = st.number_input("HIK Vision Dome 8MP",   min_value=0, value=0, step=1,
                                               key="cctv_dome",   help="buy £125 / sell £400.00")
            cctv_nvr_qty    = st.number_input("HIK Vision 24TB NVR",   min_value=0, value=0, step=1,
                                               key="cctv_nvr",    help="buy £750 / sell £1,875")
        with _cctv_col2:
            cctv_int_qty  = st.number_input("Intercom System", min_value=0, value=0, step=1,
                                             key="oth_Intercom System")
            cctv_spk_qty  = st.number_input("Loud Speaker", min_value=0, value=0, step=1,
                                             key="oth_Loud Speaker")
        with _cctv_col3:
            door_qty      = st.number_input("Door Entry System", min_value=0, value=0, step=1,
                                             key="oth_Door Entry System")
            cctv_mon_qty  = st.number_input("Monitor", min_value=0, value=0, step=1, key="cctv_monitor")

    with st.expander("🎧 Headsets", expanded=False):
        headset_quantities = {}
        for name, info in HEADSETS.items():
            qty = st.number_input(name, min_value=0, value=0, step=1, key=f"hs_{name}")
            if qty > 0:
                headset_quantities[name] = qty

    with st.expander("📦 Other Hardware (ATA, WiFi, Routers)", expanded=False):
        other_quantities = {}
        for name, info in OTHER_HARDWARE.items():
            # Skip items handled elsewhere:
            # - CCTV section: HIK Vision cameras/NVR
            # - Router section: Broadband Router (auto-added)
            # - CCTV section: Intercom, Loud Speaker, Door Entry
            # - Headsets section: Bluetooth Headset
            # - PBX: shown in desktop grid
            if name in (
                "PBX Unit",
                "Door Entry System", "Intercom System", "Loud Speaker",
                "HIK Vision Turret 8MP", "HIK Vision Dome 8MP", "HIK Vision 24TB NVR",
                "Broadband Router",
                "Call Scope AI Setup (one-off)",
                "Bluetooth Headset",
            ):
                continue
            qty = st.number_input(name, min_value=0, value=0, step=1, key=f"oth_{name}")
            if qty > 0:
                other_quantities[name] = qty

    # Merge quick-select system add-ons into other_quantities
    if pbx_qty > 0:     other_quantities["PBX Unit"] = pbx_qty
    if door_qty > 0:    other_quantities["Door Entry System"] = door_qty
    if cctv_int_qty > 0: other_quantities["Intercom System"] = cctv_int_qty
    if cctv_spk_qty > 0: other_quantities["Loud Speaker"] = cctv_spk_qty
    # CCTV cameras - merge into other_quantities with pricebook pricing
    if cctv_turret_qty > 0: other_quantities["HIK Vision Turret 8MP"] = cctv_turret_qty
    if cctv_dome_qty   > 0: other_quantities["HIK Vision Dome 8MP"]   = cctv_dome_qty
    if cctv_nvr_qty    > 0: other_quantities["HIK Vision 24TB NVR"]   = cctv_nvr_qty

    # Auto-add Broadband Router when BB is selected.
    # Key insight: the "Other Hardware" expander widgets only appear in session_state
    # once the expander is opened. So get("oth_Broadband Router", 1) returns 1 (not 0)
    # when the user has never opened the expander - meaning auto-add should fire.
    # If the user opened the expander and explicitly set it to 0, it returns 0 - skip auto-add.
    _router_user_val = st.session_state.get("oth_Broadband Router", 1)
    # Check via session state whether the router section will add a router
    _router_mode_val = st.session_state.get("router_mode", "Auto-select")
    _router_will_add = (
        (_router_mode_val == "Auto-select" and bb_provider != "None / Customer Supplied") or
        (_router_mode_val == "Manual select" and
         any(st.session_state.get(f"rt_qty_{rn}", 0) > 0 for rn in ROUTERS.keys()))
    )
    _bb_auto_router = (
        bb_provider != "None / Customer Supplied" and
        "Broadband Router" in OTHER_HARDWARE and
        "Broadband Router" not in other_quantities and
        _router_user_val != 0 and                        # 0 = user explicitly cleared it
        not _router_will_add and                         # skip if router section will add one
        _router_mode_val != "None / Customer Supplied"   # respect explicit "no router" choice
    )
    if _bb_auto_router:
        other_quantities["Broadband Router"] = 1

    # Auto-add Call Scope AI Setup fee when agent is selected
    if st.session_state.get("q_sw_crm", 0) > 0:
        if "Call Scope AI Setup (one-off)" not in other_quantities:
            other_quantities["Call Scope AI Setup (one-off)"] = 1
        # Ensure it's in the catalogue (may be missing from old config)
        if "Call Scope AI Setup (one-off)" not in OTHER_HARDWARE:
            OTHER_HARDWARE["Call Scope AI Setup (one-off)"] = {"buy": 1000.00, "sell": 2500.00}

    # Auto-add PBX Unit when total users >= 5 (pricebook rule)
    # total_voice_channels computed after this block - use desk phone count as proxy
    _desk_total = sum(desktop_quantities.values())
    _soft_total = st.session_state.get("standalone_softphones_key", 0)
    _total_users_preview = _desk_total + _soft_total
    if _total_users_preview >= 5 and "PBX Unit" not in other_quantities:
        other_quantities["PBX Unit"] = 1
        st.info("🔧 PBX Unit auto-added (required for 5+ users)")


    st.markdown("**🎙️ Licences & Add-ons**")
    wallboard_users = 0

    with st.expander("💻 Software Licences & Add-ons", expanded=False):
        st.caption("Optional Telepo features and softphone users")
        standalone_softphones = st.number_input(
            "📱 Mobile App / Softphone-Only Users",
            min_value=0, value=0, step=1,
            help="Users with no desk phone - mobile app or PC softphone. Each adds one hosted user licence.",
            key="standalone_softphones_key"
        )
        st.markdown("---")
        _sw_col1, _sw_col2 = st.columns(2)
        with _sw_col1:
            _sw_studio_on    = st.checkbox("SY Comms Studio  (£11.95/mo)", key="q_sw_studio")
            sw_studio_qty    = 1 if _sw_studio_on else 0
            sw_callrec_qty   = st.number_input("Call Recording",    0, 50, 0, key="q_sw_callrec", help="sell £1.50/user")
        with _sw_col2:
            sw_ctd_qty       = st.number_input("Click to Dial",     0, 50, 0, key="q_sw_ctd",    help="sell £3.75/user")
            sw_wallboard_qty = st.number_input("HTML Wallboard",    0, 10, 0, key="q_sw_wb",      help="sell £99.00/instance")
    SW_ADDONS = [
        ("SY Comms Studio",   sw_studio_qty,    4.50, 11.95),
        ("Call Recording",    sw_callrec_qty,   0.01,  1.50),
        ("Click to Dial",     sw_ctd_qty,       0.75,  3.75),
        ("HTML Wallboard",    sw_wallboard_qty, 5.00, 99.00),
    ]
    sw_sell_total = sum(qty * sell for _, qty, _, sell in SW_ADDONS if qty > 0)
    sw_cost_total = sum(qty * cost for _, qty, cost, _ in SW_ADDONS if qty > 0)

    with st.expander("🌐 Networking", expanded=False):
        _switch_mode = st.radio("Switch", ["Auto-select", "Manual select", "None / Customer Supplied"],
                                horizontal=True, key="switch_mode")
        if _switch_mode == "None / Customer Supplied":
            auto_switch = False; manual_switch_name = None; _no_switch = True
            switch_quantities = {}
        elif _switch_mode == "Auto-select":
            auto_switch = True; manual_switch_name = None; _no_switch = False
            switch_quantities = {}
        else:
            auto_switch = False
            _no_switch  = False
            manual_switch_name = None
            st.caption("Set quantities for each switch needed:")
            _sw_cols = st.columns(3)
            switch_quantities = {}
            for _si, _sw in enumerate(SWITCHES):
                with _sw_cols[_si % 3]:
                    _sq = st.number_input(_sw["name"], min_value=0, value=0, step=1,
                                          key=f"sw_qty_{_sw['name']}", label_visibility="visible")
                    if _sq > 0:
                        switch_quantities[_sw["name"]] = _sq
        # Auto-select Draytek when SY Comms BB is selected, same pattern as switch
        _default_router_mode = "Auto-select" if bb_provider != "None / Customer Supplied" else "None / Customer Supplied"
        _router_mode = st.radio("Router", ["Auto-select", "Manual select", "None / Customer Supplied"],
                                horizontal=True, key="router_mode",
                                index=["Auto-select","Manual select","None / Customer Supplied"].index(
                                    st.session_state.get("router_mode", _default_router_mode)
                                ) if st.session_state.get("router_mode") else
                                ["Auto-select","Manual select","None / Customer Supplied"].index(_default_router_mode))
        # Smart default: FTTP → GWN 706, SoGEA → Technicolour, else Draytek
        _bb_pkg_lower = (bb_package or "").lower()
        if "fttp" in _bb_pkg_lower and "Grandstream GWN7062E (FTTP)" in ROUTERS:
            _default_router = "Grandstream GWN7062E (FTTP)"
        elif "fttp" in _bb_pkg_lower and "Grandstream GWN 706 (FTTP)" in ROUTERS:
            _default_router = "Grandstream GWN 706 (FTTP)"
        elif "sogea" in _bb_pkg_lower and "Technicolour DGA Series (SoGEA)" in ROUTERS:
            _default_router = "Technicolour DGA Series (SoGEA)"
        elif any(x in _bb_pkg_lower for x in ("sogea", "fttp", "leased", "etherway")):
            # Other fibre types — use Draytek as fallback
            _default_router = next((k for k in ROUTERS if "Draytek" in k), list(ROUTERS.keys())[0])
        else:
            # FTTC, ADSL etc — no auto router (ISP provides modem/router)
            _default_router = None
        router_quantities = {}
        add_router = False
        if _router_mode == "None / Customer Supplied":
            router_type = "None / Customer Supplied"
            add_router  = False
        elif _router_mode == "Auto-select":
            if bb_provider != "None / Customer Supplied" and _default_router:
                router_type = _default_router
                router_quantities = {_default_router: 1}
                add_router = True
            else:
                router_type = "None / Customer Supplied"
                add_router  = False
        else:  # Manual select
            add_router = False
            router_type = "None / Customer Supplied"
            st.caption("Set quantities for each router needed:")
            _rt_cols = st.columns(2)
            for _ri, (_rname, _rbuy) in enumerate(ROUTERS.items()):
                with _rt_cols[_ri % 2]:
                    _rq = st.number_input(_rname, min_value=0, value=0, step=1,
                                          key=f"rt_qty_{_rname}", label_visibility="visible")
                    if _rq > 0:
                        router_quantities[_rname] = _rq
                        add_router = True
                        router_type = _rname

        additional_wired_ports = st.number_input(
            "Additional wired network ports", min_value=0,
            value=st.session_state.get("add_wired_ports", 0),
            step=1, key="add_wired_ports",
            help="Extra POE ports needed beyond desk phones - affects switch auto-selection")

    with st.expander("📱 Mobiles", expanded=False):
        mobile_rows = []
        for net, pkgs in MOBILE_NETWORKS.items():
            for pkg, pricing in pkgs.items():
                qty = st.number_input(
                    f"{net} - {pkg}",
                    min_value=0, value=0, step=1, key=f"mob_{net}_{pkg}"
                )
                if qty > 0:
                    mobile_rows.append({"network": net, "package": pkg, "qty": qty, **pricing})


    with st.expander("💻 IT Services", expanded=False):
        st.caption("Per-user monthly licences — billed separately to the hardware lease")
        it_rows = []
        for it_cat, it_pkgs in IT_SERVICES.items():
            st.markdown(f"**{it_cat}**")
            for pkg_name, pkg_info in it_pkgs.items():
                _it_sell = round(pkg_info.get("sell") or pkg_info["cost"] * (1 + IT_UPLIFT_PCT / 100), 2)
                qty = st.number_input(
                    f"{pkg_name}  (£{_it_sell:.2f}/user/mo)",
                    min_value=0, value=0, step=1, key=f"it_{pkg_name}"
                )
                if qty > 0:
                    it_rows.append({"service": pkg_name, "qty": qty,
                                    "cost": pkg_info["cost"], "sell": _it_sell})

    # ── System Security expander ─────────────────────────────────────────────
    with st.expander("🛡️ System Security", expanded=False):
        st.caption("Managed security tiers — per instance per month")
        if "system_security" not in st.session_state.active_config:
            st.session_state.active_config["system_security"] = [
                {"name": "Bronze Security", "buy": 7.00,  "sell": 10.00},
                {"name": "Silver Security", "buy": 10.00, "sell": 15.00},
                {"name": "Gold Security",   "buy": 14.00, "sell": 20.00},
            ]
        sec_cfg = st.session_state.active_config.get("system_security", [])
        for _sc in sec_cfg:
            st.number_input(f"{_sc['name']}  (£{_sc['sell']:.2f}/instance/mo)",
                            min_value=0, value=0, step=1, key=f"sec_{_sc['name']}")


    with st.expander("🔮 Call Scope", expanded=False):
        st.caption("Call Scope platform modules — monthly service charges unless noted")
        if "call_scope_services" not in st.session_state.active_config:
            st.session_state.active_config["call_scope_services"] = [
                {"name": "AI Integration - Portal", "buy": 20.00, "sell": 29.00},
                {"name": "AI Integration - CRM",    "buy": 25.00, "sell": 35.00},
                {"name": "Manager Dashboard",        "buy": 40.00, "sell": 59.00},
                {"name": "Call Score",               "buy": 20.00, "sell": 29.00},
            ]
        _cs_exp_cfg = st.session_state.active_config.get("call_scope_services", [])
        _cse_col1, _cse_col2 = st.columns(2)
        with _cse_col1:
            for _cs in _cs_exp_cfg[:2]:
                st.number_input(
                    f"{_cs['name']}  £{_cs['sell']:.2f}/mo",
                    min_value=0, value=0, step=1, key=f"cs_{_cs['name']}"
                )
                if "AI Integration" in _cs["name"] and st.session_state.get(f"cs_{_cs['name']}", 0) > 0:
                    st.selectbox(
                        f"Minutes for {_cs['name']}",
                        ["None", "500 mins  — £25/mo", "1000 mins — £35/mo", "1500 mins — £45/mo"],
                        key=f"cs_mins_{_cs['name']}"
                    )
            _mypa_opts_cfg = st.session_state.active_config.get("mypa_bundles", [
                {"name": "My PA 500 mins",  "sell": 149.0},
                {"name": "My PA 1000 mins", "sell": 199.0},
                {"name": "My PA 2000 mins", "sell": 249.0},
            ])
            _mypa_opts = ["None"] + [
                f"{mp['name'].replace('My PA ','')} — £{mp['sell']:.0f}/mo"
                for mp in _mypa_opts_cfg
            ]
            st.selectbox("Call Answer - My PA", _mypa_opts, key="cs_mypa")
        with _cse_col2:
            for _cs in _cs_exp_cfg[2:]:
                st.number_input(
                    f"{_cs['name']}  £{_cs['sell']:.2f}/mo",
                    min_value=0, value=0, step=1, key=f"cs_{_cs['name']}"
                )
            st.selectbox("Website Widget",
                         ["None", "Include — £50/mo"],
                         key="cs_website")
        st.checkbox("🎁 AI Portal — 1st month free (500 mins)", key="cs_ai_portal_free",
                    help="Promotional offer: first month of AI Portal 500-min bundle at no charge")

# ─── POST-EXPANDER REBUILDS (session state → module-level lists) ─────────────
# Call Scope services
cs_cfg_mod = st.session_state.active_config.get("call_scope_services", [
    {"name": "AI Integration - Portal", "buy": 20.00, "sell": 29.00},
    {"name": "AI Integration - CRM", "buy": 25.00, "sell": 35.00},
    {"name": "Manager Dashboard", "buy": 40.00, "sell": 59.00},
    {"name": "Call Score", "buy": 20.00, "sell": 29.00},
])
_CS_MINS_COSTS = {"500 mins  — £25/mo": 25.0, "1000 mins — £35/mo": 35.0, "1500 mins — £45/mo": 45.0}
cs_svc_rows = []
for _cs in cs_cfg_mod:
    qty = st.session_state.get(f"cs_{_cs['name']}", 0)
    if qty > 0:
        cs_svc_rows.append({"name": _cs["name"], "qty": qty, "buy": _cs["buy"], "sell": _cs["sell"]})
        # Add minutes bundle cost if selected for AI Integration modules
        if "AI Integration" in _cs["name"]:
            _mins_sel = st.session_state.get(f"cs_mins_{_cs['name']}", "None")
            _mins_cost = _CS_MINS_COSTS.get(_mins_sel, 0.0)
            if _mins_cost > 0:
                cs_svc_rows.append({"name": f"{_cs['name']} — {_mins_sel.split('—')[0].strip()}",
                                    "qty": 1, "buy": _mins_cost * 0.7, "sell": _mins_cost})
_cs_mypa_sel  = st.session_state.get("cs_mypa", "None")
_cs_web_sel   = st.session_state.get("cs_website", "None")
cs_call_answer = _cs_mypa_sel != "None"
cs_website     = _cs_web_sel != "None"
cs_any_selected = bool(cs_svc_rows or cs_call_answer or cs_website)
# Build My PA cost lookup from config (picks up admin price changes)
_mypa_defaults_calc = [
    {"name": "My PA 500 mins",  "buy": 100.0, "sell": 149.0},
    {"name": "My PA 1000 mins", "buy": 140.0, "sell": 199.0},
    {"name": "My PA 2000 mins", "buy": 180.0, "sell": 249.0},
]
_mypa_cfg_calc = st.session_state.active_config.get("mypa_bundles", _mypa_defaults_calc)
_CS_MYPA_COSTS = {
    f"{mp['name'].replace('My PA ','')} — £{mp['sell']:.0f}/mo": mp["sell"]
    for mp in _mypa_cfg_calc
}
_CS_MYPA_BUY = {
    f"{mp['name'].replace('My PA ','')} — £{mp['sell']:.0f}/mo": mp["buy"]
    for mp in _mypa_cfg_calc
}
_mypa_sel = st.session_state.get("cs_mypa", "None")
if _mypa_sel != "None":
    _mypa_cost = _CS_MYPA_COSTS.get(_mypa_sel, 0.0)
    _mypa_buy  = _CS_MYPA_BUY.get(_mypa_sel, _mypa_cost * 0.7)
    if _mypa_cost > 0:
        cs_svc_rows.append({"name": f"Call Answer - My PA ({_mypa_sel.split(' —')[0]})",
                            "qty": 1, "buy": _mypa_buy, "sell": _mypa_cost})
_web_sel = st.session_state.get("cs_website", "None")
if _web_sel != "None":
    _web_cs_cfg = next((s for s in st.session_state.active_config.get("call_scope_services", [])
                        if s.get("name") == "Website Widget"), {"buy": 30.0, "sell": 50.0})
    cs_svc_rows.append({"name": "Website Widget", "qty": 1,
                        "buy": _web_cs_cfg.get("buy", 30.0), "sell": _web_cs_cfg.get("sell", 50.0)})

# System Security
sec_cfg_mod = st.session_state.active_config.get("system_security", [
    {"name": "Bronze Security", "buy": 7.00, "sell": 10.00},
    {"name": "Silver Security", "buy": 10.00, "sell": 15.00},
    {"name": "Gold Security", "buy": 14.00, "sell": 20.00},
])
sec_rows = []
for _sc in sec_cfg_mod:
    qty = st.session_state.get(f"sec_{_sc['name']}", 0)
    if qty > 0:
        sec_rows.append({"name": _sc["name"], "qty": qty, "buy": _sc["buy"], "sell": _sc["sell"]})

# Auto-add Call Scope lease items to other_quantities
# Call Answer - My PA and Website Widget are monthly services, not lease items
if cs_any_selected and "Call Scope Platform Setup" not in other_quantities:
    if "Call Scope Platform Setup" not in OTHER_HARDWARE:
        OTHER_HARDWARE["Call Scope Platform Setup"] = {"buy": 300.00, "sell": 500.00}
    other_quantities["Call Scope Platform Setup"] = 1

# ─── MANAGER OVERRIDE SECTION ────────────────────────────────────────────────

# --- AUTO-CALCULATE VOICE CHANNELS -----------------------------------
# One licence required per physical handset (mirrors Excel SYSTEM BUILDER I16)
# Standalone softphones add extra seats on top
auto_handset_licences = (
    sum(desktop_quantities.values()) +
    sum(cordless_quantities.values())
)
user_licences        = auto_handset_licences
softphone_licences   = standalone_softphones
total_voice_channels = user_licences + softphone_licences

st.info(
    f"🎙️ **Voice Channels: {total_voice_channels}** "
    f"({user_licences} desk phone{"s" if user_licences != 1 else ""} + {softphone_licences} softphone/mobile app)"
)
if total_voice_channels >= 5:
    _pbx_qty = sum(q for n, q in other_quantities.items() if "PBX" in n.upper() or "pbx" in n.lower())
    if _pbx_qty == 0:
        st.warning("⚠️ 5+ users: a **PBX Unit** is required - add one from the Other Hardware section above.")
    else:
        st.success(f"✅ PBX Unit included (×{_pbx_qty})")

# ─── TABS ─────────────────────────────────────────────────────────────────────

def s(text):
    """Sanitise text for fpdf2 - replaces/strips characters outside latin-1."""
    if not text:
        return ""
    replacements = {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u00a0": " ",
        "\u00ae": "(R)", "\u00a9": "(C)", "\u00e9": "e", "\u00e8": "e",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def build_proposal_pdf():
    """Visually rich two-page proposal matching brand identity."""
    from fpdf import FPDF

    def _ps(text):
        return str(text or "").encode("latin-1", errors="replace").decode("latin-1")

    p = FPDF()
    p.set_auto_page_break(True, margin=15)
    _p_logo_bytes = base64.b64decode(SYCOMMS_LOGO_B64) if _BRAND["logo_key"] else None
    _p_logo_buf   = io.BytesIO(_p_logo_bytes) if _p_logo_bytes else None

    PW = 210  # page width mm

    # ─────────────────────────────────────────────────────────────────────────────
    # PAGE 1 — ABOUT SY COMMS
    # ─────────────────────────────────────────────────────────────────────────────
    p.add_page()

    # ── Full-bleed hero (deep purple, 85mm) ──────────────────────────────────────
    p.set_fill_color(31, 20, 80)
    p.rect(0, 0, PW, 85, "F")
    # Teal diagonal accent strip
    p.set_fill_color(0, 181, 163)
    p.rect(0, 82, PW, 3, "F")
    # Logo
    try:
        if _p_logo_buf: p.image(_p_logo_buf, x=10, y=8, h=28); _p_logo_buf.seek(0)
    except Exception: pass
    # Hero headline
    p.set_text_color(255, 255, 255)
    p.set_font("Helvetica", "B", 22)
    p.set_y(18); p.set_x(48)
    p.cell(0, 10, s(_CO_LEGAL.upper()), ln=True)
    p.set_font("Helvetica", "", 11); p.set_x(48)
    p.set_text_color(0, 200, 180)
    p.cell(0, 7, "Short term contracts, long term relationships.", ln=True)
    p.set_font("Helvetica", "", 8.5); p.set_x(48)
    p.set_text_color(180, 190, 220)
    p.multi_cell(PW - 60, 4.5, _ps(
        "Empowering local businesses through reliable telecoms, IT services, "
        "high-speed internet and streamlined communication systems."))
    # Teal tag pills
    p.set_text_color(255, 255, 255)
    p.set_font("Helvetica", "B", 7.5)
    tags = ["All-Inclusive", "Fully Managed", "Local Engineers", "12-Month Contracts"]
    tx = 48
    for tag in tags:
        tw = len(tag) * 2.5 + 6
        p.set_fill_color(0, 140, 130)
        p.rect(tx, 62, tw, 6, "F")
        p.set_xy(tx + 2, 62.5)
        p.cell(tw - 4, 5, tag, ln=False)
        tx += tw + 3
    p.set_text_color(0, 0, 0)

    # ── Why SY Comms — 3-col icon cards ─────────────────────────────────────────
    p.set_y(90)
    p.set_font("Helvetica", "B", 10); p.set_text_color(31, 20, 80)
    p.cell(0, 6, s(f"Why businesses trust {_CO}"), ln=True); p.ln(1)

    vals3 = [
        ("ONE BILL",         "Hardware, licences, broadband and support - one monthly payment."),
        ("FULLY MANAGED",    "We handle installation, programming, warranty and helpdesk."),
        ("UK CONNECTIVITY",  "FTTP, SoGEA, leased line and 4G/5G solutions available."),
        ("LOCAL ENGINEERS",  "On-site support from engineers who know your area."),
        ("NO LOCK-IN FEAR",  "Flexible terms - you stay because the service is great."),
        ("CALL SCOPE AI",    "AI-powered call analytics built for modern business."),
    ]
    COL = 3; BW = (PW - 20 - (COL-1)*3) / COL; BH = 28
    bx0 = p.l_margin
    by  = p.get_y()  # initialise before loop
    for n, (title, desc) in enumerate(vals3):
        col = n % COL; row = n // COL
        bx  = bx0 + col * (BW + 3)
        if col == 0 and row > 0: by += BH + 3
        # Card bg
        p.set_fill_color(245, 247, 255)
        p.rect(bx, by, BW, BH, "F")
        # Teal left border
        p.set_fill_color(0, 181, 163)
        p.rect(bx, by, 2.5, BH, "F")
        # Title
        p.set_xy(bx + 5, by + 4)
        p.set_font("Helvetica", "B", 7.5); p.set_text_color(31, 20, 80)
        p.cell(BW - 6, 4, _ps(title), ln=True)
        # Desc
        p.set_x(bx + 5)
        p.set_font("Helvetica", "", 6.8); p.set_text_color(80, 80, 80)
        p.multi_cell(BW - 7, 3.5, _ps(desc))
        if col == COL - 1:
            p.set_y(by + BH + 3)

    p.set_text_color(0, 0, 0)
    p.set_y(by + BH + 5)

    # ── Contact strip ────────────────────────────────────────────────────────────
    p.set_fill_color(31, 20, 80); p.set_text_color(255, 255, 255)
    p.set_font("Helvetica", "B", 8)
    p.cell(0, 7, "  Get in touch today", fill=True, ln=True)
    p.set_font("Helvetica", "", 8)
    contacts = [
        ("Email",   _CO_EMAIL),
        ("Phone",   _CO_PHONE),
        ("Address", "Suite C Jupiter House, Shrewsbury Business Park, SY2 6LG"),
        ("Web",     _CO_WEB),
    ]
    for lbl, val in contacts:
        p.set_fill_color(45, 31, 110)
        p.cell(22, 5.5, _ps(f"  {lbl}:"), fill=True, ln=False)
        p.set_fill_color(55, 40, 130)
        p.cell(0, 5.5, _ps(val), fill=True, ln=True)
    p.set_text_color(0, 0, 0)

    # ─────────────────────────────────────────────────────────────────────────────
    # PAGE 2 — PERSONALISED PROPOSAL
    # ─────────────────────────────────────────────────────────────────────────────
    p.add_page()

    # ── Compact header ────────────────────────────────────────────────────────────
    p.set_fill_color(31, 20, 80); p.rect(0, 0, PW, 22, "F")
    try:
        if _p_logo_buf: p.image(_p_logo_buf, x=8, y=3, h=16); _p_logo_buf.seek(0)
    except Exception: pass
    p.set_text_color(255, 255, 255); p.set_font("Helvetica", "B", 13)
    p.set_y(4); p.set_x(34)
    p.cell(0, 8, "Your Personalised Proposal", ln=True)
    p.set_font("Helvetica", "", 8); p.set_x(34)
    p.set_text_color(160, 180, 220)
    p.cell(0, 5, _ps(f"Prepared for: {s(comp_name or 'Your Company')}   |   {date.today().strftime('%d %B %Y')}"), ln=True)
    p.set_fill_color(0, 181, 163); p.rect(0, 22, PW, 2, "F")
    p.set_text_color(0, 0, 0); p.set_y(27)

    # ── COST COMPARISON — 3 cards side by side ────────────────────────────────────
    CW = 60; CH = 38; CG = 4; cy = p.get_y()
    cx1, cx2, cx3 = p.l_margin, p.l_margin + CW + CG, p.l_margin + (CW + CG) * 2

    def _big_card(cx, cy, cw, ch, bg, accent_col, label, value, sub=""):
        p.set_fill_color(*bg); p.rect(cx, cy, cw, ch, "F")
        p.set_fill_color(*accent_col); p.rect(cx, cy, cw, 2.5, "F")
        p.set_xy(cx + 3, cy + 5)
        p.set_font("Helvetica", "", 6)
        if bg == (31, 20, 80):
            p.set_text_color(160, 160, 180)
        else:
            p.set_text_color(100, 100, 100)
        p.cell(cw - 6, 3.5, _ps(label), ln=True)
        p.set_x(cx + 3)
        p.set_font("Helvetica", "B", 13)
        tc = (0, 220, 180) if bg == (31, 20, 80) else (31, 20, 80)
        p.set_text_color(*tc)
        p.cell(cw - 6, 8, _ps(value), ln=True)
        if sub:
            p.set_x(cx + 3)
            p.set_font("Helvetica", "", 6.5)
            if bg == (31, 20, 80):
                p.set_text_color(130, 140, 160)
            else:
                p.set_text_color(100, 100, 100)
            p.cell(cw - 6, 4, _ps(sub), ln=True)
        p.set_text_color(0, 0, 0)

    curr_hw  = f"GBP {current_system:.2f}" if current_system > 0 else "Not entered"
    new_lease = f"GBP {hw_monthly_spread:.2f}"
    _sv = current_system - hw_monthly_spread if current_system > 0 else 0

    _ = _big_card(cx1, cy, CW, CH, (248, 248, 252), (200, 200, 210),
              "CURRENT LEASE / SYSTEM", curr_hw, "per month"); _ = None
    _ = _big_card(cx2, cy, CW, CH, (31, 20, 80), (0, 181, 163),
              f"NEW MONTHLY LEASE  ({LEASE_TERM_LABELS[lease_term]})", new_lease + "/mo", "hardware spread over term"); _ = None
    if current_system > 0:
        sv_bg = (232, 250, 240) if _sv >= 0 else (255, 240, 240)
        sv_ac = (0, 160, 80)   if _sv >= 0 else (180, 30, 30)
        sv_lb = "MONTHLY LEASE SAVING" if _sv >= 0 else "MONTHLY INCREASE"
        _ = _big_card(cx3, cy, CW, CH, sv_bg, sv_ac, sv_lb,
                  f"{'GBP ' + f'{abs(_sv):.2f}' + '/mo'}", f"GBP {abs(_sv*12):.0f} per year")
    else:
        _ = _big_card(cx3, cy, CW, CH, (248,248,252), (0,181,163), "FULL MONTHLY TOTAL", f"GBP {total_mo:.2f}/mo", "all services + lease")

    p.set_y(cy + CH + 3)

    # ── TOTAL MONTHLY BANNER ─────────────────────────────────────────────────────
    p.set_fill_color(31, 20, 80); p.rect(p.l_margin, p.get_y(), 189, 12, "F")
    p.set_fill_color(0, 181, 163); p.rect(p.l_margin, p.get_y(), 3, 12, "F")
    p.set_font("Helvetica", "", 7.5); p.set_text_color(160, 180, 220)
    p.set_xy(p.l_margin + 7, p.get_y() + 2.5)
    p.cell(80, 4, "TOTAL ALL-INCLUSIVE MONTHLY COMMITMENT (excl. VAT)", ln=False)
    p.set_font("Helvetica", "B", 12); p.set_text_color(0, 230, 190)
    p.cell(0, 4, _ps(f"GBP {total_mo:.2f} / month"), ln=True, align="R")
    p.set_text_color(0, 0, 0)
    p.ln(5)

    # ── PHONE IMAGES — larger, proper aspect ratio ────────────────────────────────
    _phone_items = [(n, q) for n, q in list(desktop_quantities.items()) + list(cordless_quantities.items()) if q > 0]
    if _phone_items:
        p.set_font("Helvetica", "B", 9); p.set_text_color(31, 20, 80)
        p.cell(0, 5, "Your New Phone System", ln=True)
        p.set_fill_color(0, 181, 163); p.rect(p.l_margin, p.get_y(), 40, 1, "F")
        p.ln(4)
        _tw = 32; _th_fixed = 24; _tgap = 3
        _tx = p.l_margin
        _thumb_start_y = p.get_y()
        for idx, (_pname, _pqty) in enumerate(_phone_items[:5]):
            _pb64, _pext = get_product_image_b64(_pname)
            _card_h = _th_fixed + 8
            # Card background
            p.set_fill_color(245, 247, 255)
            p.rect(_tx, _thumb_start_y, _tw, _card_h, "F")
            p.set_fill_color(0, 181, 163)
            p.rect(_tx, _thumb_start_y, _tw, 1.5, "F")
            if _pb64:
                try:
                    import tempfile as _ptf, os as _pos
                    _praw = base64.b64decode(_pb64)
                    with _ptf.NamedTemporaryFile(suffix=f".{_pext}", delete=False) as _ptmp:
                        _ptmp.write(_praw); _ptmp_path = _ptmp.name
                    p.image(_ptmp_path, x=_tx+2, y=_thumb_start_y+3,
                            w=_tw-4, h=_th_fixed-2)
                    _pos.unlink(_ptmp_path)
                except Exception: pass
            # Label below image inside card
            p.set_xy(_tx, _thumb_start_y + _th_fixed + 2)
            p.set_font("Helvetica", "B", 5.5); p.set_text_color(31, 20, 80)
            _short = _pname.split("(")[0].strip()[:18]
            p.cell(_tw, 4, _ps(f"{_short} x{_pqty}"), ln=False, align="C")
            _tx += _tw + _tgap
        p.set_text_color(0, 0, 0)
        # Always advance past image cards before next section
        p.set_y(_thumb_start_y + _th_fixed + 12)

    # ── SERVICES TABLE ───────────────────────────────────────────────────────────
    p.set_fill_color(31, 20, 80); p.set_text_color(255, 255, 255)
    p.set_font("Helvetica", "B", 8)
    p.cell(0, 6, "  Monthly Services Included", fill=True, ln=True)
    svc_rows = []
    # Broadband — with free year note if active
    if svc["bb_sell"] > 0:
        if bb_free_year and _bb_yr1_saving > 0:
            svc_rows.append((f"Broadband — {bb_provider} {bb_package} (FREE yr 1)",
                             f"GBP 0.00/mo (then GBP {_bb_full_sell:.2f})"))
        else:
            svc_rows.append((f"Broadband — {bb_provider} {bb_package}", f"GBP {svc['bb_sell']:.2f}/mo"))
    if svc["lic_monthly"] > 0:
        svc_rows.append((f"Hosted User Licences ({total_voice_channels} users)", f"GBP {svc['lic_monthly']:.2f}/mo"))
    if sw_sell_total > 0:
        svc_rows.append(("Software / Add-ons", f"GBP {sw_sell_total:.2f}/mo"))
    # Call Scope services
    for _csr in cs_svc_rows:
        if _csr.get("qty", 0) > 0:
            _csr_label = _csr["name"]
            _csr_sell  = _csr["sell"] * _csr["qty"]
            svc_rows.append((_csr_label, f"GBP {_csr_sell:.2f}/mo"))
    # AI Portal first month free note
    if st.session_state.get("cs_ai_portal_free", False):
        svc_rows.append(("  AI Portal 500 mins — 1st month FREE", "GBP 0.00 month 1"))
    # System Security
    for _sr in sec_rows:
        if _sr.get("qty", 0) > 0:
            svc_rows.append((f"{_sr['name']} x{_sr['qty']}",
                             f"GBP {_sr['sell']*_sr['qty']:.2f}/mo"))
    # IT Services
    for _ir in it_rows:
        if _ir.get("qty", 0) > 0:
            svc_rows.append((f"IT: {_ir['service']} x{_ir['qty']}",
                             f"GBP {_ir.get('sell', _ir.get('cost',0)) * _ir['qty']:.2f}/mo"))
    # Mobile SIMs
    for _mr in mobile_rows:
        if _mr.get("qty", 0) > 0:
            svc_rows.append((f"Mobile — {_mr['network']} {_mr['package']} x{_mr['qty']}",
                             f"GBP {_mr['sell']*_mr['qty']:.2f}/mo"))
    for i, (lbl, val) in enumerate(svc_rows):
        if i % 2 == 0:
            p.set_fill_color(245, 247, 255)
        else:
            p.set_fill_color(255, 255, 255)
        _lbl_safe = _ps(lbl.replace("—", "-").replace("–", "-"))
        p.set_text_color(60, 60, 60); p.set_font("Helvetica", "", 8)
        p.cell(140, 5.5, f"  {_lbl_safe}", fill=True, ln=False)
        p.set_font("Helvetica", "B", 8); p.set_text_color(31, 20, 80)
        p.cell(0, 5.5, _ps(val), fill=True, ln=True, align="R")
    p.set_text_color(0, 0, 0)
    p.ln(3)

    # ── AGREEMENT TERMS — 2-col ──────────────────────────────────────────────────
    p.set_fill_color(31, 20, 80); p.set_text_color(255, 255, 255)
    p.set_font("Helvetica", "B", 8)
    p.cell(0, 6, "  Agreement at a Glance", fill=True, ln=True)
    terms = [
        ("Term", LEASE_TERM_LABELS[lease_term]),     ("Installation", install_type),
        ("On-site Warranty", "12 months inclusive"), ("Support", "Remote diagnostics included"),
    ]
    HW = 91
    for i in range(0, len(terms), 2):
        pair = terms[i:i+2]
        if (i // 2) % 2 == 0:
            p.set_fill_color(245, 247, 255)
        else:
            p.set_fill_color(255, 255, 255)
        for j, (lbl, val) in enumerate(pair):
            cx = p.l_margin + j * HW
            p.set_xy(cx, p.get_y())
            p.set_font("Helvetica", "B", 7.5); p.set_text_color(31, 20, 80)
            p.cell(28, 5, _ps(f"  {lbl}:"), fill=True, ln=False)
            p.set_font("Helvetica", "", 7.5); p.set_text_color(60, 60, 60)
            p.cell(HW - 28, 5, _ps(val), fill=True, ln=False)
        p.ln(5)
    p.set_text_color(0, 0, 0)

    # ── SAVING BANNER ────────────────────────────────────────────────────────────
    if current_total > 0 and total_mo < current_total:
        _sv_tot = current_total - total_mo
        p.ln(2)
        p.set_fill_color(0, 181, 163); p.set_text_color(255, 255, 255)
        p.set_font("Helvetica", "B", 10)
        p.cell(0, 9, _ps(f"  Estimated Total Monthly Saving:  GBP {_sv_tot:.2f}   (GBP {_sv_tot*12:.0f} / year)"),
               fill=True, ln=True)
        p.set_text_color(0, 0, 0)

    # ── CTA FOOTER ───────────────────────────────────────────────────────────────
    p.ln(3)
    p.set_fill_color(31, 20, 80); p.set_text_color(255, 255, 255)
    p.set_font("Helvetica", "B", 8)
    p.cell(0, 6, "  Ready to proceed? We're here to help.", fill=True, ln=True)
    p.set_font("Helvetica", "", 8); p.set_fill_color(45, 31, 110)
    p.cell(0, 6, s(f"  {_CO_EMAIL}   |   {_CO_PHONE}   |   {_CO_WEB}"),
           fill=True, ln=True)
    p.set_text_color(0, 0, 0)

    return bytes(p.output())


def build_pdf(sig_bytes=None, sig_name='', sig_company='', sig_timestamp='', sig_ip='',
              curr_total=0.0, curr_bb=0.0, curr_system=0.0, curr_calls=0.0,
              curr_mobile=0.0, curr_support=0.0, curr_other=0.0):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)

    # Sanitise all user inputs going into PDF
    _comp     = s(comp_name)
    _reg      = s(comp_reg)
    _btype    = s(biz_type)
    _contact  = s(contact_name)
    _phone    = s(company_phone)
    _demail   = s(director_email)
    _bemail   = s(billing_email)
    _addr     = s(install_address)
    _bank     = s(bank_name)
    _holder   = s(acc_holder)
    _accno    = s(acc_no)
    _sort     = s(sort_code)

    # -- PAGE 1: PROPOSAL --
    # Embed logo for PDF (conditional on brand having a logo)
    _logo_bytes = base64.b64decode(SYCOMMS_LOGO_B64) if _BRAND["logo_key"] else None
    _logo_buf   = io.BytesIO(_logo_bytes) if _logo_bytes else None

    def _add_header(pdf_obj, subtitle="Customer Proposal & Order Documentation"):
        # Deep purple background
        pdf_obj.set_fill_color(31, 20, 80)
        pdf_obj.rect(0, 0, 210, 42, 'F')
        # Logo on left (if available for this brand)
        if _logo_buf:
            pdf_obj.image(_logo_buf, x=10, y=6, h=30)
            _logo_buf.seek(0)
        # Company name right of logo
        pdf_obj.set_font("Helvetica", "B", 20)
        pdf_obj.set_text_color(255, 255, 255)
        pdf_obj.set_y(7)
        pdf_obj.set_x(48)
        pdf_obj.cell(120, 10, s(_CO.upper()), ln=False, align="L")
        pdf_obj.set_font("Helvetica", "", 9)
        pdf_obj.set_y(19)
        pdf_obj.set_x(48)
        pdf_obj.cell(120, 6, s(subtitle), ln=False, align="L")
        # Teal accent bar
        pdf_obj.set_fill_color(0, 181, 163)
        pdf_obj.rect(0, 42, 210, 2, 'F')
        pdf_obj.set_text_color(0, 0, 0)
        pdf_obj.set_y(48)

    # ── PAGE 1: SY COMMS COMPANY INTRODUCTION ───────────────────────────────
    pdf.set_auto_page_break(False)   # disable so cover page content doesn't spill
    pdf.add_page()

    # Full-page gradient cover
    pdf.set_fill_color(31, 20, 80)
    pdf.rect(0, 0, 210, 297, 'F')

    # Teal accent stripe at top
    pdf.set_fill_color(0, 181, 163)
    pdf.rect(0, 0, 210, 5, 'F')

    # Logo centred - large (only shown for brands that have a logo)
    if _logo_buf:
        pdf.image(_logo_buf, x=75, y=25, h=55)
        _logo_buf.seek(0)

    # Company name
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(90)
    pdf.cell(0, 12, s(_CO.upper()), ln=True, align="C")

    # Tagline
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(0, 181, 163)
    pdf.set_y(106)
    pdf.cell(0, 8, "Connecting local businesses to success", ln=True, align="C")

    # Divider
    pdf.set_draw_color(0, 181, 163)
    pdf.set_line_width(0.6)
    pdf.line(40, 120, 170, 120)

    # Proposal label
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(126)
    pdf.cell(0, 8, s(f"CUSTOMER PROPOSAL"), ln=True, align="C")
    if _comp:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(0, 181, 163)
        pdf.set_y(136)
        pdf.cell(0, 7, s(f"Prepared for: {_comp}"), ln=True, align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(200, 200, 220)
    pdf.set_y(146)
    pdf.cell(0, 6, s(f"Date: {date.today().strftime('%d %B %Y')}"), ln=True, align="C")

    # ── About Us section ──────────────────────────────────────────────────────
    pdf.set_y(165)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 181, 163)
    pdf.cell(0, 8, s(f"About {_CO}"), ln=True, align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(220, 220, 230)
    pdf.set_x(30)
    pdf.multi_cell(150, 5.5,
        s(_CO_ABOUT +
        "serving businesses across the UK. We understand the "
        "unique needs of our community and are committed to delivering solutions that "
        "work for you. Our experienced local engineers are always on hand to provide "
        "friendly, fast and personalised service."),
        align="C"
    )

    # ── Values section ────────────────────────────────────────────────────────
    pdf.set_y(215)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 181, 163)
    pdf.cell(0, 7, "Our Values", ln=True, align="C")
    pdf.ln(1)

    values = [
        (">  Rapid",    "Response times within the hour to minimise downtime"),
        (">  Complete", "Full-stack: Telecoms, Mobile, Networking, IT & Payments"),
    ]
    for title, desc in values:
        pdf.set_x(30)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(45, 5.5, s(title), ln=False)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(190, 190, 210)
        pdf.cell(0, 5.5, s(desc), ln=True)
        pdf.ln(0.5)

    # ── Contact footer ────────────────────────────────────────────────────────
    pdf.set_fill_color(0, 181, 163)
    pdf.rect(0, 263, 210, 0.6, 'F')

    pdf.set_y(267)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(200, 200, 220)
    pdf.cell(0, 5, s(f"{_CO_PHONE}   |   {_CO_EMAIL}   |   {_CO_WEB}"), ln=True, align="C")
    pdf.set_y(273)
    pdf.cell(0, 5, s(_BRAND.get("address", "Suite C Jupiter House, Sitka Drive, Shrewsbury Business Park, Shrewsbury SY2 6LG")), ln=True, align="C")

    # Teal accent stripe at bottom
    pdf.set_fill_color(0, 181, 163)
    pdf.rect(0, 292, 210, 5, 'F')

    # ── PAGE 2 onwards: standard proposal pages ───────────────────────────────
    pdf.set_auto_page_break(True, margin=15)   # re-enable for content pages
    pdf.add_page()
    _add_header(pdf)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "CUSTOMER PROFILE", ln=True)
    pdf.set_draw_color(240, 240, 240)
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    def row2(l1, v1, l2="", v2=""):
        """Two-column label+value row. Auto-shrinks font if value is long."""
        def _val_font(val):
            """Pick font size so text fits in 55mm column."""
            return 8 if len(str(val)) > 28 else 10

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(40, 6, l1, ln=False)
        pdf.set_font("Helvetica", "", _val_font(v1))
        pdf.set_text_color(0, 0, 0)
        # Clip at 40 chars to guarantee no overflow
        v1_str = str(v1)[:40] + ("..." if len(str(v1)) > 40 else "")
        pdf.cell(55, 6, v1_str, ln=False)
        if l2:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(120, 120, 120)
            pdf.cell(40, 6, l2, ln=False)
            pdf.set_font("Helvetica", "", _val_font(v2))
            pdf.set_text_color(0, 0, 0)
            v2_str = str(v2)[:36] + ("..." if len(str(v2)) > 36 else "")
            pdf.cell(0, 6, v2_str, ln=True)
        else:
            pdf.ln()

    row2("Company:", _comp or "-", "Entity Type:", _btype)
    row2("Reg. No.:", _reg or "-", "No. of Employees:", str(num_employees))
    row2("Contact:", _contact or "-", "Phone:", _phone or "-")
    row2("Email:", _demail or "-", "Billing Email:", _bemail or "-")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(40, 6, "Install Address:", ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(pdf.l_margin + 40)          # start AFTER the label, not at left edge
    pdf.multi_cell(pdf.epw - 40, 5.5, _addr or "-")
    pdf.ln(4)

    # Commercial Summary
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "COMMERCIAL SUMMARY", ln=True)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(2)

    # Cost comparison table
    pdf.set_fill_color(31, 20, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(90, 7, "Description", border=0, fill=True, ln=False)
    pdf.cell(50, 7, "Current", border=0, fill=True, ln=False, align="C")
    pdf.cell(50, 7, _CO, border=0, fill=True, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 9)

    if is_spread:
        curr_hw  = f"£{current_system:.2f}/mo" if current_system > 0 else "-"
        curr_svc = f"£{(current_bb + current_calls + current_mobile):.2f}/mo" if (current_bb + current_calls + current_mobile) > 0 else "-"
        _curr_hosted = f"£{current_hosted:.2f}/mo" if current_hosted > 0 else "-"
        rows = [
            ("Hardware (spread over term)", curr_hw,  f"£{hw_monthly_spread:.2f}/mo"),
            ("User / Voice Licences", _curr_hosted, f"£{svc['lic_monthly']:.2f}/mo"),
            ("Network & Connectivity (BB, Mobile)", curr_svc, f"£{pure_connectivity:.2f}/mo"),
            ("Installation / Setup", "-", "Included in lease rental"),
        ]
    else:
        curr_hw  = f"£{current_system:.2f}/mo" if current_system > 0 else "-"
        curr_svc = f"£{(current_bb + current_calls + current_mobile):.2f}/mo" if (current_bb + current_calls + current_mobile) > 0 else "-"
        _curr_hosted = f"£{current_hosted:.2f}/mo" if current_hosted > 0 else "-"
        rows = [
            ("Upfront Hardware (one-off)", curr_hw,  f"£{upfront:.2f}"),
            ("User / Voice Licences", _curr_hosted, f"£{svc['lic_monthly']:.2f}/mo"),
            ("Network & Connectivity (BB, Mobile)", curr_svc, f"£{pure_connectivity:.2f}/mo"),
            ("Installation", "-", f"£{compute_install_cost():.2f}"),
        ]
    for i, (desc, curr, new) in enumerate(rows):
        bg = (248, 249, 255) if i % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*bg)
        pdf.cell(90, 6, f"  {desc}", border=0, fill=True, ln=False)
        pdf.cell(50, 6, curr, border=0, fill=True, ln=False, align="C")
        pdf.cell(50, 6, new, border=0, fill=True, ln=True, align="C")

    # Total row
    curr_total_str = f"£{current_total:.2f}/mo" if current_total > 0 else "-"
    pdf.set_fill_color(0, 181, 163)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(90, 7, "  TOTAL MONTHLY (excl. VAT)", fill=True, ln=False)
    pdf.cell(50, 7, curr_total_str, fill=True, ln=False, align="C")
    pdf.cell(50, 7, f"£{total_mo:.2f}/mo" + ("" if is_spread else f" + £{upfront:.2f} upfront"), fill=True, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    if credits_months > 0:
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, f"* Introductory credit of £{credits_amount:.2f}/month applied for {credits_months} months", ln=True)
    pdf.ln(2)

    # Equipment table
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "EQUIPMENT & SERVICES", ln=True)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(2)

    pdf.set_fill_color(31, 20, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(110, 7, "Description", fill=True, ln=False)
    pdf.cell(30, 7, "Qty", fill=True, ln=False, align="C")
    pdf.cell(50, 7, "Monthly Charge", fill=True, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 9)

    all_equip_pdf = []
    _pdf_hw_billing = "In Monthly Lease" if is_spread else "Paid Upfront"

    # Physical hardware (qty > 0 only)
    for name, qty in {**desktop_quantities, **cordless_quantities,
                       **headset_quantities, **other_quantities}.items():
        if qty > 0:
            all_equip_pdf.append((name, qty, _pdf_hw_billing))
    if auto_switch and not _no_switch:
        all_equip_pdf.append((f"Switch: {rec_switch['name']}", 1, _pdf_hw_billing))
    if add_router:
        if router_quantities:
            for _rn, _rq in router_quantities.items():
                all_equip_pdf.append((_rn, _rq, _pdf_hw_billing))
        elif router_type not in ("None / Customer Supplied", ""):
            all_equip_pdf.append((router_type, 1, _pdf_hw_billing))

    # Voice Channel Licences
        vc_billing_pdf = f"£{svc['lic_monthly']:.2f}/mo"  # always monthly - not part of lease
        all_equip_pdf.append((f"User / Voice Licences x{total_voice_channels}",
                               total_voice_channels, vc_billing_pdf))

    # Software add-ons
    for addon_name, addon_qty, addon_cost, addon_sell in SW_ADDONS:
        if addon_qty > 0:
            addon_billing_pdf = f"£{addon_sell * addon_qty:.2f}/mo"  # SW always monthly
            all_equip_pdf.append((addon_name, addon_qty, addon_billing_pdf))

    # Network & Connectivity
    if svc["bb_sell"] > 0:
        all_equip_pdf.append((f"Broadband - {bb_provider} {bb_package}", 1,
                               f"£{svc['bb1_sell']:.2f}/mo"))
    if second_fttp and second_fttp_pkg:
        bb2 = svc["bb2_sell"]
        all_equip_pdf.append((f"Broadband - {bb_provider} {second_fttp_pkg} (2nd line)", 1,
                               f"£{bb2:.2f}/mo"))
    for r in mobile_rows:
        if r["qty"] > 0:
            all_equip_pdf.append((f"{r['network']} - {r['package']}", r["qty"],
                                   f"£{r['sell']*r['qty']:.2f}/mo"))
    for r in it_rows:
        if r["qty"] > 0:
            all_equip_pdf.append((f"IT: {r['service']} x{r['qty']}", r["qty"],
                                   f"£{r['sell']*r['qty']:.2f}/mo"))


    for i, (name, qty, charge) in enumerate(all_equip_pdf):
        bg = (248, 249, 255) if i % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*bg)
        pdf.cell(110, 6, f"  {name}", fill=True, ln=False)
        pdf.cell(30, 6, str(qty), fill=True, ln=False, align="C")
        pdf.cell(50, 6, charge, fill=True, ln=True, align="C")
    pdf.ln(4)

    # -- PAGE 2: ORDER FORM --
    pdf.add_page()
    _add_header(pdf, "Telephony System Order Form")

    row2("Date:", str(date.today()), "Contract Term:", LEASE_TERM_LABELS[lease_term])
    row2("Company:", _comp or "-", "Reg. No.:", _reg or "-")
    row2("No. of Employees:", str(num_employees), "Install Type:", install_type)
    row2("No. of Sites:", str(num_sites), "Payment Profile:", f"1+{lease_term-1}")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Equipment & Services", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_fill_color(31, 20, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(130, 6, "Item", fill=True, ln=False)
    pdf.cell(30, 6, "Quantity", fill=True, ln=False, align="C")
    pdf.cell(30, 6, "Notes", fill=True, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    for i, (name, qty, charge) in enumerate(all_equip_pdf):
        bg = (248, 249, 255) if i % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*bg)
        pdf.cell(130, 6, f"  {name}", fill=True, ln=False)
        pdf.cell(30, 6, str(qty), fill=True, ln=False, align="C")
        pdf.cell(30, 6, "", fill=True, ln=True)
    pdf.ln(4)

    # Hardware & payment summary
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Hardware & Payment Summary", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_x(pdf.l_margin)
    if is_spread:
        # Note: hw_monthly_spread includes termination cost if applicable - do not
        # expose the raw hw_sell figure as the maths would not reconcile for the customer
        pdf.multi_cell(pdf.epw, 5,
            f"Your system investment of £{hw_monthly_spread:.2f} + VAT per month covers all hardware, "
            f"configuration and associated setup costs, spread over the {LEASE_TERM_LABELS[lease_term]} agreement. "
            f"Total monthly payment of £{total_mo:.2f} + VAT will be collected by Direct Debit, "
            f"covering your complete telephony solution and all service charges."
        )
    else:
        pdf.multi_cell(pdf.epw, 5,
            f"Hardware is provided on a one-off upfront basis. "
            f"Total hardware investment: £{upfront:.2f} + VAT. "
            f"Monthly service charges of £{total_mo:.2f} + VAT will be collected by Direct Debit."
        )
    pdf.ln(4)

    # Special conditions
    if credits_months > 0 or cashback_amount > 0:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, "Special Conditions", ln=True)
        pdf.set_font("Helvetica", "", 9)
        if credits_months > 0:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.epw, 5,
                f"An introductory credit of £{credits_amount:.2f}/month will be applied for {credits_months} months, "
                f"after which it will automatically cease. {_CO} reserves the right to suspend or withdraw "
                "this credit in the event of any arrears."
            )
        if cashback_amount > 0:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.epw, 5,
                f"{_CO_LEGAL} agrees to contribute £{cashback_amount:.2f} towards extricating the customer "
                f"from existing agreements. This amount will be paid once {_CO} have taken over the lines and the "
                "system has been formally accepted into service."
            )
        pdf.ln(3)

    # Signatures
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Signatures", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "For (Company Name):", ln=True)
    pdf.ln(2)
    _embed_sig(pdf, sig_bytes, signer_name=sig_name,
               company=sig_company, timestamp=sig_timestamp)
    pdf.cell(0, 0.5, "", border="T", ln=True)
    pdf.ln(3)
    pdf.cell(0, 5, f"Name & Position: {_contact or '___________________________'}", ln=True)
    pdf.ln(6)

    # -- PAGE 3: NETWORK SERVICES AGREEMENT --
    pdf.add_page()
    _add_header(pdf, "Network Services & Broadband Agreement")

    row2("Date:", str(date.today()), "Agreement Term:", LEASE_TERM_LABELS[lease_term])
    row2("Company:", _comp or "-", "Company Phone:", _phone or "-")
    row2("Billing Email:", _bemail or "-")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Service Charge Breakdown", ln=True)
    pdf.set_font("Helvetica", "", 9)

    if bb_free_year and _bb_yr1_saving > 0:
        svc_items = [(f"{bb_provider} - {bb_package} (FREE months 1-12)", 1,
                      f"£0.00/mo (then £{_bb_full_sell:.2f}/mo)")]
    else:
        svc_items = [(f"{bb_provider} - {bb_package}", 1, f"£{svc['bb1_sell']:.2f}/mo")]
    if st.session_state.get("cs_ai_portal_free", False):
        svc_items.append(("AI Integration Portal - 1st month FREE (500 mins)", 1, "£0.00 month 1 only"))
    if second_fttp and second_fttp_pkg:
        bb2_sell = svc["bb2_sell"]
        svc_items.append((f"{bb_provider} - {second_fttp_pkg} (2nd line)", 1, f"£{bb2_sell:.2f}/mo"))
    if total_voice_channels > 0:
        svc_items.append((f"User / Voice Licences x{total_voice_channels}", total_voice_channels, f"£{svc['lic_monthly']:.2f}/mo"))
    if ooh_support:
        svc_items.append(("24/7 OOH Support", 1, "£25.00/mo"))
    if dark_web_mon:
        svc_items.append(("Dark Web Monitoring", 1, "£10.00/mo (after 3m FOC)"))
    if proactive_bb:
        svc_items.append(("Proactive Broadband Management", 1, "£10.00/mo (after 3m FOC)"))
    # Call Scope monthly services
    for _csr in cs_svc_rows:
        if _csr.get("qty", 0) > 0:
            svc_items.append((s(_csr["name"]), _csr["qty"],
                              f"£{_csr['sell']*_csr['qty']:.2f}/mo"))
    # Security tiers
    for _sr in sec_rows:
        if _sr.get("qty", 0) > 0:
            svc_items.append((s(_sr["name"]), _sr["qty"],
                              f"£{_sr['sell']*_sr['qty']:.2f}/mo"))

    pdf.set_fill_color(31, 20, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(100, 6, "Service", fill=True, ln=False)
    pdf.cell(30, 6, "Qty", fill=True, ln=False, align="C")
    pdf.cell(60, 6, "Monthly Charge", fill=True, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    for i, (name, qty, charge) in enumerate(svc_items):
        bg = (248, 249, 255) if i % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*bg)
        pdf.cell(100, 6, f"  {name}", fill=True, ln=False)
        pdf.cell(30, 6, str(qty), fill=True, ln=False, align="C")
        pdf.cell(60, 6, charge, fill=True, ln=True, align="C")

    pdf.set_fill_color(0, 181, 163)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(130, 6, "  TOTAL MONTHLY SERVICE CHARGES", fill=True, ln=False)
    pdf.cell(60, 6, f"£{svc['total_sell']:.2f}/mo", fill=True, ln=True, align="C")
    pdf.set_font("Helvetica","I",7); pdf.set_text_color(128,128,128)
    pdf.multi_cell(pdf.epw,3.5,"* Monthly service charges are subject to standard annual price adjustment in accordance with contractual terms.",align="L")
    pdf.set_text_color(0,0,0)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 8)
    terms = (
        f"Whilst {_CO} have agreed to supply connectivity services, we are not the provider of these services. "
        f"{_CO} can advise on lead times, however you understand that there are circumstances outside of our control "
        f"(for example, if infrastructure is required in your area, or subject to survey), which {_CO} are not liable for. "
        "The broadband speeds stated are estimates only and are dependent on services supplied by third-party network providers. "
        "Actual speeds may vary due to network availability and other external factors.\n\n"
        "NB: the above charges are estimated based on information provided and are subject to an engineer report. "
        "Your first bill will be higher due to part period charges."
    )
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 4.5, terms)
    pdf.ln(6)

    # ── Special Conditions (from consultant notes) ───────────────────────────
    _special_conds = st.session_state.get("c_notes", "").strip()
    if _special_conds:
        pdf.ln(2)
        pdf.set_fill_color(31, 20, 80); pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(0, 6, "  Special Conditions / Agreed Terms", fill=True, ln=True)
        pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", "", 8)
        pdf.set_x(pdf.l_margin)
        pdf.set_fill_color(255, 250, 230)
        pdf.multi_cell(pdf.epw, 4.5, s(_special_conds.replace("-", "-").replace("-", "-")), fill=True, align="J")
        pdf.ln(4)
        pdf.set_fill_color(255, 255, 255)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_font("Helvetica", "B", 9)
    pdf.ln(2)
    _embed_sig(pdf, sig_bytes, signer_name=sig_name,
    company=sig_company, timestamp=sig_timestamp)
    pdf.cell(0, 0.5, "", border="T", ln=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Name & Position: {_contact or '___________________________'}", ln=True)
    pdf.ln(4)
    # -- PAGE 4: LEASE AGREEMENT / QUOTATION SUMMARY --
    pdf.add_page()
    _add_header(pdf, "Equipment Lease Agreement")

    # ── Quotation Includes ────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Quotation Includes", ln=True)
    pdf.ln(1)

    def _qi_row(label, value, bold_val=False):
        pdf.set_fill_color(248, 249, 255)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(120, 6, f"  {label}", fill=True, ln=False)
        pdf.set_font("Helvetica", "B" if bold_val else "", 9)
        pdf.cell(0, 6, str(value), fill=True, ln=True, align="R")

    _settle_str = f"£{termination_cost:.2f}" if termination_cost > 0 else "£0.00"
    _qi_row("Settlements", _settle_str)
    _qi_row("Programmed equipment for self installation", "Yes")
    _qi_row("Full equipment and software listed", "Yes")
    _qi_row("Project management", "Yes")
    _qi_row("Includes 1 year on-site warranty", "Yes")
    pdf.ln(6)

    # ── Equipment Rental Terms ────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Equipment Rental Terms", ln=True)
    pdf.ln(1)

    pdf.set_fill_color(31, 20, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(60, 8, "  Monthly rental period of", fill=True, ln=False)
    pdf.set_fill_color(0, 181, 163)
    pdf.cell(35, 8, f"  £{pl_data['rental']:.2f}", fill=True, ln=False)
    pdf.set_fill_color(31, 20, 80)
    pdf.cell(0, 8, "  plus VAT at the prevailing rate", fill=True, ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # ── Separate billing note ─────────────────────────────────────────────────
    pdf.set_font("Helvetica", "", 8)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 4.5,
    f"Monthly services (hosted licences, broadband, calls) of £{svc['total_sell']:.2f} + VAT "
    f"will be billed separately by {_CO} Ltd under a separate agreement. "
    f"Total monthly commitment: £{total_mo:.2f} + VAT. "
    f"*Fair usage policy applies, subject to terms and conditions.",
    align="J"
    )
    pdf.ln(6)

    # ── Customer confirmation text ────────────────────────────────────────────
    pdf.set_fill_color(248, 249, 255)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 4.5,
    f"I confirm that the above figures are representative of our current average expenditure "
    f"and I understand that I will be billed in line with {_CO} Ltd's current Terms and Conditions. "
    f"I understand that I will be billed separately for the system rental by a 3rd party funder "
    f"and lines, calls, maintenance and broadband by {_CO} Ltd under a separate agreement. "
    f"*Fair usage policy applies, subject to terms and conditions.",
    align="J"
    )
    pdf.ln(8)

    # ── Signature section ─────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, f"For {s(_comp or 'Company Name')}:", ln=True)
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Company Name: {s(_comp or '')}", ln=True)

    if sig_bytes:
        try:
            import tempfile as _tf2, os as _os2
            with _tf2.NamedTemporaryFile(suffix=".png", delete=False) as _stf:
                _stf.write(sig_bytes); _stf_path = _stf.name
            try:
                pdf.image(_stf_path, x=pdf.l_margin, y=pdf.get_y(), h=14)
            finally:
                _os2.unlink(_stf_path)
            pdf.ln(16)
        except Exception:
            pdf.cell(0, 14, "Signed: ________________", ln=True)
    else:
        pdf.cell(0, 14, "Signed: ________________", ln=True)
    pdf.set_font("Helvetica", "", 9)
    _la_contact_raw = sig_name or _contact or ""
    _la_parts = [p.strip() for p in _la_contact_raw.split(" - ", 1)]
    _la_name  = s(_la_parts[0]) if _la_parts[0] else "________________________"
    _la_pos   = s(_la_parts[1]) if len(_la_parts) > 1 else "________________________"
    pdf.cell(0, 5, f"Name: {_la_name}", ln=True)
    pdf.cell(0, 5, f"Position / Title: {_la_pos}", ln=True)
    pdf.cell(0, 5, f"Date: {date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.add_page()
    _add_header(pdf, "Direct Debit Mandate & Customer Checklist")

    if bank_name or acc_no:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, "Direct Debit Banking Mandate", ln=True)
        row2("Bank Name:", _bank or "-", "Account Holder:", _holder or "-")
        row2("Account Number:", _accno or "-", "Sort Code:", _sort or "-")
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 4.5,
        f"By signing this mandate you authorise {_CO} to collect payments by Direct Debit in "
        "accordance with the agreed terms. Payments will be collected on or around the 1st of each month."
        )
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(90, 5, "Authorised Signature:", ln=False)
        pdf.cell(0, 5, "Date:", ln=True)
        pdf.ln(2)
        _embed_sig(pdf, sig_bytes, signer_name=sig_name,
                   company=sig_company, timestamp=sig_timestamp)
        pdf.cell(90, 0.5, "", border="T", ln=False)
        pdf.cell(15, 0.5, "", ln=False)
        pdf.cell(75, 0.5, "", border="T", ln=True)
        pdf.ln(2)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Customer Requirements Checklist", ln=True)
    pdf.set_font("Helvetica", "", 9)
    checklist = [
        "I am aware there may be a delay in switching to the agreed carrier after installation.",
        f"I acknowledge the monthly service charge is £{total_mo:.2f} + VAT per month for {LEASE_TERM_LABELS[lease_term]}.",
        f"I understand {_CO} will only pay the amounts stated toward extricating us from current agreements.",
        "I understand that any 'Special Conditions' are only valid if stated on the Order Form and initialled.",
        "I agree that service charges apply regardless of third-party supplier performance.",
        "I confirm I have received copies of: Support Agreement, Network Service Agreement, Line Rental Agreement, Order Form, Rental Document, and Customer Requirements.",
    ]
    for i, item in enumerate(checklist, 1):
        pdf.set_x(pdf.l_margin)
        pdf.cell(8, 4.5, f"{i}.", ln=False)
        pdf.multi_cell(pdf.epw - 8, 4.5, item)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, f"For {_comp or '(Company Name)'}:", ln=True)
    pdf.ln(2)
    _embed_sig(pdf, sig_bytes, signer_name=sig_name,
               company=sig_company, timestamp=sig_timestamp)
    pdf.cell(90, 0.5, "", border="T", ln=False)
    pdf.cell(15, 0.5, "", ln=False)
    pdf.cell(75, 0.5, "", border="T", ln=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Name & Position: {_contact or '___________________________'}", ln=True)
    pdf.cell(0, 5, f"Date: {date.today()}", ln=True)



    # ── EXCEPTIONAL COMMERCIAL ARRANGEMENT (only when settlement > 0) ──
    if termination_cost > 0:
        # Read rep details from session state (defined in sidebar, not passed as params)
        rep_name     = st.session_state.get("q_rep_name",     "")
        rep_position = st.session_state.get("q_rep_position", "")
        pdf.add_page()
        _add_header(pdf, "Exceptional Commercial Arrangement")
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, "Customer Acknowledgement & Authority to Proceed", ln=True)
        pdf.ln(2)
        def _eca_row(lbl, val=""):
            pdf.set_font("Helvetica", "", 9); pdf.set_fill_color(248,249,255)
            pdf.cell(70, 5, f"  {lbl}", fill=True, ln=False)
            pdf.cell(0, 5, f"  {val}", fill=True, ln=True, border="B")
        def _eca_hdr(title):
            pdf.set_fill_color(31,20,80); pdf.set_text_color(255,255,255)
            pdf.set_font("Helvetica","B",10); pdf.cell(0,6,f"  {title}",fill=True,ln=True)
            pdf.set_text_color(0,0,0)
        _eca_hdr("Customer Details")
        _eca_row("Customer Name", s(_contact or "________________________"))
        _eca_row("Company",       s(_comp    or "________________________"))
        _eca_row("Date",          date.today().strftime("%d/%m/%Y"))
        pdf.ln(2)
        _eca_hdr("Commercial Summary")
        pdf.set_font("Helvetica","B",8); pdf.set_fill_color(210,218,235)
        pdf.cell(0,4,"  Existing Finance Agreements",fill=True,ln=True)
        _eca_row("Current Monthly Lease Payment", f"\xa3{current_system:.2f}" if current_system > 0 else "\xa3________________")
        _eca_row("Total Lease Settlement charges", f"\xa3{termination_cost:.2f}")
        pdf.set_font("Helvetica","B",8); pdf.set_fill_color(210,218,235)
        pdf.cell(0,4,"  New Finance Agreement",fill=True,ln=True)
        _eca_row("Finance Provider",         "Shire Leasing")
        _eca_row("Agreement Term",           LEASE_TERM_LABELS[lease_term])
        _eca_row("Monthly Amount",           f"\xa3{hw_monthly_spread:.2f} + VAT")
        _eca_row("Total Existing Finance to settle", f"\xa3{termination_cost:.2f}")
        pdf.ln(2)
        _eca_hdr("Customer Acknowledgement")
        pdf.set_font("Helvetica","",7.5)
        for n, ack in enumerate([
            f"Telecommunications equipment supplied by {_CO_LEGAL.upper()} are financed under a new finance agreement.",
            "Our existing finance agreement will be terminated early and an early settlement payment is required.",
            "We understand the settlement of our existing finance agreement does not include settlement of any existing contracts for telecom services or maintenance.",
            "We have reviewed the Commercial Summary and confirm it accurately reflects the key commercial terms.",
            "We have had sufficient opportunity to ask questions.",
            "We have had the opportunity to obtain independent legal and/or financial advice.",
            "We are entering into this agreement voluntarily.",
            f"This transaction is our own commercial decision. {_CO_LEGAL.upper()} has not provided legal, financial, tax or accounting advice.",
            f"We authorise {_CO_LEGAL.upper()} to proceed and authorise {_CO_LEGAL} to receive the settlement payment from the new finance provider.",
        ], 1):
            pdf.set_x(pdf.l_margin); pdf.multi_cell(pdf.epw, 3.8, f"{n}.  {s(ack)}", align="J")
        pdf.ln(2)
        _eca_hdr("Customer Initial Confirmation")
        for item in [
            "I understand the Current Lease Settlement Figure.",
            f"I understand the new agreement is for {LEASE_TERM_LABELS[lease_term]}.",
            "I understand the new monthly payment.",
            "I understand the Total Finance Amount.",
            f"I authorise {_CO_LEGAL.upper()} to settle the existing agreement.",
            "I understand this is my company's commercial decision.",
            "I understand any settlement amount may change until confirmed by the finance provider.",
            "I confirm I have authority to enter into this agreement on behalf of the Customer.",
        ]:
            pdf.set_font("Helvetica","",8)
            pdf.set_x(pdf.l_margin)
            # Draw tick box instead of initials/blank
            _bx = pdf.l_margin + 2
            _by = pdf.get_y() + 1
            _bs = 4.5
            pdf.set_draw_color(31, 20, 80)
            pdf.rect(_bx, _by, _bs, _bs)
            pdf.set_draw_color(0, 181, 163)
            pdf.line(_bx + 0.6, _by + 2.2, _bx + 1.7, _by + 3.8)
            pdf.line(_bx + 1.7, _by + 3.8, _bx + 3.9, _by + 0.6)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_x(pdf.l_margin + 10)
            pdf.multi_cell(pdf.epw - 10, 5, s(item))
            pdf.set_x(pdf.l_margin)
        pdf.ln(2)
        _eca_hdr("Final Declaration")
        pdf.set_font("Helvetica","",7.5); pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw,3.8,
            "This document records the exceptional commercial arrangement only and does not amend or replace "
            "the terms of the Commercial Proposal, Service Agreement or Finance Agreement. "
            "We confirm this document, together with the Commercial Proposal, Service Agreement and Finance Agreement, "
            f"accurately reflects the transaction we have chosen to enter into. We authorise {_CO_LEGAL.upper()} to proceed.", align="J")
        pdf.ln(3)
        _eca_hdr("Signatures")
        pdf.ln(1)
        pdf.set_font("Helvetica","B",9)
        pdf.set_font("Helvetica","B",9)
        pdf.cell(0,5,"Customer Signature",ln=True)
        pdf.set_font("Helvetica","",9)
        pdf.cell(80,5,f"Name: {s(_contact or '')}",ln=False)
        pdf.cell(0,5,f"Company: {s(_comp or '')}",ln=True)
        if sig_bytes:
            try:
                import tempfile as _tf2, os as _os2
                with _tf2.NamedTemporaryFile(suffix=".png", delete=False) as _stf:
                    _stf.write(sig_bytes); _stf_path = _stf.name
                try:
                    pdf.image(_stf_path, x=pdf.l_margin, y=pdf.get_y(), h=14)
                finally:
                    _os2.unlink(_stf_path)
                pdf.ln(16)
            except Exception: pdf.cell(0,14,"Signature: ________________",ln=True)
        else:
            pdf.cell(0,14,"Signature: ________________",ln=True)
        pdf.cell(0,5,f"Date: {date.today().strftime('%d/%m/%Y')}",ln=True)
        pdf.ln(2)
        pdf.set_font("Helvetica","I",7); pdf.set_text_color(128,128,128)
        pdf.multi_cell(pdf.epw,3.5,"I confirm that I am authorised to sign this agreement on behalf of the Customer.",align="C")
        pdf.set_text_color(0,0,0)

    # ── ON-SITE WARRANTY FORM ─────────────────────────────────────────────────
    pdf.add_page()
    _add_header(pdf, "On-Site Warranty Agreement")

    # Maintenance monthly charge from P&L: (hw_buy × 1.5 × 0.2) / 12
    _maint_monthly = round(pl_data.get("maintenance_annual", 0) / 12, 2)

    # Customer details
    pdf.set_font("Helvetica","B",10)
    pdf.set_fill_color(31,20,80); pdf.set_text_color(255,255,255)
    pdf.cell(0,6,"  Customer Details",fill=True,ln=True)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Helvetica","",9)
    pdf.set_fill_color(248,249,255)
    def _w_row(lbl, val):
        pdf.cell(60,5,f"  {lbl}:",fill=True,ln=False)
        pdf.cell(0,5,f"  {s(val)}",fill=True,ln=True,border="B")
    _w_row("Customer Name",   _comp or "")
    _w_row("Address",         _addr or "")
    _w_row("Date",            date.today().strftime("%d/%m/%Y"))
    pdf.ln(4)

    # Equipment list
    pdf.set_fill_color(31,20,80); pdf.set_text_color(255,255,255)
    pdf.set_font("Helvetica","B",10)
    pdf.cell(0,6,"  Equipment Covered",fill=True,ln=True)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Helvetica","B",8)
    pdf.set_fill_color(210,218,235)
    pdf.cell(95,5,"  Item",fill=True,ln=False)
    pdf.cell(45,5,"Qty",fill=True,ln=False,align="C")
    pdf.cell(0,5,"Billing",fill=True,ln=True,align="C")
    pdf.set_font("Helvetica","",8)
    _cs_names = {r["name"] for r in cs_svc_rows}  # exclude CS software from warranty
    for _name, _qty, _billing in all_equip_pdf:
        _is_cs       = _name in _cs_names or "Call Scope" in _name
        _is_svc_line = (_name.startswith("Broadband -") or
                        _name.startswith("User / Voice Licences") or
                        "Mobile" in _name or
                        _name.startswith("IT:"))
        if _qty > 0 and not _is_cs and not _is_svc_line:
            pdf.set_fill_color(248,249,255)
            pdf.cell(95,5,f"  {s(_name)}",fill=True,ln=False)
            pdf.cell(45,5,str(_qty),fill=True,ln=False,align="C")
            pdf.cell(0,5,s(_billing),fill=True,ln=True,align="C")
    pdf.ln(4)

    # Warranty terms
    pdf.set_fill_color(31,20,80); pdf.set_text_color(255,255,255)
    pdf.set_font("Helvetica","B",10)
    pdf.cell(0,6,"  Warranty Terms",fill=True,ln=True)
    pdf.set_text_color(0,0,0); pdf.set_font("Helvetica","",8.5)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw,4,
        f"{_CO_LEGAL} agrees to provide on-site warranty cover including remote diagnostics "
        f"and programming of faults to the equipment listed above for an agreement term of "
        f"{LEASE_TERM_LABELS[lease_term]}. "
        f"Faulty equipment will be repaired or replaced. Additional equipment added will be "
        f"charged and warranty premium will be added to this agreement.",align="J")
    pdf.ln(2)

    # Inclusive period + monthly charge highlight
    pdf.set_fill_color(0,181,163); pdf.set_text_color(255,255,255)
    pdf.set_font("Helvetica","B",9)
    pdf.cell(0,7,f"  Inclusive Period: 12 months  |  Monthly charge after inclusive period: £{_maint_monthly:.2f} + VAT",
             fill=True,ln=True,align="C")
    pdf.set_text_color(0,0,0)
    pdf.ln(2)

    # Tier level
    pdf.set_font("Helvetica","B",9)
    pdf.cell(0,5,"Tier 1 Support Includes:",ln=True)
    pdf.set_font("Helvetica","",8.5)
    pdf.cell(0,5,"  [X]  Remote diagnostics and programming",ln=True)
    pdf.cell(0,5,"  [X]  Engineer call-outs for repair or replacement of equipment",ln=True)
    pdf.set_font("Helvetica","I",8)
    pdf.set_text_color(120,120,120)
    pdf.cell(0,5,"  Note: Excludes additional equipment added to the system in future.",ln=True)
    pdf.set_text_color(0,0,0)
    pdf.ln(3)

    # Declaration
    pdf.set_fill_color(31,20,80); pdf.set_text_color(255,255,255)
    pdf.set_font("Helvetica","B",10)
    pdf.cell(0,6,"  Declaration",fill=True,ln=True)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Helvetica","",8)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw,4,
        f"{_CO_LEGAL} agrees to provide remote and on-site maintenance cover for the equipment above "
        "at the tier level set out above and the customer agrees to pay the monthly charge as set out "
        "above for the Agreement Term, subject to the terms and conditions. As a duly authorised "
        "representative of the customer, I confirm that I have read, understood and accept the terms "
        "and conditions of this agreement.",align="J")
    pdf.ln(4)

    # Signature
    pdf.set_font("Helvetica","B",9)
    pdf.cell(0,5,"On Behalf of (The Customer):",ln=True)
    pdf.set_font("Helvetica","",9)
    pdf.cell(80,5,f"Name & Position: {s(_contact or '')}",ln=False)
    pdf.cell(0,5,f"Date: {date.today().strftime('%d/%m/%Y')}",ln=True)
    if sig_bytes:
        try:
            import tempfile as _tf2, os as _os2
            with _tf2.NamedTemporaryFile(suffix=".png", delete=False) as _stf:
                _stf.write(sig_bytes); _stf_path = _stf.name
            try:
                pdf.image(_stf_path, x=pdf.l_margin, y=pdf.get_y(), h=14)
            finally:
                _os2.unlink(_stf_path)
            pdf.ln(16)
        except Exception:
            pdf.cell(0,14,"Signed: ________________",ln=True)
    else:
        pdf.cell(0,14,"Signed: ________________",ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica","I",7.5); pdf.set_text_color(80,80,80)
    pdf.cell(0,4,"Annual price review applies after inclusive period. Subject to standard Terms & Conditions.",ln=True,align="C")
    pdf.set_text_color(0,0,0)

    # ── CUSTOMER REQUIREMENT FORM ────────────────────────────────────────────
    pdf.add_page()
    # Header
    pdf.set_font("Helvetica","B",11)
    pdf.cell(0,5,"CUSTOMER REQUIREMENT FORM",ln=True,align="C")
    pdf.ln(1)
    pdf.set_font("Helvetica","",8)
    pdf.set_text_color(100,100,100)
    pdf.multi_cell(0,4,f"{_CO_LEGAL} are committed to the very highest levels of customer care. This Questionnaire "
        "is essential for our understanding of your needs and therefore satisfaction with our services.",align="C")
    pdf.set_text_color(0,0,0)
    pdf.ln(2)

    # Helper functions
    def _crf_tick(checked=False):
        return "[X]" if checked else "[ ]"

    def _crf_q(num, text, has_yn=False, yn=None, extra=""):
        pdf.set_font("Helvetica","B",8)
        pdf.set_fill_color(245,247,255)
        pdf.cell(8,5,str(num),fill=True,ln=False)
        pdf.set_font("Helvetica","",7.5)
        pdf.set_x(pdf.l_margin+8)
        if has_yn:
            _yn_start_y = pdf.get_y()
            pdf.multi_cell(pdf.epw-28,3.5,s(text))
            _yn_end_y = pdf.get_y()
            # Place Yes/No at the top-right aligned with question start
            pdf.set_xy(pdf.w - pdf.r_margin - 26, _yn_start_y)
            pdf.cell(13,3.5,f"Yes {_crf_tick(yn==True)}",ln=False,align="C")
            pdf.cell(13,3.5,f"No  {_crf_tick(yn==False)}",ln=False,align="C")
            pdf.set_y(_yn_end_y)
        else:
            pdf.multi_cell(pdf.epw-8,4,s(text))
        if extra:
            pdf.set_x(pdf.l_margin+8)
            pdf.set_font("Helvetica","I",7)
            pdf.set_text_color(120,120,120)
            pdf.multi_cell(pdf.epw-8,3.8,s(extra))
            pdf.set_text_color(0,0,0)
        pdf.ln(1)

    # Y/N header
    pdf.set_font("Helvetica","",7.5)
    pdf.ln(1)

    _bb_desc = f"{bb_provider} {bb_package}" if svc["bb_sell"]>0 else "None / Customer Supplied"
    _vc_desc = str(total_voice_channels)

    _crf_q(1,"I currently have a PDQ line that connects to a Bank or Post office. (Yes / No)")
    _crf_q(2,"I currently have a Redcare, or similar alarm system connected to a telephone line. "
             "I understand that liaison with the alarm company is my responsibility. (Yes / No)",
             extra="If alarm works via the main system lines then a new standalone line may need to be added.")
    _crf_q(3,f"This agreement includes: {_vc_desc} voice channels and {_bb_desc} broadband service(s) as agreed. "
             "Additional services will be added at our standard tariffs.")
    _crf_q(4,f"I am aware, if we have signed up for {_CO_LEGAL} line provision, a single figure code such as '9' "
             "must be used to make external calls. Other methods may result in these calls being charged by other providers.")
    _crf_q(5,f"I can confirm that I currently have {num_employees or '______'} employees")
    _crf_q(6,f"{_CO_LEGAL} are unable to make any representations to any carrier or service provider on our behalf. "
             f"I appreciate that {_CO_LEGAL} can provide advice, but understand that any correspondence with current providers is ultimately our responsibility.")
    _crf_q(7,"I am aware that there may be a delay in switching chosen carrier after installation has taken place "
             "and that calls during this period may be routed through your existing provider.")
    _crf_q(8,"I understand that in the event that our telephone numbers do not exist within the BT network, "
             f"Cloud5 Comms Network Services Ltd cannot guarantee that they will be ported to the {_CO_LEGAL} Network.")
    _crf_q(9,"I am aware that the engineer will conduct a physical line check on site to help identify all available lines "
             "coming into the premises. It is ultimately my responsibility to ensure all lines are accounted for.")
    if termination_cost > 0:
        _crf_q(10,f"We acknowledge that in entering into the above agreement you have agreed to not only rent new equipment "
                 f"supplied by {_CO_LEGAL}, but also settlement of an existing agreement to the maximum sum of: "
                 f"£{termination_cost:.2f} as per the figure agreed on the order forms.")
    else:
        _crf_q(10,"We acknowledge that in entering into the above agreement you have agreed to rent new equipment "
                 f"supplied by {_CO_LEGAL} as per the figure agreed on the order forms.")
    _crf_q(11,"I have confirmed the number of months remaining on existing contracts to the sales consultant")
    _crf_q(12,"I understand that only the cash back for ETC charges agreed & listed on the order forms will be paid "
             f"by {_CO_LEGAL} upon receipt of a copy invoice & contract from the previous supplier")
    _crf_q(13,f"I understand that any 'Special Conditions' agreed by {_CO_LEGAL} representative may not be considered "
             f"valid by {_CO_LEGAL} unless stated on the Order Form and clearly initialled by their representative.")
    _crf_q(14,"I understand that UK Local, UK National and UK Mobile call costs only have been accounted for on my "
             f"call cost proposal with {_CO_LEGAL}")
    _crf_q(15,f"I understand that if I do not take {_CO_LEGAL} mobiles after my current contract ends "
             f"{_CO_LEGAL} cannot guarantee the mobile savings.")
    _crf_q(16,"I agree that the rentals due under the Rental Agreement have been calculated based on the full purchase "
             "price of the Equipment. We agree and accept that our obligation to pay the Rentals in full on their due "
             "dates without reduction, deduction, withholding, or offset whatsoever, shall apply notwithstanding any "
             "failure on the part of the Supplier or the Equipment.")
    _crf_q(17,f"I fully understand that {_CO_LEGAL} will be and will at all times remain solely responsible for "
             "providing any maintenance or service provision in respect of the Equipment in a separate agreement. "
             "We are fully aware that if the Supplier stops providing maintenance for any reason we must fully "
             "comply with all obligations under the Rental Agreement to keep the Equipment maintained.")
    _crf_q(18,f"I understand that due to the data protection act, {_CO_LEGAL} have no authority to cancel any "
             "existing agreements with 3rd party suppliers. I am aware that (where applicable) it is my responsibility "
             "to cancel any existing agreements.")
    _crf_q(19,"Any settlement charges other than those on the Order Form can only be settled with supporting contracts "
             f"from existing providers which must be provided to {_CO_LEGAL} on request.")
    _crf_q(20,f"I understand that due to current trading climate {_CO_LEGAL} may require supportive additional "
             "financial information prior to installation.")
    _crf_q(22,f"I have provided a copy of bills relevant to the new services to be provided by {_CO_LEGAL}.")
    _crf_q(23,"I am fully aware that the CTI (screen popping) may not fully integrate with my current database "
             "and that screen popping may not be possible.")

    # Received forms checklist
    pdf.ln(2)
    pdf.set_font("Helvetica","I",8)
    pdf.multi_cell(0,4,"I have been explained in detail the following forms and am in receipt of copies for: (tick as appropriate)",align="L")
    pdf.ln(1)
    _forms = [
        ("This Form","[X]"),("Order Form","[X]"),("Terms & Conditions","[X]"),
        ("Quotation - inc. tariff","[X]"),("Rental Document","[X]"),("Network Service Agreement","[X]"),
        ("On Site Maintenance Agreement","[X]"),
    ]
    pdf.set_font("Helvetica","",8)
    _fc = st.columns if False else None  # PDF only - use cells
    for i in range(0,len(_forms),3):
        for label,tick in _forms[i:i+3]:
            pdf.cell(65,5,f"{tick}  {label}",ln=False)
        pdf.ln(5)

    # Declaration & signature
    pdf.ln(3)
    pdf.set_font("Helvetica","",8)
    pdf.multi_cell(0,4,"I declare that, to the best of my knowledge, the above statements are true.",align="L")
    pdf.ln(3)
    pdf.set_font("Helvetica","B",9)
    pdf.cell(0,5,"For & on Behalf of (The Customer)",ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica","",9)
    pdf.cell(90,5,f"Name & Position: {s(_contact or '')} {s(_btype or '')}",ln=False)
    pdf.cell(0,5,f"Date: {date.today().strftime('%d/%m/%Y')}",ln=True)
    if sig_bytes:
        try:
            import tempfile as _tf2, os as _os2
            with _tf2.NamedTemporaryFile(suffix=".png", delete=False) as _stf:
                _stf.write(sig_bytes); _stf_path = _stf.name
            try:
                pdf.image(_stf_path, x=pdf.l_margin, y=pdf.get_y(), h=14)
            finally:
                _os2.unlink(_stf_path)
            pdf.ln(16)
        except Exception:
            pdf.cell(0,14,"Signed: ________________",ln=True)
    else:
        pdf.cell(0,14,"Signed: ________________",ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica","I",7.5)
    pdf.set_text_color(80,80,80)
    pdf.multi_cell(0,3.8,s(f"{_CO_LEGAL} confirm that any financial information given will be treated with utmost confidentiality."),align="C")
    pdf.set_text_color(0,0,0)

    # ── TERMS & CONDITIONS PAGE ──────────────────────────────────────
    pdf.add_page()
    _add_header(pdf, "Terms & Conditions - Network Services")

    _tc_sections = [
        ("1. DEFINITIONS", f"Contract means these terms and the Order. Charges are payable under clause 10. Initial Term means 12 months from Start Date. Extended Term means any 12-month renewal per clause 3. We/us means {_CO_LEGAL}. You means the customer in the Order."),
        ("3. DURATION & AUTOMATIC RENEWAL", "This contract automatically extends for 12 months at the end of the Minimum Term and each Extended Term unless 90 days written notice is given. You may add Services at any time."),
        ("4. SERVICES", "We provide Services with reasonable skill and care. We do not warrant uninterrupted or error-free service. Service Failures must be reported via our Helpdesk."),
        ("6. USE OF SERVICES", "Services are for business use only and must comply with our Acceptable Use Policy. You must not use Services to breach any law, compromise network security, or degrade service to other customers."),
        ("10. CHARGES AND PAYMENT", "All Charges exclude VAT. Invoices due within 14 days. Late payment fee £25 after 7 days. DD cancellation fee £50. Annual price increase up to 5% with 30 days notice. Rental invoiced in advance; calls in arrears. Port/activation: £25+VAT per CLI. Engineer callout: min £250+VAT. Remote changes: £35+VAT. Call recording: included 12 months then £20/month+VAT."),
        ("12. LIABILITY", "No liability for loss of profits, business opportunity, goodwill or indirect loss. Total liability capped at Charges paid in prior 12 months. Nothing limits liability for death or fraud."),
        ("13. CANCELLATION", "90 days notice required. Cancellation during term incurs Cancellation Charge. Introductory credits repayable on early exit. Subsidised early termination charges repayable pro-rata."),
        ("15. TERMINATION FEES", "On termination all invoices become immediately due; Equipment must be returned. Cancellation fee: £299+VAT per CLI. Port-away: £15+VAT per number. Account closure: £250+VAT. We may terminate for non-payment (7+ days), unremedied breach, or insolvency."),
        ("16. CONFIDENTIALITY", "Each party protects the other's confidential information with reasonable care for 3 years."),
        ("20. GENERAL", "This Contract is the whole agreement between us, governed by English law. We may vary terms on notice. You may not assign without our prior written consent. Subject to the exclusive jurisdiction of the English courts."),
    ]
    for _sec_title, _sec_text in _tc_sections:
        pdf.ln(2)
        pdf.set_fill_color(31, 20, 80); pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(0, 5, f"  {_sec_title}", fill=True, ln=True)
        pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", "", 7)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 3.8, s(_sec_text), align="J")
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 6.5); pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(pdf.epw, 3.5,
        "This is a summary of key terms. Full Terms & Conditions available at https://sycomms.co.uk/terms-conditions "
        "- by signing below you confirm you have read, understood and agree to the full Terms & Conditions at the link above.",
        align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # ── T&C Confirmation Signature ────────────────────────────────────────────
    pdf.set_fill_color(31, 20, 80); pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(0, 6, "  Confirmation - I have read and agree to the full Terms & Conditions", fill=True, ln=True)
    pdf.set_text_color(0, 0, 0); pdf.ln(3)
    pdf.set_font("Helvetica", "", 8)
    _tc_half = pdf.epw / 2
    # Split "Name - Position" from the contact field
    _tc_contact_raw = sig_name or _contact or ""
    _tc_parts   = [p.strip() for p in _tc_contact_raw.split(" - ", 1)]
    _tc_name    = s(_tc_parts[0]) if _tc_parts[0] else "________________________"
    _tc_pos     = s(_tc_parts[1]) if len(_tc_parts) > 1 else "________________________"
    # Row 1: Name + Company
    pdf.cell(_tc_half, 5.5, f"Name:     {_tc_name}", ln=False)
    pdf.cell(_tc_half, 5.5, f"Company:  {s(_comp or '________________________')}", ln=True)
    pdf.ln(1)
    # Row 2: Date (pre-filled) + Position/Title (split from contact field)
    pdf.cell(_tc_half, 5.5, f"Date:     {date.today().strftime('%d/%m/%Y')}", ln=False)
    pdf.cell(_tc_half, 5.5, f"Position / Title:  {_tc_pos}", ln=True)
    pdf.ln(4)
    # Signature row — stamp if captured, else blank line
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(40, 5, "Signature:", ln=False)
    if sig_bytes:
        try:
            import tempfile as _tf_tc, os as _os_tc
            with _tf_tc.NamedTemporaryFile(suffix=".png", delete=False) as _stc:
                _stc.write(sig_bytes); _stc_path = _stc.name
            try:
                pdf.image(_stc_path, x=pdf.get_x(), y=pdf.get_y() - 1, h=12)
            finally:
                _os_tc.unlink(_stc_path)
            pdf.ln(14)
        except Exception:
            pdf.cell(0, 14, "________________________________", ln=True)
    else:
        pdf.cell(0, 14, "________________________________", ln=True)
    pdf.set_text_color(0, 0, 0)

    # ── AUDIT CERTIFICATE PAGE - DocuSign-style ─────────────────────────────
    if sig_bytes and sig_timestamp:
        import uuid as _uuid, hashlib as _hl
        from datetime import datetime as _dt

        _envelope_id = str(_uuid.uuid4()).upper()
        _doc_hash    = _hl.sha256(sig_bytes).hexdigest().upper()
        _signed_at   = sig_timestamp
        _sent_at     = _signed_at  # same session
        _signer_name = sig_name or "Customer"
        _signer_co   = sig_company or _comp or "-"
        _signer_email= _demail or _bemail or "-"
        _signer_ip   = sig_ip or "Not captured"
        _orig_email  = cfg.get("email", {}).get("username", "hello@sycomms.co.uk")

        # ── Helper functions ──────────────────────────────────────────────────
        def _section(title):
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(220, 235, 245)
            pdf.set_text_color(13, 46, 74)
            pdf.cell(0, 6, f"  {title}", fill=True, ln=True)
            pdf.set_text_color(0, 0, 0)

        def _row3(c1, c2, c3, h=5.5, bold1=False):
            """Three-column table row."""
            pdf.set_font("Helvetica", "B" if bold1 else "", 8)
            pdf.cell(65, h, c1, border="B", ln=False)
            pdf.set_font("Helvetica", "", 8)
            pdf.cell(65, h, c2, border="B", ln=False)
            pdf.cell(0,  h, c3, border="B", ln=True)

        def _kv(label, value, lw=52):
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(lw, 5.5, label, ln=False)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 5.5, str(value), ln=True)

        pdf.add_page()

        # ── Page header (light - no logo for certificate page) ────────────────
        pdf.set_fill_color(31, 20, 80)
        pdf.rect(0, 0, 210, 22, "F")
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_y(5)
        pdf.cell(0, 6, "CERTIFICATE OF COMPLETION", ln=True, align="C")
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 5, s(f"{_CO}  |  Electronic Signing Record"), ln=True, align="C")
        pdf.set_fill_color(0, 180, 216)
        pdf.rect(0, 22, 210, 1.5, "F")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(8)

        # ── Envelope summary grid ─────────────────────────────────────────────
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(13, 46, 74)
        lx = pdf.l_margin
        pdf.cell(0, 6, "Envelope Summary", ln=True)
        pdf.set_draw_color(0, 180, 216)
        pdf.set_line_width(0.4)
        pdf.line(lx, pdf.get_y(), 195, pdf.get_y())
        pdf.set_line_width(0.2)
        pdf.set_draw_color(200, 200, 200)
        pdf.ln(2)

        def _env_row(l, v, color=(0,0,0)):
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(52, 5.5, l, ln=False)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*color)
            pdf.cell(0, 5.5, str(v)[:70], ln=True)
            pdf.set_text_color(0, 0, 0)

        _env_row("Envelope ID:", _envelope_id)
        _env_row("Status:", "COMPLETED", color=(0, 140, 70))
        _env_row("Subject:", s(f"{_CO} Proposal - {_signer_co[:40]}"))
        _env_row("Originator:", s(_CO))
        _env_row("Document Pages:", "4   |   Signatures: 3")
        _env_row("Time Zone:", "(UTC+00:00) Dublin, Edinburgh, Lisbon, London")
        _env_row("Originator Email:", _orig_email)
        pdf.ln(4)

        # ── Record Tracking ───────────────────────────────────────────────────
        _section("Record Tracking")
        pdf.ln(1)
        _row3("Status", "Holder", "Location", bold1=True)
        _row3("Original", s(_CO), s(_CO_TAG))
        _row3(_sent_at, _orig_email, "Streamlit Cloud")
        pdf.ln(4)

        # ── Signer Events ─────────────────────────────────────────────────────
        _section("Signer Events")
        pdf.ln(1)
        _row3("Signer Details", "Signature", "Timestamps", bold1=True)

        # Left: signer info
        y_row = pdf.get_y()
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(65, 5, _signer_name, ln=False)
        pdf.set_font("Helvetica", "", 8)
        # Middle: signature image
        if sig_bytes:
            try:
                import tempfile as _tf3, os as _os3
                with _tf3.NamedTemporaryFile(suffix=".png",delete=False) as _atf:
                    _atf.write(sig_bytes); _atf_path=_atf.name
                _s_buf2 = open(_atf_path,"rb")
                pdf.image(_s_buf2, x=lx + 67, y=y_row, w=60, h=18)
            except Exception:
                pass
        # Right: timestamps
        pdf.set_xy(lx + 135, y_row)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.cell(0, 5, f"Sent:   {_sent_at}", ln=True)
        pdf.set_xy(lx + 135, y_row + 5)
        pdf.cell(0, 5, f"Viewed: {_sent_at}", ln=True)
        pdf.set_xy(lx + 135, y_row + 10)
        pdf.cell(0, 5, f"Signed: {_signed_at}", ln=True)

        pdf.set_y(y_row + 1)
        pdf.set_x(lx)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(65, 5, _signer_email, ln=True)
        pdf.set_x(lx)
        pdf.cell(65, 5, _signer_co, ln=True)
        pdf.set_x(lx)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(65, 5, "Security: In-person, Device", ln=True)
        pdf.set_x(lx)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.cell(65, 5, f"Using IP: {_signer_ip}", ln=True)
        pdf.set_x(lx)
        pdf.cell(65, 5, "Signature Adoption: Hand-drawn (in person)", ln=True)
        pdf.ln(2)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(lx, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(4)

        # ── Carbon Copy Events ────────────────────────────────────────────────
        _section("Carbon Copy Events")
        pdf.ln(1)
        _row3("Recipient", "Status", "Timestamps", bold1=True)
        _row3(_orig_email, "COPIED", f"Sent: {_sent_at}")
        pdf.ln(4)

        # ── Envelope Summary Events ───────────────────────────────────────────
        _section("Envelope Summary Events")
        pdf.ln(1)
        _row3("Event", "Status", "Timestamp", bold1=True)
        _row3("Envelope Sent",      "Hashed / Encrypted",   _sent_at)
        _row3("Certified Delivered","Security Checked",      _sent_at)
        _row3("Signing Complete",   "Security Checked",      _signed_at)
        _row3("Completed",          "Security Checked",      _signed_at)
        pdf.ln(4)

        # ── Document Integrity ────────────────────────────────────────────────
        _section("Document Integrity")
        pdf.ln(2)
        _kv("Document Hash (SHA-256):", _doc_hash[:40])
        _kv("Signing Method:",          "In-person electronic signature")
        _kv("Platform:",                "SY Comms Quotation Tool - Streamlit Cloud")
        _kv("Full Envelope ID:",        _envelope_id)
        pdf.ln(4)

        # ── Disclaimer ────────────────────────────────────────────────────────
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(120, 120, 120)
        pdf.set_x(lx)
        pdf.multi_cell(pdf.epw, 4,
            "This certificate serves as an electronic record confirming that the above-named "
            "signer reviewed and signed the attached documentation. The timestamp, IP address and "
            "signature were recorded at the moment of signing by the SY Comms Quotation "
            "Tool. This record constitutes a valid electronic agreement under the Electronic "
            "Communications Act 2000 and eIDAS Regulation (EU) 910/2014."
        )


    return bytes(pdf.output())


def _embed_sig(pdf_obj, sig_bytes, x=15, w=65, h=20,
               signer_name="", company="", timestamp=""):
    """Render signature + metadata in the LEFT customer column only.
    Layout:
      [image if available]
      Signed: Name | Company | Date  (italic, left-aligned, below image)
    Then the signature underline is drawn by the caller.
    """
    if not (sig_bytes or signer_name):
        return
    try:
        y_start = pdf_obj.get_y()
        if sig_bytes and len(sig_bytes) > 100:  # skip placeholder/corrupt bytes
            try:
                import tempfile, os as _os
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as _tf:
                    _tf.write(sig_bytes)
                    _tmp_sig_path = _tf.name
                try:
                    pdf_obj.image(_tmp_sig_path, x=x, y=y_start, w=w, h=h)
                    pdf_obj.set_y(y_start + h + 1)
                finally:
                    _os.unlink(_tmp_sig_path)
            except Exception:
                pass  # image unreadable - skip, show name only

        # Metadata - always in left column (x=15), max 90mm wide
        pdf_obj.set_font("Helvetica", "I", 8)
        pdf_obj.set_text_color(80, 80, 80)
        for line in [
            f"Signed: {signer_name}",
            f"Company: {company}",
            f"Date/Time: {timestamp}",
        ]:
            if line.split(": ", 1)[1]:          # only print if value exists
                pdf_obj.set_x(x)
                pdf_obj.cell(90, 5, line, ln=True)
        pdf_obj.set_text_color(0, 0, 0)
        pdf_obj.ln(2)
    except Exception:
        pass



# ─── EMAIL SEND HELPER ───────────────────────────────────────────────────────
def send_proposal_email(em_cfg, to_addr, cc_addr, pdf_bytes, filename, customer, total):
    """Send the signed PDF via SMTP. Returns (success, message)."""
    if not em_cfg.get("username") or not em_cfg.get("password"):
        return False, "Email not configured - add SMTP credentials in Admin - Email."
    try:
        msg = MIMEMultipart()
        from_str = f"{em_cfg['from_name']} <{em_cfg['username']}>"
        msg["From"]    = from_str
        msg["To"]      = to_addr
        msg["Subject"] = f"Your {_CO} Proposal - {customer or 'Telecoms Quote'}"
        if cc_addr:
            msg["Cc"] = cc_addr
        if em_cfg.get("reply_to"):
            msg["Reply-To"] = em_cfg["reply_to"]

        body = MIMEText(f"""
        <html><body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:0 auto">
          <div style="background:#1f1450;padding:20px 30px;border-radius:8px 8px 0 0">
            <h2 style="color:#fff;margin:0"><span style="color:#00b5a3">Novalink</span> Hardware</h2>
            <p style="color:rgba(255,255,255,0.6);margin:4px 0 0">Telecoms Quotation</p>
          </div>
          <div style="background:#f9f9f9;padding:24px 30px;border:1px solid #e8e8e8;border-top:none">
            <p>Dear {customer or "Valued Customer"},</p>
            <p>Thank you for your time. Please find attached your signed telecoms proposal for review.</p>
            <table style="width:100%;border-collapse:collapse;margin:16px 0">
              <tr style="background:#1f1450;color:#fff">
                <td style="padding:8px 12px;border-radius:4px 0 0 4px"><strong>Total Monthly</strong></td>
                <td style="padding:8px 12px;border-radius:0 4px 4px 0;text-align:right"><strong>£{total:.2f} + VAT</strong></td>
              </tr>
            </table>
            <p>If you have any questions please don't hesitate to get in touch.</p>
            <p style="margin-top:24px">Kind regards,<br/><strong>{em_cfg["from_name"]}</strong></p>
          </div>
          <div style="background:#e8e8e8;padding:10px 30px;font-size:11px;color:#888;border-radius:0 0 8px 8px">
            All figures exclude VAT. Subject to survey and credit approval.
          </div>
        </body></html>""", "html")
        msg.attach(body)

        # Attach PDF
        part = MIMEBase("application", "octet-stream")
        part.set_payload(pdf_bytes)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)

        recipients = [r.strip() for r in [to_addr, cc_addr] if r and r.strip()]
        with smtplib.SMTP(em_cfg["smtp_host"], int(em_cfg["smtp_port"])) as srv:
            srv.ehlo()
            srv.starttls()
            srv.ehlo()
            srv.login(em_cfg["username"], em_cfg["password"])
            srv.sendmail(em_cfg["username"], recipients, msg.as_string())
        return True, f"✅ Email sent to {to_addr}"
    except smtplib.SMTPAuthenticationError as e:
        hint = ""
        if "5.7.8" in str(e) or "BadCredentials" in str(e):
            hint = (
                "\n\nGmail fix - do all 3 steps:\n"
                "1. Go to myaccount.google.com - Security\n"
                "2. Turn ON 2-Step Verification\n"
                "3. Go to myaccount.google.com/apppasswords - create a new App Password\n"
                "4. Paste that new 16-char password into Admin - Email - App Password"
            )
        return False, f"❌ Gmail authentication failed.{hint}"
    except Exception as e:
        return False, f"❌ Email failed: {e}"


# ── Admin panel variable defaults (overridden inside tab7 when unlocked) ──────
# These must be defined before tabs so tab1-tab6 can reference them safely.
# Values are read from session state where widgets write them.
override_customer       = st.session_state.get("mgr_cust", "")
override_initials       = st.session_state.get("mgr_init", "")
override_monthly_lease  = 0.0
override_bb_sell        = float(st.session_state.get("adm_bb_override", 0.0))
override_upfront        = float(st.session_state.get("adm_override_upfront", 0.0))
override_install_cost   = float(st.session_state.get("adm_override_install", 0.0))
credits_months          = int(st.session_state.get("adm_credits_months", 0))
credits_amount          = float(st.session_state.get("adm_credits_amount", 0.0))
cashback_amount         = float(st.session_state.get("adm_cashback", 0.0))


# ─── CALCULATIONS ENGINE (Recurring model - hardware upfront, services monthly) ─

def compute_poe_needed():
    poe = 0
    for name, qty in desktop_quantities.items():
        if HANDSETS_DESKTOP[name]["poe"]:
            poe += qty
    poe += additional_wired_ports
    return poe

def get_recommended_switch(poe_needed):
    if not auto_switch and manual_switch_name:
        return next((s for s in SWITCHES if s["name"] == manual_switch_name), SWITCHES[0])
    # Each desk phone needs 1 POE port (for phone) + 1 standard port (for PC)
    # Total ports needed = poe_needed (phones) + poe_needed (PCs)
    total_ports_needed = poe_needed * 2
    for sw in SWITCHES:
        if sw["poe_ports"] >= poe_needed and sw.get("total_ports", sw["poe_ports"]) >= total_ports_needed:
            return sw
    return SWITCHES[-1]

def compute_hw_buy():
    """Sum of all hardware at wholesale buy price."""
    total = 0.0
    for name, qty in desktop_quantities.items():
        total += HANDSETS_DESKTOP[name]["buy"] * qty
    for name, qty in cordless_quantities.items():
        total += HANDSETS_CORDLESS[name]["buy"] * qty
    for name, qty in headset_quantities.items():
        total += HEADSETS[name]["buy"] * qty
    for name, qty in other_quantities.items():
        _oh_info = OTHER_HARDWARE.get(name)
        if _oh_info: total += _oh_info["buy"] * qty
    if not _no_switch:
        if switch_quantities:  # manual multi-switch
            for _sn, _sq in switch_quantities.items():
                _si = next((s for s in SWITCHES if s["name"] == _sn), None)
                if _si: total += _si["buy"] * _sq
        else:  # auto-select
            poe_n = compute_poe_needed()
            total += get_recommended_switch(poe_n)["buy"]
    if add_router:
        if router_quantities:
            for _rn, _rq in router_quantities.items():
                if _rn in ROUTERS: total += ROUTERS[_rn] * _rq
        elif router_type not in ("None / Customer Supplied", "") and router_type in ROUTERS:
            total += ROUTERS[router_type]
    return total

def compute_hw_sell(uplift_pct=None):
    """Compute total hardware sell value.
    Falls back to buy x (1 + uplift/100) for items without a sell price."""
    if uplift_pct is None:
        uplift_pct = hw_uplift_override
    total = 0.0
    for name, qty in desktop_quantities.items():
        info = HANDSETS_DESKTOP[name]
        sell = info.get("sell", info["buy"] * (1 + hw_uplift_override / 100))
        total += sell * qty
    for name, qty in cordless_quantities.items():
        info = HANDSETS_CORDLESS[name]
        sell = info.get("sell", info["buy"] * (1 + hw_uplift_override / 100))
        total += sell * qty
    for name, qty in headset_quantities.items():
        info = HEADSETS[name]
        sell = info.get("sell", info["buy"] * (1 + hw_uplift_override / 100))
        total += sell * qty
    for name, qty in other_quantities.items():
        _oh_info2 = OTHER_HARDWARE.get(name)
        if _oh_info2:
            sell = _oh_info2.get("sell", _oh_info2["buy"] * (1 + hw_uplift_override / 100))
            total += sell * qty
    # Switch and router use uplift (no item-specific sell price stored)
    if not _no_switch:
        if switch_quantities:
            for _sn, _sq in switch_quantities.items():
                _si = next((s for s in SWITCHES if s["name"] == _sn), None)
                if _si: total += _si["buy"] * (1 + hw_uplift_override / 100) * _sq
        else:
            sw = get_recommended_switch(compute_poe_needed())
            total += sw.get("sell", sw["buy"] * (1 + hw_uplift_override / 100))
    if add_router:
        if router_quantities:
            for _rn, _rq in router_quantities.items():
                if _rn in ROUTERS: total += ROUTERS[_rn] * (1 + hw_uplift_override / 100) * _rq
        elif router_type not in ("None / Customer Supplied", "") and router_type in ROUTERS:
            total += ROUTERS[router_type] * (1 + hw_uplift_override / 100)
            total += ROUTERS[router_type] * (1 + hw_uplift_override / 100)
    return round(total, 2)

def compute_install_cost():
    if override_install_cost > 0:
        return override_install_cost         # manager override
    if install_type == "Engineer Install":
        return 500.0
    return 0.0

def compute_upfront():
    """Upfront = hw_sell + installation + BB install charge."""
    bb_inst = BROADBAND[bb_provider][bb_package]["install"]
    # Override with bespoke pricing for Leased Line / Other
    if bb_package == "Leased Line / Other":
        bb_inst = ll_install
    return compute_hw_sell() + compute_install_cost() + bb_inst

def compute_service_charges(sw_sell=0.0, sw_cost=0.0):
    """Compute all monthly service charges. sw_sell/sw_cost come from software add-ons."""
    uplift   = service_uplift_pct / 100.0
    bb_cost  = BROADBAND[bb_provider][bb_package]["cost"]
    if bb_package == "Leased Line / Other":
        bb_cost = ll_cost
    if bb_package == "Leased Line / Other":
        bb1_sell  = ll_sell                  # bespoke sell price entered by consultant
        bb1_floor = ll_cost                  # bespoke cost is the floor
    elif override_bb_sell > 0:
        bb1_sell  = override_bb_sell         # manager override
        bb1_floor = bb_cost
    else:
        bb1_sell  = 0.0 if bb_cost == 0.0 else bb_cost * (1.0 + uplift)
        bb1_floor = bb_cost                  # wholesale - never sell below this
    if bb_care == "Business (+£8/mo)":
        bb1_sell  += 8.0
        bb1_floor += 8.0                     # care charge passed through, not discountable
    bb2_sell = bb2_floor = 0.0
    if second_fttp and second_fttp_pkg:
        bb_cost2  = BROADBAND[bb_provider][second_fttp_pkg]["cost"]
        bb2_sell  = bb_cost2 * (1.0 + uplift)
        bb2_floor = bb_cost2
    bb_sell = bb1_sell + bb2_sell

    # Voice channels - fixed sell price from pricebook (Professional Bundle)
    vc_sell_per_seat = C.get("vc_sell_per_seat", 12.00)
    vc_cost_per_seat = C.get("vc_cost_per_seat", 2.95)
    lic_monthly      = total_voice_channels * vc_sell_per_seat

    # Wallboard - computed here to avoid global scope issues
    wallboard_mo_val = wallboard_users * C.get("wallboard_sell", 99.00)

    mobile_sell      = sum(r["sell"] * r["qty"] for r in mobile_rows)
    mobile_cost      = sum(r["cost"] * r["qty"] for r in mobile_rows)
    total_sell       = bb_sell + lic_monthly + wallboard_mo_val + mobile_sell + sw_sell

    return {
        "bb_cost":        bb_cost,
        "bb_sell":        bb_sell,
        "bb1_sell":       bb1_sell,
        "bb2_sell":       bb2_sell,
        "bb1_floor":      bb1_floor,
        "bb2_floor":      bb2_floor,
        "lic_monthly":    lic_monthly,
        "wallboard_mo":   wallboard_mo_val,
        "mobile_sell":    mobile_sell,
        "mobile_cost":    mobile_cost,
        "sw_sell":        sw_sell,
        "sw_cost":        sw_cost,
        "total_sell":     total_sell,
    }


def compute_pricebook_pl():
    """P&L using exact pricebook formula (verified against P & L Calcs sheet).
    hw_rrp=hw_buy×1.5 | maintenance=0.2×hw_rrp | hw_srrp=hw_sell×1.5
    sub_total=cos_ex+hw_srrp | rental=(sales_rate/1000)×sub_total
    disc_turnover=(rental/true_rate)×1000 | gp=disc_turnover-cos_full
    commission=(gp/4000)×1000
    """
    # LEASE_RATES is {months: sales_rate}, TRUE_LEASE_RATES is {months: true_rate}
    _fallback_lr = {36: (39.45, 31.56), 60: (26.26, 21.01), 84: (20.58, 16.46), 24: (46.94, 37.5)}
    sales_rate = LEASE_RATES.get(lease_term, _fallback_lr.get(lease_term, (20.58, 16.46))[0])
    true_rate  = TRUE_LEASE_RATES.get(lease_term, _fallback_lr.get(lease_term, (20.58, 16.46))[1])
    _hw_buy    = compute_hw_buy()
    _hw_sell   = compute_hw_sell()
    hw_rrp     = _hw_buy  * 1.5
    hw_srrp    = _hw_sell * 1.5
    maintenance_annual = 0.2 * hw_rrp
    cos_ex     = maintenance_annual + 200.0 + compute_install_cost() + termination_cost + 400.0
    sub_total  = cos_ex + hw_srrp
    rental     = (sales_rate / 1000.0) * sub_total
    disc_turn  = (rental / true_rate) * 1000.0
    cos_full   = cos_ex + _hw_buy
    gp         = disc_turn - cos_full
    units      = gp / 4000.0
    return {
        "gross_profit": round(gp, 2), "comm_units": round(units, 3),
        "commission": round(units * 1000, 2), "rental": round(rental, 2),
        "disc_turnover": round(disc_turn, 2), "sub_total": round(sub_total, 2),
        "hw_srrp": round(hw_srrp, 2), "maintenance_annual": round(maintenance_annual, 2),
        "cos_full": round(cos_full, 2), "sales_rate": sales_rate, "true_rate": true_rate,
    }

def compute_pat(svc):
    """Legacy - returns gross_profit from pricebook P&L formula as PAT proxy."""
    return compute_pricebook_pl()["gross_profit"]

# ── Compute everything ────────────────────────────────────────────────────────
poe_needed = compute_poe_needed()
rec_switch = get_recommended_switch(poe_needed)
hw_buy     = compute_hw_buy()
hw_sell    = compute_hw_sell()
svc        = compute_service_charges(sw_sell=sw_sell_total, sw_cost=sw_cost_total)

# BB free year: compute Year 1 total (£0 BB) for customer display
bb_free_year   = st.session_state.get("q_bb_free_year", False)
_bb_full_sell  = svc["bb_sell"]                                   # standard BB sell price
_bb_yr1_sell   = 0.0 if bb_free_year else _bb_full_sell          # £0 in year 1 if promo
_bb_yr1_saving = _bb_full_sell if bb_free_year else 0.0          # saving in yr1

# Add Call Scope services + Security to total monthly
_cs_svc_sell  = sum(r["sell"] * r["qty"] for r in cs_svc_rows)
_cs_svc_cost  = sum(r["buy"]  * r["qty"] for r in cs_svc_rows)
_sec_svc_sell = sum(r["sell"] * r["qty"] for r in sec_rows)
_sec_svc_cost = sum(r["buy"]  * r["qty"] for r in sec_rows)
svc["cs_sell"]  = _cs_svc_sell
svc["sec_sell"] = _sec_svc_sell
svc["total_sell"] = svc["total_sell"] + _cs_svc_sell + _sec_svc_sell

# ── Consultant services discount (0-40% slider in Consultant tab) ─────────────
# Applies to hosted user licences, software add-ons and broadband (broadband is capped
# at wholesale cost). Mobiles are not discountable. Commission is reduced by the same %.
svc_disc_pct  = max(0.0, min(40.0, float(st.session_state.get("c_svc_disc", 0))))
_svc_mult     = 1.0 - svc_disc_pct / 100.0
lic_list_total = float(svc["lic_monthly"])          # undiscounted, for consultant display
bb1_list       = float(svc["bb1_sell"])
bb2_list       = float(svc["bb2_sell"])
sw_list_total  = float(sw_sell_total)               # undiscounted, for consultant display
if svc_disc_pct > 0:
    SW_ADDONS = [(n, q, c, round(sell * _svc_mult, 2)) for n, q, c, sell in SW_ADDONS]
    sw_sell_total = sum(qty * sell for _, qty, _, sell in SW_ADDONS if qty > 0)
    svc["sw_sell"]     = sw_sell_total
    svc["lic_monthly"] = round(lic_list_total * _svc_mult, 2)
    # Broadband: discounted, but NEVER below wholesale cost (per line)
    if bb1_list > 0:
        svc["bb1_sell"] = round(max(bb1_list * _svc_mult, svc["bb1_floor"]), 2)
    if bb2_list > 0:
        svc["bb2_sell"] = round(max(bb2_list * _svc_mult, svc["bb2_floor"]), 2)
    svc["bb_sell"]     = svc["bb1_sell"] + svc["bb2_sell"]
    svc["total_sell"]  = (svc["bb_sell"] + svc["lic_monthly"] + svc.get("wallboard_mo", 0.0) +
                          svc.get("mobile_sell", 0.0) + sw_sell_total +
                          _cs_svc_sell + _sec_svc_sell)
pat_base   = compute_pat(svc)
pl_data    = compute_pricebook_pl()  # full pricebook P&L breakdown

is_spread  = ("Lease" in payment_model)

if is_spread:
    # Use pricebook lease rental formula
    hw_monthly_spread = pl_data["rental"]
    total_mo   = svc["total_sell"] + hw_monthly_spread
    upfront    = 0.0
    pat        = pat_base
else:
    # Upfront: compute hw_sell at upfront uplift % (default 20%, not lease uplift)
    hw_sell    = compute_hw_sell(uplift_pct=hw_uplift_upfront_override)
    hw_monthly_spread = 0.0
    _bb_inst   = BROADBAND[bb_provider][bb_package]["install"]
    if bb_package == "Leased Line / Other":
        _bb_inst = ll_install
    upfront    = hw_sell + compute_install_cost() + _bb_inst + termination_cost
    if override_upfront > 0:
        upfront = override_upfront           # manager override
    total_mo   = svc["total_sell"]
    pat        = pat_base
# ── Consultant desired rental - adjusts lease amount and commission ───────────
deal_type = "Hardware Lease (spread over term)" if is_spread else f"Upfront Purchase (cost + {hw_uplift_upfront_override:.0f}% uplift)"
base_rental   = pl_data["rental"]      # the calculated lease rental (floor/reference)
st.session_state["_prev_base_rental"] = round(base_rental, 2)
true_rate     = pl_data["true_rate"]

# Read consultant's desired rental from session state (default = calculated rental)
_desired_rental = st.session_state.get("c_desired_rental", 0.0)
if _desired_rental <= 0:
    _desired_rental = base_rental      # default to calculated if not set

# Recalculate GP and commission from desired rental
# Formula: disc_turnover = (desired_rental / true_rate) × 1000
# GP = disc_turnover - cos_full
_desired_disc_turnover = (_desired_rental / true_rate) * 1000 if true_rate > 0 else 0
_adjusted_gp           = _desired_disc_turnover - pl_data["cos_full"]
commission_units       = _adjusted_gp / 4000
commission             = round(commission_units * commission_per_unit, 2)
st.session_state["_prev_commission_units"] = round(commission_units, 2)
st.session_state["_prev_true_rate"]        = pl_data["true_rate"]
st.session_state["_prev_cos_full"]         = pl_data["cos_full"]
# Services discount removes the same % of commission (e.g. 10% discount = -10% commission)
commission_full        = commission
if svc_disc_pct > 0 and commission > 0:
    commission_units   = commission_units * _svc_mult
    commission         = round(commission * _svc_mult, 2)
commission_lost        = round(commission_full - commission, 2)

# Rental adjustment (vs calculated) - can be positive (premium) or negative (discount)
rental_adjustment = _desired_rental - base_rental

# In lease mode, use desired_rental as the actual hw_monthly_spread
if is_spread:
    hw_monthly_spread = _desired_rental
    total_mo          = svc["total_sell"] + hw_monthly_spread

base_total_mo = total_mo
rate_uplift   = rental_adjustment  # for display purposes
adjusted_pat  = _adjusted_gp

# Aliases for PDF / legacy references
kit_cost    = hw_buy
lease_mo    = hw_monthly_spread  # used in PDF as "Hardware Monthly" when spread
rec_upfront = upfront

# Pure connectivity cost - broadband + mobile only (for Commercial Summary card)
pure_connectivity = round(svc["bb_sell"] + svc["mobile_sell"], 2)

# SGP / sales comms
# SGP / sales comms
sgp          = pat * 0.10



tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📄 Proposal Summary", "🖋️ Order Form Preview", "📥 Download Documents", "👤 Customer View", "💼 Consultant", "✍️ Sign & Send", "🔐 Admin"])

# ── TAB 1: PROPOSAL SUMMARY ──────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="tab-content"></div>', unsafe_allow_html=True)

    if comp_name:
        st.markdown(f"### Prepared for: **{comp_name}** ({biz_type})")
    if install_address:
        st.markdown(f"📍 {install_address}")
    st.markdown("")

    prop_col1, prop_col2 = st.columns(2)

    with prop_col1:
        st.markdown("#### 🖥️ System, Software & Hardware")

        all_hw_items = []
        _hw_billing = "In Monthly Lease" if is_spread else "Paid Upfront"
        _sw_billing = "Monthly Add-on"

        # Physical hardware
        for name, qty in desktop_quantities.items():
            if qty > 0: all_hw_items.append((name, qty, _hw_billing))
        for name, qty in cordless_quantities.items():
            if qty > 0: all_hw_items.append((name, qty, _hw_billing))
        for name, qty in headset_quantities.items():
            if qty > 0: all_hw_items.append((name, qty, _hw_billing))
        for name, qty in other_quantities.items():
            if qty > 0: all_hw_items.append((name, qty, _hw_billing))
        if not _no_switch:
            if switch_quantities:
                for _sn, _sq in switch_quantities.items():
                    all_hw_items.append((f"Switch: {_sn}", _sq, _hw_billing))
            elif auto_switch:
                all_hw_items.append((f"Switch: {rec_switch['name']}", 1, _hw_billing))
        if add_router:
            if router_quantities:
                for _rn, _rq in router_quantities.items():
                    all_hw_items.append((_rn, _rq, _hw_billing))
            elif router_type not in ("None / Customer Supplied", ""):
                all_hw_items.append((router_type, 1, _hw_billing))
        if all_hw_items:
            hw_df = pd.DataFrame(all_hw_items, columns=["Description", "Qty", "Billing"])
            st.dataframe(hw_df, use_container_width=True, hide_index=True)
        else:
            st.info("No hardware selected yet.")

        st.markdown("#### 🌐 Network & Connectivity")
        st.caption("Ongoing monthly service charges")
        net_items = []
        if svc["bb_sell"] > 0:
            net_items.append((f"{bb_provider} - {bb_package}", 1, f"£{svc['bb1_sell']:.2f}/mo"))
        # Voice Channel Licences - always show with monthly amount
        if total_voice_channels > 0:
            net_items.append((f"Hosted User Licences x{total_voice_channels} (Professional Bundle)",
                              total_voice_channels, f"£{svc['lic_monthly']:.2f}/mo"))
        # SW Add-ons - monthly amounts
        for addon_name, addon_qty, addon_cost, addon_sell in SW_ADDONS:
            if addon_qty > 0:
                net_items.append((addon_name, addon_qty, f"£{addon_sell * addon_qty:.2f}/mo"))
        # 2nd line BB
        if second_fttp and second_fttp_pkg:
            bb2_sell = svc["bb2_sell"]
            net_items.append((f"{bb_provider} - {second_fttp_pkg} (2nd line)", 1, f"£{bb2_sell:.2f}/mo"))
        # Mobile rows

        net_df = pd.DataFrame(net_items, columns=["Service", "Qty", "Charge"])
        st.dataframe(net_df, use_container_width=True, hide_index=True)

        if cs_svc_rows:
            st.markdown("#### 🔮 Call Scope Services")
            cs_df = pd.DataFrame([{"Service": r["name"], "Qty": r["qty"],
                                   "Monthly": f"£{r['sell']*r['qty']:.2f}/mo"} for r in cs_svc_rows])
            st.dataframe(cs_df, use_container_width=True, hide_index=True)

    with prop_col2:
        st.markdown("#### Commercial Summary")
        # Build commercial summary cards - content varies by payment model
        _hw_card = "" if is_spread else f"""
        <div class="metric-card" style="text-align:left; margin-bottom:1rem">
          <div class="metric-label">Upfront Hardware Cost</div>
          <div style="font-size:1.4rem; font-weight:700">£{upfront:.2f} (one-off)</div>
        </div>"""

        _spread_note = f"""
        <div class="metric-card" style="text-align:left; margin-bottom:1rem">
          <div class="metric-label">Hardware Lease Rental</div>
          <div style="font-size:1.4rem; font-weight:700; color:#00b5a3">
            £{hw_monthly_spread:.2f}/mo
          </div>
          <div style="font-size:0.78rem;color:#888;margin-top:0.2rem">
            Spread over {LEASE_TERM_LABELS[lease_term]}
          </div>
        </div>""" if is_spread else ""

        st.markdown(f"""
        <div style="font-size:0.72rem;color:#999;margin-bottom:0.2rem">
          Agreement term: <strong>{lease_term} months</strong>
        </div>
        {_hw_card}
        {_spread_note}
        <div class="metric-card" style="text-align:left; margin-bottom:1rem">
          <div class="metric-label">Network & Services</div>
          <div style="font-size:1.4rem; font-weight:700">£{svc["total_sell"]:.2f} + VAT</div>
          <div style="font-size:0.78rem;color:#888;margin-top:0.2rem">Licences, broadband, software &amp; mobiles</div>
        </div>
        <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
             letter-spacing:0.1em;color:#aaaaaa;margin-bottom:0.4rem;padding-left:0.2rem">
          TOTAL MONTHLY COMMITMENT
        </div>
        <div style="background:linear-gradient(135deg,#1f1450,#2d1f6e);border-radius:12px;
             padding:1.2rem 1.4rem;border:1px solid rgba(0,181,163,0.25)">
          <div style="font-size:2rem;font-weight:800;color:#00b5a3">
            £{total_mo:.2f} + VAT
          </div>
          <div style="font-size:0.8rem;color:rgba(255,255,255,0.45);margin-top:0.4rem">
            {"All services + hardware included" if is_spread else "Services per month"}
            &nbsp;·&nbsp; {LEASE_TERM_LABELS[lease_term]}
          </div>
        </div>
        """, unsafe_allow_html=True)

        if credits_months > 0:
            st.markdown(f'<div class="info-box">🎁 Introductory credit of <strong>£{credits_amount:.2f}/mo</strong> applied for {credits_months} months</div>', unsafe_allow_html=True)

        if mobile_rows:
            st.markdown("#### Mobile SIMs")
            mob_df = pd.DataFrame([
                {"Network": r["network"], "Package": r["package"], "Qty": r["qty"], "Monthly": f"£{r['sell'] * r['qty']:.2f}"}
                for r in mobile_rows
            ])
            st.dataframe(mob_df, use_container_width=True, hide_index=True)

        if it_rows:
            st.markdown("#### 💻 IT Services")
            it_df = pd.DataFrame([
                {"Service": r["service"], "Qty": r["qty"],
                 "Monthly": f"£{r['sell']*r['qty']:.2f}/mo"}
                for r in it_rows
            ])
            st.dataframe(it_df, use_container_width=True, hide_index=True)

        if sec_rows:
            st.markdown("#### 🛡️ System Security")
            sec_df = pd.DataFrame([{"Tier": r["name"], "Qty": r["qty"],
                                    "Monthly": f"£{r['sell']*r['qty']:.2f}/mo"} for r in sec_rows])
            st.dataframe(sec_df, use_container_width=True, hide_index=True)



    # summary banner removed
with tab2:
    st.markdown('<div class="tab-content"></div>', unsafe_allow_html=True)
    missing = []
    if not comp_name:     missing.append("Company Name")
    if not comp_reg:      missing.append("Company Registration No.")
    if not install_address: missing.append("Installation Address")
    if not contact_name:  missing.append("Signatory Name & Position")
    if not bank_name:     missing.append("Bank Name")
    if not acc_no:        missing.append("Account Number")
    if not sort_code:     missing.append("Sort Code")

    if missing:
        st.markdown(f'<div class="warning-box">⚠️ Missing fields required for order form: <strong>{", ".join(missing)}</strong></div>', unsafe_allow_html=True)

    of_col1, of_col2 = st.columns(2)

    with of_col1:
        st.markdown("#### 🏢 Legal & Company Details")
        fields = {
            "Trading / Company Name": comp_name or "⚠️ Not provided",
            "Company Reg. No.": comp_reg or "⚠️ Not provided",
            "Entity Type": biz_type,
            "No. of Employees": str(num_employees),
            "Signatory Name & Position": contact_name or "⚠️ Not provided",
            "Company Phone": company_phone or "-",
            "Director's Email": director_email or "-",
            "Billing Email": billing_email or "-",
            "Installation Address": install_address or "⚠️ Not provided",
        }
        for label, val in fields.items():
            colour = "#008078" if "⚠️" in val else "#333"
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid #f0f0f0;font-size:0.88rem'><span style='color:#888'>{label}</span><span style='color:{colour};font-weight:500'>{val}</span></div>", unsafe_allow_html=True)

        st.markdown("#### 🏦 Direct Debit Mandate")
        bank_fields = {
            "Bank Name": bank_name or "⚠️ Not provided",
            "Account Holder": acc_holder or "⚠️ Not provided",
            "Account Number": acc_no or "⚠️ Not provided",
            "Sort Code": sort_code or "⚠️ Not provided",
        }
        for label, val in bank_fields.items():
            colour = "#008078" if "⚠️" in val else "#333"
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid #f0f0f0;font-size:0.88rem'><span style='color:#888'>{label}</span><span style='color:{colour};font-weight:500'>{val}</span></div>", unsafe_allow_html=True)

    with of_col2:
        st.markdown("#### 📋 Deal & System Configuration")
        config_fields = {
            "Deal Type":       deal_type,
            "Contract Term":   LEASE_TERM_LABELS[lease_term],
            "Payment Profile": f"1+{lease_term-1}",
            "Installation":    install_type,
            "No. of Sites":    str(num_sites),
        }
        if svc["bb_sell"] > 0:
            config_fields["Broadband"] = f"{bb_provider} - {bb_package}"
        if is_spread:
            config_fields["Hardware Rental"] = f"£{hw_monthly_spread:.2f}/mo (lease)"
            config_fields["Note"] = "Install & setup included in lease rental"
        else:
            config_fields["Upfront Hardware"] = f"£{upfront:.2f} (one-off)"
        config_fields["Monthly Services"] = f"£{svc['total_sell']:.2f} + VAT"
        config_fields["Total Monthly"]    = f"£{total_mo:.2f} + VAT"
        if credits_months > 0:
            config_fields["Introductory Credit"] = f"£{credits_amount:.2f}/mo × {credits_months} months"
        if cashback_amount > 0:
            config_fields["Settlement / Cashback"] = f"£{cashback_amount:.2f}"
        for label, val in config_fields.items():
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid #f0f0f0;font-size:0.88rem'><span style='color:#888'>{label}</span><span style='color:#333;font-weight:500'>{val}</span></div>", unsafe_allow_html=True)

        st.markdown("#### 📦 Equipment Summary")
        all_equip = [(n, q) for n, q in list(desktop_quantities.items()) +
                     list(cordless_quantities.items()) + list(headset_quantities.items()) +
                     list(other_quantities.items()) if q > 0]
        if auto_switch:
            all_equip.append((f"Switch: {rec_switch['name']}", 1))
        if add_router:
            if router_quantities:
                for _rn, _rq in router_quantities.items():
                    all_equip.append((_rn, _rq))
            elif router_type not in ("None / Customer Supplied", ""):
                all_equip.append((router_type, 1))
        if total_voice_channels > 0:
            all_equip.append((f"User / Voice Licences x{total_voice_channels}", total_voice_channels))
        for _ir in it_rows:
            if _ir["qty"] > 0:
                all_equip.append((f"IT: {_ir['service']} x{_ir['qty']}", _ir["qty"]))
        for addon_name, addon_qty, _, _ in SW_ADDONS:
            if addon_qty > 0:
                all_equip.append((addon_name, addon_qty))
        for r in cs_svc_rows:
            if r.get("qty", 0) > 0:
                all_equip.append((r["name"], r["qty"]))
        for r in sec_rows:
            if r.get("qty", 0) > 0:
                all_equip.append((r["name"], r["qty"]))
        for name, qty in all_equip:
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:0.2rem 0;font-size:0.85rem'><span style='color:#555'>{name}</span><span style='font-weight:600'>×{qty}</span></div>", unsafe_allow_html=True)


# ── TAB 3: DOWNLOAD ───────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="tab-content"></div>', unsafe_allow_html=True)
    st.markdown("Generate the complete customer-facing paperwork package. All documents are pre-populated from the deal configuration.")

    doc_col1, doc_col2 = st.columns(2)

    with doc_col1:
        st.markdown("#### 📄 What's included in the PDF")
        docs = [
            "✅ Commercial Proposal / Cost Comparison",
            "✅ Equipment Rental Agreement",
            "✅ Network Services & Broadband Agreement",
            "✅ Telephone System Order Form",
            "✅ Inclusive Support & Maintenance",
            "✅ Customer Requirements Checklist",
            "✅ Direct Debit Mandate",
            "✅ Signature Blocks (all sections)",
        ]
        for d in docs:
            st.markdown(f"<div style='font-size:0.88rem;padding:0.25rem 0'>{d}</div>", unsafe_allow_html=True)

    with doc_col2:
        st.markdown("#### 📋 Deal Summary")
        summary = [
            f"Customer: {comp_name or '-'}",
            f"Agreement Term: {LEASE_TERM_LABELS[lease_term]}",
            f"Payment Model: {payment_model}",
            f"Monthly Total: £{total_mo:.2f} + VAT",
            f"Broadband: {bb_provider} - {bb_package}",
            f"Voice Channels: {total_voice_channels}",
            f"Install Type: {install_type}",
        ]
        for d in summary:
            st.markdown(f"<div style='font-size:0.88rem;padding:0.2rem 0;color:#555'>{d}</div>", unsafe_allow_html=True)

    # ── DOWNLOAD BUTTON ──
    st.markdown("")
    pdf_ready = bool(comp_name)

    if not pdf_ready:
        st.markdown('<div class="warning-box">⚠️ Add a company name in the sidebar to enable PDF generation.</div>', unsafe_allow_html=True)
    else:
        pdf_bytes = build_pdf()
        safe_name = s(comp_name).replace(" ", "_").replace("/", "-")
        st.download_button(
            label=f"📥 Download Full Proposal Pack - {comp_name}",
            data=pdf_bytes,
            file_name=f"SYComms_Proposal_{safe_name}_{date.today()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('<div class="success-box">✅ PDF ready - 4 sections: Proposal, Order Form, Network Agreement, Mandate & Checklist.</div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown("---")
        st.markdown("#### 📋 One-Page Proposal")
        st.caption(f"Clean two-page summary: About {_CO} + deal breakdown. Great for emailing to a prospect before the full paperwork.")
        proposal_bytes = build_proposal_pdf()
        st.download_button(
            label=f"📋 Download Proposal Summary - {comp_name}",
            data=proposal_bytes,
            file_name=f"SYComms_Proposal_Summary_{safe_name}_{date.today()}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="dl_proposal"
        )

# ── TAB 4: CUSTOMER VIEW ──────────────────────────────────────────────────────
with tab4:
    st.markdown("""
    <style>
      .cv-header {
        background: linear-gradient(135deg, #1f1450 0%, #2d1f6e 100%);
        border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; color: white;
      }
      .cv-header h2 { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; margin:0; color:white !important; }
      .cv-header p  { color:rgba(255,255,255,0.6); margin:0.3rem 0 0; font-size:0.95rem; }
      .cv-section   { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:#1f1450;
                      margin:1.5rem 0 0.75rem; padding-bottom:0.4rem; border-bottom:2px solid #f0f0f0; }
      .cv-hw-card   { background:#fff; border:1px solid #e8e8f0; border-radius:12px; padding:12px;
                      text-align:center; height:100%; }
      .cv-hw-name   { font-size:0.8rem; font-weight:600; color:#333; margin-top:6px; line-height:1.3; }
      .cv-hw-qty    { background:#00b5a3; color:white; border-radius:12px; padding:2px 10px;
                      font-size:0.75rem; font-weight:700; display:inline-block; margin-top:4px; }
      .cv-price-row { display:flex; justify-content:space-between; padding:0.6rem 0;
                      border-bottom:1px solid #f5f5f5; font-size:0.95rem; }
      .cv-price-label { color:#555; }
      .cv-price-val   { font-weight:600; color:#1f1450; }
      .cv-total-box { background:linear-gradient(135deg,#1f1450,#2d1f6e); border-radius:12px;
                      padding:1.5rem 2rem; margin-top:1rem; text-align:center; }
      .cv-total-label { color:rgba(255,255,255,0.6); font-size:0.8rem; font-weight:700;
                        text-transform:uppercase; letter-spacing:0.08em; }
      .cv-total-val   { color:#ffffff; font-family:'Syne',sans-serif; font-size:2.5rem;
                        font-weight:800; margin-top:0.3rem; }
      .cv-total-note  { color:rgba(255,255,255,0.5); font-size:0.8rem; margin-top:0.3rem; }
      .cv-include-item { font-size:0.85rem; padding:0.25rem 0; color:#444; }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div class="cv-header">
      <h2>{_CO_PKG}</h2>
      <p>{'Prepared for: ' + comp_name if comp_name else 'Complete the customer details in the sidebar'} &nbsp;|&nbsp; {LEASE_TERM_LABELS[lease_term]} agreement</p>
    </div>
    """, unsafe_allow_html=True)

    if not (desktop_quantities or cordless_quantities or headset_quantities or other_quantities or standalone_softphones > 0):
        st.info("👈 Select hardware from the builder above to populate this view.")
    else:
        # ── Selected Hardware ──────────────────────────────────────────────────
        st.markdown('<div class="cv-section">📦 Your New System</div>', unsafe_allow_html=True)

        # Items hidden from customer view (backend/setup costs)
        _CV_HIDE = {"Call Scope AI Setup (one-off)"}
        all_selected = (
            [(n, q, HANDSETS_DESKTOP[n])   for n, q in desktop_quantities.items() if q > 0]  +
            [(n, q, HANDSETS_CORDLESS[n])  for n, q in cordless_quantities.items() if q > 0] +
            [(n, q, HEADSETS[n])           for n, q in headset_quantities.items()   if q > 0] +
            [(n, q, OTHER_HARDWARE.get(n, {"cat":"Other"}))
             for n, q in other_quantities.items()
             if q > 0 and n not in _CV_HIDE]
        )

        # Add switch card(s)
        if switch_quantities:
            for _sn, _sq in switch_quantities.items():
                all_selected.append((f"Switch: {_sn}", _sq, {"cat": "Switch"}))
        elif not _no_switch:
            sw_name = rec_switch["name"]
            all_selected.append((f"Switch: {sw_name}", 1, {"cat": "Switch"}))

        # Add router card(s) - iterate router_quantities for multi-router support
        if add_router:
            if router_quantities:
                for _rn, _rq in router_quantities.items():
                    all_selected.append((_rn, _rq, {"cat": "Router"}))
            elif router_type not in ("None / Customer Supplied", ""):
                all_selected.append((router_type, 1, {"cat": "Router"}))
        # Add software add-ons as cards
        for addon_name, addon_qty, _, _ in SW_ADDONS:
            if addon_qty > 0:
                all_selected.append((addon_name, addon_qty, {"cat": "Software"}))

        # IT service cards
        for _ir in it_rows:
            all_selected.append((_ir["service"], _ir["qty"], {"cat": "IT"}))


        # Call Scope service cards
        for _ir in cs_svc_rows:
            all_selected.append((f"Call Scope: {_ir['name']}", _ir["qty"], {"cat": "Call Scope"}))
        # Security cards
        for _ir in sec_rows:
            all_selected.append((_ir["name"], _ir["qty"], {"cat": "Security"}))
        # Add Mobile App / Softphone users as a card
        if standalone_softphones > 0:
            all_selected.append((
                "Mobile App / Softphone Users",
                standalone_softphones,
                {"cat": "Mobile"}
            ))

        # Add additional wired ports as a card
        if additional_wired_ports > 0:
            all_selected.append((
                "Extra Network Ports",
                additional_wired_ports,
                {"cat": "Switch"}
            ))

        # Show in rows of 4
        for row_start in range(0, len(all_selected), 4):
            row_items = all_selected[row_start:row_start + 4]
            cols = st.columns(4)
            for col, (name, qty, info) in zip(cols, row_items):
                with col:
                    b64_cv, ext_cv = get_product_image_b64(name)
                    if b64_cv:
                        img_html = f'<img src="data:image/{ext_cv};base64,{b64_cv}" style="width:100%;height:100px;object-fit:contain;border-radius:8px;">'
                    else:
                        cat = info.get("cat", "Desktop")
                        icon_map = {"Desktop":"📱","DECT":"📞","Wi-Fi":"📡","Switch":"🔌","Router":"🌐","Software":"💻","IT":"🖥️","Mobile":"📱","Headset":"🎧"}
                        icon = icon_map.get(cat, PRODUCT_ICONS.get(cat, "📱"))
                        img_html = f'<div style="height:100px;background:linear-gradient(135deg,#2d1f6e,#3b2882);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:2.8rem">{icon}</div>'

                    st.markdown(f"""
                    <div class="cv-hw-card">
                      {img_html}
                      <div class="cv-hw-name">{name}</div>
                      <div class="cv-hw-qty">Qty: {qty}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Auto-included note (simplified)
        st.markdown(f"""
        <div style="margin-top:0.75rem;padding:0.6rem 1rem;background:#f8f9ff;border-radius:8px;font-size:0.82rem;color:#555">
          <strong>{total_voice_channels} Voice Channel Licence{"s" if total_voice_channels != 1 else ""}</strong> included
          &nbsp;&middot;&nbsp; {LEASE_TERM_LABELS[lease_term]} agreement
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # ── Pricing breakdown ──────────────────────────────────────────────────
        # ── Pricing breakdown ──────────────────────────────────────────────────
    # ── COST COMPARISON SECTION ───────────────────────────────────────
    if current_total > 0:
        st.markdown("---")
        st.markdown('''
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;
             color:#1f1450;margin:1rem 0 0.6rem">📊 Cost Comparison</div>
        ''', unsafe_allow_html=True)

        saving_mo  = current_total - total_mo
        saving_yr  = saving_mo * 12
        saving_pct = (saving_mo / current_total * 100) if current_total > 0 else 0

        # Build comparison rows
        # Build comparison using pricebook category structure
        # SY Comms side matches: Call Charges | Hosted Licences | Software | BB | Equipment Rental
        comp_rows = []
        if current_calls > 0:
            comp_rows.append(("Call Charges", current_calls, 0.0))  # calls included in licence
        if current_lines > 0:
            comp_rows.append(("Line Rental & Associated", current_lines, 0.0))
        if current_bb > 0:
            comp_rows.append(("Broadband Charges", current_bb, svc["bb_sell"]))
        if current_system > 0:
            sys_new = hw_monthly_spread if is_spread else 0
            comp_rows.append(("Equipment Rental", current_system, sys_new))
        if current_support > 0:
            _cv_it_sell = sum(r["sell"]*r["qty"] for r in it_rows) if it_rows else 0.0
            if current_it > 0 or _cv_it_sell > 0:
                comp_rows.append(("IT Services / M365",
                                   current_it if current_it > 0 else 0.0,
                                   _cv_it_sell if _cv_it_sell > 0 else 0.0))
            comp_rows.append(("Maintenance & Support", current_support, 0.0))
        if current_hosted > 0:
            comp_rows.append(("Hosted System / User Licences", current_hosted, svc["lic_monthly"]))
        else:
            # Always show our hosted licences if we have them
            if svc["lic_monthly"] > 0:
                comp_rows.append(("Hosted User Licences", 0.0, svc["lic_monthly"]))
        if current_onhold > 0:
            comp_rows.append(("On Hold Marketing", current_onhold, 0.0))
        # Software add-ons
        if current_other > 0 or sw_sell_total > 0:
            comp_rows.append(("Software Charges / Other", current_other, sw_sell_total))
        elif sw_sell_total > 0:
            comp_rows.append(("Software Charges", 0.0, sw_sell_total))

        # Comparison table - built as a flat string to avoid markdown code-block indentation
        _saving_bg  = "#e8f8f0"  # always green — increase is also a positive investment
        _saving_col = "#1a7a40"  # always green
        if saving_mo >= 0:
            _saving_lbl  = "Annual Saving"
            _saving_disp = f"{chr(163)}{abs(saving_yr):,.2f}"
            _saving_sub  = f"per year  ({chr(163)}{abs(saving_mo):.2f}/mo)"
        else:
            _daily       = abs(saving_mo) / 30.44
            _saving_lbl  = "Daily Investment"
            _saving_disp = f"{chr(163)}{_daily:.2f}"
            _saving_sub  = "per day"
        _arrow = "-" if saving_mo >= 0 else "+"

        _tbl = '<table style="width:100%;border-collapse:collapse;font-size:0.88rem;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06)">'
        _tbl += '<thead><tr style="background:#1f1450;color:#fff">'
        _tbl += '<th style="padding:10px 12px;text-align:left">Category</th>'
        _tbl += '<th style="padding:10px 12px;text-align:right">Current</th>'
        _tbl += '<th style="padding:10px 12px;text-align:right">SY Comms</th>'
        _tbl += '<th style="padding:10px 12px;text-align:right">Difference</th>'
        _tbl += "</tr></thead><tbody>"

        for _label, _curr_v, _new_v in comp_rows:
            _diff  = _curr_v - _new_v
            _dcol  = "#1a7a40" if _diff >= 0 else "#c0392b"
            _dstr  = f"-{chr(163)}{_diff:.2f}" if _diff >= 0 else f"+{chr(163)}{abs(_diff):.2f}"
            _tbl += f'<tr>'
            _tbl += f'<td style="padding:8px 12px;border-bottom:1px solid #eee">{_label}</td>'
            _tbl += f'<td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right;color:#888">{chr(163)}{_curr_v:.2f}</td>'
            _tbl += f'<td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right;color:#1f1450;font-weight:600">{chr(163)}{_new_v:.2f}</td>'
            _tbl += f'<td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right;color:{_dcol};font-weight:700">{_dstr}</td>'
            _tbl += "</tr>"

        _tbl += f'<tr style="background:#f5f5f5;font-weight:700">'
        _tbl += f'<td style="padding:10px 12px">Total Monthly (excl. VAT)</td>'
        _tbl += f'<td style="padding:10px 12px;text-align:right">{chr(163)}{current_total:.2f}</td>'
        _tbl += f'<td style="padding:10px 12px;text-align:right;color:#1f1450">{chr(163)}{total_mo:.2f}</td>'
        _tbl += f'<td style="padding:10px 12px;text-align:right;color:{_saving_col}">{_arrow}{chr(163)}{abs(saving_mo):.2f}</td>'
        _tbl += "</tr></tbody></table>"

        _tbl += f'<div style="margin-top:1rem;padding:1rem 1.4rem;background:{_saving_bg};border-radius:10px;border-left:4px solid {_saving_col}">'
        _tbl += f'<div style="font-size:0.8rem;color:{_saving_col};font-weight:700;text-transform:uppercase;letter-spacing:.06em">{_saving_lbl}</div>'
        _tbl += f'<div style="font-size:1.8rem;font-weight:800;color:{_saving_col}">{_saving_disp}</div>'
        _tbl += f'<div style="font-size:1rem;color:{_saving_col};margin-top:0.2rem">{_saving_sub}</div>'
        _tbl += "</div>"

        st.markdown(_tbl, unsafe_allow_html=True)
    else:
        st.markdown('''
    <div style="margin-top:1rem;padding:0.8rem 1rem;background:#f0f4ff;border-radius:8px;
         font-size:0.83rem;color:#555;text-align:center;border:1px dashed #c0cce0">
      💡 Fill in the customer's <strong>Current Customer Costs</strong> in the sidebar
      to show a cost comparison here.
    </div>
    ''', unsafe_allow_html=True)



    cv_col1, cv_col2 = st.columns([3, 2])

    with cv_col1:
        st.markdown('<div class="cv-section">🌐 Your Services</div>', unsafe_allow_html=True)
        svc_lines = [
            (f"Business Broadband - {bb_provider} {bb_package}", f"£{svc['bb1_sell']:.2f}/mo"),
        ]
        if second_fttp and second_fttp_pkg:
            bb2_sell = svc["bb2_sell"]
            svc_lines.append((f"2nd Line - {bb_provider} {second_fttp_pkg}", f"£{bb2_sell:.2f}/mo"))
        if total_voice_channels > 0:
            svc_lines.append((f"User / Voice Licences ({total_voice_channels} users)", f"£{svc['lic_monthly']:.2f}/mo"))
        if ooh_support:
            svc_lines.append(("24/7 Out-of-Hours Support", "£25.00/mo"))
        if dark_web_mon:
            svc_lines.append(("Dark Web Monitoring", "£10.00/mo (after 3m FOC)"))
        if proactive_bb:
            svc_lines.append(("Proactive Broadband Management", "£10.00/mo (after 3m FOC)"))
        if mobile_rows:
            mob_total = sum(r["sell"] * r["qty"] for r in mobile_rows)
            svc_lines.append((f"Mobile SIMs ({sum(r['qty'] for r in mobile_rows)} connections)", f"£{mob_total:.2f}/mo"))

        for label, val in svc_lines:
            st.markdown(f"""
            <div class="cv-price-row">
              <span class="cv-price-label">{label}</span>
              <span class="cv-price-val">{val}</span>
            </div>""", unsafe_allow_html=True)

            for _ir in it_rows:
                if _ir["qty"] > 0:
                    all_equip.append((f"IT: {_ir['service']}", _ir["qty"]))
        st.markdown('<div class="cv-section">✅ What\'s Included</div>', unsafe_allow_html=True)
        includes = [
            "Manufacturer hardware warranty",
            "Full configuration & setup",
        ]
        if credits_months > 0:
            includes.append(f"£{credits_amount:.2f}/mo introductory credit for {credits_months} months")
        if cashback_amount > 0:
            includes.append(f"£{cashback_amount:.2f} settlement contribution")

        for item in includes:
            st.markdown(f'<div class="cv-include-item">✅ {item}</div>', unsafe_allow_html=True)

        # Software add-on images - show if any selected
        active_addons = [(name, qty) for name, qty, _, _ in SW_ADDONS if qty > 0]
        if active_addons:
            st.markdown('<div class="cv-section">💻 Software &amp; Add-ons</div>', unsafe_allow_html=True)
            addon_cols = st.columns(min(len(active_addons), 4))
            for idx, (addon_name, addon_qty) in enumerate(active_addons):
                with addon_cols[idx % 4]:
                    b64_sw, ext_sw = get_product_image_b64(addon_name)
                    if b64_sw:
                        st.markdown(
                            f'<div style="background:#f8f9ff;border-radius:10px;padding:0.6rem;text-align:center;margin-bottom:0.5rem">'
                            f'<img src="data:image/{ext_sw};base64,{b64_sw}" style="max-height:70px;max-width:100%;object-fit:contain;border-radius:6px"/>'
                            f'<div style="font-size:0.75rem;color:#1f1450;font-weight:600;margin-top:0.3rem">{addon_name}</div>'
                            f'<div style="font-size:0.7rem;color:#888">x{addon_qty}</div></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div style="background:#f0f4ff;border-radius:10px;padding:0.8rem;text-align:center;margin-bottom:0.5rem">'
                            f'<div style="font-size:1.6rem">💻</div>'
                            f'<div style="font-size:0.75rem;color:#1f1450;font-weight:600;margin-top:0.3rem">{addon_name}</div>'
                            f'<div style="font-size:0.7rem;color:#888">x{addon_qty}</div></div>',
                            unsafe_allow_html=True
                        )


    with cv_col2:
        st.markdown('<div class="cv-section">💳 Your Investment</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="cv-price-row">
          <span class="cv-price-label">{"Hardware Lease (monthly rental)" if is_spread else "Hardware (one-off)"}</span>
          <span class="cv-price-val" style="color:#1f1450;font-weight:700">
            {"£" + f"{hw_monthly_spread:.2f}" + "/mo" if is_spread else "£" + f"{upfront:.2f}"}
          </span>
        </div>
        <div class="cv-price-row">
          <span class="cv-price-label">Network &amp; Services</span>
          <span class="cv-price-val" style="color:#1f1450;font-weight:700">£{svc["total_sell"]:.2f}/mo</span>
        </div>
        <div class="cv-price-row" style="font-weight:700;border-top:2px solid #1f1450;margin-top:4px;padding-top:8px">
          <span style="color:#1f1450">Total (excl. VAT)</span>
          <span style="color:#1f1450;font-size:1.1rem">£{total_mo - _bb_yr1_saving:.2f}/mo</span>
        </div>
        """, unsafe_allow_html=True)
        if bb_free_year and _bb_yr1_saving > 0:
            st.markdown(f"""
            <div style="background:#e8f8f0;border-left:3px solid #1a7a40;border-radius:6px;
                 padding:0.5rem 0.8rem;font-size:0.8rem;color:#1a7a40;margin-top:0.3rem">
              🎁 <strong>Broadband FREE for the first 12 months</strong><br>
              From month 13: £{total_mo:.2f}/mo (broadband £{_bb_full_sell:.2f}/mo resumes)
            </div>""", unsafe_allow_html=True)
        if st.session_state.get("cs_ai_portal_free", False):
            st.markdown("""
            <div style="background:#e8f8f0;border-left:3px solid #1a7a40;border-radius:6px;
                 padding:0.5rem 0.8rem;font-size:0.8rem;color:#1a7a40;margin-top:0.3rem">
              🎁 <strong>AI Integration Portal — first month free</strong> (500 min bundle)<br>
              <span style="font-size:0.75rem">From month 2: £25.00/mo (500 min bundle)</span>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;padding:0.5rem 0;font-size:0.8rem;color:#aaa">
          Agreement term: <strong style="color:#555">{lease_term} months</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:1rem;padding:0.8rem 1rem;background:#f8f9ff;border-radius:8px;font-size:0.82rem;color:#555;text-align:center">
          All figures exclude VAT.<br>
          Subject to survey & credit approval.
        </div>
        """, unsafe_allow_html=True)




# ── TAB 5: CONSULTANT VIEW ──────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="tab-content"></div>', unsafe_allow_html=True)

    # ── Password gate ──────────────────────────────────────────────────────
    if not st.session_state.consultant_unlocked:
        st.markdown("### 💼 Consultant View")
        st.caption("Enter the consultant password to access deal pricing tools.")
        c_col1, c_col2 = st.columns([3, 1])
        with c_col1:
            c_pw = st.text_input("", type="password", placeholder="Enter consultant password...",
                                 label_visibility="collapsed", key="consultant_pw")
        with c_col2:
            if st.button("Unlock 💼", type="primary", use_container_width=True, key="c_unlock"):
                if c_pw == "SYComms2026!!":
                    st.session_state.consultant_unlocked = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
    else:
        # ── Locked button ──────────────────────────────────────────────────
        if st.button("🔒 Lock Consultant View", key="c_lock"):
            st.session_state.consultant_unlocked = False
            st.rerun()

        st.markdown("## 💼 Consultant Deal Tools")

        # ── Deal snapshot strip ────────────────────────────────────────────
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1f1450,#2d1f6e);border-radius:12px;
             padding:1rem 1.5rem;margin-bottom:1.2rem;display:flex;
             justify-content:space-between;align-items:center;color:#fff">
          <div><div style="font-size:0.72rem;color:rgba(255,255,255,0.55)">CUSTOMER</div>
               <div style="font-size:1rem;font-weight:700">{comp_name or "-"}</div></div>
          <div style="text-align:center">
               <div style="font-size:0.72rem;color:rgba(255,255,255,0.55)">BASE MONTHLY</div>
               <div style="font-size:1.4rem;font-weight:800;color:#00b5a3">£{total_mo:.2f}</div></div>
          <div style="text-align:right">
               <div style="font-size:0.72rem;color:rgba(255,255,255,0.55)">TERM</div>
               <div style="font-size:1rem;font-weight:700">{LEASE_TERM_LABELS[lease_term]}</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Desired Rental adjustment ─────────────────────────────────
        st.markdown("### 🎯 Lease Rental Adjustment")
        st.caption("Adjust the hardware lease rental. "
                   "Increasing earns more commission. Decreasing discounts the deal (reduces commission). "
                   "Commission is calculated only on the lease amount, not total monthly.")

        c_left, c_right = st.columns([3, 2])
        with c_left:
            # Only sync from sidebar when flag is set
            if st.session_state.pop("_sync_rental_to_cons", False):
                st.session_state["c_desired_rental_input"] = round(
                    st.session_state.get("c_desired_rental") or base_rental, 2)
            desired_rental_input = st.number_input(
                "Desired Lease Rental (£/mo)",
                min_value=0.01,
                step=1.0,
                key="c_desired_rental_input",
                help=f"Calculated rental: £{base_rental:.2f}. "
                     "Increase to earn more commission, decrease to offer the customer a discount."
            )
            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("✅ Apply Rental", type="primary",
                             use_container_width=True, key="c_apply"):
                    st.session_state["c_desired_rental"]        = desired_rental_input
                    st.session_state["_sync_rental_to_sidebar"] = True
                    st.rerun()
            with btn2:
                if st.button("↩️ Reset to Calculated", use_container_width=True, key="c_reset"):
                    st.session_state["c_desired_rental"]        = 0.0
                    st.session_state["_sync_rental_to_sidebar"] = True
                    st.session_state["_sync_rental_to_cons"]    = True
                    st.rerun()
            est_earnings = commission

        with c_right:
            _adj_colour = "#1a7a40" if rental_adjustment >= 0 else "#c0392b"
            _adj_bg     = "#e8f8f0" if rental_adjustment >= 0 else "#fdf0f0"
            _adj_label  = "Premium vs Calculated" if rental_adjustment >= 0 else "Discount vs Calculated"
            _adj_prefix = "+" if rental_adjustment >= 0 else ""
            st.markdown(f"""
            <div style="background:{_adj_bg};border-left:4px solid {_adj_colour};
                 border-radius:0 8px 8px 0;padding:1rem 1.2rem;margin-top:1.6rem">
              <div style="font-size:0.72rem;color:{_adj_colour};font-weight:700;text-transform:uppercase">{_adj_label}</div>
              <div style="font-size:1.6rem;font-weight:800;color:{_adj_colour}">{_adj_prefix}£{rental_adjustment:.2f}/mo</div>
              <div style="font-size:0.8rem;color:#555;margin-top:0.2rem">
                Calculated: £{base_rental:.2f}/mo &nbsp;·&nbsp; Desired: £{_desired_rental:.2f}/mo
              </div>
            </div>
            """, unsafe_allow_html=True)


        # Row 1 - Lease-only comparison
        r1a, r1b, r1c = st.columns(3)
        with r1a:
            if current_system > 0:
                st.markdown(f"""
                <div style="background:#fff;border:2px solid #e0e8f0;border-radius:12px;
                     padding:1.2rem;text-align:center">
                  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:.08em;color:#888;margin-bottom:0.5rem">Phone System / Lease (Current)</div>
                  <div style="font-size:2rem;font-weight:800;color:#c0392b">£{current_system:.2f}</div>
                  <div style="font-size:0.78rem;color:#aaa">per month + VAT</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#f8f9ff;border:2px dashed #d0d8e8;border-radius:12px;
                     padding:1.2rem;text-align:center">
                  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:.08em;color:#888;margin-bottom:0.5rem">Phone System / Lease (Current)</div>
                  <div style="font-size:1rem;color:#aaa">Enter under<br>Current Costs →</div>
                </div>
                """, unsafe_allow_html=True)

        with r1b:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1f1450,#2d1f6e);
                 border-radius:12px;padding:1.2rem;text-align:center;border:2px solid #00b5a3">
              <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                   letter-spacing:.08em;color:rgba(255,255,255,0.6);margin-bottom:0.5rem">New Monthly Lease with SY Comms</div>
              <div style="font-size:2rem;font-weight:800;color:#00b5a3">£{_desired_rental:.2f}</div>
              <div style="font-size:0.78rem;color:rgba(255,255,255,0.5)">hardware lease per month + VAT</div>
            </div>
            """, unsafe_allow_html=True)

        with r1c:
            if current_system > 0:
                _ls_saving = current_system - _desired_rental
                _ls_col    = "#1a7a40" if _ls_saving >= 0 else "#c0392b"
                _ls_bg     = "#e8f8f0" if _ls_saving >= 0 else "#fdf0f0"
                _ls_lbl    = "Lease Saving" if _ls_saving >= 0 else "Lease Increase"
                _ls_pfx    = "-" if _ls_saving >= 0 else "+"
                st.markdown(f"""
                <div style="background:{_ls_bg};border:2px solid {_ls_col};
                     border-radius:12px;padding:1.2rem;text-align:center">
                  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:.08em;color:{_ls_col};margin-bottom:0.5rem">{_ls_lbl}</div>
                  <div style="font-size:2rem;font-weight:800;color:{_ls_col}">{_ls_pfx}£{abs(_ls_saving):.2f}</div>
                  <div style="font-size:0.78rem;color:{_ls_col}">per month  &middot;  {_ls_pfx}£{abs(_ls_saving*12):.0f}/yr</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#f8f9ff;border:2px dashed #d0d8e8;border-radius:12px;
                     padding:1.2rem;text-align:center">
                  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:.08em;color:#888;margin-bottom:0.5rem">Lease Saving</div>
                  <div style="font-size:1rem;color:#aaa">Add current costs<br>to calculate</div>
                </div>
                """, unsafe_allow_html=True)

        # Row 2 - Full monthly total
        # Use adjusted values from breakdown if consultant has made changes
        _c_adj_total = svc["total_sell"] + _desired_rental
        _diff_total    = current_total - _c_adj_total
        _diff_col      = "#1a7a40" if _diff_total >= 0 else "#c0392b"
        _curr_total_str = f"£{current_total:.2f}" if current_total > 0 else "-"
        _curr_sys_str   = f"£{current_system:.2f}" if current_system > 0 else "-"
        st.markdown(f"""
        <div style="background:#f0f4ff;border:1px solid #c0cce0;border-radius:10px;
             padding:0.8rem 1.2rem;margin-top:0.5rem">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div style="flex:1;text-align:center;border-right:1px solid #c0cce0;padding-right:1rem">
              <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:#888">Customer Current Total</div>
              <div style="font-size:1.4rem;font-weight:800;color:#c0392b">{_curr_total_str}<span style="font-size:0.75rem;font-weight:400"> /mo</span></div>
              <div style="font-size:0.72rem;color:#aaa">Lease {_curr_sys_str} + other spend</div>
            </div>
            <div style="flex:1;text-align:center;padding:0 1rem">
              <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:#1f1450">New Monthly Total (Lease + Services)</div>
              <div style="font-size:1.6rem;font-weight:800;color:#1f1450">£{_c_adj_total:.2f}<span style="font-size:0.75rem;font-weight:400"> + VAT</span></div>
              <div style="font-size:0.72rem;color:#555">£{_desired_rental:.2f} lease + £{svc["total_sell"]:.2f} services</div>
            </div>
            <div style="flex:1;text-align:center;border-left:1px solid #c0cce0;padding-left:1rem">
              <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:{_diff_col}">{"Total Saving" if _diff_total >= 0 else "Total Increase"}</div>
              <div style="font-size:1.4rem;font-weight:800;color:{_diff_col}">{"+" if _diff_total < 0 else "-"}£{abs(_diff_total):.2f}<span style="font-size:0.75rem;font-weight:400"> /mo</span></div>
              <div style="font-size:0.72rem;color:{_diff_col}">£{abs(_diff_total*12):.0f}/yr</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


        st.markdown("")

        # Row 2 - Commission (full width, prominent)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d4a2a,#1a7a40);border-radius:12px;
             padding:1.4rem 2rem;margin-top:0.5rem;display:flex;
             justify-content:space-between;align-items:center">
          <div>
            <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;
                 letter-spacing:.1em;color:rgba(255,255,255,0.6)">Your Estimated Commission</div>
            <div style="font-size:2.2rem;font-weight:800;color:#fff">£{est_earnings:.2f}</div>
          <div style="font-size:0.82rem;color:rgba(255,255,255,0.55)">{commission_units:.2f} units × £{commission_per_unit:.0f} - {LEASE_TERM_LABELS[lease_term]}</div>\n          </div>
          {"<div style='text-align:right'><div style='font-size:0.75rem;color:rgba(255,255,255,0.5);'>Rate Uplift Applied</div><div style='font-size:1.3rem;font-weight:700;color:#7fe8a0'>+£" + f"{rate_uplift:.2f}" + "/mo</div></div>" if rate_uplift > 0 else "<div style='text-align:right'><div style='font-size:0.75rem;color:rgba(255,255,255,0.5)'>Tip</div><div style='font-size:0.88rem;color:rgba(255,255,255,0.7)'>Increase the monthly<br>rate above to earn more</div></div>"}
        </div>
        """, unsafe_allow_html=True)


        # ── Services Discount (slider) ────────────────────────────────────────
        _appt = st.session_state.get("q_appt_type", "Self Gen")
        _appt_rates = {"Self Gen": 1000, "Base Deal": 600, "Acquisition": 500, "Telemarketer": 650}
        st.info(f"📋 Appointment type: **{_appt}** — commission rate £{_appt_rates.get(_appt, 1000):,}/unit")
        st.markdown("### 🏷️ Services Discount")
        st.caption("Discount monthly licences, software & broadband by up to 40%. "
                   "Every 1% of discount removes 1% of your commission.")

        def _sync_svc_disc():
            st.session_state["c_svc_disc"]    = st.session_state["c_svc_disc_w"]
            st.session_state["q_svc_discount"] = st.session_state["c_svc_disc_w"]

        _sd_col1, _sd_col2 = st.columns([3, 2])
        with _sd_col1:
            # Keep widget key in sync with c_svc_disc (allows sidebar to push value here)
            st.session_state["c_svc_disc_w"] = int(st.session_state.get("c_svc_disc", 0))
            st.slider("Services discount (%)", min_value=0, max_value=40, step=5,
                      key="c_svc_disc_w", on_change=_sync_svc_disc,
                      help="Applies to hosted user licences, software add-ons and broadband. "
                           "Broadband can never go below wholesale cost. Mobiles are not discountable.")

            def _svc_row(label, list_price, new_price, note=""):
                _chg = new_price < list_price - 0.005
                _was = (f"<span style='color:#aaa;text-decoration:line-through;margin-right:0.5rem'>£{list_price:.2f}</span>"
                        if _chg else "")
                _nt  = f"<span style='color:#aaa;font-size:0.75rem'> {note}</span>" if note else ""
                return (f"<div style='display:flex;justify-content:space-between;padding:0.35rem 0;"
                        f"border-bottom:1px solid #f0f0f0;font-size:0.88rem'>"
                        f"<span style='color:#555'>{label}{_nt}</span>"
                        f"<span>{_was}<strong style='color:#1f1450'>£{new_price:.2f}/mo</strong></span></div>")

            _svc_saving = ((lic_list_total - svc["lic_monthly"]) + (sw_list_total - sw_sell_total) +
                           (bb1_list + bb2_list - svc["bb_sell"]))
            _rows = ""
            if lic_list_total > 0:
                _rows += _svc_row(f"Hosted User Licences ({total_voice_channels} users)", lic_list_total, svc["lic_monthly"])
            for _an, _aq, _ac, _asell in SW_ADDONS:
                if _aq > 0:
                    _alist = _asell / _svc_mult if _svc_mult > 0 else _asell
                    _rows += _svc_row(f"{_an} x{_aq}", _alist * _aq, _asell * _aq)
            if bb1_list > 0:
                _rows += _svc_row(f"Broadband - {bb_package}", bb1_list, svc["bb1_sell"],
                                  "(at wholesale floor)" if svc_disc_pct > 0 and svc["bb1_sell"] <= svc["bb1_floor"] + 0.005 else "")
            if bb2_list > 0:
                _rows += _svc_row(f"Broadband 2nd line - {second_fttp_pkg}", bb2_list, svc["bb2_sell"],
                                  "(at wholesale floor)" if svc_disc_pct > 0 and svc["bb2_sell"] <= svc["bb2_floor"] + 0.005 else "")
            if svc.get("mobile_sell", 0) > 0:
                _rows += _svc_row("Mobiles", svc["mobile_sell"], svc["mobile_sell"], "(fixed)")
            if not _rows:
                _rows = "<div style='color:#aaa;font-size:0.85rem'>No licences or services on this deal yet.</div>"
            st.markdown(_rows + _svc_row("<strong>Total monthly services</strong>",
                                         svc["total_sell"] + _svc_saving,
                                         svc["total_sell"]),
                        unsafe_allow_html=True)

        with _sd_col2:
            _cm_col = "#c0392b" if commission_lost > 0 else "#1a7a40"
            _cm_bg  = "#fdf0f0" if commission_lost > 0 else "#e8f8f0"
            st.markdown(f"""
            <div style="background:{_cm_bg};border-left:4px solid {_cm_col};
                 border-radius:0 8px 8px 0;padding:1rem 1.2rem;margin-top:1.6rem">
              <div style="font-size:0.72rem;color:{_cm_col};font-weight:700;text-transform:uppercase">Commission Impact</div>
              <div style="font-size:0.85rem;color:#555;margin-top:0.3rem">Before discount: <strong>£{commission_full:.2f}</strong></div>
              <div style="font-size:0.85rem;color:{_cm_col}">Discount {svc_disc_pct:.0f}%: <strong>-£{commission_lost:.2f}</strong></div>
              <div style="font-size:1.5rem;font-weight:800;color:#1f1450;margin-top:0.3rem">£{commission:.2f}</div>
              <div style="font-size:0.75rem;color:#888">Services saving to customer: £{_svc_saving:.2f}/mo</div>
            </div>
            """, unsafe_allow_html=True)

        # Values used by the panels below
        adj_rental      = float(_desired_rental)
        adj_total_mo    = svc["total_sell"] + adj_rental
        _adj_units      = commission_units
        _adj_commission = commission

        # Feasibility mini-panel ────────────────────────────────────────────────
        _buyout_rental      = (pl_data["sales_rate"] / 1000.0) * termination_cost
        _feas_lease_total   = max(adj_rental - _buyout_rental, 0) * lease_term
        _feas_max_settle    = round(_feas_lease_total * 0.70, 2)
        _settle_ok          = termination_cost <= _feas_max_settle
        _f_col  = "#1a7a40" if _settle_ok else "#c0392b"
        _f_bg   = "#e8f8f0" if _settle_ok else "#fdf0f0"
        _f_icon = "✅" if _settle_ok else "🔴"
        _f_msg  = "Settlement feasible" if _settle_ok else "Settlement exceeds 70% - review"
        _f_diff = _feas_max_settle - termination_cost

        st.markdown(f"""
        <div style="margin-top:0.8rem;padding:0.8rem 1.2rem;background:{_f_bg};border:1px solid {_f_col};
             border-radius:10px;display:flex;justify-content:space-between;align-items:center">
          <div>
            <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;color:{_f_col}">
              {_f_icon} Feasibility - Max Settlement (70%)</div>
            <div style="font-size:1.2rem;font-weight:800;color:{_f_col}">£{_feas_max_settle:.2f}</div>
            <div style="font-size:0.78rem;color:{_f_col}">{_f_msg} &nbsp;·&nbsp;
              {"£" + f"{abs(_f_diff):.2f}" + " headroom" if _settle_ok else "£" + f"{abs(_f_diff):.2f}" + " over limit"}
            </div>
          </div>
          <div style="text-align:right">
            <div style="font-size:0.75rem;color:{_f_col}">Settlement / Buyout</div>
            <div style="font-size:1.4rem;font-weight:800;color:{_f_col}">£{termination_cost:.2f}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Summary bar ────────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="background:#1f1450;border-radius:10px;padding:0.8rem 1.2rem;margin-top:0.6rem;
             display:flex;justify-content:space-between;align-items:center;color:#fff">
          <div><span style="font-size:0.8rem;color:rgba(255,255,255,0.6)">ADJUSTED TOTAL</span>
               <div style="font-size:1.6rem;font-weight:800;color:#00b5a3">£{adj_total_mo:.2f}/mo</div></div>
          <div style="text-align:right">
               <span style="font-size:0.8rem;color:rgba(255,255,255,0.6)">COMMISSION ON ADJ. RENTAL</span>
               <div style="font-size:1.4rem;font-weight:700;color:#7fe8a0">£{_adj_commission:.2f}
               <span style="font-size:0.8rem;font-weight:400"> ({_adj_units:.2f} units)</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Sales Calcs (pricebook-style) ─────────────────────────────────
        st.markdown("### 📐 Sales Calcs")
        _cash_price_load = 1.10   # pricebook: Cash Price Load % = 1.10
        _cash_price      = round(pl_data["sub_total"] * _cash_price_load, 2)
        _cash_gp         = _cash_price - pl_data["cos_full"]
        _cash_units      = round(_cash_gp / 4000, 2)

        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e0e8f0;border-radius:10px;
                 padding:1rem;font-size:0.85rem">
              <table style="width:100%;border-collapse:collapse">
                <tr><td style="color:#888;padding:3px 0">Cash Sale?</td>
                    <td style="font-weight:600;text-align:right">No (Lease)</td></tr>
                <tr><td style="color:#888;padding:3px 0">Term</td>
                    <td style="font-weight:600;text-align:right">1+{lease_term-1}</td></tr>
                <tr><td style="color:#888;padding:3px 0">Rental (Calculated)</td>
                    <td style="font-weight:600;text-align:right;color:#1f1450">£{pl_data["rental"]:.2f}</td></tr>
                <tr><td style="color:#888;padding:3px 0">Adjustment</td>
                    <td style="font-weight:600;text-align:right;color:{"#1a7a40" if rental_adjustment>=0 else "#c0392b"}">{"+" if rental_adjustment>=0 else ""}£{rental_adjustment:.2f}</td></tr>
                <tr><td style="color:#888;padding:3px 0">Units</td>
                    <td style="font-weight:600;text-align:right;color:#00b5a3">{commission_units:.2f}</td></tr>
                <tr><td style="color:#888;padding:3px 0">Desired Rental</td>
                    <td style="font-weight:600;text-align:right;color:#1f1450">£{_desired_rental:.2f}</td></tr>
                <tr style="border-top:1px solid #eee">
                    <td style="color:#888;padding:3px 0">Adjustment Required</td>
                    <td style="font-weight:600;text-align:right">£{abs(rental_adjustment):.2f}</td></tr>
              </table>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e0e8f0;border-radius:10px;
                 padding:1rem;font-size:0.85rem">
              <table style="width:100%;border-collapse:collapse">
                <tr><td style="color:#888;padding:3px 0">Cash Adjustment</td>
                    <td style="font-weight:600;text-align:right">£0.00</td></tr>
                <tr><td style="color:#888;padding:3px 0">Cash Price</td>
                    <td style="font-weight:600;text-align:right">£{_cash_price:.2f}</td></tr>
                <tr><td style="color:#888;padding:3px 0">Cash Units</td>
                    <td style="font-weight:600;text-align:right">{_cash_units:.2f}</td></tr>
                <tr style="border-top:1px solid #eee">
                    <td style="color:#888;padding:3px 0">Other Costs</td>
                    <td style="font-weight:600;text-align:right">£{termination_cost:.2f}</td></tr>
                <tr><td style="color:#888;padding:3px 0">Sub Total</td>
                    <td style="font-weight:600;text-align:right">£{pl_data["sub_total"]:.2f}</td></tr>
                <tr><td style="color:#888;padding:3px 0">Gross Profit</td>
                    <td style="font-weight:600;text-align:right;color:#1a7a40">£{pl_data["gross_profit"]:.2f}</td></tr>
              </table>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")
        # ── Proposal notes ─────────────────────────────────────────────────
        st.markdown("### 📝 Consultant Notes / Special Conditions")
        consultant_notes = st.text_area(
            "", height=100, key="c_notes",
            placeholder="Add any special conditions, agreed credits, or notes for this deal...",
            label_visibility="collapsed"
        )

# ── TAB 6: SIGN & SEND ────────────────────────────────────────────────────────

    # ── Feasibility Calculator ──────────────────────────────────────────
    st.markdown('---')
    with st.expander('📊 Feasibility Calculator', expanded=False):
        st.caption('Checks whether the customer\'s existing settlement can be absorbed into the new lease.')
        st.markdown('## 📊 Feasibility Calculator')
        st.caption('Checks whether the customer\'s existing settlement can be absorbed into the new lease.')
    
        _new_rental    = float(st.session_state.get('adj_rent', pl_data['rental']))
        _buyout_rental = (pl_data['sales_rate'] / 1000.0) * termination_cost
        _lease_total   = max(_new_rental - _buyout_rental, 0) * lease_term
        _max_settlement = round(_lease_total * 0.70, 2)
        _settlement_ok  = termination_cost <= _max_settlement
    
        feas_col1, feas_col2 = st.columns(2)
        with feas_col1:
            st.markdown(f"""
            <div style='background:#fff;border:1px solid #e0e8f0;border-radius:12px;padding:1.2rem'>
              <div style='font-size:0.75rem;font-weight:700;text-transform:uppercase;color:#888'>New Monthly Rental</div>
              <div style='font-size:2rem;font-weight:800;color:#1f1450'>£{_new_rental:.2f}</div>
              <div style='font-size:0.8rem;color:#aaa'>per month over {LEASE_TERM_LABELS[lease_term]}</div>
              <hr style='margin:0.8rem 0'>
              <div style='font-size:0.75rem;font-weight:700;text-transform:uppercase;color:#888'>Total Lease Value</div>
              <div style='font-size:1.3rem;font-weight:700;color:#1f1450'>£{_lease_total:.2f}</div>
              <div style='font-size:0.8rem;color:#aaa'>({lease_term} months × £{_new_rental:.2f})</div>
              <hr style='margin:0.8rem 0'>
              <div style='font-size:0.75rem;font-weight:700;text-transform:uppercase;color:#888'>Max Settlement (70%)</div>
              <div style='font-size:1.6rem;font-weight:800;color:#1a7a40'>£{_max_settlement:.2f}</div>
              <div style='font-size:0.8rem;color:#aaa'>70% of total lease value</div>
            </div>
            """, unsafe_allow_html=True)
        with feas_col2:
            _col  = '#1a7a40' if _settlement_ok else '#c0392b'
            _bg   = '#e8f8f0' if _settlement_ok else '#fdf0f0'
            _icon = '✅' if _settlement_ok else '🔴'
            _msg  = 'Settlement FEASIBLE' if _settlement_ok else 'Settlement EXCEEDS 70% - Review Required'
            _diff = _max_settlement - termination_cost
            st.markdown(f"""
            <div style='background:{_bg};border:2px solid {_col};border-radius:12px;padding:1.4rem;text-align:center'>
              <div style='font-size:2.5rem'>{_icon}</div>
              <div style='font-size:1rem;font-weight:700;color:{_col};margin-top:0.5rem'>{_msg}</div>
              <hr style='margin:0.8rem 0;border-color:{_col};opacity:0.3'>
              <div style='font-size:0.75rem;font-weight:700;text-transform:uppercase;color:{_col}'>Customer Settlement / Buyout</div>
              <div style='font-size:1.8rem;font-weight:800;color:{_col}'>£{termination_cost:.2f}</div>
              <div style='font-size:0.8rem;color:{_col};margin-top:0.4rem'>
                {'£' + f'{abs(_diff):.2f}' + ' headroom remaining' if _settlement_ok else '£' + f'{abs(_diff):.2f}' + ' over the 70% limit'}
              </div>
            </div>
            """, unsafe_allow_html=True)
    
        if termination_cost == 0:
            st.info('💡 Enter a buyout / termination cost in the sidebar Deal Adjustments to run the feasibility check.')
    
    

with tab6:
    st.markdown('<div class="tab-content"></div>', unsafe_allow_html=True)

    if not comp_name:
        st.warning("👈 Add a customer name in the sidebar first.")
    em_cfg = st.session_state.active_config.get("email", {})

    # Capture client IP from Streamlit request headers (best effort)
    def _get_ip():
        try:
            headers = st.context.headers
            for h in ["X-Forwarded-For", "X-Real-IP", "CF-Connecting-IP", "True-Client-IP"]:
                ip = headers.get(h, "")
                if ip:
                    return ip.split(",")[0].strip()
        except Exception:
            pass
        return "Not captured"
    _client_ip = _get_ip()

    # ── Deal summary strip ────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1f1450,#2d1f6e);border-radius:12px;
            padding:1rem 1.5rem;margin-bottom:1.2rem;display:flex;
            justify-content:space-between;align-items:center;color:#fff">
      <div>
    <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:.08em">Customer</div>
    <div style="font-size:1.1rem;font-weight:700">{comp_name}</div>
      </div>
      <div style="text-align:center">
    <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:.08em">Monthly Services</div>
    <div style="font-size:1.4rem;font-weight:800;color:#00b5a3">£{total_mo:.2f} + VAT</div>
      </div>
      <div style="text-align:right">
    <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:.08em">Upfront</div>
    <div style="font-size:1.1rem;font-weight:700">£{upfront:.2f} + VAT</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    sign_col, send_col = st.columns([3, 2])

    with sign_col:
        st.markdown("### Customer Signature")
        st.caption("Ask the customer to sign below, or photograph their signature.")

        # Two options: draw on screen OR upload photo
        sig_method = st.radio(
            "Capture method:",
            ["Draw on screen", "Upload photo of signature"],
            horizontal=True, key="sig_method_radio"
        )

        if sig_method == "Upload photo of signature":
            st.caption("Take a photo of the customer's handwritten signature or upload an image file.")
            sig_upload = st.file_uploader(
                "Signature image (JPG or PNG)", type=["jpg","jpeg","png"],
                key="sig_photo_upload", label_visibility="collapsed"
            )
            if sig_upload:
                from PIL import Image as _PILImage
                _simg = _PILImage.open(sig_upload).convert("RGB")
                # Resize to standard signature dimensions
                _simg = _simg.resize((400, 120), _PILImage.LANCZOS)
                _sbuf = io.BytesIO()
                _simg.save(_sbuf, format="PNG")
                st.session_state["_sig_bytes"] = _sbuf.getvalue()
                st.image(sig_upload, caption="Signature preview", width=300)
                st.success("Signature uploaded")
            elif not st.session_state.get("_sig_bytes"):
                st.session_state.pop("_sig_bytes", None)

        else:  # Draw on screen
            if not CANVAS_OK:
                st.warning("Drawing pad unavailable. Please use Upload photo instead.")
            else:
                with st.container(border=True):
                    st.caption("Draw with mouse, finger or stylus. Toolbar (top-right of box) to undo/clear.")
                    try:
                        canvas_result = st_canvas(
                            fill_color="rgba(0,0,0,0)",
                            stroke_width=3,
                            stroke_color="#000000",
                            background_color="#EAF4FB",
                            update_streamlit=True,
                            return_image_data=True,
                            height=180,
                            width=510,
                            drawing_mode="freedraw",
                            display_toolbar=True,
                            key="sig_canvas",
                        )
                    except TypeError:
                        canvas_result = st_canvas(
                            fill_color="rgba(0,0,0,0)",
                            stroke_width=3,
                            stroke_color="#000000",
                            background_color="#EAF4FB",
                            update_streamlit=True,
                            return_image_data=True,
                            height=180,
                            width=510,
                            drawing_mode="freedraw",
                            key="sig_canvas",
                        )
                # Explicit save button - more reliable than auto-detect
                _btn_col, _clr_col = st.columns(2)
                with _btn_col:
                    if st.button("✅ Save Signature", use_container_width=True,
                                 type="primary", key="btn_save_sig"):
                        try:
                            _img_data = canvas_result.image_data if canvas_result else None
                            if _img_data is not None:
                                from PIL import Image as _PILImage
                                # Save as RGBA PNG - fpdf2 temp file handles transparency
                                sig_pil = _PILImage.fromarray(
                                    _img_data.astype("uint8"), "RGBA"
                                )
                                # Flatten onto white
                                _white = _PILImage.new("RGBA", sig_pil.size, (255,255,255,255))
                                _white.paste(sig_pil, mask=sig_pil.split()[3])
                                sig_pil_rgb = _white.convert("RGB")
                                sig_buf = io.BytesIO()
                                sig_pil_rgb.save(sig_buf, format="PNG")
                                st.session_state["_sig_bytes"] = sig_buf.getvalue()
                                st.rerun()
                            else:
                                st.warning("Canvas returned no data - please try Upload photo.")
                        except Exception as _ce:
                            st.warning(f"Canvas capture failed ({type(_ce).__name__}: {_ce}). Use Upload photo.")
                with _clr_col:
                    if st.button("🗑️ Clear", use_container_width=True, key="btn_clr_sig"):
                        st.session_state.pop("_sig_bytes", None)
                        st.rerun()

        sig_bytes = st.session_state.get("_sig_bytes")
        if sig_bytes:
            # Show preview so consultant can confirm it captured correctly
            st.success("✅ Signature saved")
            try:
                st.image(sig_bytes, width=200, caption="Signature preview")
            except Exception:
                pass
        else:
            st.caption("✏️ Draw signature above then click Save Signature")

        sig_bytes = st.session_state.get("_sig_bytes")
        if sig_bytes:
            st.success("✅ Signature saved - ready to download")
        else:
            st.caption("✏️ Draw signature above then click Save Signature")

        # Confirm name typed
        sig_name = st.text_input("Customer full name (typed confirmation)",
                                 value=contact_name or "", key="sig_name_confirm",
                                 placeholder="e.g. Jane Smith - Director")
    with send_col:
        st.markdown("### 📥 Download & Send")
        sig_bytes = st.session_state.get("_sig_bytes")
        safe = (comp_name or "quote").replace(" ","_")

        # ── Download unsigned PDF (always available) ─────────────────────────
        st.markdown("**Unsigned Pack**")
        st.caption("Full proposal pack without signature - for review or printing.")
        _unsigned_bytes = build_pdf(
            sig_bytes=None,
            curr_total=current_total, curr_bb=current_bb,
            curr_system=current_system, curr_calls=current_calls,
            curr_mobile=current_mobile,
        )
        st.download_button(
            "📥 Download Full Pack (Unsigned)",
            data=_unsigned_bytes,
            file_name=f"SYComms_{safe}_{date.today()}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="dl_unsigned",
        )

        st.divider()

        # ── Generate & download signed PDF ───────────────────────────────────
        st.markdown("**Signed Pack**")
        # Status check
        _missing = []
        if not sig_bytes: _missing.append("signature")
        if not sig_name:  _missing.append("customer name")
        if _missing:
            st.caption(f"Still needed: {', '.join(_missing)}")
        if sig_bytes and sig_name:
            from datetime import datetime as _dtnow
            _ts = _dtnow.now().strftime("%d/%m/%Y  %H:%M")
            _signed_bytes = build_pdf(
                sig_bytes=sig_bytes,
                sig_name=sig_name,
                sig_company=comp_name or "",
                sig_timestamp=_ts,
                sig_ip=_client_ip,
                curr_total=current_total, curr_bb=current_bb,
                curr_system=current_system, curr_calls=current_calls,
                curr_mobile=current_mobile,
            )
            st.session_state["_signed_pdf_bytes"]    = _signed_bytes
            st.session_state["_signed_pdf_filename"] = f"SYComms_{safe}_SIGNED_{date.today()}.pdf"
            st.download_button(
                "✅ Download Signed Pack",
                data=_signed_bytes,
                file_name=f"SYComms_{safe}_SIGNED_{date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
                key="dl_signed",
            )
        else:
            st.info("Add signature and name on the left to enable the signed download.")
            st.button("✅ Download Signed Pack", disabled=True,
                      use_container_width=True, key="dl_signed_dis")

        st.divider()


    st.divider()
    st.markdown("### ✍️ Send via Zoho Sign")
    st.caption("Download the signed pack above, then upload it to Zoho Sign to send the customer a legally-binding e-signature request.")
    st.link_button("Open Zoho Sign →", "https://sign.zoho.eu", use_container_width=False)

with tab7:
    st.markdown('<div class="tab-content"></div>', unsafe_allow_html=True)

    st.markdown("### 🔐 Manager & Admin Panel")

    # ── PASSWORD GATE ──────────────────────────────────────────────────────────
    if not st.session_state.admin_unlocked:
        st.markdown("#### Enter password to unlock")
        pw_col1, pw_col2 = st.columns([3, 1])
        with pw_col1:
            entered_pw = st.text_input("Password", type="password", key="admin_pw_input", label_visibility="collapsed", placeholder="Enter manager password...")
        with pw_col2:
            if st.button("Unlock 🔓", use_container_width=True):
                h = hashlib.sha256(entered_pw.encode()).hexdigest()
                if h == st.session_state.active_config["meta"]["password_hash"]:
                    st.session_state.admin_unlocked = True
                    st.rerun()
                else:
                    st.error("Incorrect password")
        # Still need these vars defined even when locked
        override_customer = ""; override_initials = ""
        override_monthly_lease = 0.0; override_bb_sell = 0.0
        override_upfront = 0.0; override_install_cost = 0.0
        credits_months = 0; credits_amount = 0.0; cashback_amount = 0.0
    else:
        # ── UNLOCKED - show lock button + tabs ─────────────────────────────────
        lock_col, info_col = st.columns([1, 4])
        with lock_col:
            if st.button("🔒 Lock Panel", use_container_width=True):
                st.session_state.admin_unlocked = False
                st.rerun()
        with info_col:
            st.markdown('<span class="override-badge">🔓 Admin Unlocked</span>', unsafe_allow_html=True)

        panel_tabs = st.tabs(["📋 Per-Deal Overrides", "🖥️ Hardware", "💳 Service Pricing", "🌐 Broadband & Rates", "💰 Costs & Fees", "🎨 Branding", "📧 Email", "📸 Images", "🔒 Security"])

        # ── TAB 1: Per-Deal Overrides (existing functionality) ────────────────
        with panel_tabs[0]:
            mgr_col1, mgr_col2 = st.columns(2)
            with mgr_col1:
                override_customer = st.text_input("Customer Name (for audit)", key="mgr_cust")
                override_initials = st.text_input("Manager Initials", key="mgr_init")
                override_monthly_lease = 0.0  # not used in recurring
                override_bb_sell = st.number_input("Override BB Sell (£/mo) - 0 = auto", min_value=0.0, value=float(st.session_state.get("adm_bb_override",0.0)), step=1.0, key="adm_bb_override")
            with mgr_col2:
                override_upfront = st.number_input("Override Upfront Capital (£) - 0 = auto", min_value=0.0, value=float(st.session_state.get("adm_override_upfront",0.0)), step=10.0, key="adm_override_upfront")
                override_install_cost = st.number_input("Override Install Charge (£) - 0 = auto", min_value=0.0, value=float(st.session_state.get("adm_override_install",0.0)), step=50.0, key="adm_override_install")
                credits_months = st.number_input("Introductory Credit Period (months)", min_value=0, value=int(st.session_state.get("adm_credits_months",0)), step=1, key="adm_credits_months")
                credits_amount = st.number_input("Monthly Credit Amount (£)", min_value=0.0, value=float(st.session_state.get("adm_credits_amount",0.0)), step=5.0, key="adm_credits_amount")
                cashback_amount = st.number_input("Cashback / Settlement Fund (£)", min_value=0.0, value=float(st.session_state.get("adm_cashback",0.0)), step=50.0, key="adm_cashback")

        # ── TAB 2: Hardware Catalogue ──────────────────────────────────────────
        with panel_tabs[1]:
            st.markdown("**System Desk Phones** - edit buy prices, add or remove rows")
            desk_df = pd.DataFrame(cfg["handsets_desktop"])
            edited_desk = st.data_editor(desk_df, num_rows="dynamic", use_container_width=True, key="de_desktop",
                column_config={"poe": st.column_config.CheckboxColumn("PoE"),
                               "buy": st.column_config.NumberColumn("Buy £", format="%.2f"),
                               "cat": st.column_config.SelectboxColumn("Category", options=["Desktop","Conference"])})

            st.markdown("**Cordless Handsets**")
            cord_df = pd.DataFrame(cfg["handsets_cordless"])
            edited_cord = st.data_editor(cord_df, num_rows="dynamic", use_container_width=True, key="de_cordless",
                column_config={"bogof": st.column_config.CheckboxColumn("BOGOF Promo"),
                               "buy": st.column_config.NumberColumn("Buy £", format="%.2f"),
                               "cat": st.column_config.SelectboxColumn("Category", options=["Wi-Fi","DECT"])})

            st.markdown("**Headsets**")
            hs_df = pd.DataFrame(cfg["headsets"])
            edited_hs = st.data_editor(hs_df, num_rows="dynamic", use_container_width=True, key="de_headsets",
                column_config={"buy": st.column_config.NumberColumn("Buy £", format="%.2f")})

            # ── Call Scope AI Setup cost ──────────────────────────────────
            st.markdown("**Call Scope AI Setup (one-off lease cost)**")
            _cs_item = next((i for i in cfg["other_hardware"]
                             if i.get("name") == "Call Scope AI Setup (one-off)"), None)
            _cs_buy  = float(_cs_item["buy"]) if _cs_item else 1000.0
            _cs_sell = float(_cs_item.get("sell", 2500.0)) if _cs_item else 2500.0
            cs_col1, cs_col2 = st.columns(2)
            with cs_col1:
                new_cs_buy  = st.number_input("Setup Cost to SY Comms (Buy £)", value=_cs_buy,
                                               step=50.0, key="cs_buy_input")
            with cs_col2:
                new_cs_sell = st.number_input("Setup Price to Customer (Sell £)", value=_cs_sell,
                                               step=50.0, key="cs_sell_input")
            if st.button("Update Call Scope Setup Cost", key="cs_update"):
                for item in st.session_state.active_config["other_hardware"]:
                    if item.get("name") == "Call Scope AI Setup (one-off)":
                        item["buy"]  = new_cs_buy
                        item.setdefault("sell", new_cs_sell)
                        item["sell"] = new_cs_sell
                        break
                else:
                    st.session_state.active_config["other_hardware"].append(
                        {"name": "Call Scope AI Setup (one-off)", "buy": new_cs_buy, "sell": new_cs_sell}
                    )
                st.success(f"Updated: Buy £{new_cs_buy:.2f} / Sell £{new_cs_sell:.2f}")
                st.rerun()
            st.markdown("---")
            st.markdown("**Other Hardware**")
            st.markdown("**Call Scope Platform — Service Pricing**")
            cs_svc_df = pd.DataFrame(cfg.get("call_scope_services", []))
            if not cs_svc_df.empty:
                edited_cs = st.data_editor(cs_svc_df, num_rows="dynamic",
                    use_container_width=True, key="de_cs_svc",
                    column_config={
                        "buy": st.column_config.NumberColumn("Buy £/user/mo", format="%.2f"),
                        "sell": st.column_config.NumberColumn("Sell £/user/mo", format="%.2f")})

                if st.button("Apply Call Scope Service Pricing", key="cs_svc_apply"):
                    st.session_state.active_config["call_scope_services"] = edited_cs.to_dict("records")
                    st.success("Call Scope service pricing updated"); st.rerun()
            st.markdown("**Call Scope Lease Items (incl. Platform Setup Fee)**")
            _cs_lease_items = [i for i in cfg.get("other_hardware", [])
                               if i.get("name","") in ("Call Answer (500 mins)", "Website Widget", "Call Scope Platform Setup")]
            cs_lease_df = pd.DataFrame(_cs_lease_items)
            if not cs_lease_df.empty:
                edited_csl = st.data_editor(cs_lease_df, num_rows="fixed",
                    use_container_width=True, key="de_cs_lease",
                    column_config={
                        "buy": st.column_config.NumberColumn("Buy £", format="%.2f"),
                        "sell": st.column_config.NumberColumn("Sell £", format="%.2f")})
                if st.button("Apply Call Scope Lease Pricing", key="csl_apply"):
                    names_to_update = {r["name"]: r for r in edited_csl.to_dict("records")}
                    for item in st.session_state.active_config["other_hardware"]:
                        if item.get("name") in names_to_update:
                            item.update(names_to_update[item["name"]])
                    st.success("Call Scope lease pricing updated"); st.rerun()
            st.markdown("**System Security Tier Pricing**")
            sec_df_admin = pd.DataFrame(cfg.get("system_security", []))
            if not sec_df_admin.empty:
                edited_sec = st.data_editor(sec_df_admin, num_rows="fixed",
                    use_container_width=True, key="de_security",
                    column_config={
                        "buy": st.column_config.NumberColumn("Buy £/instance/mo", format="%.2f"),
                        "sell": st.column_config.NumberColumn("Sell £/instance/mo", format="%.2f")})
                if st.button("Apply Security Pricing", key="sec_apply"):
                    st.session_state.active_config["system_security"] = edited_sec.to_dict("records")
                    st.success("Security tier pricing updated"); st.rerun()
            st.markdown("---")
            oh_df = pd.DataFrame(cfg["other_hardware"])
            edited_oh = st.data_editor(oh_df, num_rows="dynamic", use_container_width=True, key="de_other",
                column_config={"buy": st.column_config.NumberColumn("Buy £", format="%.2f")})

            hw_col1, hw_col2 = st.columns(2)
            with hw_col1:
                st.markdown("**Switches**")
                sw_df = pd.DataFrame(cfg["switches"])
                edited_sw = st.data_editor(sw_df, num_rows="dynamic", use_container_width=True, key="de_switches",
                    column_config={"buy": st.column_config.NumberColumn("Buy £", format="%.2f"),
                                   "poe_ports": st.column_config.NumberColumn("POE Ports")})
            with hw_col2:
                st.markdown("**Routers**")
                rt_df = pd.DataFrame(cfg["routers"])
                edited_rt = st.data_editor(rt_df, num_rows="dynamic", use_container_width=True, key="de_routers",
                    column_config={"buy": st.column_config.NumberColumn("Buy £", format="%.2f")})

            if st.button("✅ Apply Hardware Changes", type="primary", key="apply_hw"):
                st.session_state.active_config["handsets_desktop"] = edited_desk.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["handsets_cordless"] = edited_cord.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["headsets"] = edited_hs.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["other_hardware"] = edited_oh.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["switches"] = edited_sw.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["routers"] = edited_rt.dropna(subset=["name"]).to_dict("records")
                st.success("Hardware catalogue updated! Changes are live for this session.")
                st.rerun()

            st.markdown("---")
            st.markdown("**🖼️ Product Image Assignment**")
            st.caption("Assign an image to any product - saved directly in config.json "
                       "so it's always matched by exact name, no fuzzy logic needed.")

            # Build complete product list from all categories
            _all_products = (
                [d["name"] for d in cfg.get("handsets_desktop", []) if d.get("name")] +
                [d["name"] for d in cfg.get("handsets_cordless", []) if d.get("name")] +
                [d["name"] for d in cfg.get("headsets", []) if d.get("name")] +
                [d["name"] for d in cfg.get("other_hardware", []) if d.get("name")] +
                [f"Switch: {d['name']}" for d in cfg.get("switches", []) if d.get("name")] +
                [d["name"] for d in cfg.get("routers", []) if d.get("name")] +
                ["SY Comms Studio", "Call Recording", "Call Scope AI Agent",
                 "ACD Light Agent", "Click to Dial", "HTML Wallboard"]
            )

            img_col1, img_col2 = st.columns([2, 3])
            with img_col1:
                selected_product = st.selectbox("Select product", sorted(_all_products),
                                                key="img_product_select")
                img_upload = st.file_uploader("Upload image (JPG or PNG)",
                                              type=["jpg","jpeg","png"],
                                              key="img_product_upload",
                                              label_visibility="collapsed")
                if img_upload and selected_product:
                    from PIL import Image as _PILImg
                    _img = _PILImg.open(img_upload).convert("RGB")
                    _img = _img.resize((400, 300), _PILImg.LANCZOS)
                    _buf = io.BytesIO()
                    _img.save(_buf, format="JPEG", quality=85, optimize=True)
                    _b64 = base64.b64encode(_buf.getvalue()).decode()
                    if "product_images" not in st.session_state.active_config:
                        st.session_state.active_config["product_images"] = {}
                    st.session_state.active_config["product_images"][selected_product] = _b64
                    st.success(f"✅ Image assigned to '{selected_product}' - download config.json below to make permanent.")

            with img_col2:
                _assigned = st.session_state.active_config.get("product_images", {})
                if _assigned:
                    st.markdown(f"**Currently assigned: {len(_assigned)} product image(s)**")
                    _img_cols = st.columns(min(len(_assigned), 4))
                    for _idx, (_pname, _pb64) in enumerate(_assigned.items()):
                        with _img_cols[_idx % 4]:
                            st.markdown(
                                f'<div style="background:#f8f9ff;border-radius:8px;padding:0.4rem;'
                                f'text-align:center;margin-bottom:0.4rem">'
                                f'<img src="data:image/jpeg;base64,{_pb64}" '
                                f'style="max-height:60px;max-width:100%;object-fit:contain;border-radius:4px"/>'
                                f'<div style="font-size:0.65rem;color:#555;margin-top:0.2rem;'
                                f'word-break:break-word">{_pname}</div></div>',
                                unsafe_allow_html=True
                            )
                            if st.button("🗑️", key=f"del_img_{_idx}", help=f"Remove image for {_pname}"):
                                del st.session_state.active_config["product_images"][_pname]
                                st.rerun()
                else:
                    st.info("No product images assigned yet. Upload one on the left.")


        # ── TAB 3: Service Pricing ────────────────────────────────────────────
        with panel_tabs[2]:
            st.markdown("### 💳 Service Pricing")
            st.caption("Edit wholesale (buy) and customer (sell) prices for all monthly service items. Changes apply immediately to new deals.")

            # Show current deal discount impact
            _adm_disc = max(0.0, min(40.0, float(st.session_state.get("c_svc_disc", 0))))
            if _adm_disc > 0:
                st.info(f"ℹ️ Consultant has applied a **{_adm_disc:.0f}% service discount** on this deal. "
                        f"Effective sell prices and margins shown below reflect this.")
            else:
                st.caption("No service discount active — prices shown are list prices.")
            _adm_mult = 1.0 - _adm_disc / 100.0

            # ── Call Scope — Monthly Services ─────────────────────────────────
            st.markdown("#### 🔮 Call Scope — Monthly Services")
            st.caption("Per-user per-month charges. Buy = SY Comms wholesale cost. Sell = customer price.")
            cs_svc_cfg = st.session_state.active_config.get("call_scope_services", [
                {"name": "AI Integration - Portal", "buy": 20.00, "sell": 29.00},
                {"name": "AI Integration - CRM",    "buy": 25.00, "sell": 35.00},
                {"name": "Manager Dashboard",        "buy": 40.00, "sell": 59.00},
                {"name": "Call Score",               "buy": 20.00, "sell": 29.00},
            ])
            cs_svc_cols = st.columns(4)
            cs_svc_new = []
            for _ci, _cs in enumerate(cs_svc_cfg):
                with cs_svc_cols[_ci % 4]:
                    st.markdown(f"**{_cs['name']}**")
                    _b = st.number_input(f"Buy £/mo", value=float(_cs["buy"]), step=0.50,
                                         key=f"adm_cs_buy_{_ci}", format="%.2f")
                    _s = st.number_input(f"Sell £/mo", value=float(_cs.get("sell", _cs["buy"]*1.45)), step=0.50,
                                         key=f"adm_cs_sell_{_ci}", format="%.2f")
                    _eff_s  = round(_s * _adm_mult, 2)
                    _margin = round((_eff_s - _b) / _eff_s * 100, 1) if _eff_s > 0 else 0
                    _disc_note = f" → £{_eff_s:.2f}/mo after discount" if _adm_disc > 0 else ""
                    st.caption(f"Margin: {_margin:.1f}%{_disc_note}")
                    cs_svc_new.append({"name": _cs["name"], "buy": _b, "sell": _s})
            if st.button("💾 Save Call Scope Service Pricing", key="adm_cs_svc_save"):
                st.session_state.active_config["call_scope_services"] = cs_svc_new
                st.success("Call Scope service pricing saved"); st.rerun()

            st.markdown("---")

            # ── Call Scope — My PA Minute Bundles ─────────────────────────────
            st.markdown("#### 📞 Call Answer - My PA Bundles")
            st.caption("Flat monthly fee per bundle. These are service charges (not lease).")
            _mypa_defaults = [
                {"name": "My PA 500 mins", "buy": 100.0, "sell": 149.0},
                {"name": "My PA 1000 mins","buy": 140.0, "sell": 199.0},
                {"name": "My PA 2000 mins","buy": 180.0, "sell": 249.0},
            ]
            _mypa_cfg = st.session_state.active_config.get("mypa_bundles", _mypa_defaults)
            mypa_cols = st.columns(3)
            mypa_new = []
            for _mi, _mp in enumerate(_mypa_cfg):
                with mypa_cols[_mi]:
                    st.markdown(f"**{_mp['name']}**")
                    _mb = st.number_input("Buy £/mo", value=float(_mp["buy"]), step=5.0,
                                          key=f"adm_mypa_buy_{_mi}", format="%.2f")
                    _ms = st.number_input("Sell £/mo", value=float(_mp.get("sell", _mp["buy"]*1.5)), step=5.0,
                                          key=f"adm_mypa_sell_{_mi}", format="%.2f")
                    _eff_ms = round(_ms * _adm_mult, 2)
                    _mm = round((_eff_ms - _mb) / _eff_ms * 100, 1) if _eff_ms > 0 else 0
                    _mypa_note = f" → £{_eff_ms:.2f}/mo" if _adm_disc > 0 else ""
                    st.caption(f"Margin: {_mm:.1f}%{_mypa_note}")
                    mypa_new.append({"name": _mp["name"], "buy": _mb, "sell": _ms})
            if st.button("💾 Save My PA Bundle Pricing", key="adm_mypa_save"):
                st.session_state.active_config["mypa_bundles"] = mypa_new
                st.success("My PA pricing saved"); st.rerun()

            st.markdown("---")

            # ── Call Scope — Lease Add-ons ─────────────────────────────────────
            st.markdown("#### 🏷️ Call Scope — Lease Add-ons")
            st.caption("One-off items added to the hardware lease (Website Widget, Platform Setup).")
            _cs_lease_names = ("Website Widget", "Call Scope Platform Setup", "Call Scope AI Setup (one-off)")
            _cs_lease_items = [i for i in cfg.get("other_hardware", [])
                                if i.get("name","") in _cs_lease_names]
            if _cs_lease_items:
                cl_cols = st.columns(len(_cs_lease_items))
                cl_new_vals = {}
                for _li, _li_item in enumerate(_cs_lease_items):
                    with cl_cols[_li]:
                        st.markdown(f"**{_li_item['name']}**")
                        _lb = st.number_input("Buy £", value=float(_li_item["buy"]), step=5.0,
                                              key=f"adm_cl_buy_{_li}", format="%.2f")
                        _ls = st.number_input("Sell £", value=float(_li_item.get("sell", _li_item["buy"]*1.5)), step=5.0,
                                              key=f"adm_cl_sell_{_li}", format="%.2f")
                        _lm = round((_ls - _lb) / _ls * 100, 1) if _ls > 0 else 0
                        st.caption(f"Margin: {_lm:.1f}%")
                        cl_new_vals[_li_item["name"]] = {"buy": _lb, "sell": _ls}
                if st.button("💾 Save Lease Add-on Pricing", key="adm_cl_save"):
                    for item in st.session_state.active_config["other_hardware"]:
                        if item.get("name") in cl_new_vals:
                            item.update(cl_new_vals[item["name"]])
                    st.success("Lease add-on pricing saved"); st.rerun()

            st.markdown("---")

            # ── System Security ────────────────────────────────────────────────
            st.markdown("#### 🛡️ System Security Tiers")
            st.caption("Per-instance per-month. Buy = SY Comms cost. Sell = customer price.")
            _sec_defaults = [
                {"name": "Bronze Security", "buy": 7.00,  "sell": 10.00},
                {"name": "Silver Security", "buy": 10.00, "sell": 15.00},
                {"name": "Gold Security",   "buy": 14.00, "sell": 20.00},
            ]
            _sec_cfg = st.session_state.active_config.get("system_security", _sec_defaults)
            sec_adm_cols = st.columns(3)
            sec_new = []
            for _si, _sc in enumerate(_sec_cfg):
                with sec_adm_cols[_si]:
                    st.markdown(f"**{_sc['name']}**")
                    _sb = st.number_input("Buy £/mo", value=float(_sc["buy"]), step=0.50,
                                          key=f"adm_sec_buy_{_si}", format="%.2f")
                    _ss = st.number_input("Sell £/mo", value=float(_sc.get("sell", _sc["buy"]*1.43)), step=0.50,
                                          key=f"adm_sec_sell_{_si}", format="%.2f")
                    _eff_ss = round(_ss * _adm_mult, 2)
                    _sm = round((_eff_ss - _sb) / _eff_ss * 100, 1) if _eff_ss > 0 else 0
                    _sec_note = f" → £{_eff_ss:.2f}/mo" if _adm_disc > 0 else ""
                    st.caption(f"Margin: {_sm:.1f}%{_sec_note}")
                    sec_new.append({"name": _sc["name"], "buy": _sb, "sell": _ss})
            if st.button("💾 Save Security Tier Pricing", key="adm_sec_save"):
                st.session_state.active_config["system_security"] = sec_new
                st.success("Security tier pricing saved"); st.rerun()

            st.markdown("---")

            # ── IT Services ────────────────────────────────────────────────────
            st.markdown("#### 💻 IT Services")
            st.caption("Per-user per-month. Buy = wholesale cost. Sell = customer price (explicit sell overrides IT uplift %).")
            _it_svc_all = []
            for _cat, _pkgs in IT_SERVICES.items():
                for _pname, _pinfo in _pkgs.items():
                    _it_svc_all.append({"category": _cat, "name": _pname,
                                        "buy": _pinfo.get("cost", 0),
                                        "sell": round(_pinfo.get("sell") or _pinfo.get("cost", 0) * (1 + IT_UPLIFT_PCT/100), 2)})
            if _it_svc_all:
                it_df = pd.DataFrame(_it_svc_all)
                edited_it = st.data_editor(it_df, num_rows="dynamic", use_container_width=True,
                    key="adm_it_svc",
                    column_config={
                        "category": st.column_config.TextColumn("Category"),
                        "name":     st.column_config.TextColumn("Service"),
                        "buy":      st.column_config.NumberColumn("Buy £/user/mo", format="%.2f"),
                        "sell":     st.column_config.NumberColumn("Sell £/user/mo", format="%.2f"),
                    })
                st.caption("Note: updating IT pricing here updates the live catalogue for the current session.")
                if st.button("💾 Apply IT Services Pricing", key="adm_it_save"):
                    # Rebuild IT_SERVICES from edited data
                    for row in edited_it.to_dict("records"):
                        cat, name, buy, sell = row["category"], row["name"], row["buy"], row["sell"]
                        if cat in IT_SERVICES and name in IT_SERVICES[cat]:
                            IT_SERVICES[cat][name]["cost"] = buy
                            IT_SERVICES[cat][name]["sell"] = sell
                        else:
                            if cat not in IT_SERVICES:
                                IT_SERVICES[cat] = {}
                            IT_SERVICES[cat][name] = {"cost": buy, "sell": sell}
                    # Persist to active_config so it survives rerun
                    st.session_state.active_config["it_services"] = IT_SERVICES
                    st.success("IT Services pricing updated for this session"); st.rerun()

        # ── TAB 3: Broadband & Lease Rates ────────────────────────────────────

        with panel_tabs[3]:
            st.markdown("**Broadband Packages** - edit wholesale costs and install charges")
            bb_df = pd.DataFrame(cfg["broadband"])
            edited_bb = st.data_editor(bb_df, num_rows="dynamic", use_container_width=True, key="de_bb",
                column_config={
                    "provider": st.column_config.TextColumn("Provider"),
                    "package":  st.column_config.TextColumn("Package"),
                    "cost":     st.column_config.NumberColumn("Wholesale Cost £", format="%.2f"),
                    "install":  st.column_config.NumberColumn("Install Charge £", format="%.2f"),
                })

            if st.button("✅ Apply Broadband Changes", type="primary", key="apply_bb"):
                st.session_state.active_config["broadband"] = edited_bb.dropna(subset=["provider","package"]).to_dict("records")
                st.success("Broadband updated!")
                st.rerun()

        # ── TAB 4: Costs & Fees ───────────────────────────────────────────────
        with panel_tabs[4]:
            st.markdown("**Fixed Deal Costs** - these feed directly into the lease capital calculation")
            c = cfg["constants"]
            cc1, cc2 = st.columns(2)
            with cc1:
                new_vc_cost    = st.number_input("Voice Channel Cost £/seat/mo (wholesale)", value=float(c.get("vc_cost_per_seat", 2.95)), step=0.10)
                new_vc_sell    = st.number_input("Voice Channel Sell £/seat/mo (to customer)", value=float(c.get("vc_sell_per_seat", 12.00)), step=0.50,
                                                  help="Professional Bundle sell rate per hosted user per month")
                new_wallboard  = st.number_input("Wallboard Sell £/user/mo",           value=float(c.get("wallboard_sell", 99.00)),    step=0.50)
                new_uplift     = st.number_input("Default Service Uplift %",           value=float(c.get("default_service_uplift_pct", 40)), min_value=0.0, max_value=100.0, step=1.0)
            with cc2:
                new_hw_uplift_up = st.number_input("Upfront Purchase Uplift %",
                    value=float(c.get("hw_uplift_upfront_pct",20)), min_value=0.0,
                    max_value=100.0, step=1.0, key="adm_hw_upfront_uplift",
                    help="Markup on hardware cost for upfront purchase deals")
                new_hw_uplift  = st.slider("Hardware Sell Margin %",
                    min_value=0, max_value=100, value=int(c.get("hw_uplift_pct", 50)), step=5,
                    help="Controls the hardware sell markup. Set before generating a quote. Not visible to customers.")
                new_commission = st.slider("Commission per Unit (£)",
                    min_value=500, max_value=2000, value=int(c.get("commission_per_unit", 1000)), step=50,
                    help="£ paid per unit of gross profit. 1 unit = £4,000 GP. Internal only - not visible to consultants.")

            if st.button("✅ Apply Cost Changes", type="primary", key="apply_costs"):
                st.session_state.active_config["constants"].update({
                    "vc_cost_per_seat":  new_vc_cost,
                    "vc_sell_per_seat":  new_vc_sell,
                    "wallboard_sell":   new_wallboard,
                    "default_service_uplift_pct": new_uplift,
                    "hw_uplift_upfront_pct": new_hw_uplift_up,
                    "hw_uplift_pct": new_hw_uplift,
                    "commission_per_unit": new_commission,
                })
                st.success("Costs updated!"); st.rerun()

        # ── TAB 5: Branding ───────────────────────────────────────────────────
        with panel_tabs[5]:
            st.markdown("**Company Branding** - updates login screen, all PDF documents and customer view instantly")
            br = cfg.get("branding", {})
            bc1, bc2 = st.columns(2)
            with bc1:
                new_co_name   = st.text_input("Company Name",          value=br.get("company_name",    "SY Comms"), key="br_name")
                new_co_legal  = st.text_input("Legal Entity Name",     value=br.get("company_legal",   "SY Comms Ltd"), key="br_legal",
                                              help="Used in legal clauses in PDF documents")
                new_co_tag    = st.text_input("App Tagline",           value=br.get("company_tagline", "SY Comms Pricing Tool"), key="br_tag")
            with bc2:
                new_co_cap    = st.text_input("Login Page Caption",    value=br.get("login_caption",   f"Authorised {br.get('company_name','SY Comms')} users only."), key="br_cap")
                new_co_pkg    = st.text_input("Customer Package Label",value=br.get("customer_pkg_label", "Your SY Comms Package"), key="br_pkg",
                                              help="Shown on the Customer View tab header")
                new_co_file   = st.text_input("PDF Filename Prefix",   value=br.get("proposal_filename_prefix", "SYComms_Proposal"), key="br_file",
                                              help="e.g. 'Acme_Proposal' → Acme_Proposal_CompanyName_2026-01-01.pdf")
                new_co_foot   = st.text_input("PDF Footer Text",       value=br.get("pdf_footer", "SY Comms | All figures exclude VAT | This document is confidential"), key="br_foot")

            st.info("💡 After applying, download **config.json** below and commit to GitHub to make permanent.")

            if st.button("✅ Apply Branding", type="primary", key="apply_branding"):
                st.session_state.active_config["branding"] = {
                    "company_name":    new_co_name,
                    "company_legal":   new_co_legal,
                    "company_tagline": new_co_tag,
                    "login_caption":   new_co_cap,
                    "customer_pkg_label": new_co_pkg,
                    "proposal_filename_prefix": new_co_file,
                    "pdf_footer":      new_co_foot,
                }
                st.success(f"✅ Branding updated to '{new_co_name}' - takes effect immediately!")
                st.rerun()

        # ── TAB 6: Email Settings ────────────────────────────────────────────
        with panel_tabs[6]:
            st.markdown("**Email / SMTP Configuration** - used to send signed proposals to customers")
            em = cfg.get("email", {})
            ecol1, ecol2 = st.columns(2)
            with ecol1:
                new_smtp_host  = st.text_input("SMTP Host",     value=em.get("smtp_host",  "smtp.gmail.com"),  help="Gmail: smtp.gmail.com  |  Outlook: smtp.office365.com")
                new_smtp_port  = st.number_input("SMTP Port",   value=int(em.get("smtp_port",  587)), step=1, help="587 (TLS) or 465 (SSL)")
                new_from_name  = st.text_input("From Name",     value=em.get("from_name",  "SY Comms"))
            with ecol2:
                new_email_user = st.text_input("Email Address / Username", value=em.get("username", ""))
                new_email_pass = st.text_input("App Password",  value=em.get("password",  ""), type="password",
                                               help="For Gmail use an App Password (not your regular password). Settings → Security → 2-Step → App Passwords")
                new_reply_to   = st.text_input("Reply-To Address", value=em.get("reply_to", ""), help="Leave blank to use sender address")

            st.info("💡 Gmail users: enable 2-Step Verification then create an **App Password** at myaccount.google.com/apppasswords")
            if st.button("✅ Save Email Settings", type="primary", key="save_email"):
                st.session_state.active_config["email"] = {
                    "smtp_host":  new_smtp_host,
                    "smtp_port":  int(new_smtp_port),
                    "username":   new_email_user,
                    "password":   new_email_pass,
                    "from_name":  new_from_name,
                    "reply_to":   new_reply_to,
                }
                st.success("✅ Email settings saved! Download config.json below to make permanent.")

        # ── TAB 7: Product Images ─────────────────────────────────────────────
        with panel_tabs[7]:
            st.markdown("**Upload product images** - filenames are matched to product names automatically")
            st.caption("Tip: name files like `fanvil_v66_pro.jpg` or `v66pro.png` - the app fuzzy-matches the name")
            uploaded_files = st.file_uploader(
                "Drag & drop product images here",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key="img_uploader_admin"
            )
            if uploaded_files:
                for uf in uploaded_files:
                    raw = uf.name.rsplit(".", 1)[0].lower()
                    norm = "".join(c for c in raw if c.isalnum())
                    st.session_state.uploaded_images[norm] = uf.read()
            if st.session_state.uploaded_images:
                st.success(f"✅ {len(st.session_state.uploaded_images)} image(s) loaded for this session")
                img_names = list(st.session_state.uploaded_images.keys())
                st.caption("Loaded: " + ", ".join(img_names))
                if st.button("🗑️ Clear all images", key="clear_imgs"):
                    st.session_state.uploaded_images = {}
                    st.rerun()

        # ── TAB 6: Security ───────────────────────────────────────────────────
        with panel_tabs[8]:
            st.markdown("**Change Admin Password**")
            pw1 = st.text_input("New password", type="password", key="new_pw1")
            pw2 = st.text_input("Confirm new password", type="password", key="new_pw2")
            if st.button("Update Password", key="update_pw"):
                if pw1 and pw1 == pw2:
                    st.session_state.active_config["meta"]["password_hash"] = hashlib.sha256(pw1.encode()).hexdigest()
                    st.success("Password updated! Download config below to make it permanent.")
                elif pw1 != pw2:
                    st.error("Passwords don't match")
                else:
                    st.warning("Enter a new password first")

        # ── SAVE CONFIG ───────────────────────────────────────────────────────
        st.divider()
        st.markdown("**💾 Save Configuration**")
        _n_imgs = len(st.session_state.get("uploaded_images", {}))
        _img_note = f" + {_n_imgs} product image(s)" if _n_imgs else " (upload images in the Images tab to include them)"
        st.caption(f"Saves all pricing, branding{_img_note}. Commit to GitHub to make permanent.")
        config_json = _cfg_to_json(st.session_state.active_config)
        st.download_button(
            "📥 Download config.json",
            data=config_json,
            file_name="config.json",
            mime="application/json",
            use_container_width=True,
            key="dl_config"
        )

# ─── KPI METRICS ROW ─────────────────────────────────────────────────────────

def pat_class(v):
    if v >= 1000: return "green"
    if v >= 500:  return "amber"
    return "red"

# ── 3 customer-safe metrics always visible ─────────────────────────────────
st.markdown('<div class="section-header">📊 Deal Dashboard</div>', unsafe_allow_html=True)

if is_spread:
    k1, k2 = st.columns(2)
    with k1:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Total Monthly</div>
          <div class="metric-value">£{total_mo:.2f}</div>
          <div class="metric-sub">Services + HW spread excl. VAT</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Monthly Services</div>
          <div class="metric-value">£{svc["total_sell"]:.2f}</div>
          <div class="metric-sub">BB + Licences + Mobiles</div>
        </div>""", unsafe_allow_html=True)
else:
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Total Monthly</div>
          <div class="metric-value">£{total_mo:.2f}</div>
          <div class="metric-sub">Services excl. VAT</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Upfront Hardware</div>
          <div class="metric-value">£{upfront:.0f}</div>
          <div class="metric-sub">One-off payment excl. VAT</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Monthly Services</div>
          <div class="metric-value">£{svc["total_sell"]:.2f}</div>
          <div class="metric-sub">BB + Licences + Mobiles</div>
        </div>""", unsafe_allow_html=True)

# ── Internal financials
# ── Internal financials - collapsed by default, hidden from customer ────────
pc = pat_class(pat)
pat_warn = ""
if pat < 250:
    pat_warn = "⚠️ Below £250 - must go to office"
elif pat < 500:
    pat_warn = "⚠️ Low PAT - consider manager review"

if st.session_state.admin_unlocked:
    # Row 1 - 4 original cards
    fi1, fi2, fi3, fi4 = st.columns(4)
    with fi1:
        st.markdown(f'''<div class="metric-card">
          <div class="metric-label">Gross Profit (Lease)</div>
          <div class="metric-value {pc}">£{pl_data["gross_profit"]:.0f}</div>
          <div class="metric-sub">Rental: £{pl_data["rental"]:.2f}/mo</div>
        </div>''', unsafe_allow_html=True)
    with fi2:
        st.markdown(f'''<div class="metric-card">
          <div class="metric-label">HW Buy → Sell</div>
          <div class="metric-value" style="font-size:1.3rem">£{hw_buy:.0f} → £{hw_sell:.0f}</div>
          <div class="metric-sub">Sell: £{hw_sell:.0f} (pricebook rates)</div>
        </div>''', unsafe_allow_html=True)
    with fi3:
        st.markdown(f'''<div class="metric-card">
          <div class="metric-label">Sub Total (SRRP basis)</div>
          <div class="metric-value" style="font-size:1.3rem">£{pl_data["sub_total"]:.0f}</div>
          <div class="metric-sub">SRRP £{pl_data["hw_srrp"]:.0f} + COS £{pl_data["cos_full"]:.0f}</div>
        </div>''', unsafe_allow_html=True)
    with fi4:
        st.markdown(f'''<div class="metric-card">
          <div class="metric-label">Commission ({commission_units:.2f} units)</div>
          <div class="metric-value" style="font-size:1.3rem;color:#00b5a3">£{commission:.0f}</div>
          <div class="metric-sub">£{commission_per_unit:.0f}/unit · £{commission_unit_size:.0f} GP = 1 unit</div>
        </div>''', unsafe_allow_html=True)
    st.markdown("---")
    # Row 2 - Profit breakdown cards
    _svc_cost_pm    = svc["bb_cost"] + total_voice_channels * C.get("vc_cost_per_seat",2.95) + sw_cost_total + svc.get("mobile_cost",0.0)
    _svc_sell_pm    = svc["total_sell"]
    _svc_margin_pm  = _svc_sell_pm - _svc_cost_pm
    _svc_profit_term = round(_svc_margin_pm * lease_term, 2)
    _total_gp        = round(pl_data["gross_profit"] + _svc_profit_term, 2)
    pb1, pb2, pb3   = st.columns(3)
    with pb1:
        st.markdown(f'''<div class="metric-card" style="border-left:4px solid #1f1450">
          <div class="metric-label">Lease Profit</div>
          <div class="metric-value" style="color:#1f1450">£{pl_data["gross_profit"]:.0f}</div>
          <div class="metric-sub">From pricebook P&L formula</div>
        </div>''', unsafe_allow_html=True)
    with pb2:
        st.markdown(f'''<div class="metric-card" style="border-left:4px solid #00b5a3">
          <div class="metric-label">Services Profit</div>
          <div class="metric-value" style="color:#00b5a3">£{_svc_profit_term:.0f}</div>
          <div class="metric-sub">£{_svc_margin_pm:.2f}/mo × {lease_term}mo  ·  sell £{_svc_sell_pm:.2f} cost £{_svc_cost_pm:.2f}</div>
        </div>''', unsafe_allow_html=True)
    with pb3:
        st.markdown(f'''<div class="metric-card" style="border-left:4px solid #1a7a40;background:#f0faf4">
          <div class="metric-label" style="color:#1a7a40">Total Gross Profit</div>
          <div class="metric-value" style="color:#1a7a40">£{_total_gp:.0f}</div>
          <div class="metric-sub">Lease £{pl_data["gross_profit"]:.0f} + Services £{_svc_profit_term:.0f}</div>
        </div>''', unsafe_allow_html=True)
    if termination_cost > 0:
        st.markdown(
            f'<div class="info-box">🔒 Termination / Buyout: <strong>£{termination_cost:.2f}</strong> - '
            f'{"spread at £" + str(round(termination_cost/lease_term,2)) + "/mo over " + LEASE_TERM_LABELS[lease_term] if is_spread else "included in upfront cost"}</div>',
            unsafe_allow_html=True
        )
    if pat_warn:
        st.markdown(f'<div class="warning-box">{pat_warn}</div>', unsafe_allow_html=True)
    if override_bb_sell > 0:
        st.markdown(f'<div class="info-box">🔐 BB Override by: {override_initials or "?"} | Customer: {override_customer or "?"}</div>', unsafe_allow_html=True)
