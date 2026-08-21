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
    page_title="SY Comms | Quotation Tool",
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

# ─── APP LOGIN GATE ──────────────────────────────────────────────────────────
_APP_PASSWORD = "SYComms2026!!"   # ← change to update access password    # ← change this to update the app password

if "app_authenticated" not in st.session_state:
    st.session_state.app_authenticated = False

if not st.session_state.app_authenticated:
    _logo_src = f'data:image/jpeg;base64,{SYCOMMS_LOGO_B64}'
    login_html = (
        '<style>'
        '.login-wrap{max-width:420px;margin:6vh auto 0;background:linear-gradient(160deg,#1f1450 0%,#2d1f6e 100%);border-radius:20px;padding:2.5rem 2.5rem 2rem;box-shadow:0 20px 60px rgba(0,0,0,0.4);text-align:center;border:1px solid rgba(0,181,163,0.2)}.'
        'login-wrap h1{font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#fff;margin:0 0 0.2rem}.'
        'login-wrap p{color:rgba(255,255,255,0.45);font-size:0.85rem;margin:0 0 1.8rem}.'
        'login-accent{color:#00b5a3}</style>'
        f'<div class="login-wrap"><img src="{_logo_src}" style="width:110px;margin-bottom:0.8rem;border-radius:8px;"><br>'
        '<h1><span class="login-accent">SY</span>&middot;COMMS</h1>'
        '<p>SY Comms Quotation Tool</p></div>'
    )
    st.markdown(login_html, unsafe_allow_html=True)
    # Centred login form
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown("###")
        entered = st.text_input("", type="password",
                                placeholder="Enter access password...",
                                label_visibility="collapsed",
                                key="login_pw_input")
        if st.button("Sign In →", use_container_width=True, type="primary"):
            if entered == _APP_PASSWORD:
                st.session_state.app_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password — please try again.")
        st.markdown("")
        st.caption(_CO_CAP)

    st.stop()   # ← nothing below renders until authenticated

# ─── CONFIG SYSTEM ───────────────────────────────────────────────────────────
CONFIG_FILE = "config.json"
_DEFAULT_PWD_HASH = hashlib.sha256(b"araconnect").hexdigest()

def _default_config():
    return {
        "meta": {"version": "1.0", "password_hash": _DEFAULT_PWD_HASH},
        "email": {
            "smtp_host":    "smtp.gmail.com",
            "smtp_port":    587,
            "username":     "sammyatt2010@googlemail.com",
            "password":     "ltvkqbxtjukvrzdm",
            "from_name":    "SY Comms",
            "reply_to":     "sammyatt2010@googlemail.com",
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
        ],
        "switches": [
            {"name": "5-Port (4x POE)",   "buy": 29.00,  "poe_ports": 4},
            {"name": "8-Port (4x POE)",   "buy": 34.00,  "poe_ports": 4},
            {"name": "8-Port (8x POE)",   "buy": 57.00,  "poe_ports": 8},
            {"name": "16-Port (8x POE)",  "buy": 80.00,  "poe_ports": 8},
            {"name": "16-Port (16x POE)", "buy": 152.00, "poe_ports": 16},
            {"name": "24-Port (24x POE)", "buy": 172.00, "poe_ports": 24},
            {"name": "48-Port (32x POE)", "buy": 344.00, "poe_ports": 32},
        ],
        "routers": [
            {"name": "Technicolour DGA Series (SoGEA)", "buy": 107.50},
            {"name": "Zyxel DX Series (FTTP)",          "buy": 64.95},
            {"name": "Draytek 2927LAC (FTTP/Leased Line)", "buy": 386.40},
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
            {"provider": "SY Comms", "package": "FTTP 40/10 Unlimited",   "cost": 22.45, "sell": 35.00, "install": 100.00},
            {"provider": "SY Comms", "package": "FTTP 80/20 Unlimited",   "cost": 29.00, "sell": 35.00, "install": 100.00},
            {"provider": "SY Comms", "package": "FTTP 115/20 Unlimited",  "cost": 25.20, "sell": 35.00, "install": 100.00},
            {"provider": "SY Comms", "package": "FTTP 160/30 Unlimited",  "cost": 26.48, "sell": 36.00, "install": 100.00},
            {"provider": "SY Comms", "package": "FTTP 220/30 Unlimited",  "cost": 26.72, "sell": 37.00, "install": 100.00},
            {"provider": "SY Comms", "package": "FTTP 330/50 Unlimited",  "cost": 34.66, "sell": 39.00, "install": 100.00},
            {"provider": "SY Comms", "package": "FTTP 550/75 Unlimited",  "cost": 34.66, "sell": 45.00, "install": 100.00},
            {"provider": "SY Comms", "package": "FTTP 1000/115 Unlimited","cost": 38.61, "sell": 55.00, "install": 100.00},
            {"provider": "SY Comms", "package": "SOGEA 40/10 Unlimited",  "cost": 27.49, "sell": 30.00, "install": 122.50},
            {"provider": "SY Comms", "package": "SOGEA 80/20 Unlimited",  "cost": 28.12, "sell": 32.00, "install": 122.50},
            {"provider": "SY Comms", "package": "Leased Line / Ethernet", "cost": 200.00,"sell": 350.00,"install": 0.00},
        ],
        "constants": {
            "vc_cost_per_seat":    2.95,   # Professional Bundle buy cost per user/mo
            "vc_sell_per_seat":   12.00,   # Professional Bundle fixed sell price per user/mo
            "wallboard_sell":     99.00,   # Live HTML Wallboard sell price
            "wallboard_cost":      5.00,   # Live HTML Wallboard buy cost
            "default_service_uplift_pct": 40,
            "hw_uplift_pct":     200,      # SY Comms use 3x (200% uplift) on hardware
            "commission_pct":     10,
            "install_engineer":  450.00,   # On-site installation
            "install_remote":     50.00,   # Remote installation
        }
    }

def _load_config():
    if Path(CONFIG_FILE).exists():
        try:
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
            # Merge with defaults so new keys are always present
            defaults = _default_config()
            for k, v in defaults.items():
                if k not in cfg:
                    cfg[k] = v
            if "constants" in defaults:
                for k, v in defaults["constants"].items():
                    cfg.setdefault("constants", {}).setdefault(k, v)
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
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = {}

cfg = st.session_state.active_config
C   = cfg["constants"]   # shorthand for constants dict
hw_uplift_override = C.get("hw_uplift_pct", 50)  # from admin panel — not visible to customer
commission_pct     = C.get("commission_pct", 10)   # consultant commission % of gross margin
B   = cfg.get("branding", {})     # shorthand for branding dict
# Branding helpers — refresh from full config (overrides early load)
_CO       = B.get("company_name",    _CO)
_CO_LEGAL = B.get("company_legal",   _CO_LEGAL)
_CO_TAG   = B.get("company_tagline", _CO_TAG)
_CO_CAP   = B.get("login_caption",   _CO_CAP)
_CO_FOOT  = B.get("pdf_footer",      _CO_FOOT)
_CO_PKG   = B.get("customer_pkg_label", _CO_PKG)
_CO_FILE  = B.get("proposal_filename_prefix", _CO_FILE)

# Keys captured when saving a quote
QUOTE_KEYS = [
    "q_comp_name","q_comp_reg","q_biz_type","q_contact","q_phone",
    "q_dir_email","q_bill_email","q_address","q_employees",
    "q_deal_type","q_lease_term","q_install_type","q_num_sites",
    "q_bb_provider","q_bb_package","q_bb_care","q_second_fttp",
    "q_bank_name","q_acc_holder","q_acc_no","q_sort_code",
    "q_bogof","q_darkweb","q_proactive","q_ooh","q_moh","q_website",
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
    'Grandstream GRP2601P': ('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', 'jpeg'),
    'Grandstream GRP2602P': ('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', 'jpeg'),
    'Grandstream GRP2603P': ('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', 'jpeg'),
    'Grandstream GRP2615': ('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', 'jpeg'),
    'Grandstream GRP2616': ('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', 'jpeg'),
    'Grandstream GXV3350': ('/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUSFBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCT/wAARCADcAMEDASIAAhEBAxEB/8QAHQAAAQQDAQEAAAAAAAAAAAAAAAEFBggDBAcCCf/EAF4QAAEDAgQCAwgIDg4HCQAAAAEAAgMEEQUGEiEHMUFRYRMUInGBkbHRCBcyQnSUobIVFiMmQ1JVcnOTlaLB0yUzNlNUVoSSo7O0wuHwJDdERmNl8Sc0NUVkdYOk0v/EABoBAQEAAwEBAAAAAAAAAAAAAAABAgQFBgP/xAAsEQEAAgIBAwEGBgMAAAAAAAAAAQIDEQQFEjFCBhMUITJSFTNBQ2GRUVOB/9oADAMBAAIRAxEAPwC0N0XRdF0BdF0XRdAXRdF0XQF0XRdF0BdF0XRdAXRdF0XQF0XRdF0BdF0XRdAXRdF0XQF0XRdF0BdF0XRdAXRdF0XQF0IuhAWRZFkWQFkWRZeSQASfGg9WRZawr6W5BqqcW/4gXrv6j/hdP+Mb60GeyLLX7/o/4XT/AIwetDa2ne8Mjnhkcb+C14J8yaGxZFkg3F0j3BjHOJFgL78kHqyLKJP4rZIie5jsy0Bc02Ja4uHkIFj5F5HFrI38ZKL871IJfZFlEfbZyN/GSi/O9SPbYyOeWZKL871IJdZFlEhxWyQf946Lzu9SX21cknlmOiPld6kEssiyio4o5LdyzFRn+d6kvtn5M/jDRec+pBKbIsot7Z2TTyzDQ/zj6kreJOUJHBrcwUJceQ1/4KTOhKLIso4c/ZWAJOO0H40LEOJmTR/vFQfzz6lK3i3hjW0T4SiyLJswbMmEZhY+TCsRpqxkZs8wvDi09o6E5LJkWyEWQgTT2o09qEIAhQjjPVy0nDzEzDNJC6RoYXRuLTbmRcddreJTe65rx/nfFw7q29Lzb80+tBUYvd0kkncpA93WvZCA3/PkWcQxmSaielOOW62ooMw4XU00skUrKuIhzHFp92OrzeK61Gw359K3sMi0YvhvRadrvMQUnwL1UsraimimZ7mRgePERdR7iVI+Hh/mF7HOa4UE1iDYjwSnbL7THgWHMJJtTR7n70Jn4ob8PMxfAJvmlYMnzde4uNzz6e1JdFkWQF0XRZFkBdeomGV7WN5uIAXmyy00ncJ45ftHB3mKCc4Th8uG4JA6Q3Ej3cuu6R8zQOtZJ8cNdhFHFoDA1ocbNAvt2LBJhOLCPX9C8QDbNOo0zwPC9zva2/R12NuSDBJKCbkDyrXlkaegeZZnYdiZvfDq/YAn/R37X5X22WGTCsSG5w2ua3exdTvF+V+jrIHjKDWkey3IeZa0jht4IWd1JVnYUlTffbuTrjyW7QtF7twpEf4SKxHhYj2G73fTJj0YJDDSsdpB2vqVsbKpPsMjqzRj/wAFZ85W1RS2QkQqBCNXYjV2IBce9kPjNJJlSbDWVMb6yJ7ZJYWuu5jXGwJ8ZXYdVlVzi74GYM6HneqpR+Y0qpLk7Rz8S0R9Eyd2vLb3GlouRqPRbqt505QtJ8qcqaAFtjyKyRgoKaR0ERlsJNI1gcr23Wz9TpMWw10rtDA57nOtyAanKmpr2TVmtncJoNvsEhUmdqt3k/PuW8xQ02H4XicdRUR07PqYa5pNgAbXAusnE/8A1eZi+ATfNKr/AMF6nvTNWFvJsPcHykD9KsBxQ/1dZj+AS/NWJt83U64Jg7MU7trkLO5gWsmkKS5SNoqs8xYXHXutvhUrfLEWj5PjybzTHNq+WX6Uqb+Ffnf4I+lGn6Ko+QhSOuxLCqysdPSYMyCFzWNbCZ3WDh7qxBHPlvdNrnNc8uaA0E3AHUuzjw4LRE9mnLjkZtfUb/pPi/f3o+k+L9/kUijF2Nt9qFmjZd48y6X4Vx9RPa1Z6hmifLHHlCHuLGCpksGho26gE4GDGdAYzHcQY0ANAD7WH+enmnele2Koie62gPBcCL+Dff5Fmpg1rIGyM1GOQkhzT7nbs8fX+hYT03jx6XznqOX7kdfh+LS6teOVztQsdT79FunxLGcErp5zJLjVaO6PBe9pu49FyOk7cuxTCQRGnkZp8I2sbDd3g9Q5Df0b9OsKPsVjpvG+1q5esZqepFqrLE8dNNN9MFSXMa5wZY2fsbjotyXNXSOJ3N13utwWT6BS4hGe6Qhj2zaRYwv3AB8Y0kf4Kvz3eEVw+q4cWKaxjh2ujczJya2nJ+ixvsLnXzRmD4Kz5ytxZVH9hYfrmx/4Kz5ytzqXHdkIRq7EIEui69XRdAiqzxjcRjmbz0ur6Yf0TVae6qvxqNsYzS7pOJwj+gYg5tSAEi6eKSO+5CZqHchSLD4ybAKsdnKkgsBso5ndlqxkYO5pH2HjuplSQ6gNlDuIDu54o0A3/wBF/vFFSLh/V95V1PVjlBpk/myNP6FZTii7/s6zH8Al+aqt5QeTTzfBz84K0nE23tb5iP8Ay+X5iSbfN9STKbrRVmwOw2PLmo2DZSbKDSYq23UP0rd6d+fDX5cbxSlmPZokxzF318mFYdRPdCyIxRR6WANv4VieZv6E0SyOncHujYw2AswWCcRPi9NVOEjZoqhwaS0xAm1iAbEdRWrJG8yvdI2z3OJcLAG/TsF26an6XMybruLRpvwRXjab8wPQtqngJkbboN16poHGFn3o9C36eDS8EBehr9EODmyas9DmD1LcbXVbnNLp5SW+5LnXLeuy8tiLuSzMprutZfG0NPJnAmllH1SRzxe9nG62IXXNrJY6Qi9lsMpyAsHMzZdtCtimOG1NUIH9wAdH3XT4OqxNr+JcAf7oqxlbiE4y1VYOIoO93OdUai069diL3v1bclXI+6PjXl+sTM2rv+XtPZrtnHft/hZD2Fh+ubHvgrPnK3KqN7Cw/XNj3wVnzlblcZ6Ul0L1dCBEIQgFVbjYf2VzN/7rEP8A68atSqq8cDbFcxHqxaP+zxKo5th3MKV4Y3kohhz/AAw1THCt0EkpI7tFtlz3iW8sx5rR/B4x8pXRqMeCFzbiYb5iA6oYx8pQZsKlljpqcRyPj7o8Ru0mxI0k284HmUgzBmvMc2DVUM2YcXmikYWPjfVvc17TzBBO6juGf93o/wAMPmuW9jp/Yqc9gUkcLUsyQ28Feb2IaLfKompTkvEqDD++m1s4jEgAFwdxvdbvT7RXPE28NfmRacU9vlKIKjFcSr2NZV1U1VKGxM0vOp3QB/1XmppZRVTCWVssgcQ6QP1hx6w733jWSlzBlmlkZJFiJjkYbte0vBHltstj6YMpSOc9+IFznG5LtRJ+Rd6vuqzqLQ4eTJmt85rM/wDD5SUl6ePb3g9C3YqEh2wumyDPGVomtb9E2WAAH1N3V4luQ8QMpNbvisf4t3qW/wDH4YjXdDhZeLybTuMcnGKiIZuLLbjo9+Sa2cRsojni0f4t/qWWPiTk8c8Wj/Fu9SwnnYZ9UOdfg8yf25/o7R0duhZW0thyTQOJmTenF4x/8bvUsntnZN+67PxbvUp8Zhn1NS/Tud/qn+jliVPRvy5VMMOmsjjfaRrf20b8zfYgG3m6lV2258asPiPEnJ89DURR4swvfE9rR3N25LT2KvJG5PauB1XJW9q9k7e19lsOfHiv76s18eXU+A+L1+DYpUy4dVy0kkvgPdEbFzQ1xA84B8isdkfOeOTZko6Orr5aumqX9zcyax07GxB6N1WPg0f2Ql++P9W9d/yN+6/Ct/s49BXIeo0sBbtPnQlshFLp7Uae1LZFkHmyqpxwd+y2Y22/83j/ALPErWKqXHH/AMXzIf8Am0f9niVgcxw91pQFM8IcoPQu0zDZS7B5RfdETWjd4IXMuI++ZT+CjXRKOQaRYrmvEN+vMcluZijt49O3y2QbmH7U9H+FB/NK3sc3wmo8QWjhzgaaicDs6QWvz9yU44rBJU4fNFE3U8gWF7XSRwlAPmUhGQcxH/YP6RvrWRvDnMruVA38cz1qKZquibTQ08gla/uzNfg+93It8i1QpMOGWaHcqBh/lEf/AOlkZwqzZIbNw+G/bVRD+8qGOuw0UMULxUQzd1vsw7i1t/Eb7HpsepaNlNIuC+dJvcYfSb9dfTj0vWf2is9fc6h/KdN+sUEMxCifRuZrN9YNtiOXjWs2xNibDrU89orPf3OoPynTfrEvtFZ7+51B+U6b9YqIXX0bKMxhlVBUCRmq8Tr6ew9RWKEMcQ18jYx0uO9vMp17ROe/udQflOm/WI9ojPh5YdQnxYlTfrFBDK6mZSS6GTsnaRcPaCLi5HI7jlyPWtYuBCnntEZ8+5lF+Uqb9Yj2iM+fcyi/KVN+sQ22eDe2JTffH+reu/ZFN834V+HHoK5FkPh7mLJ1YZMZpIYGyOOkx1MUvvHfaONtyF1vIzvrwwkdc49BV0LDaR1IXiyFB6QhCBLKqXHCxxvM9jyxSH+ojVrlVDjWb47m0W5YjTnzws9SsI5VTP0yBSbCpwCLFRWJ1ngp9w+YNtZBNqSo8Ebrn2fX68wSHcgMjJAHPZS6kqfBCh2bXd0x1zr7aIyPkQOmGjTS0Ave0gFx965PgKZKH9oovww+a5PYKDKCehe1gDwASbCwvuVqjHaLrm8kTvUgcwV6G2+57G7lYKeojqYxJEdTXC42I7Lb+JPOWZ6Smx+hnr3hlLHJeRxaXWFj0BA3uLmmximb99G4foXu9uQc6/INBJPkC6pS5hyXTULYJMVjle1rgCIZNxvbmPJ5FCcn1eF0mJVbsRqGwxvppIoXua4gONrX078uq3jQMbb73jlZ1F8bgL9G9lkbq97HK+wJ8Bhd6F0PFceyw7LM9JDisU9V3qGMAik1PksN7kW3N+pMmT67CKbD6yGtrm0dQ+eJ8TnMefBbv70fJfe/MbEBG2g3AdFI3q1sLb+K43XsAN5W8inWe8fwDFMDEOG1kdRP3w17WMgc2zQDe9/vvl8igQRO5mulWjJiMEdQae00kosNMcLn3JF7Cw6lko8QgrdXcdfg2uHsLTv4x2IrdDk/5EP144R+HHoKjwN0/ZF/dlg/wgegoLE2QvGo9aFFLdF0Xd2eZFz02QKqncZyTmPObb7NraU/0YVp67EqbDYhLVVEFOwmwdK8NBNuQuqm8UMVo8axvOFdh88dTSTzU8kU0ZuHANaNvlSElzBp3unGjlLQmxZ4Xlp57KiTUtYbCxTDmB+vFib+8YtinqLHmtDFHd0rgenSLoJDSbQ0X4X+65PITPBtBR/hB81ydWuQZNOoEdeyz01fiFLhcuFxVMQpJSXOYYhckix38XoWvqDQSepa8LsVmhbNFhErontc9rxILEN5nl/ntQbdJD3CIRhxcBc79pJTng2HuxbFKagbIYnTv06gLkWBcfkBTTSVXfMLZNGm97i97EEj9CcMPrKugrIqqhkkiqY3XjfGLkO7BvdBMMO4duxGj75jqqpge6QBsjW3u1xFz4It7nketMGDYK/GZ6uIPe3vWnfUODNIJ09F3bDxpwOdM7MBDsQxKxbZxMFv7t01YTimKYXVPqMLmnjqXtIc6FmokE3O1j2IJJVZBfTYDJizayoc1kAqDGQ21uo+CD0pqwXAo8Uop6ueaeFkUzIB3ENuS4XJuQb2sdhuSLC5ssldmfNVVTSQV9RXOpnN0P10+kaeonSLDzLXwPG8ewrurcHnqo2PIdI2CLWLgWBOxtyt/wBAgesyZHGXsP7+FZJPaYRuDw3pB5WaDsQoyCnPFsw5jxWmFPitTVyQag8Nlh0tLgDb3o38aagUCUzZqKsfV00jGSOJIuy9rtDevq9KSmp+4ve8uBL7XsLcr+tYG1FbVV7qOiohO5p037qG3Ngenot2r1Q1klQZGywdyc2xtq1XBv2dhQOAddSDIZ+vHCPhDfQVHAVIchm+csI2/wBoHoKCxN0JEKK9FwaCSQABckm1lxnih7ICiyu+XD8FfHUVLB4U7mnSDcizRtq5e6BI7CnnjhnaTLeB94UchbU1LS52gEu0crWHWb+ZcH4YcK6vixmWerr6mSHCKKQGpma7wpZOehvRq9zc25C9gSEEcnxnPHFPF3x0EGKYlK4g6WkvLQCLEnZrLde3TdbM2DYjl7D8YwjF4HU+IQQN7vG57Xljrh9rtJB2PQSrkZZytg+UMMZhmCYfTUVM212wxhpebW1PPNztuZ3VY+LHhcQ84R/bMHyQxq6HJV7aVj90Lr0EYtmKQtWCrfeoBP2oXpp0lY595gipTCbQUf4UfNcnNp3TU0WZRj/iD5rk5hBm90FjEDWgNa6RrRyAeUF5aw26rrRb9EJKV0wracPY4B0RjaHBp6Rvc9Ow5c+VyAdIWtiYI2CzW3snfLddTYfj1DWVrHOpopLyhjbkjSR/j5ExUE0k1Ix8v7Zcg25c08YDhv0Zxmkw7UWd8P0Et5gWJ/RbyoOi0mc8nUVKIYTXWGpzmtpWta5ziSTa+wudh0BQ/KmI4XQ1tb3+Z44KilkgY+KPWWOcRYkXHpT5hvDN1bDUvlp66kdFI6NomNi8D3w7D51G8vYC/GamrhAlc+mpnzhkZOqQtIAAsCd+zdBMMQzbll+WJcLo310s/eogYZKcNaXAAajvt8qZsrYpglLQ1dNjDqqMSTxzMdBGH7AbjmLX6DzGxG9itms4fspMBkxF3fjJY4e7Fj2u0jrG4G3jTTgmW3YxhVdXsgqat9K9rG09OQHPvz+T0IJHnTN2B41gwpMOfVun7u2T6rE1g0gG+48YUIBUszVkAZawiOvEs2oytjcx5uBcHb5LKIg7XQKIhqc9pcx55ljiL9HoXuKJkZLm3u7nc3WrRU1ViOJT07sSpMOhYDpfPGbO2BsOsm58yKN1UyeeConZOI3eDIxtg7cj9CBwCkGQHfXpg/wgegqOgqQ5A/dpg/wgegoLIWQk1diFFV29kK2R+YQ58pLI44tLNI9zub7ncXLujzronAano6bh5RtpC0vdNO6ch1yZC88/Jpt2WWtxmyo3E6FmLBrT3Jhhm1Gwa0m7Xno8Ek7m+kOJAvYjm3DLiBJw9xV+F4oH/Q+cgvJaBp2FpQOja1wQDa19xZBZayqXxWkYzifmYPcGh5DbnkPqTPUrV4fiNHilIyroqqKpgk9zJE4OafKFxXinwQxjM+ZqnHMDmpZmVoaZoZpNDmuDQ24O4IIA6unrV2is2myVdgd7G3OZNzS4dc/+qHqUdg4O5gxfME2AYT3jVVNIA+rnp6jXDTb7RvfyDzv4PPY3QQMLzodNURta0ku22XYB7GvOP8Gw742Fnp/Y5Zvp3hzKbD2u6++Qf0IIEI3EU4aLljwT2DSQtwOU/bwEzq37Fh4/lI9S9N4D50HOHDz/ACkepBAQUdzj/e2+ZdAHArOfTDQeSpHqXr2i85D7DQ/GQggLDboWzTVE1NMyanlkhlYbskjdpc09h6FNhwMzl+80PxkepZBwNziPsFD8ZHqQRf6aMeLbfRvFCDzvVP3+Va9FX1eHzGajqqinlILS+KQtcQeYJCmQ4I5wG3caH4wPUlHBLOA+w0PxkepBFp8wYxVxOhqMWr5on7OZJUPcHDqO+680OLYhhod3jXVVJqILu4yuZe3iUuHBPN/TDQ/GR6l6HBbN37zRfGR6kETqsaxPEIu5VmJVlTGCCGTTOeAewErWvZTX2l83H7DRfGR6ko4LZt6YaL4wEEJLGP3c256T1pWtDPcgDxKcDgxm237VR/jwl9prNo+w0fxgKiFBykWQHXzng/wgegp19pvNY5w0Y/lAUiyJwpxXCsep8Uxd9PGylJeyKJ+svdYgXNtgL369lJkdaQvOkdTkKKSeFk8To5GMexws5rhcEdIIXEOInDVmC0lZXhz5sIbeUOAvLRc3HTbmCS53aXNBuGrudl5exr2lrgHNPMEXCCrGUc+Y/wANC+Sbuc+FPeRKANcTpBbU0OAuHNvpLtwXBw8IhddylnHNPEahdX4PiOXcNpA/ub4zDJU1EJHQ4amtBtY9I38ajPGbgdVY7hcLcmwxRnu5mno3S6GucffNJvp2Ltu0p+4B8K63hjgNe3FJ45MQxKZssscT9TIQ0EBt+l25JPaOpBI3cPqvFdQzDmvGcThfzponNpIj2ERBriPG5P8AgmXsMy5QMw/CKKnoaSP3MMMYaAek9p7TunIIQGntKLdpRp7Uae1AW7Si3aUlkWQLbtKLdpRp7Uae1AW7Si3aUlkWQLbtKLdpRp7Uae1AW7Si3aUlkWQLbtKLdpRp7Uae1AW7Si3aUlkWQLbtKLdpRp7Uae1AW7ShJZCBbHqRY9SVCDzY9SLHqXpCBN+pG/UlQgTfqRv1JUIE36kb9SVCBN+pG/UlQgTfqRv1JUIE36kb9SVCBN+pG/UlQgTfqRv1JUIE36kb9SVCBN+pG/UlQgTfqQlQgEIQgEIQgEIQgEIQgEIQgEIQgEIQgEIQgEIQgEIQgEIQgEIQgEIQg//Z', 'jpeg'),
    'Grandstream GXV3470': ('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', 'jpeg'),
    'Grandstream GXV3480': ('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', 'jpeg'),
    'Grandstream DP720': ('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', 'jpeg'),
    'Grandstream DP722': ('/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUSFBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCT/wAARCAEBAMEDASIAAhEBAxEB/8QAHAABAAIDAQEBAAAAAAAAAAAAAAYHBAUIAwIB/8QARBAAAQMDAgMEBwUFBAsBAAAAAQACAwQFEQYhBxIxEyJBURRhcYGRocEIIzKSsRVCYnLCM4Ky8BYkQ1JTY4Oi0eHx0v/EABoBAQADAQEBAAAAAAAAAAAAAAABAgUDBAb/xAAjEQEAAgICAgICAwAAAAAAAAAAAQIDEQQhBTESQVFhIjKB/9oADAMBAAIRAxEAPwDqFERAREQEREBERBq9UXV9lsdTXRMD52ANiaehe4gNz7yFzjdeLM9HdKumreKVTT1UMrmSw09ukkZG8HBa1zW4ODtt5K++IMrY7VSMd+/WxbeeMu+i4Er6r064VdXnJqJ5Js+fM4u+qC+o+LwLu7xbqgf+Za5R/SVs6bi5Wgfc8WbK4+VVAY/1iXNgX4EHWNs4paqqC0UurdFXU+AZVRhx+bVJIOImvoQHVGkqSuYRnno5859mC5cWljXjDgCPIr3oJaikka2hnnpHFw3p5HRnPtaQg7Xi4zwUzg28abu9vPieUOA/Nylbu3cVNJ3LAbcvR3HoKiNzPnjHzXPOndYamoKSGNl9uD8NGRPMZh8H5CksOrpKze62a03HzeacQyfmjwM+5B0FTXm21haKavpJi8ZaI5WuJHsBWZlUrr/S9oq7TRPZA6nkpXMfTyMPK+MOGccw38veFOeFF6rb7oqmqK+d1RPFNPTdu7rK2OVzGuPrwBk+JCCYoiICIiAiIgIiICIiAiIgIiICIiCA8Xq0Udqp3uOGwsqak/8AThcfquEo9mNHqC7L+0RV9jpu5M8W2eqx7ZMM+q426IC8vTqdji1z8EeYK9V9NaCO80EE+KD4bVQO6SsPvW0sUIq7lE0AOaDkkFauSkgdnMMeT4hqk+hrZFHPJMyPHdwTlBP6OMN2C31DA6dzYWfikIaPaTj6rX26YRRTs7GJ5mYGh725Me+ct8ipJpWmNTqC2RjcOq4eYfwh4J+QKhETtN+IUrWN5DsO2OfY0Y+qlPB6l9F4b2UYwZo31BHrkke/P/cq+4n1fZ0j3k/hglkI9oVtaLoTbtIWOjcMOgoIIyPWIwD81KW5REQEREBERAREQEREBERAREQEREFAfaarg2y3ZrXYIp6OnPr56jmPyC5ZhlFPK2UsDww55T4rof7T9wIgroh3mz3Onh9zKcvP/cuf7dbJ7tVNpabl7V2SOY4Gwz1U1rNp1HtFrRWNyyDcqSTAloGY5uY8pw5wx0Jx/nC+GG3P6xyNBG53PTG/XY9fUsybRt7h3FGJR5xyNOfmsGa0XGm/taCpb7Iyf0XW2DJX3WXOM+OfVoevo9se4AVMveDdz0BOc52z/wDVaOlNDMbQUzqO7U0/pJeckBrWcpIALubdzjjAx4qo4oS6dkbgQSfwnYqzbTB2VNGAOgXHTpExPpKpbHVWyGCaoMQZMcN5XgnZrScjwxzY9oKlGgIubUtI4jaNssh9WI3EfPChtGCQBk4B6KwOHMWbjWTEbR0bx+ZzW/oSiWt4nl1Q80bNzKIqce1z8Y+a6EijEUTI27BjQ0ewKgLyz0/X9nowSe0utOMDyZ3voV0CgIiICIiAiIgIiICIiAiIgIiICIhOAT4DdByD9pKu7erghJ/tLnWSD1hgZH9VBuE9lnv+sYaCn5RJLE9rS7oDt1+a3nHetFRd7SzqXQ1FSf8AqVD/AP8AIWX9m6EO106YkAxQODSfMtft8laMlse8lY3MRMx/jnlrFq/GfvpYlZwn1DTZ7N1HVY8GS8pPsDsLRx3G3Ny2rtgkLCAOR5bjHhgYyM567+vZXrda5kdNEA7mdC1z3Dkc315yR5KqtCxUVRQVQqoIZJJZxyNlIAIAGRv4nJWh4HyXJ5lLzyY9a9ftgeZ42PgxW2HubNHBRWGqlPo8U5eCCGzhpB339nxytuyzW94y6jhz5tby/ovGjp4Z77L2EQiic9rGtYAAOmTt71OLtp2mt9EypYJW87ScHoDnputHl3xY7xS0e3k4/IvqJ9K4raaCnuL4oG8rGgbZJ8FOuHkIFHdJXbZ7GMfFzj+gUJqz2l0qDnI7Qge5WDoseiabq53bc1S5w9YbG3/yV8/eY+U6fV4/6xtotMNNx4s2jPe7OSrqvZhhaD8XK+lRnCOH0niRUTeFNbHH2F8rfo0q81RcREQEREBERAREQEREBERAREQFjXSf0W21dR4RQvf8Gk/RZK0mtqg02kbvIDv6JI0eskY+qDifjBKZNW08Oc+jW2mjPtIMh/xhbDhJb/2hLJCC5hqahsQLeo7p/wDK0HFF4l4g3og7MkiiH9yGNn9Kk3DOWa32ltTBgS9s94JGegAWh4yu8zy8zJSlInJ63G1laos130pAyJ92qHQ1BMfZsndyuGNwQD8isS2aKvlytsdzoow+B2c8ry0jBI3ONuh8VgXTUNdfWRiumMvZuLm5cTjPlnopXpjXtLbbPBaZaWYOa1zTI0ZGXe/29QVp+RycnjYqzxqxNpnvUM348Hk8iYmdViOmDZKOpgc2NrXuqWuIwO87mH6+KkEtwuE8Ap618xaDkNkBG68NJ1ENNeoauoc1rGlzzk4zkefvUh1fdaSro2voy3DeZziPHA2WdyeVNs9aXr9e3CmKm/4z9qzh+8mdJj8bi5WLRg0egmPzh7oamQe9zmj/AAhV5RtPjurCvrhSaJpmN6ilhb73ODj+pWdM9voqxqHnwKpi+9amrSB3W0tO13sD3OHzarhVZ8BoC2wXerIwai5yAH1NYxv65VmKEiIiAiIgIiICIiAiIgIiICIiAorxNl5NI1EQPenmghHvlapUoXxTmbHabZG79+4xn3Ma9/8ASg4f1fUem6uvtRnPaXGpIP8AD2rgPkArc4M1NNa6WmmqntYx8L24Jxnmd193VUlVTmpqZ6k9ZXuk+JJ+qu7Sdutk+n7cw18Uc7IGh4cOYDYeI6evqtXxMROSd/hleWiZxREfluda1dPU3BhpmQCOOEDMJJa84GXZIBUyl0PaIdPMu7G8k0cLHuw8hpcSRgb4JyCSFXddb46PlDZ2Tc7ebmiJx/ndbezz1ckRD6uZ8ZOzXHIW7nwXmlfhPphcfNjraYvHcpDYLSbpI+Nr+Qtbzfhyvu/UDrTSVEL3iR3KBt6//q+LTVVNuke+AMJIAOf8+teepqyWpo3TSDvPLWny6/8ApZ3K3Wsz+mjxaxNoaClZkY6ZU44kTsobXTQHODNFAGj1Mxj44UUsdKKqvpYCNpJmM+LgFtuMNR3IX9o5nZOmqBjxw0gA+rqvnZl9CnvBGlFPw4tsmO9UvmnPr5pHb/ABTtaDh9Qm3aHsNKRgx0MORjxLQT8ypBhSPxERAREQEREBERAREQEREBERAVY8b64Uluo5Oohgran8sBA+b1Zyq/ilQQagv8FoqS4wSWqdknKcECR7WZHrwEHEzG8rGt8gAvuNzoHc0T3xu82kg/JXNcPs2TZ5rXqNjm+DKum3/M0/0qM3LgPrqhy6C301wYPGlqW5x7H8qROuye+kSpNT3mk5WRXGoLScYe7nHzyrH01rG5RUkZnZTykjJPJjPwVe1GkNQ2qpay52O6UYB3dLSvDPz45fgVMLcyMxs5cFoG2DleivKzV6i0vPbi4bdzWFlWTX7adrhJR458c2+Rt8Fl3q/wBLeKWCOnj7NzXEvbjGRv7vFQakat5RtU35eS8TFkU4uOk7qlejIi/UNvGNhL2n5Wl36gLVcXKh89VHRxjL5IWxAZ6Fzj/6Ug0JDzXh0n/CppH59oDf6lHNVA3LidZ6Jrch9ypIyM/uhzC4/DK8unpdHUsDaWmigZ+GNjWD2AYXuvlfSkfKIiAiIgIiICIiAiIgIiICIiAqc4oV74r/AH2Zjyw0trgha4dQXuef6grjVJ6wt9RqG8argp5GslfUQQsc7OD2bGEg496CtWf6Q2WGOZtTeKKJwBY/nf2TgemObLfkpvoLUV8rKaquV5rIXWWFpZHUSRNbLLIHbkFuAWjp+HJPToonV6D1X2BoYInhkpDDNHOzkjycF5BIPdGT08FI9QRRwRw2iia2KitzWxRxsGASAN/d0+Pmg+LnxqqaerdBabB6Ty/vVVUIS72NDXfNeth4i6P1ZXxW3U+m4LRX1DuWJ1S1skUzvJswAwfIHCqq4ajnFwNXZYJGmme5rK1sj2FxGQ7l5GudgbjJACwIq6nvVHJSTRlzSO9G9wcMHo5pHUeRHl4HKDpOfhhpiZ33TJqJ7ieVsU3X2B3N8liycJuzyaK6g46Nnhx8wfooBpC5f6Y6Oko7wG1tz05I2MSzND3TUr8BjznOSMYJ/hUkoaa525jZYKq8UbHAFgFRJ2WPU1xLPkgl1i0rWacZVVNY+FzntbCwRknYuBJOQP8AdH+esB06wXjjXbsgObBUzTDP8DH4+isKw3mtumlI6ivn7eZtXURdqWNaXsjke0EgADPdHQYUM4PQNruJ09Z17CglkJ9b3tA+WUF+oiICIiAiIgIiICIiAiIgIiICIiAub9d1rpKS5Fsjm+mXucnBI5mtJHX+6PgukFzhUafqtVaYoJ6SaFj3SzVRbLkc4kcT1AOD7kEat19uen7xQx/tOrdT+mwwTMfMZI3te8M/ezj8QORhSy+SSMNwoiGBzppHtdyjnJOcd7y3yoreNE6ikoH0stvJIaWtqKflke047vTfukAjI8FKqqOtummqPUNTQy09WIA2thLSHAt2LwDvj6YKK03rtXnDuS1xwPF0ZU9o2ibFT9i4YZOwBrg/PgHB2fb61Hr+2mGqJhQPjhjnmLOY7RsJbGHOz4N5+p8w71re3DTL7m6rutskqKGNzwKktDHxyPdnBLHeJAO48lpJbLDboZpKidz5HgdrNKQMAdAMbADyCLJtwXoZZNaXq2xyxSiezvje9j8seRIAxwPkckg+SsMWa/W5ropqOrMGe82AmRhHsbn9FEuG9qqNJaRrtQ1hfR3C+ObDRtBLXxUrf3vMF2SfMZC3T9XXuy2usrKS/wBVKaWB83Z1bWztPK0nBLhz7/zKJmForaY+WukupI6iycO6JlXE6CqbRyzzRubgse/vEH1guK1fAGlDr5qKrxtHDTQN9/O4/RbriJWOj0/UOeOVz4GNLc9C4gELz+z5TBtivVX/AMa4uYPYyNg+pUqrUREQEREBERAREQEREBERAREQEREGBqCsFvsVxq3HAgpZZSfLlYT9FztcKq4UsWnrRQ3Ka35ohI+SNocSeXIyCNxsVeXE2c0+gL88HBdRyRj+8OX6qmtTT6Zhq6eluprYqqGENbPTMf8AdtI6d0H1+Hig1Fs11qmCF8gbBcIIx946WnLXNz0y9mGj3tUztev6SfTMV9raaamEkz6cwxfeuLmuc08uAMju9dlGbVbKSWmqqHTWr6Z8dU3kmpZmsc54wR6nN2yM48Vn1GkLhatN2aggD6v0SodPVOpg3n7x5iWNecHqQMoPyR/D7UEzXwXiOzVUp2bJ/q3OfUyUAE9fwreWXhNp2OsjudbNPe5GkGM1LmmEY6EMaA0+/KhFyENTd6qS5Cqt7Hkcnb0zu/gY72/U4BJ3yclbLQFS+02bVldQu7ANfDHH2YDQ2TlyXAdASJG/AeSCS33SmpK6vlrHPgrY8/dNjeGFjPBoBwBj2rQVunrm6m9BmtVa2SqcynLuxcdnva13eAwQASeuBgrNgvup7TBSSw311U2oa5/Z1tM1/Z4OC08vK715J9ak2mte1tbd6S13CgpQasuYyoppXZ52sLu9G4bDDTuHHfwUaWi9ojX0xOLNS1ttc3OOedjcewE/RSPgXSmDhzQzO/FVTVE598rgPkAoJxgrGsiiaDjMk0mP5Rj6q1uG9ELfoGwU4GMUMTyPW5ocf1UqpIiIgIiICIiAiIgIiICIiAiIgIiIIZxcfjRkkGcGpq6aD4ytz8gVUV/objFc7xVCzz1rKyn7GCeAtcY+6AQW9d/Mb7bZyVanFuX/AFOxU2f7W6RvPsYx7v1AVMVt1u0lZcK2ivddG9lZ6NDStY18c256B2dwBk4HiN90EYujKKG1yyVuW1MbHF9PUQEFoGTnJ9QBU+mqLuyn09Z6e8VNvlFuZJPUZaSTy9Xc+Q7dvj4uWnHEG5wBkV6tlvuNPzsa4iIxPaC4DOHcwJ9W2VKdTXDTMN3iFwqa+ir2MDWVVI1+WA5wCWgjx8R4oNHFxG1JbpRT1kFJdoy4se2aLsnNI2JJG3n0Z5qXW6/WC6aLnq622C30b53wTU1NGSXSNd+JvZgF2cZzjO26jlv0tSXKCaHTuqqGtZJs+B4a54PTct3B3P7q2rtI11n0hbbaaeSvdHWPqawUxyQHuc48vicZxnHh4IPSlg05c6mn/ZWspqeoiZywU9ce/G3GOUMkDXAY8At7ZdIXOk1NT3m4VNLNDTQyFr488z3uAaDjGwA5s+1Q2udaq641DJy2ja4MDYJ6UtaTjcBpJLQCNs569VuuHEfod4vcFNzR0kNDC4xtd932hfKOZregOB4Dy8kEa4uTGeohp894wkAet7sfRdF22mFFbqWlb+GGJkY9wA+i5y1XGbpxAt9CBkPq6SDHq5g4/VdKoCIiAiIgIiICIiAiIgIiICIiAiFwaMk4A6rnSv8AtBSisq462jqHRxyP7PsJMAsBOPkEFhcUqhkuotMUwe1wZ6VO5oP4cMa0E+X4yqjrbhoq61UpnZcba9zy4TtY4teSd3d3mAB9eFnaf15BxFvk8lHQT0raOifEDKckvcWnOB4LXVtsvNJZKW2VFjANPMXGtpvvSWnGcgZd4HwHTCDNi0jFqWSjfR6shuVFDPHK9rsPka1rmuLcg+IaBvjC2t2pq+ju96q5bTUVkdZT9lBJCwSBvdxuAcjcDfB6HbcFQ2zR0z9f2mGiMjhHUOPayN5ZC0RO5iRgEAnGx8x4qQT3e+mWvutJfpYWRzyNZSmJr2OYxzGnqNsGRmwIJwUEZrYbYaJ0tTyOnhZl0U8J5mEdS0kbfIqx/Tr3BaNMWukuklNVvoWyzSvYJHSkMHUFri4907AZJWgZr+V8DRqGxW26QghskkLeVzQXYPcfzA9enMpbqio0y27Urbndam118EYMVRG0hkbc5HM7lLGnOSNwfFBhDWV9p55aG60NnuzYpHRvBBhO2QSAQ8H4D3KTaZudorrNdKi12kWuVtQKeqh5Ggl4a1w7zSQRyubjHn0BytHbtOVlTRskst8tt3pBvGHhrhj+ZpP6hbjT1lqbBp6dle2NtRV1zp3tY7mAGA1u/wDKxv8AkIKwuFylg4i09XCQHw1znsLhkZY0gbe5WhRcYayDAuFvgnb4ugcWH4HI/RU2ZfSdWMkBziOab8zgB+pW0mlcWdUF7Wvihpm5PbG+tNFIf3apvIPzfh+alUU8VRGJIZGSxu3D2OBB94XJ80px54S3aovGnpO1tNxqKQ5yWxu7p9rTkH4IOs0VG6c+0NNTFsGo7eJmZwaqkHK72lh2PuI9it/T2pbTqq3tuFnrYqundsSw4cw+Tmndp9RQbNERAREQEREBERAREQa7UlcLZp651xOPR6WWTPsaVwzc5OWKpe4ZJZj25Ib9SuxOMVf6Bw4vDs4MrGwj+84D9Mrje5NklgkEUb3kuAcGtJwNyTt4bBTroSnhRI+ksGqLgx5Y4RsjY4dQTzDb19FILCNQC11d1tt9fHS0TS6WKpn7Yndo/C/JwS9o2IHVfHAilhqNJXB0sbJYqiqcxzXtBDhyg4IP8ymFToGzVHaGBs9E6VvK70eUtDhkHBacjGQDj1KBi6N1nXXm9tt9wpaQzGndI2qp2ljhyuaCC05xnmzkHwK3dfoK21rZWU89ZRNmf2j2Qyns3O8yw7ZWDpXRDNOXWouPpzqkyQ9jG0x8pYOYOOdzknA8lIrtaYrxTtgkqa6m5HiRslHUvgeHAEdWkZG/Q5B8tggitVw0ulRVU4FzpJIGVMUkznRdk8tD2ucMNBDiQ3GSR1W3uvJQajuNbc7PVVVM+Jvo744y9uQ0ZyR0323wpXTtLImsc9zyxobzO6ux4n1qDM1RqSo1HLT2q5RydpOYYqaeBro24ONiC1w893FBr6a0W2e1Mu/b0rakzdjyxv5J2jBPNzNIcOhU0o7lUu4e2qtrJ31Er6IzmSR2XOHKS0k+OxC0tVqSjBlGqNLUk3Y57Wqt8zZC1o6u35XYx/uucs3i1W01h0PXPp2tjp6eg5IWM7oa13daAPYgqqzP9Jv1bM3dsNPHGD6y4n6Lbyu25R4qJaGnELq6rra6KL0zkEcDzytLW5IeCcZznqPBSuTBHOCCD0IQYFQ7AwsCf8JWTV3GmjLgHCQjYhp2Hv6e7qtPPWPk8OUeGD9eqvEDzmeMho3cPBT3gJV1dJxDgp4qhzIauCVs0IJ5X8rS5pPhkEfr5qvC4+GB5gbKf8CWk8SaEjwgnJ/IR9UkdRIiKgIiICIiAiIgIiIKo+0dX+j6KpqUOwairbkeYa0n9cLmJtFDcGPppwTG/GQDg/FXz9p+4jt7LQZPK2OWUj+Yho/wlUla299XrHQzdPW++6ZgMWnL46nhLjJ6PPGHsLsAZz16AKS03E7VVpw28WGOsiHWahfv+U5WNQxkNbnoehWzZ1z5JMDcWnjFpa4u7Oepfb5s4MdS3lx71ObfcaOvY2SkqYp2OGeZjgQqpq7Rb7k0isooJ/Ivbkj39VpToOlpZO2s1fXWqXzglOPhlV+MjoOFwd0PitI/QVNDcv2lbauWln7TtOR7e0jLs5xy7HB9qquj1HxI069vLV0d+gb1E3ceR7dt1J7Zx4o6Ytg1JY7haXZwZBH2kefVjf8AVQNvcdAagqO2gbJS1DKl/LJKJC0hpd3nEHyBJ2JOy032mq0waJrIIzvJNTwj197m+isnTmuNN6la39l3ikqHOGezD8PHtad1UnH+Vtyr7Ba2YcKm78zhnq1jcfVB8y0jKSz0tGWtLYIGR4IBHdaAovS8kVe9rIomsawkjkGPgpVfJQ0OyPBRGF4M1U4dWxn5rpWBgvcXuyT7vJfiIgKy/s/0FTUa9FVFC50FNSy9rJjZhdgNBPmd/gfJQbTmnLhqy8QWi2RdpUTHqfwxtHV7j4Af+vFdY6M0hb9E2OG2UDMn8c0zhh08mN3H6DwGAq2kb5ERVBERAREQEREBERBzZ9pemr49U0dTLA9tFJSNihkx3XOa5xcM+fe6KrrW3cErtS+WG26ktsttu1HFWUko70cg8fAg9QR4EbqldRfZ3q7dM+p0xV+lU+c+iVTuWRvqa/GHe/HtKtEiO2DUsNFbILfV0D6iGORryBL3XASc5BYRguO7c56Y2W09E09c5Hupqv0KV7ohHE4YDW90PJOA3m7zjgYHc267Ryssd0sT+yudvqaR48JWYB9h6H3FfLN1OxIH6YnDGSQ1VNI2UNMOXFpm5i/lDf4iIycHHXHVYFTb6yjYySppZomPaHNc5hwRt49PEfFfNHc62kD2U1VNC14w4MeRzD1/EraO1bcMRZLWuihkhY6IlhHOAM7HwDdgMBOxqYzhwK9XMbIOV7Wub4gjIKkrLlp27OHb0jKSVkT2tLvuxI7LA3Lm48OY5cepPgsePS7qmKGSiq4ZpJGyOkja8OETgAWR5HUkHHQbgqBEqrRVhrz2rreyGXqJadxieD5gtIXja+Hdps9wFwbUXGqljJdGKmfnbGT4gY96lVRRTW+Y09Q0CQNa8gEHAcAR08cFecrsN6KBG7/IQ0qMQuxBWPA2cQ1b2+zHldnwUfYR+z377OkwFeBjBe9BRVNzrYKKjgfPU1DxHFEwZc9x8AvEAlwa0Oc5xAAaMkldJcG+Fw0nRNvN3hb+2Klncjdv6JGf3f5j4+XT2xMjd8MuHVNoO0FknJNdKlrXVc4G2fBjf4Rv7Tv7JphEVAREQEREBERAREQEREBERB51EEVVEYZ4o5onfiZI0OafaConduFWmLmXSMo3UMx/fpXco/Lu35KYIgpu68FrrTkutddBWNG/LKOyf9R+ih9007d7IT+0bdU0zR++5mWH+8Mj5rpRfjgHDBAIPgVPykcvtPkvaGRzSQ0lpI6gq+rroHTt3JdNbYopD/tIPu3fLY+8FRSv4NAEuttzGPCOpjGfzNx/hTexX/avm78jy52AMk52AAHyAC+KlwbHknCklVw+1HQkj9nidoP4oJA7Pu6/JaG62a6U0bu2tlaz2wO/8KIEFv7vvCtQ92LdEMficStveLTdJXEMttc8525ad5z8lYHDHg7WXeppbjqSjkpbdTd9tNKOV1U7Owc07hg8c9cY6K+xs+CPC7DYdVXuE5I56CnkHT/muH+Ee/yV4L8Y0MaGjGB0wML9VZkERFAIiICIiAiIgIiICIiAiIgIiICIiAhREHyfH2L6REBfg/EURB+oiICIiAiIgIiICIiD/9k=', 'jpeg'),
    'Grandstream DP730': ('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', 'jpeg'),
    'Grandstream DP750 (Base)': ('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', 'jpeg'),
    'Grandstream DP752 (Base)': ('/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUSFBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCT/wAARCADcAMEDASIAAhEBAxEB/8QAHAAAAwACAwEAAAAAAAAAAAAAAAIDBQcBBggE/8QAWhAAAQIDBAMGDA8MCgMAAAAAAQACAwQRBQYhMQcSQVFhcXLR0hMWIjJFdJKTobGysxQXJDQ1NjdDVVZkc4GRlBUjJTNCREZUYnWiwQgnY2WCg6PC4fBSpMP/xAAXAQEBAQEAAAAAAAAAAAAAAAAAAQMC/8QAIBEBAQACAgIDAQEAAAAAAAAAAAECERIxIUEDBBORUf/aAAwDAQACEQMRAD8A9QoQhBo2/wDfS80LSXMWFJ25NyNnwYUNzYUuyGMS0EklzCczurG2reS9ErHDYV6rYDSMi6FzFDSCP66pz5mD5DVG3T6paN5dyeEjg3tvZtvZa5+mFzFPpuvX8a7Y7uHzF8KmQmor7ze69dadNdsd2zmLh1772DK9dsd2zmrHlTIqrJBkjfK9vxrtju2cxI6+d7fjXbHfGc1Y0hIQrxgyb75XtH6V2z31o/2pOnS9vxrtrvzeasY/JTolxgyhvpe8fpZbHfW8im6+17x+llsd9byLGuzSEVw2qcYMp08Xv+Nds99bzUnTxe/42Wz34c1YnFKa7imoMsb93xH6V2x30ciU3+viP0rtjvw5FiCkfg05FXUGX6fr4/Gu2O+jkSOv5fH42W138ciw1EtEkgyx0hXzZMQGtvbbVHuofv4P8lsaxb13kgTtjOdeC0I7Y87AhRIccse17Xva1wNW1yOw1WnHj1ZLccLaNmCk9d/95SvnWqWRHopCELlQhCFAIQhB510h4aapz5iD5AUreHqlvAq6Rfdqmu14PkBTt81jsP7K1x6GKSPGCcpXYiigmkKdI4UKsglSieC6GyNDdFZrww4Fza01huLhwqKKEcxGwnGE0OeMQD4fBVRx8mHPG4/6+m0YsrMTb4kpB6DBIFG0pwqMnFl4E1CiTMMxYLT1bBtFMPDRfNKuimG4RdY0NGuczVLhQYkbMaqdoPjMgep4b3xXuDAWgHUr+VjsGa6k9Mp9bGfD+Et1rXfn+vpn4kKNORYkCH0KE49SzcCey48pLzjYk5AMeFQgtArjwL4JR8WLLsdHY5kTFp1gKuoaVw2HP6Uk5EjwWtdAlxHJOqRrBurXImuzdpjvFc2a8Qz+tjn8P423Wtd+f6tHMN0aI6CwshucS1pPWjYFEjhXLNfUHRHBz9pAoK7yHCtE6bYY8cZjPSbkjxUV3FQpCaCqrpFKUyRygk713LfOLaNnevrv/vGV861atd67leOtpWb7I3fb/eMr51qqPRCEIWShCEIBCEIPO2kYU01zI3ZaCf4ApW8PVDOKq6RsNNMY/JYI/gClb4pMQ99tVrj0jFkJU9EiikfsU3BOTUpXIJPOCRVUqIFKSIaNVCkeKtK6E1NMl2VU2IpXKjm6u1I4IJlKW6wpVOUpwFVBFwokoqxMaDeqplB87jSclRuvW0rMFLTu/wDvGV861atcKz0p84tq2UzWta7g3bRlvONVHoVCELICEIQCEIQedtJOGmiL2tB8kJLweuIXEVNJWGmmKfkkI/whJb/46Gdxq0l8DEpE6RArsqbqm7JVcKqaBCKKT+uKokfsQIVN/WlUKVWCC4cuVw5UI40UzlVM/NKcqKCaU44Jkqgi/rilKo/riplBA+vpTjra9jY2xdzftCX8sLVB9fSnHW17G9mrtn+8JfywqPQSEIWQEIQgEIQg88aTPdned2VheSElv/jWcQJtJvu1O7VheSFxbv49nFWgw6U5piKFK7NArslNUdkpoJpH9aU6R2xAhSpkrz0MAnbirBJ4xruqZR6Ihud14XKoR1KYqao8VbwKagQihSFOc0qgk81GRCmRXaVZ9KYqSCBPq2V3nra1jD8NXb/eEDygtUH1/K8ZbZsX2bu3+8IHjQegEIQswIQhAIQhB540oYaZ2ndlIXiC4t7qYzDvfzTaUfdmZ2pD8SW8GEeHwLT1Bh3GpSuyXK4KBH5Kao/JTQIRRI9O7NTiZVQQtW0Idh2Z6Le1sSNEq2E05E0qSd4CpP1bVrePake1I/RZ2ZdEachEdRoG80Gg/wC4rt+kwO6DKgEgeh8OAxG18TF0iXlQfvgB1m5uaGVA3avwAG1Edmsyy3TMPokjMua/INLy6E7eIrhwtoVkbMm4heYEcOa8Egtdm0jAj/uyhVLsyLYEERnN++RBi5zWhxaDhUsNDug7hS2sGtt53QwKktLqD8otFfAGor7n9apnAVVHE0wNFIlXYUVqaFK5Mc0hUEn4GiQp34mqQoIdkZTjLbNi+z12u34PjWpB7ISnGW3bBwvDdsfLoX81b0N/IQhZAQhCAQhCDzzpT92aF2nDS3g/HQ+BNpV92WD2pDS3gNI0I/srSdRGGOa4cmcTXFKUUpyKkqnIqSBHZqb8q0Ko7NTiZFBC2rPbb1kiAwNM1AqYbXGjYjSOqYTsrQY7CAdi6PCs2Vb0SRtEshte0tfBjnob6cFfCCRvrvgJblmpx4bJhmpFY2I3cc0FBiZe27OsuVbLSRhzT4bQxkGA+rWAdbrHJopumvCpWfLx40Z01NOD4jnFznUprOOf8gN4BZL0HBYephgDcAwT4AUAoroKclJUcDTNTQIUpTEUSuwNFBKJsSKjqHBTQfMB+EZTjLb92sbz3cHytvkuWoeyMpxlt67Htpu4PlQ8hyt6G+0IQsgIQhAIQhB540rmmmWD2nD/AJpbwCseFwJ9LIpplgdpQ/GUlvGseEf2arX0MQ7NIUy4coFJoKqRxVHGimgQ4FSdmqHEpHGoKBEpTFI7rSrBImpSOzTJSqFeaDIHhU079im4kCoKgUpDiapylcMapBF+4lTPxckPgUEOyMpxlt67Xtpu52yPIctQ9kZTjLb12fbXdrtr/Y5W9DfaEIWQEIQgEIQg89aWhTTFK78lD8ZSW5+Oh8VNpbd/XFKYfmUMeEpLfwiwuBa+hh39cUpTJFAjxjXdSpn7EqCaR+AonKm41KBCUrjQJjgkdQihIC6gmc0hTJUCRM6qTslR+dEj8lAhSlMUpUE3mrkhTPOO+kKCA9lJPjci29df22XaHyn/AOblqDspJ8bkW4Lq+2+7I+UO809BvpCELMCEIQCEIQeeNLo1dMUnvycPxlcXgP3yEd5c6Y/deke0meMpLw9fC4q0l8DEJEzkpQTdmlcudqVyBVNOTQVU0ClI/AVTlTiHALoTSptlEqQSdiSUrskxzSPBDjUKBSlTFKkEXVriKJHZpyalI7NB89fwpJ8bkW47o9VfK7Q/t3n/AEXrTnZSUH7S3Fc/26Xa+eieZiIN8oQhZAQhCAQhCDzxpi91+zxuyTPKcp3h6+FxVTTL1Ol+zj8iZ5Tkl4TjB4Fp6GHckdgmKRyBSpuTHKiRBw40Uk78aKblaOFJ5qabirkouNSSqFK48S5dmkeAWmpogRTOBonKQqUKVN7qUwBTlScgVKc0yUpB8/ZWT4arcdz/AG6Xa+dieZiLTTPZWU4y3Jc/273Z+dieZeg3yhCFkBCEIBCEIPPGmn3XrO7SZ5TlK384PAVXTT7rtmndkmeU5Rt/OFwLT0MSkeUymTVAjiuGw3vrqMc6mdBkgrM2HbsGy5OJLxYk5D1o7Y1ZfJ4DXN1XUc006oHPYmxgi15BIhvNDQ0Ck40BdsG1dwk78S8rMPe2WmRDizsaaqYzgWhwZq4BwD6FuIdUHdxKxf3bs8WEbGbJRuhahe6NrgEx8w/V3Mm59bXapyowJPXAg1GYU9UjMEHcIXaJu9spNxZ2M6Se2JHmIURsRlATCZEDg17a0LqYAj6UR72yzpqHHMa0JoNnhN60y1pMBoDuoYNY1rrCuI60cIcqOquaQ4gtcCN5SfXWxXbot8oTLWkJqXi2gIUHWExi4dEacgAYjsjjntyUbJvp6FlIEGc9Fx4wdGdFjmK41c4NDat1gIgFDUO+gpyo6q7FTcV2aPb0jNWRJWeZu0IMOBBhwYzILCWxA09ViYlN8dTWoXMW9dnRZuWn2SD5ePKsiQocMlsRhhuhuDGkUGDSQMjgTjgFB1aqic1mbYtiVm7NlpOUkhJtgxokQMB1upcGZuzJqDnkKBYVdbHBSopRcFwCogPZeU4y3Fc/273Z+dieYiLTbXVteV4y3NcoB1+rt1GTox/0IiDfCEIWQEIQgEIQg88aazq6WrMPyJnlOUbfOMHfatnX60TQL5W/K27DtaNITkvCEHVMIRYbwCTWlWkHE7Vq7TVJTmjqxZKbiWlIT83MxegwZVsu6G57QKveTrmgb1IyzcFpLBiHvoVN0Ru6tZemRbD8fuZKj/G5KdIlsHsdK925E22WXqT3jatcjSHa/wAGS/0RHJTpDtP4Mg92UNtjF7d1I9w2YroAv7POFTJQmmmIDiuRf2eP5nC7oq6V3qqUuC6Mb9TjvzKF3RR08TX6lD7soO7FwSOIXSjfia/Umd2eRL07TX6m3uzXxKDuhdRK5wGa6aL6TH6k36X/APCV98ZilfQTMP7Q8iDt73jbgkecF03p1mjnZpH+Z/wuBfWYPY13fByIjt5ck1l1PpzjnsY7vgR06RttmvH+YFVdlhmtrym+5bouNjfq7nDG8xEWv9GGja2tJVnQrw2fN2bLQpeYfAiQI8R/RGPaGnHVaRiHAhb1ujoynbItmRtW0J+We+TD9WFLtJDnOaW1LnbKOOFNxS2aGw0IQswIQhAIQhALQv8ASHs6Ba177sScyyrHQI+uW4OprN2rfSx1sXcse24sKJadmys5EghxhRIsMF8PEV1XZiu8rLoeULV0c2JLTbocMzYaAM4g5F8JuHZI/Lmu7HIvU81o1upOROjRrJDnkUqI8VvgDlH0q7n/AAR/7Mbnq8h5bdcOysw+aH+McimbjWZ/5zPdDkXqh2ii5rs7IP2qNz0p0TXM+B3fao3PV5QeWOkezR77M/W3kSPuTZ2H32Z7pvIvVB0TXM+B3fa4/PXHpRXKcQPuO4cE3H56nIeVukyzx77M/W3kSm5kjsjTI+lvIvVTtD1y6gCyoo3xNxuepnQ1cw4fc6P9ri85XkPKzrmyQ9/mPrHIpm5skBXo0f8Ah5F6rdoWuV8HTH2yLzkvpLXK+DZj7ZG5ybg8q9KEiPfo4+kciQ3Rk9keP/DyL1f6SVyD2NmPtkXnLj0kblOaHegJob3ouLzk2PJzrpSoyjxh9XIlN1JUe/xvByL1c7QXcrD1JOfa38qR2gu5n6tO/anpyHlLpTlT7/G8C4l7rykS0JeWiRo2pFOJwqF6tGge5h95n/tTlxC0CXJgzECZ9Dzz3sxGtNOp4KK3JIxOgGxZS70O3bOkg8QuiQIx13VJc5rgT9TQttLG2RYVm2E2JDs6Thy+uRruFS59K0qTiaY/WVkgs6oQhCAQhCD/2Q==', 'jpeg'),
}

# ─── PRODUCT IMAGE MAPPING ───────────────────────────────────────────────────
# Place product images in an "images/" subfolder in the repo.
# Filenames below — add matching files to unlock real photos.
PRODUCT_IMAGES = {
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

def get_product_image_b64(name):
    """Return (b64_data, ext) — checks bundled, then session upload, then images/ dir."""
    # 1. Bundled images (Grandstream phones won't be here — falls through)
    if name in BUNDLED_IMAGES:
        return BUNDLED_IMAGES[name]
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
    """Render a product card — real image if available, styled placeholder if not."""
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

# ─── PRODUCT CATALOGUES — loaded from config (editable via Admin Panel) ────────
def _build_catalogues(cfg):
    hd = {i["name"]: {k:v for k,v in i.items() if k!="name"} for i in cfg["handsets_desktop"]}
    hc = {i["name"]: {k:v for k,v in i.items() if k!="name"} for i in cfg["handsets_cordless"]}
    hs = {i["name"]: {"buy": i["buy"]}                         for i in cfg["headsets"]}
    oh = {i["name"]: {"buy": i["buy"]}                         for i in cfg["other_hardware"]}
    sw = cfg["switches"]
    rt = {i["name"]: i["buy"]                                  for i in cfg["routers"]}
    lr = {i["months"]: i["rate"]                               for i in cfg["lease_rates"]}
    ll = {i["months"]: i["label"]                              for i in cfg["lease_rates"]}
    bb = {}
    for row in cfg["broadband"]:
        bb.setdefault(row["provider"], {})[row["package"]] = {"cost": row["cost"], "install": row["install"]}
    return hd, hc, hs, oh, sw, rt, lr, ll, bb

HANDSETS_DESKTOP, HANDSETS_CORDLESS, HEADSETS, OTHER_HARDWARE, SWITCHES, ROUTERS, LEASE_RATES, LEASE_TERM_LABELS, BROADBAND = _build_catalogues(cfg)

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

st.markdown(f"""
<div class="main-header" style="display:flex;align-items:center;gap:1.2rem;">
  <img src="data:image/jpeg;base64,{SYCOMMS_LOGO_B64}" style="height:56px;border-radius:8px;flex-shrink:0;" alt="SY Comms"/>
  <div>
    <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.7rem;color:#fff;line-height:1.1">
      <span style="color:#00b5a3">SY</span>&middot;COMMS
    </div>
    <div style="color:rgba(255,255,255,0.5);font-size:0.88rem;margin-top:0.2rem">SY Comms Quotation Tool &nbsp;·&nbsp; Build, price &amp; generate paperwork</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────

with st.sidebar:
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
    # Always recurring — hardware sold upfront, services monthly
    deal_type  = "Recurring (Monthly)"
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
    bb_provider  = st.selectbox("Provider", list(BROADBAND.keys()), key="q_bb_provider")
    bb_package   = st.selectbox("Package", list(BROADBAND[bb_provider].keys()), key="q_bb_package")
    bb_care      = st.selectbox("Care Level", ["Standard (FOC)", "Business (+£8/mo)"], key="q_bb_care")
    second_fttp  = st.checkbox("Add 2nd Broadband Line", key="q_second_fttp")
    second_fttp_pkg = None
    if second_fttp:
        second_fttp_pkg = st.selectbox("2nd Line Package", list(BROADBAND[bb_provider].keys()), key="bb2")

    st.markdown("### 💰 Pricing Controls")
    service_discount_pct = st.slider(
        "Service Discount %", 0, 30, 0, step=5,
        help="0% = standard pricing. Increase to offer the customer a lower service price.",
        key="q_svc_discount"
    )
    # Convert service discount → effective uplift (base 40%, reduced by discount)
    service_uplift_pct = max(40 - service_discount_pct, 5)

    st.markdown("### 🔒 Deal Adjustments (Internal Only)")
    termination_cost = st.number_input(
        "Buyout / Termination Cost (£)",
        min_value=0.0, value=0.0, step=50.0,
        key="q_termination",
        help="Cost to exit the customer's existing contract. Added to the lease spread — not shown to customer."
    )

    st.markdown("### 💻 Software Add-ons (per user/month)")
    st.caption("Optional Telepo features — added to monthly total")
    sw_col1, sw_col2 = st.columns(2)
    with sw_col1:
        sw_studio_qty   = st.number_input("SY Comms Studio",   0, 50, 0, key="q_sw_studio",  help="sell £11.95/user")
        sw_callrec_qty  = st.number_input("Call Recording",    0, 50, 0, key="q_sw_callrec", help="sell £1.50/user")
        sw_crm_qty      = st.number_input("CRM AI per User",   0, 50, 0, key="q_sw_crm",     help="sell £15.00/user")
    with sw_col2:
        sw_acd_qty      = st.number_input("ACD Light Agent",   0, 50, 0, key="q_sw_acd",     help="sell £1.50/user")
        sw_teams_qty    = st.number_input("Teams Integration", 0, 50, 0, key="q_sw_teams",   help="sell £3.75/user")
        sw_wallboard_qty= st.number_input("HTML Wallboard",    0, 10, 0, key="q_sw_wb",      help="sell £99.00/instance")
    SW_ADDONS = [
        ("SY Comms Studio",   sw_studio_qty,    4.50, 11.95),
        ("Call Recording",    sw_callrec_qty,   0.01,  1.50),
        ("CRM AI per User",   sw_crm_qty,       0.10, 15.00),
        ("ACD Light Agent",   sw_acd_qty,       0.30,  1.50),
        ("Teams Integration", sw_teams_qty,     0.75,  3.75),
        ("HTML Wallboard",    sw_wallboard_qty, 5.00, 99.00),
    ]
    sw_sell_total = sum(qty * sell for _, qty, _, sell in SW_ADDONS if qty > 0)
    sw_cost_total = sum(qty * cost for _, qty, cost, _ in SW_ADDONS if qty > 0)

    with st.expander("📊 Current Customer Costs", expanded=False):
        st.caption("Fill in what the customer currently pays — used in the comparison view.")
        curr_col1, curr_col2 = st.columns(2)
        with curr_col1:
            current_bb      = st.number_input("Broadband / Lines (£/mo)", 0.0, step=5.0, key="q_curr_bb")
            current_system  = st.number_input("Phone System (£/mo)",      0.0, step=5.0, key="q_curr_system")
            current_calls   = st.number_input("Call Charges (£/mo)",      0.0, step=5.0, key="q_curr_calls")
        with curr_col2:
            current_mobile  = st.number_input("Mobile (£/mo)",            0.0, step=5.0, key="q_curr_mobile")
            current_support = st.number_input("Support / Maintenance (£/mo)", 0.0, step=5.0, key="q_curr_support")
            current_other   = st.number_input("Other / Misc (£/mo)",      0.0, step=5.0, key="q_curr_other")
        current_total = current_bb + current_system + current_calls + current_mobile + current_support + current_other

    st.markdown("### 🏦 Bank Details")
    bank_name  = st.text_input("Bank Name", key="q_bank_name")
    acc_holder = st.text_input("Account Holder", key="q_acc_holder")
    acc_no     = st.text_input("Account Number", max_chars=8, key="q_acc_no")
    sort_code  = st.text_input("Sort Code", max_chars=6, key="q_sort_code")

    # Promos removed — always recurring, no BOGOF or add-on promos



# Hardcoded values (features/promos removed — must stay defined for PDF/CV references)
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
termination_cost = 0.0  # overridden by sidebar if set
# Software add-on defaults (overridden by sidebar widgets above)
sw_studio_qty = sw_callrec_qty = sw_crm_qty = 0
sw_acd_qty = sw_teams_qty = sw_wallboard_qty = 0

# ─── QUOTE SAVE / LOAD ───────────────────────────────────────────────────────
with st.expander("💾 Save / Load Quote", expanded=False):
    ql_col1, ql_col2, ql_col3 = st.columns(3)

    with ql_col1:
        st.markdown("**💾 Save current quote**")
        st.caption("Downloads a JSON file with all current inputs — share with manager or reload later.")
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
                f"📥 Download quote — {quote_name}.json",
                data=_json.dumps(snapshot, indent=2, default=str),
                file_name=f"{quote_name}_{date.today()}.json",
                mime="application/json",
                use_container_width=True,
                key="dl_quote_btn"
            )

    with ql_col2:
        st.markdown("**📂 Load previous quote**")
        st.caption("Upload a previously saved quote JSON to restore all inputs.")
        loaded_quote_file = st.file_uploader("Upload quote JSON", type=["json"],
                                             key="quote_uploader", label_visibility="collapsed")
        if loaded_quote_file:
            try:
                import json as _json
                q_data = _json.load(loaded_quote_file)
                for k, v in q_data.items():
                    st.session_state[k] = v
                st.session_state["_quote_ready"] = False
                st.success(f"✅ Quote loaded — {len(q_data)} fields restored. Page will refresh.")
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
                st.session_state.active_config = cfg_data
                st.success("✅ Config loaded! Catalogue and pricing updated.")
                st.rerun()
            except Exception as e:
                st.error(f"Could not load config: {e}")

# ─── HARDWARE BUILDER (main area) ────────────────────────────────────────────

st.markdown('<div class="section-header">📦 Hardware Builder</div>', unsafe_allow_html=True)

col_hw1, col_hw2 = st.columns([3, 2])

with col_hw1:
    st.markdown("**Desktop & Conference Handsets**")
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

    st.markdown("**Cordless Handsets**")
    cordless_quantities = {}
    cord_cols = st.columns(3)
    for i, (name, info) in enumerate(HANDSETS_CORDLESS.items()):
        with cord_cols[i % 3]:
            st.markdown(product_card_html(name, info), unsafe_allow_html=True)
            qty = st.number_input(
                name,
                min_value=0, value=0, step=1, key=f"cord_{name}",
                label_visibility="collapsed"
            )
            if qty > 0:
                cordless_quantities[name] = qty

with col_hw2:
    st.markdown("**Headsets**")
    headset_quantities = {}
    for name, info in HEADSETS.items():
        qty = st.number_input(name, min_value=0, value=0, step=1, key=f"hs_{name}")
        if qty > 0:
            headset_quantities[name] = qty

    st.markdown("**Other Hardware**")
    other_quantities = {}
    for name, info in OTHER_HARDWARE.items():
        qty = st.number_input(name, min_value=0, value=0, step=1, key=f"oth_{name}")
        if qty > 0:
            other_quantities[name] = qty

    st.markdown("**Licences**")
    # Voice channel licences auto-link to handset count (mirrors Excel SYSTEM BUILDER I16 logic)
    # Cost: £3.49/seat/month wholesale (sell: ~£4.89) — one licence required per physical phone
    # Calculated AFTER hardware inputs are collected; placeholder stored here, computed below
    standalone_softphones = st.number_input("Standalone Softphone Licences (no physical phone)", min_value=0, value=0, step=1,
                                             help="Licences not tied to a handset — e.g. desktop-only users")
    wallboard_users   = st.number_input("Live Wallboard Users", min_value=0, value=0, step=1)

    st.markdown("**Networking**")
    auto_switch  = st.checkbox("Auto-select recommended switch", value=True)
    if auto_switch:
        manual_switch_name = None
    else:
        switch_names = [s["name"] for s in SWITCHES]
        manual_switch_name = st.selectbox("Select Switch", switch_names)
    router_type  = st.selectbox("Router", list(ROUTERS.keys()))
    add_router   = st.checkbox("Include router in lease", value=True)

    st.markdown("**Mobiles**")
    mobile_rows = []
    mob_col1, mob_col2, mob_col3 = st.columns([2, 2, 1])
    for net, pkgs in MOBILE_NETWORKS.items():
        for pkg, pricing in pkgs.items():
            qty = st.number_input(
                f"{net} — {pkg}",
                min_value=0, value=0, step=1, key=f"mob_{net}_{pkg}"
            )
            if qty > 0:
                mobile_rows.append({"network": net, "package": pkg, "qty": qty, **pricing})

    additional_wired_ports = st.number_input("Additional wired network ports needed", min_value=0, value=0)

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
    f"🎙️ **Voice Channels (Auto): {total_voice_channels}** "
    f"({user_licences} handset-linked + {softphone_licences} standalone softphone)"
)

with st.expander("🔐 Manager & Admin Panel", expanded=False):

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
        # ── UNLOCKED — show lock button + tabs ─────────────────────────────────
        lock_col, info_col = st.columns([1, 4])
        with lock_col:
            if st.button("🔒 Lock Panel", use_container_width=True):
                st.session_state.admin_unlocked = False
                st.rerun()
        with info_col:
            st.markdown('<span class="override-badge">🔓 Admin Unlocked</span>', unsafe_allow_html=True)

        panel_tabs = st.tabs(["📋 Per-Deal Overrides", "🖥️ Hardware", "🌐 Broadband & Rates", "💰 Costs & Fees", "🎨 Branding", "📧 Email", "📸 Images", "🔒 Security"])

        # ── TAB 1: Per-Deal Overrides (existing functionality) ────────────────
        with panel_tabs[0]:
            mgr_col1, mgr_col2 = st.columns(2)
            with mgr_col1:
                override_customer = st.text_input("Customer Name (for audit)", key="mgr_cust")
                override_initials = st.text_input("Manager Initials", key="mgr_init")
                override_monthly_lease = 0.0  # not used in recurring
                override_bb_sell = st.number_input("Override BB Sell (£/mo) — 0 = auto", min_value=0.0, value=0.0, step=1.0)
            with mgr_col2:
                override_upfront = st.number_input("Override Upfront Capital (£) — 0 = auto", min_value=0.0, value=0.0, step=10.0)
                override_install_cost = st.number_input("Override Install Charge (£) — 0 = auto", min_value=0.0, value=0.0, step=50.0)
                credits_months = st.number_input("Introductory Credit Period (months)", min_value=0, value=0, step=1)
                credits_amount = st.number_input("Monthly Credit Amount (£)", min_value=0.0, value=0.0, step=5.0)
                cashback_amount = st.number_input("Cashback / Settlement Fund (£)", min_value=0.0, value=0.0, step=50.0)

        # ── TAB 2: Hardware Catalogue ──────────────────────────────────────────
        with panel_tabs[1]:
            st.markdown("**Desktop & Conference Handsets** — edit buy prices, add or remove rows")
            desk_df = pd.DataFrame(cfg["handsets_desktop"])
            edited_desk = st.data_editor(desk_df, num_rows="dynamic", use_container_width=True, key="de_desktop",
                column_config={"poe": st.column_config.CheckboxColumn("PoE"),
                               "buy": st.column_config.NumberColumn("Buy £", format="£%.2f"),
                               "cat": st.column_config.SelectboxColumn("Category", options=["Desktop","Conference"])})

            st.markdown("**Cordless Handsets**")
            cord_df = pd.DataFrame(cfg["handsets_cordless"])
            edited_cord = st.data_editor(cord_df, num_rows="dynamic", use_container_width=True, key="de_cordless",
                column_config={"bogof": st.column_config.CheckboxColumn("BOGOF Promo"),
                               "buy": st.column_config.NumberColumn("Buy £", format="£%.2f"),
                               "cat": st.column_config.SelectboxColumn("Category", options=["Wi-Fi","DECT"])})

            st.markdown("**Headsets**")
            hs_df = pd.DataFrame(cfg["headsets"])
            edited_hs = st.data_editor(hs_df, num_rows="dynamic", use_container_width=True, key="de_headsets",
                column_config={"buy": st.column_config.NumberColumn("Buy £", format="£%.2f")})

            st.markdown("**Other Hardware**")
            oh_df = pd.DataFrame(cfg["other_hardware"])
            edited_oh = st.data_editor(oh_df, num_rows="dynamic", use_container_width=True, key="de_other",
                column_config={"buy": st.column_config.NumberColumn("Buy £", format="£%.2f")})

            hw_col1, hw_col2 = st.columns(2)
            with hw_col1:
                st.markdown("**Switches**")
                sw_df = pd.DataFrame(cfg["switches"])
                edited_sw = st.data_editor(sw_df, num_rows="dynamic", use_container_width=True, key="de_switches",
                    column_config={"buy": st.column_config.NumberColumn("Buy £", format="£%.2f"),
                                   "poe_ports": st.column_config.NumberColumn("POE Ports")})
            with hw_col2:
                st.markdown("**Routers**")
                rt_df = pd.DataFrame(cfg["routers"])
                edited_rt = st.data_editor(rt_df, num_rows="dynamic", use_container_width=True, key="de_routers",
                    column_config={"buy": st.column_config.NumberColumn("Buy £", format="£%.2f")})

            if st.button("✅ Apply Hardware Changes", type="primary", key="apply_hw"):
                st.session_state.active_config["handsets_desktop"] = edited_desk.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["handsets_cordless"] = edited_cord.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["headsets"] = edited_hs.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["other_hardware"] = edited_oh.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["switches"] = edited_sw.dropna(subset=["name"]).to_dict("records")
                st.session_state.active_config["routers"] = edited_rt.dropna(subset=["name"]).to_dict("records")
                st.success("Hardware catalogue updated! Changes are live for this session.")
                st.rerun()

        # ── TAB 3: Broadband & Lease Rates ────────────────────────────────────
        with panel_tabs[2]:
            st.markdown("**Broadband Packages** — edit wholesale costs and install charges")
            bb_df = pd.DataFrame(cfg["broadband"])
            edited_bb = st.data_editor(bb_df, num_rows="dynamic", use_container_width=True, key="de_bb",
                column_config={
                    "provider": st.column_config.TextColumn("Provider"),
                    "package":  st.column_config.TextColumn("Package"),
                    "cost":     st.column_config.NumberColumn("Wholesale Cost £", format="£%.2f"),
                    "install":  st.column_config.NumberColumn("Install Charge £", format="£%.2f"),
                })

            if st.button("✅ Apply Broadband Changes", type="primary", key="apply_bb"):
                st.session_state.active_config["broadband"] = edited_bb.dropna(subset=["provider","package"]).to_dict("records")
                st.success("Broadband updated!")
                st.rerun()

        # ── TAB 4: Costs & Fees ───────────────────────────────────────────────
        with panel_tabs[3]:
            st.markdown("**Fixed Deal Costs** — these feed directly into the lease capital calculation")
            c = cfg["constants"]
            cc1, cc2 = st.columns(2)
            with cc1:
                new_vc_cost    = st.number_input("Voice Channel Cost £/seat/mo (wholesale)", value=float(c.get("vc_cost_per_seat", 3.49)), step=0.10)
                new_wallboard  = st.number_input("Wallboard Sell £/user/mo",           value=float(c.get("wallboard_sell", 4.99)),     step=0.50)
                new_uplift     = st.number_input("Default Service Uplift %",           value=float(c.get("default_service_uplift_pct", 40)), min_value=0.0, max_value=100.0, step=1.0)
            with cc2:
                new_hw_uplift  = st.slider("Hardware Sell Margin %",
                    min_value=0, max_value=100, value=int(c.get("hw_uplift_pct", 50)), step=5,
                    help="Controls the hardware sell markup. Set before generating a quote. Not visible to customers.")
                new_commission = st.slider("Consultant Commission %",
                    min_value=0, max_value=30, value=int(c.get("commission_pct", 10)), step=1,
                    help="% of gross deal margin shown as consultant commission in Internal Financials. Internal only.")

            if st.button("✅ Apply Cost Changes", type="primary", key="apply_costs"):
                st.session_state.active_config["constants"].update({
                    "vc_cost_per_seat": new_vc_cost,
                    "wallboard_sell":   new_wallboard,
                    "default_service_uplift_pct": new_uplift,
                    "hw_uplift_pct":    new_hw_uplift,
                    "commission_pct":   new_commission,
                })
                st.success("Costs updated!")

        # ── TAB 5: Branding ───────────────────────────────────────────────────
        with panel_tabs[4]:
            st.markdown("**Company Branding** — updates login screen, all PDF documents and customer view instantly")
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
                st.success(f"✅ Branding updated to '{new_co_name}' — takes effect immediately!")
                st.rerun()

        # ── TAB 6: Email Settings ────────────────────────────────────────────
        with panel_tabs[5]:
            st.markdown("**Email / SMTP Configuration** — used to send signed proposals to customers")
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
        with panel_tabs[6]:
            st.markdown("**Upload product images** — filenames are matched to product names automatically")
            st.caption("Tip: name files like `fanvil_v66_pro.jpg` or `v66pro.png` — the app fuzzy-matches the name")
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
        with panel_tabs[7]:
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
        st.caption("Download `config.json` and commit it to your GitHub repo to make changes permanent across all sessions.")
        config_json = _cfg_to_json(st.session_state.active_config)
        st.download_button(
            "📥 Download config.json",
            data=config_json,
            file_name="config.json",
            mime="application/json",
            use_container_width=True,
            key="dl_config"
        )

# ─── CALCULATIONS ENGINE (Recurring model — hardware upfront, services monthly) ─

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
    for sw in SWITCHES:
        if sw["poe_ports"] >= poe_needed:
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
        total += OTHER_HARDWARE[name]["buy"] * qty
    poe_n = compute_poe_needed()
    total += get_recommended_switch(poe_n)["buy"]
    if add_router:
        total += ROUTERS[router_type]
    return total

def compute_hw_sell():
    """Hardware sell price = buy × (1 + hw_uplift_override/100) — set in Admin Panel."""
    return round(compute_hw_buy() * (1 + hw_uplift_override / 100), 2)

def compute_install_cost():
    if install_type == "Engineer Install":
        return 500.0
    return 0.0

def compute_upfront():
    """Upfront = hw_sell + installation + BB install charge."""
    bb_inst = BROADBAND[bb_provider][bb_package]["install"]
    return compute_hw_sell() + compute_install_cost() + bb_inst

def compute_service_charges(sw_sell=0.0, sw_cost=0.0):
    """Compute all monthly service charges. sw_sell/sw_cost come from software add-ons."""
    uplift   = service_uplift_pct / 100.0
    bb_cost  = BROADBAND[bb_provider][bb_package]["cost"]
    bb_sell  = bb_cost * (1.0 + uplift)
    if bb_care == "Business (+£8/mo)":
        bb_sell += 8.0
    if second_fttp and second_fttp_pkg:
        bb_cost2 = BROADBAND[bb_provider][second_fttp_pkg]["cost"]
        bb_sell += bb_cost2 * (1.0 + uplift)

    # Voice channels — fixed sell price from pricebook (Professional Bundle)
    vc_sell_per_seat = C.get("vc_sell_per_seat", 12.00)
    vc_cost_per_seat = C.get("vc_cost_per_seat", 2.95)
    lic_monthly      = total_voice_channels * vc_sell_per_seat

    # Wallboard — computed here to avoid global scope issues
    wallboard_mo_val = wallboard_users * C.get("wallboard_sell", 99.00)

    mobile_sell      = sum(r["sell"] * r["qty"] for r in mobile_rows)
    mobile_cost      = sum(r["cost"] * r["qty"] for r in mobile_rows)
    total_sell       = bb_sell + lic_monthly + wallboard_mo_val + mobile_sell + sw_sell

    return {
        "bb_cost":        bb_cost,
        "bb_sell":        bb_sell,
        "lic_monthly":    lic_monthly,
        "wallboard_mo":   wallboard_mo_val,
        "mobile_sell":    mobile_sell,
        "mobile_cost":    mobile_cost,
        "sw_sell":        sw_sell,
        "sw_cost":        sw_cost,
        "total_sell":     total_sell,
    }

def compute_pat(svc):
    """PAT = hardware margin + monthly service margin × term - credits/cashback."""
    hw_margin      = compute_hw_sell() - compute_hw_buy()
    bb_cost        = BROADBAND[bb_provider][bb_package]["cost"]
    svc_margin_pm  = (svc["bb_sell"] - bb_cost)
    svc_margin_pm += svc["mobile_sell"] - svc["mobile_cost"]
    svc_margin_pm += svc["lic_monthly"] - (total_voice_channels * C["vc_cost_per_seat"])
    total_pat = hw_margin + (svc_margin_pm * lease_term)
    if credits_months > 0: total_pat -= credits_amount * credits_months
    if cashback_amount > 0: total_pat -= cashback_amount
    return total_pat

# ── Compute everything ────────────────────────────────────────────────────────
poe_needed = compute_poe_needed()
rec_switch = get_recommended_switch(poe_needed)
hw_buy     = compute_hw_buy()
hw_sell    = compute_hw_sell()
svc        = compute_service_charges(sw_sell=sw_sell_total, sw_cost=sw_cost_total)
pat_base   = compute_pat(svc)

is_spread  = ("Lease" in payment_model)

if is_spread:
    # Hardware cost + termination buyout spread over contract months
    hw_monthly_spread = round((hw_sell + termination_cost) / lease_term, 2)
    total_mo   = svc["total_sell"] + hw_monthly_spread
    # Upfront = installation + BB install only
    bb_inst    = BROADBAND[bb_provider][bb_package]["install"]
    upfront    = compute_install_cost() + bb_inst
    pat        = pat_base   # termination is pass-through (billed to customer in spread)
else:
    hw_monthly_spread = 0.0
    upfront    = compute_upfront() + termination_cost   # included in upfront total
    total_mo   = svc["total_sell"]
    pat        = pat_base

# Commission on gross margin (internal only — not customer-facing)
gross_margin = (hw_sell - hw_buy) + (pat_base - (hw_sell - hw_buy))
commission   = round(pat_base * (commission_pct / 100), 2)

# Aliases for PDF / legacy references
kit_cost    = hw_buy
lease_mo    = hw_monthly_spread  # used in PDF as "Hardware Monthly" when spread
rec_upfront = upfront

# SGP / sales comms
# SGP / sales comms
sgp          = pat * 0.10

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
# ── Internal financials — collapsed by default, hidden from customer ────────
pc = pat_class(pat)
pat_warn = ""
if pat < 250:
    pat_warn = "⚠️ Below £250 — must go to office"
elif pat < 500:
    pat_warn = "⚠️ Low PAT — consider manager review"

with st.expander("🔐 Internal Deal Financials — Admin Only", expanded=False):
    if not st.session_state.admin_unlocked:
        st.info("🔒 Unlock the Admin Panel above to view deal financials.")
    else:
        fi1, fi2, fi3, fi4 = st.columns(4)
        with fi1:
            st.markdown(f'''<div class="metric-card">
              <div class="metric-label">Deal PAT</div>
              <div class="metric-value {pc}">£{pat:.0f}</div>
              <div class="metric-sub">Over {lease_term} months</div>
            </div>''', unsafe_allow_html=True)
        with fi2:
            st.markdown(f'''<div class="metric-card">
              <div class="metric-label">HW Buy → Sell</div>
              <div class="metric-value" style="font-size:1.3rem">£{hw_buy:.0f} → £{hw_sell:.0f}</div>
              <div class="metric-sub">{hw_uplift_override}% margin</div>
            </div>''', unsafe_allow_html=True)
        with fi3:
            st.markdown(f'''<div class="metric-card">
              <div class="metric-label">BB Wholesale</div>
              <div class="metric-value" style="font-size:1.3rem">£{svc["bb_cost"]:.2f}</div>
              <div class="metric-sub">vs sell £{svc["bb_sell"]:.2f}</div>
            </div>''', unsafe_allow_html=True)
        with fi4:
            st.markdown(f'''<div class="metric-card">
              <div class="metric-label">Commission ({commission_pct}%)</div>
              <div class="metric-value" style="font-size:1.3rem;color:#00b5a3">£{commission:.0f}</div>
              <div class="metric-sub">On £{pat:.0f} gross margin</div>
            </div>''', unsafe_allow_html=True)
        if termination_cost > 0:
            st.markdown(
                f'<div class="info-box">🔒 Termination / Buyout: <strong>£{termination_cost:.2f}</strong> — '
                f'{"spread at £" + str(round(termination_cost/lease_term,2)) + "/mo over " + LEASE_TERM_LABELS[lease_term] if is_spread else "included in upfront cost"}</div>',
                unsafe_allow_html=True
            )
        if pat_warn:
            st.markdown(f'<div class="warning-box">{pat_warn}</div>', unsafe_allow_html=True)
        if override_bb_sell > 0:
            st.markdown(f'<div class="info-box">🔐 BB Override by: {override_initials or "?"} | Customer: {override_customer or "?"}</div>', unsafe_allow_html=True)
# ─── TABS ─────────────────────────────────────────────────────────────────────

def s(text):
    """Sanitise text for fpdf2 — replaces/strips characters outside latin-1."""
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
    # Embed logo for PDF
    _logo_bytes = base64.b64decode(SYCOMMS_LOGO_B64)
    _logo_buf   = io.BytesIO(_logo_bytes)

    def _add_header(pdf_obj, subtitle="Customer Proposal & Order Documentation"):
        # Deep purple background
        pdf_obj.set_fill_color(31, 20, 80)
        pdf_obj.rect(0, 0, 210, 42, 'F')
        # SY Comms circle logo on left
        pdf_obj.image(_logo_buf, x=10, y=6, h=30)
        _logo_buf.seek(0)
        # Company name right of logo
        pdf_obj.set_font("Helvetica", "B", 20)
        pdf_obj.set_text_color(255, 255, 255)
        pdf_obj.set_y(7)
        pdf_obj.set_x(48)
        pdf_obj.cell(120, 10, s("SY·COMMS"), ln=False, align="L")
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

    # Logo centred - large
    pdf.image(_logo_buf, x=75, y=25, h=55)
    _logo_buf.seek(0)

    # Company name
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(90)
    pdf.cell(0, 12, "SY" + chr(183) + "COMMS", ln=True, align="C")

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
    pdf.cell(0, 8, "About SY" + chr(183) + "COMMS", ln=True, align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(220, 220, 230)
    pdf.set_x(30)
    pdf.multi_cell(150, 5.5,
        "SY Comms is a locally owned and operated telecoms and IT services company "
        "serving businesses across the SY & TF postcode areas. We understand the "
        "unique needs of our community and are committed to delivering solutions that "
        "work for you. Our experienced local engineers are always on hand to provide "
        "friendly, fast and personalised service.",
        align="C"
    )

    # ── Values section ────────────────────────────────────────────────────────
    pdf.set_y(215)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 181, 163)
    pdf.cell(0, 7, "Our Values", ln=True, align="C")
    pdf.ln(1)

    values = [
        (">  Flexible", "12-month rolling contracts — no lengthy commitments"),
        (">  Local",    "Shropshire-based engineers serving SY & TF postcodes"),
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
    pdf.cell(0, 5, "01743 667419   |   hello@sycomms.co.uk   |   sycomms.co.uk", ln=True, align="C")
    pdf.set_y(273)
    pdf.cell(0, 5, "Suite C Jupiter House, Sitka Drive, Shrewsbury Business Park, Shrewsbury SY2 6LG", ln=True, align="C")

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
        rows = [
            ("Hardware (spread over term)", curr_hw,  f"£{hw_monthly_spread:.2f}/mo"),
            ("Monthly Service Charges (BB, Licences, Mobiles)", curr_svc, f"£{svc['total_sell']:.2f}/mo"),
            ("Installation / Setup (one-off)", "-", f"£{compute_install_cost():.2f}"),
        ]
    else:
        curr_hw  = f"£{current_system:.2f}/mo" if current_system > 0 else "-"
        curr_svc = f"£{(current_bb + current_calls + current_mobile):.2f}/mo" if (current_bb + current_calls + current_mobile) > 0 else "-"
        rows = [
            ("Upfront Hardware (one-off)", curr_hw,  f"£{upfront:.2f}"),
            ("Monthly Service Charges (BB, Licences, Mobiles)", curr_svc, f"£{svc['total_sell']:.2f}/mo"),
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
    for name, qty in {**desktop_quantities, **cordless_quantities, **headset_quantities, **other_quantities}.items():
        all_equip_pdf.append((name, qty, "Paid Upfront"))
    if auto_switch:
        all_equip_pdf.append((f"Switch: {rec_switch['name']}", 1, "Paid Upfront"))
    if add_router:
        all_equip_pdf.append((router_type, 1, "Paid Upfront"))
    all_equip_pdf.append((f"Broadband - {bb_provider} {bb_package}", 1, f"£{svc['bb_sell']:.2f}"))
    if total_voice_channels > 0:
        vc_sell_pdf = round(3.49 * (1 + service_uplift_pct/100) * total_voice_channels, 2)
        all_equip_pdf.append((f"Voice Channel Licences x{total_voice_channels}", total_voice_channels, f"£{vc_sell_pdf:.2f}/mo"))
    for r in mobile_rows:
        all_equip_pdf.append((f"{r['network']} - {r['package']}", r["qty"], f"£{r['sell']*r['qty']:.2f}"))

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
        pdf.multi_cell(pdf.epw, 5,
            f"Hardware costs of £{hw_sell:.2f} + VAT are spread over the {LEASE_TERM_LABELS[lease_term]} contract "
            f"at £{hw_monthly_spread:.2f} + VAT per month. "
            f"Total monthly payment of £{total_mo:.2f} + VAT will be collected by Direct Debit, "
            f"covering both hardware and all service charges."
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
    pdf.cell(90, 5, "For (Company Name):", ln=False)
    pdf.cell(0, 5, f"For {_CO}:", ln=True)
    pdf.ln(2)
    _embed_sig(pdf, sig_bytes, signer_name=sig_name,
               company=sig_company, timestamp=sig_timestamp)
    pdf.cell(90, 0.5, "", border="T", ln=False)
    pdf.cell(15, 0.5, "", ln=False)
    pdf.cell(75, 0.5, "", border="T", ln=True)
    pdf.ln(3)
    pdf.cell(90, 5, f"Name & Position: {_contact or '___________________________'}", ln=False)
    pdf.cell(0, 5, "Name & Position: ___________________________", ln=True)
    pdf.cell(90, 5, f"Date: {date.today()}", ln=False)
    pdf.cell(0, 5, "Date: ___________________________", ln=True)
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

    svc_items = [(f"{bb_provider} - {bb_package}", 1, f"£{svc['bb_sell']:.2f}/mo")]
    if second_fttp and second_fttp_pkg:
        bb2_sell = BROADBAND[bb_provider][second_fttp_pkg]["cost"] / (1 - service_uplift_pct/100)
        svc_items.append((f"{bb_provider} - {second_fttp_pkg} (2nd line)", 1, f"£{bb2_sell:.2f}/mo"))
    if total_voice_channels > 0:
        vc_sell_svc = round(3.49 * (1 + service_uplift_pct/100) * total_voice_channels, 2)
        svc_items.append((f"Voice Channel Licences x{total_voice_channels}", total_voice_channels, f"£{vc_sell_svc:.2f}/mo"))
    if ooh_support:
        svc_items.append(("24/7 OOH Support", 1, "£25.00/mo"))
    if dark_web_mon:
        svc_items.append(("Dark Web Monitoring", 1, "£10.00/mo (after 3m FOC)"))
    if proactive_bb:
        svc_items.append(("Proactive Broadband Management", 1, "£10.00/mo (after 3m FOC)"))

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

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(90, 5, "For (Company Name):", ln=False)
    pdf.cell(0, 5, f"For {_CO}:", ln=True)
    pdf.ln(2)
    _embed_sig(pdf, sig_bytes, signer_name=sig_name,
               company=sig_company, timestamp=sig_timestamp)
    pdf.cell(90, 0.5, "", border="T", ln=False)
    pdf.cell(15, 0.5, "", ln=False)
    pdf.cell(75, 0.5, "", border="T", ln=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(90, 5, f"Name & Position: {_contact or '___________________________'}", ln=False)
    pdf.cell(0, 5, "Name & Position: ___________________________", ln=True)
    pdf.cell(90, 5, f"Date: {date.today()}", ln=False)
    pdf.cell(0, 5, "Date: ___________________________", ln=True)
    pdf.ln(4)

    # -- PAGE 4: BANK DETAILS & CHECKLIST --
    pdf.add_page()
    _add_header(pdf, "Direct Debit Mandate & Customer Checklist")

    if bank_name or acc_no:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, "Direct Debit Banking Mandate", ln=True)
        row2("Bank Name:", _bank or "-", "Account Holder:", _holder or "-")
        row2("Account Number:", _accno or "-", "Sort Code:", _sort or "-")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 4.5,
            f"By signing this mandate you authorise {_CO} to collect payments by Direct Debit in "
            "accordance with the agreed terms. Payments will be collected on or around the 1st of each month."
        )
        pdf.ln(6)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(90, 5, "Authorised Signature:", ln=False)
        pdf.cell(0, 5, "Date:", ln=True)
        pdf.ln(2)
        _embed_sig(pdf, sig_bytes, signer_name=sig_name,
                   company=sig_company, timestamp=sig_timestamp)
        pdf.cell(90, 0.5, "", border="T", ln=False)
        pdf.cell(15, 0.5, "", ln=False)
        pdf.cell(75, 0.5, "", border="T", ln=True)
        pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Customer Requirements Checklist", ln=True)
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
        pdf.cell(8, 5, f"{i}.", ln=False)
        pdf.multi_cell(pdf.epw - 8, 5, item)
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(90, 5, f"For {_comp or '(Company Name)'}:", ln=False)
    pdf.cell(0, 5, "Signed:", ln=True)
    pdf.ln(2)
    _embed_sig(pdf, sig_bytes, signer_name=sig_name,
               company=sig_company, timestamp=sig_timestamp)
    pdf.cell(90, 0.5, "", border="T", ln=False)
    pdf.cell(15, 0.5, "", ln=False)
    pdf.cell(75, 0.5, "", border="T", ln=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(90, 5, f"Name & Position: {_contact or '___________________________'}", ln=False)
    pdf.cell(0, 5, "Name & Position: ___________________________", ln=True)
    pdf.cell(90, 5, f"Date: {date.today()}", ln=False)
    pdf.cell(0, 5, "Date: ___________________________", ln=True)

    # Ara Connect footer on all pages
    pdf.set_y(-15)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, _CO_FOOT, align="C")

    # ── AUDIT CERTIFICATE PAGE — DocuSign-style ─────────────────────────────
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

        # ── Page header (light — no logo for certificate page) ────────────────
        pdf.set_fill_color(31, 20, 80)
        pdf.rect(0, 0, 210, 22, "F")
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(255, 255, 255)
        pdf.set_y(5)
        pdf.cell(0, 6, "CERTIFICATE OF COMPLETION", ln=True, align="C")
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 5, "SY Comms  |  Electronic Signing Record", ln=True, align="C")
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
        _env_row("Subject:", f"SY Comms Proposal - {_signer_co[:40]}")
        _env_row("Originator:", "SY Comms")
        _env_row("Document Pages:", "4   |   Signatures: 3")
        _env_row("Time Zone:", "(UTC+00:00) Dublin, Edinburgh, Lisbon, London")
        _env_row("Originator Email:", _orig_email)
        pdf.ln(4)

        # ── Record Tracking ───────────────────────────────────────────────────
        _section("Record Tracking")
        pdf.ln(1)
        _row3("Status", "Holder", "Location", bold1=True)
        _row3("Original", "SY Comms", "SY Comms Quotation Tool")
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
                _s_buf2 = io.BytesIO(sig_bytes)
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

        pdf.set_y(-15)
        pdf.set_font("Helvetica", "I", 7)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 5, _CO_FOOT, align="C")

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
        if sig_bytes:
            sig_buf = io.BytesIO(sig_bytes)
            pdf_obj.image(sig_buf, x=x, y=y_start, w=w, h=h)
            pdf_obj.set_y(y_start + h + 1)

        # Metadata — always in left column (x=15), max 90mm wide
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
        msg["Subject"] = f"Your SY Comms Proposal - {customer or 'Telecoms Quote'}"
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


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📄 Proposal Summary", "🖋️ Order Form Preview", "📥 Download Documents", "👤 Customer View", "✍️ Sign & Send", "📨 Remote Signing"])

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
        st.markdown("#### System Hardware")

        all_hw_items = []
        for name, qty in desktop_quantities.items():
            all_hw_items.append((name, qty, "Included in Package"))
        for name, qty in cordless_quantities.items():
            all_hw_items.append((name, qty, "Included in Package"))
        for name, qty in headset_quantities.items():
            all_hw_items.append((name, qty, "Included in Lease"))
        for name, qty in other_quantities.items():
            all_hw_items.append((name, qty, "Included in Package"))

        # Switch
        if auto_switch:
            all_hw_items.append((f"Switch: {rec_switch['name']}", 1, "Included in Package"))
        # Router
        if add_router:
            all_hw_items.append((router_type, 1, "Included in Package"))

        if all_hw_items:
            hw_df = pd.DataFrame(all_hw_items, columns=["Description", "Qty", "Billing"])
            st.dataframe(hw_df, use_container_width=True, hide_index=True)
        else:
            st.info("No hardware selected yet.")

        st.markdown("#### Network & Connectivity")
        net_items = [
            (f"{bb_provider} — {bb_package}", 1, f"£{svc['bb_sell']:.2f}/mo"),
        ]
        if second_fttp and second_fttp_pkg:
            bb2_sell = BROADBAND[bb_provider][second_fttp_pkg]["cost"] / (1 - service_uplift_pct/100)
            net_items.append((f"{bb_provider} — {second_fttp_pkg} (2nd line)", 1, f"£{bb2_sell:.2f}/mo"))
        if total_voice_channels > 0:
            vc_sell_net = round(3.49 * (1 + service_uplift_pct/100) * total_voice_channels, 2)
            net_items.append((f"Voice Channel Licences ({user_licences} handset + {softphone_licences} softphone)", total_voice_channels, f"£{vc_sell_net:.2f}/mo"))
        if wallboard_users > 0:
            net_items.append(("Live Wallboard User", wallboard_users, f"£{wallboard_users * C['wallboard_sell']:.2f}/mo"))
        if ooh_support:
            net_items.append(("24/7 OOH Support", 1, "£25.00/mo"))
        if dark_web_mon:
            net_items.append(("Dark Web Monitoring", 1, "£10.00/mo (after 3m)"))
        if proactive_bb:
            net_items.append(("Proactive BB Management", 1, "£10.00/mo (after 3m)"))

        net_df = pd.DataFrame(net_items, columns=["Service", "Qty", "Charge"])
        st.dataframe(net_df, use_container_width=True, hide_index=True)

    with prop_col2:
        st.markdown("#### Commercial Summary")
        # Build commercial summary cards — content varies by payment model
        _hw_card = "" if is_spread else f"""
        <div class="metric-card" style="text-align:left; margin-bottom:1rem">
          <div class="metric-label">Upfront Hardware Cost</div>
          <div style="font-size:1.4rem; font-weight:700">£{upfront:.2f} (one-off)</div>
        </div>"""

        _spread_note = f"""
        <div class="metric-card" style="text-align:left; margin-bottom:1rem">
          <div class="metric-label">Hardware Payment</div>
          <div style="font-size:1.1rem; font-weight:600; color:#00b5a3">
            Included in monthly — spread over {LEASE_TERM_LABELS[lease_term]}
          </div>
        </div>""" if is_spread else ""

        st.markdown(f"""
        <div class="metric-card" style="text-align:left; margin-bottom:1rem">
          <div class="metric-label">Agreement Term</div>
          <div style="font-size:1.1rem; font-weight:600">{LEASE_TERM_LABELS[lease_term]}</div>
        </div>
        {_hw_card}
        {_spread_note}
        <div class="metric-card" style="text-align:left; margin-bottom:1rem">
          <div class="metric-label">Monthly Service Charges</div>
          <div style="font-size:1.4rem; font-weight:700">£{svc["total_sell"]:.2f} + VAT</div>
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



    # summary banner removed
# ── TAB 2: ORDER FORM PREVIEW ─────────────────────────────────────────────────
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
            "Deal Type": deal_type,
            "Contract Term": LEASE_TERM_LABELS[lease_term],
            "Agreement Type": f'{"Hardware Spread + " if is_spread else "Upfront Hardware + "}Monthly Services',
            "Installation Type": install_type,
            "No. of Sites": str(num_sites),
            "Broadband": f"{bb_provider} — {bb_package}",
            "Care Level": bb_care,
            "Upfront Hardware": f"£{upfront:.2f} (one-off)",
            "Monthly Services": f"£{svc['total_sell']:.2f} + VAT",
            "Total Monthly": f"£{total_mo:.2f} + VAT",
            "Monthly Services": f"£{total_mo:.2f} + VAT",
        }
        if credits_months > 0:
            config_fields["Introductory Credit"] = f"£{credits_amount:.2f}/mo × {credits_months} months"
        if cashback_amount > 0:
            config_fields["Settlement / Cashback"] = f"£{cashback_amount:.2f}"
        for label, val in config_fields.items():
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid #f0f0f0;font-size:0.88rem'><span style='color:#888'>{label}</span><span style='color:#333;font-weight:500'>{val}</span></div>", unsafe_allow_html=True)

        st.markdown("#### 📦 Equipment Summary")
        all_equip = list(desktop_quantities.items()) + list(cordless_quantities.items()) + \
                    list(headset_quantities.items()) + list(other_quantities.items())
        if auto_switch:
            all_equip.append((f"Switch: {rec_switch['name']}", 1))
        if add_router:
            all_equip.append((router_type, 1))
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
        st.markdown("#### 📊 Internal Deal Sheet")
        internal = [
            f"Deal PAT: £{pat:.2f}",
            f"HW Buy Cost: £{hw_buy:.2f}",
            f"HW Sell Price: £{hw_sell:.2f}",
            f"Upfront Total: £{upfront:.2f}",
            f"Broadband Wholesale: £{svc['bb_cost']:.2f}/mo",
            f"Broadband Sell: £{svc['bb_sell']:.2f}/mo",
            f"Service Uplift: {service_uplift_pct}%",
            f"SGP Estimate: £{sgp:.2f}",
        ]
        for d in internal:
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
            label=f"📥 Download Full Proposal Pack — {comp_name}",
            data=pdf_bytes,
            file_name=f"SYComms_Proposal_{safe_name}_{date.today()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('<div class="success-box">✅ PDF ready — 4 sections: Proposal, Order Form, Network Agreement, Mandate & Checklist.</div>', unsafe_allow_html=True)

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

    if not (desktop_quantities or cordless_quantities or headset_quantities or other_quantities):
        st.info("👈 Select hardware from the builder above to populate this view.")
    else:
        # ── Selected Hardware ──────────────────────────────────────────────────
        st.markdown('<div class="cv-section">📦 Your New System</div>', unsafe_allow_html=True)

        all_selected = (
            [(n, q, HANDSETS_DESKTOP[n])   for n, q in desktop_quantities.items()]  +
            [(n, q, HANDSETS_CORDLESS[n])  for n, q in cordless_quantities.items()] +
            [(n, q, HEADSETS[n])           for n, q in headset_quantities.items()]   +
            [(n, q, OTHER_HARDWARE[n])     for n, q in other_quantities.items()]
        )

        # Show in rows of 4
        for row_start in range(0, len(all_selected), 4):
            row_items = all_selected[row_start:row_start + 4]
            cols = st.columns(4)
            for col, (name, qty, info) in zip(cols, row_items):
                with col:
                    bogof_note = ""
                    
                    b64_cv, ext_cv = get_product_image_b64(name)
                    if b64_cv:
                        img_html = f'<img src="data:image/{ext_cv};base64,{b64_cv}" style="width:100%;height:100px;object-fit:contain;border-radius:8px;">'
                    else:
                        cat = info.get("cat", "Desktop")
                        icon = PRODUCT_ICONS.get(cat, "📱")
                        img_html = f'<div style="height:100px;background:linear-gradient(135deg,#2d1f6e,#3b2882);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:2.8rem">{icon}</div>'

                    st.markdown(f"""
                    <div class="cv-hw-card">
                      {img_html}
                      <div class="cv-hw-name">{name}</div>
                      <div class="cv-hw-qty">Qty: {qty}</div>
                      {bogof_note}
                    </div>
                    """, unsafe_allow_html=True)

        # Auto-included items
        st.markdown(f"""
        <div style="margin-top:0.75rem;padding:0.6rem 1rem;background:#f8f9ff;border-radius:8px;font-size:0.82rem;color:#555">
          Also included: <strong>{rec_switch['name']}</strong> switch &nbsp;·&nbsp;
          <strong>{router_type}</strong> &nbsp;·&nbsp;
          <strong>{total_voice_channels} Voice Channel Licence{'s' if total_voice_channels != 1 else ''}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

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
        comp_rows = []
        if current_bb > 0:
            comp_rows.append(("Broadband & Lines", current_bb, svc["bb_sell"]))
        if current_system > 0:
            sys_new = hw_monthly_spread if is_spread else 0
            comp_rows.append(("Phone System", current_system, sys_new))
        if current_calls > 0:
            comp_rows.append(("Call Charges / Licences", current_calls, svc["lic_monthly"]))
        if current_mobile > 0:
            comp_rows.append(("Mobile", current_mobile, svc["mobile_sell"]))
        if current_support > 0:
            comp_rows.append(("Support & Maintenance", current_support, 0))
        # Other costs + software add-ons (SY Comms side shows sw_sell_total)
        if current_other > 0 or sw_sell_total > 0:
            comp_rows.append(("Other / Software Add-ons", current_other, sw_sell_total))

        # Comparison table — built as a flat string to avoid markdown code-block indentation
        _saving_bg  = "#e8f8f0" if saving_mo >= 0 else "#fdf0f0"
        _saving_col = "#1a7a40" if saving_mo >= 0 else "#c0392b"
        _saving_lbl = "Monthly Saving" if saving_mo >= 0 else "Monthly Increase"
        _arrow      = "-" if saving_mo >= 0 else "+"

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
        _tbl += f'<div style="font-size:1.8rem;font-weight:800;color:{_saving_col}">{chr(163)}{abs(saving_mo):.2f}<span style="font-size:0.9rem;font-weight:400"> per month</span></div>'
        _tbl += f'<div style="font-size:1rem;color:{_saving_col};margin-top:0.2rem">{chr(163)}{abs(saving_yr):.2f} per year &nbsp;&middot;&nbsp; {abs(saving_pct):.0f}% {"saving" if saving_mo>=0 else "increase"}</div>'
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
            (f"Business Broadband — {bb_provider} {bb_package}", f"£{svc['bb_sell']:.2f}/mo"),
        ]
        if second_fttp and second_fttp_pkg:
            bb2_sell = BROADBAND[bb_provider][second_fttp_pkg]["cost"] * (1 + service_uplift_pct/100)
            svc_lines.append((f"2nd Line — {bb_provider} {second_fttp_pkg}", f"£{bb2_sell:.2f}/mo"))
        if total_voice_channels > 0:
            svc_lines.append((f"Voice Channel Licences ({total_voice_channels} users)", f"£{svc['lic_monthly']:.2f}/mo"))
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

    with cv_col2:
        st.markdown('<div class="cv-section">💳 Your Investment</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="cv-price-row">
          <span class="cv-price-label">Hardware</span>
          <span class="cv-price-val">{"Spread over term" if is_spread else "One-off payment"}</span>
        </div>
        <div class="cv-price-row">
          <span class="cv-price-label">Network & Services</span>
          <span class="cv-price-val">Monthly</span>
        </div>
        <div class="cv-price-row" style="font-weight:700; border-bottom:2px solid #1f1450;">
          <span style="color:#1f1450">Total (excl. VAT)</span>
          <span style="color:#1f1450">£{total_mo:.2f}/mo</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="cv-total-box">
          <div class="cv-total-label">Agreement Term</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#fff">{LEASE_TERM_LABELS[lease_term]}</div>
          <div class="cv-total-note">Contact us for full pricing details</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:1rem;padding:0.8rem 1rem;background:#f8f9ff;border-radius:8px;font-size:0.82rem;color:#555;text-align:center">
          All figures exclude VAT.<br>
          Subject to survey & credit approval.
        </div>
        """, unsafe_allow_html=True)



# ── TAB 5: SIGN & SEND ────────────────────────────────────────────────────────

with tab5:
    st.markdown('<div class="tab-content"></div>', unsafe_allow_html=True)

    if not comp_name:
        st.warning("👈 Add a customer name in the sidebar first.")
        st.stop()

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
                    canvas_result = st_canvas(
                        fill_color="rgba(0,0,0,0)",
                        stroke_width=3,
                        stroke_color="#000000",
                        background_color="#EAF4FB",
                        update_streamlit=True,
                        height=180,
                        width=510,
                        drawing_mode="freedraw",
                        display_toolbar=True,
                        key="sig_canvas",
                    )
                if canvas_result.image_data is not None:
                    alpha = canvas_result.image_data[:, :, 3]
                    if alpha.sum() > 500:
                        from PIL import Image as _PILImage
                        sig_pil = _PILImage.fromarray(
                            canvas_result.image_data.astype("uint8"), "RGBA"
                        ).convert("RGB")
                        sig_buf = io.BytesIO()
                        sig_pil.save(sig_buf, format="PNG")
                        st.session_state["_sig_bytes"] = sig_buf.getvalue()
                        st.success("Signature captured")
                    else:
                        st.session_state.pop("_sig_bytes", None)

        sig_bytes = st.session_state.get("_sig_bytes")
        if sig_bytes:
            st.success("Signature ready")

        # Confirm name typed
        sig_name = st.text_input("Customer full name (typed confirmation)",
                                 value=contact_name or "", key="sig_name_confirm",
                                 placeholder="e.g. Jane Smith - Director")
    with send_col:
        st.markdown("### 📧 Email Proposal")

        to_email = st.text_input("Send to (customer)",
                                 value=director_email or billing_email or "",
                                 key="send_to")
        cc_email = st.text_input("CC (consultant / your address)",
                                 value=em_cfg.get("reply_to", "") or em_cfg.get("username", ""),
                                 key="send_cc")

        st.markdown("")

        sig_bytes = st.session_state.get("_sig_bytes")
        ready = bool(sig_bytes and sig_name and to_email)

        # ── Generate signed PDF button ─────────────────────────────────────
        if st.button("📄 Generate Signed PDF", use_container_width=True,
                     type="secondary", disabled=not sig_bytes):
            if not sig_name:
                st.warning("Please type the customer name for confirmation.")
            else:
                from datetime import datetime as _dtnow
                _ts = _dtnow.now().strftime("%d/%m/%Y  %H:%M")
                _pdf_bytes = build_pdf(
                    sig_bytes=sig_bytes,
                    sig_name=sig_name,
                    sig_company=comp_name or "",
                    sig_timestamp=_ts,
                    sig_ip=_client_ip,
                    curr_total=current_total, curr_bb=current_bb,
                    curr_system=current_system, curr_calls=current_calls,
                    curr_mobile=current_mobile,
                )
                safe = (comp_name or "quote").replace(" ", "_")
                st.session_state["_signed_pdf_bytes"]    = _pdf_bytes
                st.session_state["_signed_pdf_filename"] = f"SYComms_{safe}_SIGNED_{date.today()}.pdf"

        if st.session_state.get("_signed_pdf_bytes"):
            st.download_button(
                "📥 Download Signed PDF",
                data=st.session_state["_signed_pdf_bytes"],
                file_name=st.session_state["_signed_pdf_filename"],
                mime="application/pdf",
                use_container_width=True,
                key="dl_signed",
            )
            st.markdown("")

        # ── Email signed PDF button ───────────────────────────────────────
        if st.button("📨 Email Signed PDF to Customer", use_container_width=True,
                     type="primary", disabled=not ready):
            if not sig_name:
                st.warning("Please type the customer name for confirmation.")
            elif not to_email:
                st.warning("Enter a recipient email address.")
            else:
                from datetime import datetime as _dtnow2
                _ts2 = _dtnow2.now().strftime("%d/%m/%Y  %H:%M")
                _pdf_bytes = st.session_state.get("_signed_pdf_bytes") or build_pdf(
                    sig_bytes=sig_bytes,
                    sig_name=sig_name,
                    sig_company=comp_name or "",
                    sig_timestamp=_ts2,
                    sig_ip=_client_ip,
                )
                safe = (comp_name or "quote").replace(" ", "_")
                fn   = f"SYComms_{safe}_SIGNED_{date.today()}.pdf"
                ok, msg = send_proposal_email(
                    em_cfg, to_email, cc_email, _pdf_bytes, fn, comp_name, total_mo
                )
                if ok:
                    st.success(msg)
                    st.balloons()
                else:
                    st.error(msg)

        if not em_cfg.get("username"):
            st.markdown('<div class="info-box">⚙️ Configure SMTP in <strong>Admin Panel → Email</strong> to enable sending.</div>',
                        unsafe_allow_html=True)
        elif not ready:
            st.markdown('<div class="info-box">✍️ Capture signature + type name to unlock email.</div>',
                        unsafe_allow_html=True)

        with st.expander("ℹ️ Gmail setup — click if email fails"):
            st.markdown("""
**One-time Gmail setup (2 minutes):**

1. Sign in to the Gmail account at [myaccount.google.com](https://myaccount.google.com)
2. Go to **Security** → turn on **2-Step Verification**
3. Go to **myaccount.google.com/apppasswords**
4. Create a new App Password - select *Mail* and *Windows Computer*
5. Copy the 16-character password it gives you
6. Go to **Admin Panel → 📧 Email** → paste it into *App Password* → Save

The password you entered when setting up the account won't work - you must use an **App Password**.
            """)

# ── TAB 6: REMOTE SIGNING ─────────────────────────────────────────────────────
with tab6:
    st.markdown("### 📨 Send Documents for Remote Signing")
    st.caption("Upload PDFs and send the customer a secure signing link — no need for them to be in the room.")

    em_cfg_rs         = st.session_state.active_config.get("email", {})
    GITHUB_TOKEN_RS   = st.secrets.get("GITHUB_TOKEN", "") if hasattr(st, "secrets") else ""
    SIGNING_PORTAL_URL = st.secrets.get("SIGNING_PORTAL_URL", "") if hasattr(st, "secrets") else ""

    # ── Helper functions ──────────────────────────────────────────────────────
    def create_signing_session(docs, cust_name, cust_email, sndr_email, message):
        """Upload PDFs to a private GitHub Gist and return (gist_id, signing_url)."""
        from datetime import datetime as _dt
        session_data = {
            "customer_name":  cust_name,
            "customer_email": cust_email,
            "sender_email":   sndr_email,
            "message":        message,
            "status":         "pending",
            "created_at":     _dt.now().isoformat(),
        }
        files = {"session.json": {"content": json.dumps(session_data, indent=2)}}
        for i, (fname, pdf_bytes) in enumerate(docs, 1):
            files[f"doc_{i}_{fname}.b64"] = {"content": base64.b64encode(pdf_bytes).decode()}

        hdrs = {"Authorization": f"token {GITHUB_TOKEN_RS}",
                "Accept": "application/vnd.github+json"}
        try:
            resp = _req.post(
                "https://api.github.com/gists",
                json={"files": files, "public": False,
                      "description": f"Novalink Signing - {cust_name}"},
                headers=hdrs, timeout=30
            )
        except Exception as e:
            return None, f"Network error: {e}"

        if resp.status_code != 201:
            return None, f"GitHub error {resp.status_code}: {resp.text[:200]}"

        gist_id     = resp.json()["id"]
        signing_url = f"{SIGNING_PORTAL_URL}?gist={gist_id}"
        return gist_id, signing_url

    def send_signing_invite(to_email, cust_name, signing_url, message, em):
        """Email the customer their unique signing link."""
        try:
            msg            = MIMEMultipart()
            msg["From"]    = f"{em.get('from_name','SY Comms')} <{em.get('username','')}>"
            msg["To"]      = to_email
            msg["Subject"] = "Please sign your documents - SY Comms"
            html = f"""<html><body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:0 auto">
              <div style="background:#1f1450;padding:20px 30px;border-radius:8px 8px 0 0">
                <h2 style="color:#fff;margin:0"><span style="color:#00b5a3">Novalink</span> Hardware</h2></div>
              <div style="background:#f9f9f9;padding:24px 30px;border:1px solid #e0e8e8;border-top:none">
                <p>Dear {cust_name},</p>
                {"<p>" + message + "</p>" if message else ""}
                <p>Your documents are ready for your electronic signature. Please click the button below:</p>
                <div style="text-align:center;margin:28px 0">
                  <a href="{signing_url}" style="background:#008078;color:#fff;padding:14px 32px;
                    border-radius:8px;text-decoration:none;font-weight:bold;font-size:1rem">
                    Review &amp; Sign Documents
                  </a>
                </div>
                <p style="font-size:0.83rem;color:#999">Or copy this link into your browser:<br/>
                  <a href="{signing_url}" style="color:#008078">{signing_url}</a></p>
                <p>Kind regards,<br/><strong>{em.get('from_name','SY Comms')}</strong></p>
              </div></body></html>"""
            msg.attach(MIMEText(html, "html"))
            with smtplib.SMTP(em.get("smtp_host","smtp.gmail.com"),
                              int(em.get("smtp_port", 587))) as srv:
                srv.ehlo(); srv.starttls(); srv.ehlo()
                srv.login(em["username"], em["password"])
                srv.sendmail(em["username"], [to_email], msg.as_string())
            return True, "sent"
        except smtplib.SMTPAuthenticationError:
            return False, "Gmail authentication failed - check App Password in Admin → Email."
        except Exception as e:
            return False, str(e)

    # ── Setup checks ──────────────────────────────────────────────────────────
    setup_ok = True
    if not GITHUB_TOKEN_RS:
        st.warning("**GitHub token not set.** Add `GITHUB_TOKEN` to your Streamlit Cloud secrets (Settings → Secrets).")
        st.code('GITHUB_TOKEN = "ghp_your_token_here"', language="toml")
        setup_ok = False

    if not SIGNING_PORTAL_URL:
        st.warning("**Signing portal URL not set.** Add `SIGNING_PORTAL_URL` to your Streamlit Cloud secrets.")
        st.code('SIGNING_PORTAL_URL = "https://your-signing-portal.streamlit.app"', language="toml")
        setup_ok = False

    if not em_cfg_rs.get("username") or not em_cfg_rs.get("password"):
        st.warning("**Email not configured.** Go to Admin Panel → Email and save your SMTP settings first.")
        setup_ok = False

    if setup_ok:
        # ── Upload + customer form ────────────────────────────────────────────
        rs_col1, rs_col2 = st.columns([3, 2])

        with rs_col1:
            st.markdown("**📎 Documents to send**")
            uploaded_docs = st.file_uploader(
                "Upload PDFs", type=["pdf"], accept_multiple_files=True,
                key="rs_docs", label_visibility="collapsed"
            )
            if uploaded_docs:
                for uf in uploaded_docs:
                    st.markdown(f"- 📄 **{uf.name}** ({len(uf.getvalue())//1024} KB)")

        with rs_col2:
            st.markdown("**👤 Customer details**")
            rs_name    = st.text_input("Customer name",  value=comp_name or "",
                                       key="rs_name", placeholder="Acme Ltd")
            rs_email   = st.text_input("Customer email", value=director_email or billing_email or "",
                                       key="rs_email", placeholder="jane@acme.co.uk")
            rs_cc      = st.text_input("CC (your address)",
                                       value=em_cfg_rs.get("reply_to", em_cfg_rs.get("username","")),
                                       key="rs_cc")
            rs_message = st.text_area("Personal message (optional)", height=90, key="rs_msg",
                                      placeholder="Please review and sign at your earliest convenience.")

        st.markdown("")
        rs_ready = bool(uploaded_docs and rs_name and rs_email)
        if not rs_ready:
            missing = [x for cond, x in [(not uploaded_docs,"at least one PDF"),
                                          (not rs_name,"customer name"),
                                          (not rs_email,"customer email")] if cond]
            st.caption(f"Still needed: {', '.join(missing)}")

        if st.button("📨 Create Signing Session & Email Customer",
                     type="primary", use_container_width=True, disabled=not rs_ready):

            with st.spinner("Uploading documents and creating signing session..."):
                docs_list = [(uf.name, uf.getvalue()) for uf in uploaded_docs]
                gist_id, result = create_signing_session(
                    docs_list, rs_name, rs_email, rs_cc, rs_message
                )

            if gist_id:
                signing_url = result
                st.success("Signing session created!")

                with st.spinner("Sending invite email to customer..."):
                    ok, msg = send_signing_invite(
                        rs_email, rs_name, signing_url, rs_message, em_cfg_rs
                    )

                if ok:
                    st.success(f"Invite email sent to **{rs_email}**")
                else:
                    st.error(f"Session created but email failed: {msg}")
                    st.info("You can manually copy and share the signing link below.")

                # Show the signing link clearly
                st.markdown("**Customer signing link:**")
                st.code(signing_url)

                st.markdown(f"""
                <div style="background:#e8f4fb;border-left:4px solid #00b5a3;border-radius:0 8px 8px 0;
                            padding:0.9rem 1.1rem;margin-top:0.4rem;font-size:0.86rem;color:#2d1f6e">
                  📋 <strong>Reference:</strong> {gist_id[:12].upper()}<br/>
                  👤 <strong>Customer:</strong> {rs_name} ({rs_email})<br/>
                  📄 <strong>Documents:</strong> {len(docs_list)}<br/>
                  Once signed, all parties automatically receive the completed documents by email.
                </div>""", unsafe_allow_html=True)
            else:
                st.error(f"Could not create signing session: {result}")
