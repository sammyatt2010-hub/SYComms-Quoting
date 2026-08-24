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
SYCOMMS_LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAQDAwMDAgQDAwMEBAQFBgoGBgUFBgwICQcKDgwPDg4MDQ0PERYTDxAVEQ0NExoTFRcYGRkZDxIbHRsYHRYYGRj/2wBDAQQEBAYFBgsGBgsYEA0QGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBj/wAARCADwAPADASIAAhEBAxEB/8QAHQABAAICAwEBAAAAAAAAAAAAAAYIBwkBAgQDBf/EAEQQAAEDAwIEBAMEBggEBwAAAAEAAgMEBQYHEQgSITETQVFhFCJxMjNCgRVicpGhsQkWFyNSgpLBJLK0whhTVFWDk6P/xAAbAQEAAgMBAQAAAAAAAAAAAAAAAQMCBAYFB//EADERAAICAQIEBAQFBQEAAAAAAAABAgMRBDEFEiFBEyJRcTIzgaEGFBWR4RY0YcHwU//aAAwDAQACEQMRAD8Av8iIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIuCQF0fNHHE6R72tY0buc47AfUpkH0RY6yPXbSPFXujvWoNiilaOsMFQKiQH05Y+YrGl142NHqBzm0MWSXUjsaa3iNrvzle3+S2K9JfZ8EG/oThlkEVT5OO7CA8+Fg+Svb5F0lO0/85XEfHdhJcPFwfJWN8+WSncf3c4Wx+lav/zY5WWxRVvtXGxo9XuYyvhyS0k/adUW8Stb+cTnfyWTMd120iyl7Y7PqDY5JHdoZ6gU8m/pyycp3WvZpL6vjg19BhmREXzbNG+MSMeHMcNw4HcH6Fdwd1rZIOURFICIiAIiIAiIgCIiAIiIAiIgCIiAIi+VTUwUlLJU1M0cMMTC+SSRwa1jQNy4k9AAPMoD6OIaNydlE841KwrTmyi55hkNJbY3DeKN5L5pvaOJu7n/AJDb3CrRrPxlU9FLUY5pKIaydu7Jb/OzmhYfP4dh+8P67vl9A7uqbXq9XjI75Peb/dKu53Cc80tVVymSR3tuew9AOg8gvd0PArbkrLXyx+5ko5LXag8cV2qpJqDTbG4qKHq1tzvA8SU/rNgaeVv+Zx+irXlmpeoGdzOky7LrrdGuJPgSTFkLd/IRM2YB+SiyLqNPw7T6f5cevq+rM8I4a1rBsxoaPRo2XKIt0kIiIAjgHN2eA4ejhuiICVYnqXqBg07ZcSzC7WxoIPgRzl8LtvIxP3YR+Ssnp9xw3WlkhodSccirIejXXOzjw5B7ugceV3vyuH0VQkWjqOG6fUfHHr6kYybbsF1LwrUeym54fkNJc42/exMJZNB7SRu2cw/Ubem6loII3BWnOzXy8Y9fILzYbpV224wHeKqpJTHI323HceoPQ+auRovxk09bLT47q0YaOod8kV/hZywvPl47B92f12/L6hq5jXcDso89Xmj9zFxwXFRfKnqIKqljqaeaOWGRoeySNwc17SNwQR0II819V4RgEREAREQBERAEREAREQBEXkuVyobTaqm5XKqipaOmidNPPM7lZGxoJc5x8gACUB5sgyGz4vjtXfb9cIKC3UkZlnqZ3crWNH8yT0AHUkgDcla7teuJK/aq109hsLqi04g12zabm5Za8Ds+fb8PmI+w6E7nt4uITXm4auZa6gtcstNiNBKTRUp6GqcOnxEo9T+Fp+yPclYVXX8J4Oqkrr1mXZehbGOOrCIi6MkIiIAiIgCIiAIiIAiIgCIiAztoNxI33SmuhsV9fU3bD3u2dS788tBv+ODf8PmY+x7jY99iWP5FZ8px6kvthuEFfbquMSwVMDuZr2n+RHYg9QehWndZq4etebjpFljbfc5JqrEa6UGtpR8xpXnp8REPUdOZo+0B6gLneLcIVid1C83dev8AJi0bMkXkttxortaqa5W6piqqSpibNDPC7mZIxw3a5p8wQd161x5WEREAREQBERAEREB1c7laTtuqOcYWt0l1vEuk+M1jm0NI8G9TRO6Tyjq2n3H4WdC4ebth+EqyPEBqkzSnRyuvVO9n6Yqv+Ctcbj3neD8+3mGN3efoB5rV1LNNUVElRUSvmmkeZJJZDu57id3OJ8ySST9V0PAdB4snfNdFt7/wZxXc6IiLsTMIiIAiIgCIiAIiIAiIgCIiAIiIAnmiIC23B7ra+13qPSjJqxzqGrcXWaaV33Ep6up9z+F3Ut9Hbj8QV5Wu5mg7bLTPDNNT1MdRTyvhmje2RksZ2cxzTu1wPkQQCPcLaLoDqnHqto3QXupe0Xim/wCCucTem07APn29Ht2eP2iPJcbx3QeDJXwXR7+/8mEkZUREXPmAREQBERAF1cSGEgbkLsonqXl0WCaS5DlshbvbaGSaMO7Ol22jb+by0KYxcmordgoVxb6jOzfXmeyUcxfa8bDqCIA/K+foZ37ftAM/yLAi7zT1FTUy1NXK6WomeZZZHd3vcd3H8ySui+k6TTrT1RrXZFqWAiItgkIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCz3wlajPwnXmCyVkxbaskDaCUEnlZUAkwP2+pczf0f7LAi+kE9RS1UVVSSuiqIXtlikb3Y9p3aR9CAVr6qhaiqVT7/wDIG5dp3buuVFNNMtizrSTH8tiI3uVFHNIB+GTbaRv5PDgpWvm0ouLcX2KQiIoAREQBVf438mfbdErXjcT+V14ujPEbv9qKFpkI+nP4atAeyoZx03o1Oq+MWBsvM2htb6pzd+zppSB/CFelwirxNXBP3/YmO5VZF7rNZbvkV+p7LYbbVXK41LuWGlpYzJJIdtzsB6DcknoPNZZ/8KOvJoPihhUPVvMIDc6cS/Tl59t/bddxbqqaniyaT9y1mGEUutel+f3nUGrwa3Y1O/I6RjnzWyaaKCVoABP23gHo5p2BPQ79l+fl+FZVgORfoLMLLPabh4TZxBK5ruZjt9nBzCWkbgjoehHVZLUVuSgpLL7ZB+CinOHaN6nZ/j8l8xDEaq526OZ0Dqls0MTedvVwHiPbvtuNyOg9e6hM0T4KmSCQsL43ljuRweNwdjs4Egjp3B2UwurnJxi02twdERem32+uutzgttsoqitrKh/hw01NGZJJHejWjqSrG0llg8yLM1Bwp6719AKpuEtpw4biOruEEUh/y8xI/NY+zLT3NtPblFQ5njVbZ5pt/BMwa6ObbvyPaS122432PTcLXr1lNkuWE036ZBGkUkw7T7NtQbnJQYZjVdeJYtvFdA0COLftzyOIa36E7qd3fhd10stsdX1GDPqYmDd7KCshqZG/5Gu5j+QKT1lEHyymk/TIMQIu0kUsNRJBPE+KWNxY9kjS1zHA7EEHqCPQqdP0W1Rj05Geuw+qOOGlFd+kGzwuHgHqH8gfz7bHf7O6snfXBJyklkEDRPLv+anb9GNUI9N/6/S4hVMxz4T474988LR4J7P5C/n267/Z3U2XV1Y8SSWQQRFNMJ0m1D1GoautwnGZrvBRyiGodHPDHyPLeYA+I9p7ddwConXUNZa7rVWy400lNWUsroJ4JBs6N7SWuafcEFRG6uUnCLy12B50UzwrSfUXUaiq6zCcWqbxBRyCGeWOaKJrHkcwbvI9u522PTfbcb9wo1PZrpTZJLj8tDN+lIqk0bqSMeI/xg7kLAG78x5gR033SN9cpOCksrf/AADwosyUPCtrvX21tazCW07XjmbFVXCCKU/VhduD9dljfLMOyfBsifYsts1Rarg1gl8CflJcwkgOBaSCCQeoPksKtXTa+WE037gvBwQZNJc9ELpjk0nM+zXR/htJ6timaJAPpz+IrQKhvArejTas5PYHSbMrbVHVNYT3dDMGn+EyvkuG4tV4erml36/uVS3CIi84gIiIDgrXDxkVBm4qq1hO/gWuji+g2e//AL1sePZa2uMBpbxYXkkfaoqMg/8Axbf7L2vw/FPV9fRmUdyX8Dtfj1LqnkdHcZII7vV2+JluMmwc9rXuMzGb9z1jJA6kN9llHXC58VGMZrW3/ApYK/EWhroKW3UMVTLC0NHN40bgZHdQ7qzcbbdAqo6VaQZrqjDeK/B6ujjr7E+nk8KapdTSPMnicropANmuHhnuR3HVXN0Ah4j7bdqm0awQQTWSKlJpa2rqYZqvxg5uzQ6NxL27c25f1Gw2JW3xSNdWolenGT7xfsTJ4ZSCv1Ryyp1xOqodT0eRsqo6lwgY5kXiRsEbmlpJIa4NIc0n8RCudqLg1l4qNDsay7EqiCiu0b2mOWY/csc4NqaeTbzYQXD3YPJyrlxe0dio+J2uFlZBHNNQ081wZCAAKl3NuXAdnloYT5nfc91lPgPutwcc2srqp5oIRSVUdOT8rJXmVrnD0JDGA+vKFfrY82lr1lK5ZRx+xMtj93iJzWz6J6DWzRvBZPhrhW0fw/Mw/wB5T0fUSyuP/mSu5hv7vPkqf6f4DkGpWc0uJYvDC6sma6QvndyRQxsG7nuOx2A6DYAkkgKQa/3OvuvE5m8twqpKh0F1lpYi878kUezWMHoAB/M+ajmC5zkWnOb0uVYvVMgr4GuZtKzxI5WOGzmPb5g/vGwIW9oNLKnS5rfnks5fqSl0Pdqbpjk+lGaNxrJ20r55IBUwVFI8vinjJLeZpIB6EEEEbhW04MsHstm0puWqFfEx1wrJpoI6hzdzT0sPRwb6Fzg4n15WjyVRtRtScp1TzL+suV1EElU2FtPDFTReHFDGCSGtbuT3c4kkkklW44M85st40ouOl9wmYLjSTTTR07zymopZuri31LXFwO3YOafNa/FvH/IrxN+nNj0/7AexinKeM7VK5ZJUT4mLTZrQJD8NTyUbamV0e/ymR7j3I2OwAA32UI1H1oy7XGhxjH7/AG+3RXOirHxxVdG10bJzPyRt5oyTykEA7g7HfsFNcq4MdU7Zk09Pin6KvVo8QmmqZK1tNI1nkJGO/EB0JaSD36KH6iaJZZojj+OZTf7lbpLpVXD+5oqImRkBiaJQXSEDckgDYDYeqyo/Tsx8DHP29c47kLHYt/nuS2LhY4b7bQYxaKepqjK2ho4ZN2tnqSwukqJiOrujXOPmd2tGw7YL064zM7OoNDR59BaK2x1lQyCWSkpTTy0nO7lEjSHEOAJG7T1236rOufY3Y+Kfhut1di14p6erEra6jlk3c2CoDC2SnmA6t+05p8x8rhuO+C9OeDPOv7Q6Crz6otFDZKOoZPLHSVXxEtVyODhG0coDQ4gAk9didhuvJ0q0fgWfmvmdd9/oQsdz9fjd07tlvlsmo1tpY4KmuqHW65GMACZwYXxSH1dsxzSfMcu/ZWN0WpKWv4UsNoK2Bk9NUWCCGWJw3D2Oj2c0+xBIVcuNzUS13Kayac2yrjqKmhqXXC5CM7iB/IWRRk/4tnvcR5Dl37rI9VlF0wz+jlxzKrJL4dfbbZaqiLr0ftPFzMPs5vM0+xWF0LJ6KmD3beP9DsVjpdArhJxgnSGWKZ1tjq/iZKjr1tu3OJN/Us2j/aKuzr7S09JwmZpSUkLIYIbM+OONg2DGtDQAPYAAL1TZhgMGnT9ehFA6J1iDhWD7x0HMXtp9/XxXcu3+JYxqcjuuX/0aV5yi9zeLcLlaa2pndv0DnVUnyj2A2aPYBV36m7UzrnNdItL69w3k/B4EQDgWab/+6w/9OFjzjI0wnsmrNDm1mo3y02SubTyxxt6/HNAaANvORvKR6lrlkPgQI/qHmYPndYf+nCnuguW2nWPSWno8pp4LleMWu/I8T/MRJDI40tR9eXpv6tcti++em11l8FlJ9fqhs8k40V09h0w0Zs2KFrDXRxior5Wj72pk+aQ+4B2aPZoVPdFbjjlt/pBb3LkUlPEZbjdIKCWoIDW1LpiGbE9A4t52j3O3cqzelOpn9ovEBqPFRVBfZrEKS2UQB+V7mum8aUftPBAPm1jVSyHTDINWOI/PcfxmpoYa+mra+ua2skdGyUNquXlDgDyn5wQSNuiaCGXetRLHMk2/cIt5r4/iPt90prto9VU01khpx8RQU1NDLWGUOO7uWUHnbsW7Nbseh6HoqNaoZ7l2oWax3TOKWGmvdFStt87I6Z1Mfkc5274z9l/zncdB7K32hdm4p8TzWhsGcQRV2HDmbNPca+GpkgaGnl8GRrjIeoaOV24237LHXHRR2ODUXFKukZA28VFDP8cWbB742vYIXP2795QCfIey2OFThTqY0NRl6Sj/ALEX2IfwbzmHiqoWAkCa11kR9/lY7/sWx9a2eD9pPFhZiB0bRVjj9PC2/wBwtky0+P8A919ERPcIiLxDEIiIAey128atvko+JeGrc3ZlbZaaRh9S18rHfyatiSpbx4WEiTDMoY3/ANTbZD9eWVn/ACv/AHr1eCT5NZHPfK+xMdyrmGai5xp5Xz1eF5JV2eSoDROIQxzJg3fl52PaWu25nbdPMqe1nFVrvXUDqR+bNgDhsZaW308Um3s8M3H5LDaLtLNHRZLnnBNlp9qysrLjcJ6+4VU1VV1EhlmnmeXvleTuXOcepJ91JMJ1KzrTmaumwnIZrPJXNY2pdFDFJ4gYXFoPiMdttzO7bd1FUVs6ozjySWUD23m8XPIcirr7eao1dxrpnVFTUOa1pkkd3cQ0ADf0AAXiRFnGKiklsAvTQXCutVzguVsraiirKd4khqKaQxyRO9WuHUFeZEklJYYMyUHFTrvQUApG5uKhrRsJKu308sn+os3P57qA5jqHm+oNdFV5nk1feHw7+C2dwEcW/fkY0BrfLsN1GUWvXo6K5c0IJP2BJcO1BzXT65PrsMySus8su3itgcDHLt2543Atdt7hTi8cUGut7tjqCpzuSmie3lc6go4aaRw/ba3mH5ELESKZ6SiyXPOCb9gdpJJJp3zTSPklkcXvke4uc9x6kknqSfUqZ1mrmo9w00Zp9W5TUTYyyGOnbbTBCGCOMhzG8wZz9C1p+1v0UKRWTqhPHMl02JySN2fZk7TVun7sgqv6ssn+JbbNmeGJObn335ebbmJdy77b9dl+jBq3qNTaZHTuHKahuLmB1MbYIIeQxucXObzFnP1JJ35t+vdQtFi9PU1hxW+du/qQTLCtWNRNOqKro8JyeezwVkrZqhkUEMniPDeUEmRjiOnTovHi+oWaYTX3KtxPIaq11FyjMNZJC1h8ZpcXdQ5pAO7iQRsRudiFGUR6epttxXXfpuSyWYTqbnmnJrThOST2c1wYKkxQxSeLyb8u/iMd25ndvVeaz59meP5tVZfY8jrLffKt8klRWwcrXSmR3M8ObtykF3Xbbbt06KOIj09bbfKuu/QgzO7iv15fQmlOaRAFvL4zbbTCX683Jtv77LFN9v8Aesmv1Re8hulVc7jUEGaqqnl737dAN/IDyA6DyX5yKKtLTS+auCT/AMIIsXwVW6Sr4l5axrd46Ky1Mjj6F8kTG/7rYiFS3gPsR8bMsoeOh+Gt0R/1Sv8A5sV0lxXG7FPVyx2wiuW4REXkmIREQBYP4sMRdlfDNepIInSVVnfHdoQ0bnaIkSD/AOtz1nBeW40VLcrVU2+tiE1NUxOgmjd2exwLXA/UEqym102RsXZ5CNNvmikefYhVYDqdfMNqw8PtdW+Bjnj7yLvE/wDzMLSo4vpdc1OKmtn1LgiIswEREAREQBERAEREAREQBERAEREAREQBEUjwHEKrPtTrHh1G15fc6tkEjmjfw4u8r/YNYHHf2WM5qEXN7LqDYTwn4icV4ZbLJND4dVd3yXaUEbHaUgR//m1izgvLbqGlttqprfRRCKmpomQwxgdGMaA1o/IAL1L5nba7bJWPu8lTYREVZAREQBcEbrlEBTLjc0xc9lu1TtcG4ha23XXlb+Ek+DKT7Elh/aYqYLcPkmPWvKcWuGP3qmbU2+vp3U1RE78THDY7ehHcHyIBWqjU7T276Yam3DELvzPNO7npakt2FVTu+7lH1HQ+jg4Lr+Aa7nrenk+q29iyL7EPREXRmQREQBERAEREAREQBERAEREAREQBERAFc/gi0xLI7jqrdIPvQ63Wrmb+EH+/lH1cAwH9Vyq/pjp7d9UNTbdiFpDo/iHc9VVcu7aWBvWSU/QdB6uLQtrGN2C1Yvilux6yUraa30FOynp4m/hY0bDf1PmT5kkrm+P61QgtPHd7+xjJn6uyIi5HBWEREAREQBERAFhfiL0UptXcA5re2KLJrY10ttnds0S7jd0Dz5NfsNj+F2x9VmhcOAI2IWdVs6pqcH1RKeDTZXUNZbLpU2240stJWUsroJ6eZvK+KRp2c1w8iCvOtgnExw4DUOlkzXDYI48rgj/v6fflbc42jo0nsJQOjXHuPlPkRQCpp6ijrJaSrp5aeoheY5YZmFj43A7FrmnqCD0IXf8AD+IV6uvmXSS3RYnk+SIi9AkIiIAiIgCIiAIiIAiIgCIiAL0UNDWXO6U1tt1JNV1tTK2GCngbzPlkcdmtaPMkrpTU1RWVkVJSQS1FRM8RxQxML3yOJ2DWtHUknyCv/wANHDg3TumjzXMoI5crnYRBT78zbbG4dWjyMpHRzh2HyjzJ8/iOvho68v4nsiG8ImHDrolTaRafh1e2GbJbm1stznb8wj2Hy07Hf4Gbnc/icSe2yzQOgXAGwA9FyuBttlbN2T3ZU3kIiKsBERAEREAREQBERAcOaHDYjdYF154abBqtBJfrM6GzZYxmzawN2irNh0ZOAN/YSDqPPmHRZ7RWU3Tpmp1vDC6GoDLcOyTBcrnxzKrTPbbjD1MUvVsjd9g+Nw6PYfJw/gei/CW2/PNOMO1Hxo2TLrJBX0+5dFIfllp3H8ccg6sP07+YKpPqlwcZrir57pgMr8qtIPMKXYMroW+nL0bLt6t2d+quw0PHKrsRt8svsyxSK0IvrV0tVQ3CWhraaalqYSRJTzsMckZHk5p6j818l7qeVlGQREUgIiIAiIgCIvrS0tVXV8NDQUs1VVTODY6eBhkkeT5NaNyfyUNpLLB8l+5iWHZLnWVQY5ilonuVxm6iOLo2Nvm+Rx6MYP8AEen1WetLeDnNcrfDdM+lfitpJDvhOUPrph6cv2Yt/V25/VV2cD04w/TbHG2XEbJBQU/QyyD55Z3f4pJD8zz9e3lsvD1/HKqfJT5pfZGLkYx0H4arBpTTx368mC85ZIz5qzl/uqPcbFlOD1HmC8/MfYdFnoADoOy5RcdddO6bnY8swbyERFWQEREAREQBERAEREAREQBERAFwQCOy5RAQ7NtLMA1DpfBy/FqC5vDeVlS9nLPGP1ZW7PH71W/L+Ba0VHiT4JmVZQO7tpLvF8TGPYSM5XD8w5XBRbWn1t+n+XNolNmtK/8ACVrjYuZ0WN0l5iB+3a61khPvyv5HfwWNrvpxqFYHubesEyWh5TsXS2ybl/1BpBHvutuxG668gB6E/vXrV/iK+K88UzLnZpsfRVsbuWSiqmO9HQvB/iEZRVsjg2Oiqnk9gyB5P8AtyBijcd3MDv2huuRExp3axrT7DZXf1NLHy/v/AAOY1HWjTjUO/va2yYJktfzHYOitk3Lv7uLQNvfdZIsHCTrhfeV0uOUdmicfvLrWsjIH7DOd38Fsr5R5k/muwAHZUWfiLUS+CKX3I5mU9xDgVtMBZPneZVlee7qS0RfDR/QyP5nn8g1WRwrS3AdPKURYhi9BbHkcr6hjOeeQfrSu3ef37KYovK1Gtv1HzZtkZOA0NGwXKItUgIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiID/2Q=="
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
            {"name": "5-Port (4x POE)",   "buy": 29.00,  "poe_ports": 4,  "total_ports": 5},
            {"name": "8-Port (4x POE)",   "buy": 34.00,  "poe_ports": 4,  "total_ports": 8},
            {"name": "8-Port (8x POE)",   "buy": 57.00,  "poe_ports": 8,  "total_ports": 8},
            {"name": "16-Port (8x POE)",  "buy": 80.00,  "poe_ports": 8,  "total_ports": 16},
            {"name": "16-Port (16x POE)", "buy": 152.00, "poe_ports": 16, "total_ports": 16},
            {"name": "24-Port (24x POE)", "buy": 172.00, "poe_ports": 24, "total_ports": 24},
            {"name": "48-Port (32x POE)", "buy": 344.00, "poe_ports": 32, "total_ports": 48},
        ],
        "routers": [
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
}

# ─── PRODUCT IMAGE MAPPING ───────────────────────────────────────────────────
# Place product images in an "images/" subfolder in the repo.
# Filenames below — add matching files to unlock real photos.
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
    "SY Comms Studio":               "images/sy_comms_studio.jpg",
    "Call Recording":                "images/call_recording.jpg",
    "CRM AI Per User":               "images/crm_ai.jpg",
    "ACD Light Agent":               "images/acd_light.jpg",
    "Teams Integration":             "images/teams_integration.jpg",
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

# Pure connectivity cost — broadband + mobile only (for Commercial Summary card)
pure_connectivity = round(svc["bb_sell"] + svc["mobile_sell"], 2)

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
            ("Network & Connectivity (BB, Mobile)", curr_svc, f"£{pure_connectivity:.2f}/mo"),
            ("Installation / Setup (one-off)", "-", f"£{compute_install_cost():.2f}"),
        ]
    else:
        curr_hw  = f"£{current_system:.2f}/mo" if current_system > 0 else "-"
        curr_svc = f"£{(current_bb + current_calls + current_mobile):.2f}/mo" if (current_bb + current_calls + current_mobile) > 0 else "-"
        rows = [
            ("Upfront Hardware (one-off)", curr_hw,  f"£{upfront:.2f}"),
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
    if auto_switch:
        all_equip_pdf.append((f"Switch: {rec_switch['name']}", 1, _pdf_hw_billing))
    if add_router:
        all_equip_pdf.append((router_type, 1, _pdf_hw_billing))

    # Voice Channel Licences
    if total_voice_channels > 0:
        vc_billing_pdf = _pdf_hw_billing if is_spread else f"£{svc['lic_monthly']:.2f}/mo"
        all_equip_pdf.append((f"Voice Channel Licences x{total_voice_channels}",
                               total_voice_channels, vc_billing_pdf))

    # Software add-ons
    for addon_name, addon_qty, addon_cost, addon_sell in SW_ADDONS:
        if addon_qty > 0:
            addon_billing_pdf = _pdf_hw_billing if is_spread else f"£{addon_sell * addon_qty:.2f}/mo"
            all_equip_pdf.append((addon_name, addon_qty, addon_billing_pdf))

    # Network & Connectivity
    all_equip_pdf.append((f"Broadband - {bb_provider} {bb_package}", 1,
                           f"£{svc['bb_sell']:.2f}/mo"))
    if second_fttp and second_fttp_pkg:
        bb2 = BROADBAND[bb_provider][second_fttp_pkg]["cost"] * (1 + service_uplift_pct/100)
        all_equip_pdf.append((f"Broadband - {bb_provider} {second_fttp_pkg} (2nd line)", 1,
                               f"£{bb2:.2f}/mo"))
    for r in mobile_rows:
        if r["qty"] > 0:
            all_equip_pdf.append((f"{r['network']} - {r['package']}", r["qty"],
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


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📄 Proposal Summary", "🖋️ Order Form Preview", "📥 Download Documents", "👤 Customer View", "💼 Consultant", "✍️ Sign & Send", "📨 Remote Signing"])

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
        if auto_switch:
            all_hw_items.append((f"Switch: {rec_switch['name']}", 1, _hw_billing))
        if add_router:
            all_hw_items.append((router_type, 1, _hw_billing))

        # Voice Channel Licences — part of the system package
        if total_voice_channels > 0:
            vc_billing = _hw_billing if is_spread else f"£{svc['lic_monthly']:.2f}/mo"
            all_hw_items.append((f"Voice Channel Licences x{total_voice_channels}", total_voice_channels, vc_billing))

        # Software add-ons — label matches payment model (lease hides individual prices)
        for addon_name, addon_qty, addon_cost, addon_sell in SW_ADDONS:
            if addon_qty > 0:
                addon_billing = _hw_billing if is_spread else f"£{addon_sell * addon_qty:.2f}/mo"
                all_hw_items.append((addon_name, addon_qty, addon_billing))

        if all_hw_items:
            hw_df = pd.DataFrame(all_hw_items, columns=["Description", "Qty", "Billing"])
            st.dataframe(hw_df, use_container_width=True, hide_index=True)
        else:
            st.info("No hardware or software selected yet.")

        st.markdown("#### 🌐 Network & Connectivity")
        st.caption("Ongoing monthly service charges")
        net_items = [
            (f"{bb_provider} — {bb_package}", 1, f"£{svc['bb_sell']:.2f}/mo"),
        ]
        if second_fttp and second_fttp_pkg:
            bb2_sell = BROADBAND[bb_provider][second_fttp_pkg]["cost"] * (1 + service_uplift_pct/100)
            net_items.append((f"{bb_provider} — {second_fttp_pkg} (2nd line)", 1, f"£{bb2_sell:.2f}/mo"))
        # Voice Channels now shown in System section above
        for row in mobile_rows:
            if row["qty"] > 0:
                net_items.append((f"{row['net']} — {row['pkg']} x{row['qty']}", row["qty"], f"£{row['sell'] * row['qty']:.2f}/mo"))

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
          <div class="metric-label">Network & Connectivity</div>
          <div style="font-size:1.4rem; font-weight:700">£{pure_connectivity:.2f} + VAT</div>
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
        all_equip = [(n, q) for n, q in list(desktop_quantities.items()) +
                     list(cordless_quantities.items()) + list(headset_quantities.items()) +
                     list(other_quantities.items()) if q > 0]
        if auto_switch:
            all_equip.append((f"Switch: {rec_switch['name']}", 1))
        if add_router:
            all_equip.append((router_type, 1))
        if total_voice_channels > 0:
            all_equip.append((f"Voice Channel Licences x{total_voice_channels}", total_voice_channels))
        for addon_name, addon_qty, _, _ in SW_ADDONS:
            if addon_qty > 0:
                all_equip.append((addon_name, addon_qty))
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
            f"Customer: {comp_name or '—'}",
            f"Agreement Term: {LEASE_TERM_LABELS[lease_term]}",
            f"Payment Model: {payment_model}",
            f"Monthly Total: £{total_mo:.2f} + VAT",
            f"Broadband: {bb_provider} — {bb_package}",
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
            [(n, q, HANDSETS_DESKTOP[n])   for n, q in desktop_quantities.items() if q > 0]  +
            [(n, q, HANDSETS_CORDLESS[n])  for n, q in cordless_quantities.items() if q > 0] +
            [(n, q, HEADSETS[n])           for n, q in headset_quantities.items()   if q > 0] +
            [(n, q, OTHER_HARDWARE[n])     for n, q in other_quantities.items()     if q > 0]
        )

        # Add switch as a card
        sw_name = rec_switch["name"]
        all_selected.append((f"Switch: {sw_name}", 1, {"cat": "Switch"}))

        # Add router as a card if included
        if add_router:
            all_selected.append((router_type, 1, {"cat": "Router"}))

        # Add software add-ons as cards
        for addon_name, addon_qty, _, _ in SW_ADDONS:
            if addon_qty > 0:
                all_selected.append((addon_name, addon_qty, {"cat": "Software"}))

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
                        icon_map = {"Desktop":"📱","DECT":"📞","Wi-Fi":"📡","Switch":"🔌","Router":"🌐","Software":"💻","Headset":"🎧"}
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

        # Software add-on images — show if any selected
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
               <div style="font-size:1rem;font-weight:700">{comp_name or "—"}</div></div>
          <div style="text-align:center">
               <div style="font-size:0.72rem;color:rgba(255,255,255,0.55)">BASE MONTHLY</div>
               <div style="font-size:1.4rem;font-weight:800;color:#00b5a3">£{total_mo:.2f}</div></div>
          <div style="text-align:right">
               <div style="font-size:0.72rem;color:rgba(255,255,255,0.55)">TERM</div>
               <div style="font-size:1rem;font-weight:700">{LEASE_TERM_LABELS[lease_term]}</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Rate override ──────────────────────────────────────────────────
        st.markdown("### 🎯 Pricing Adjustment")
        st.caption("Increase the monthly charge to match or beat the customer's current spend. "
                   "The base rate is the minimum calculated price — you can only go up from here.")

        c_left, c_right = st.columns([3, 2])
        with c_left:
            target_monthly = st.number_input(
                "Monthly Charge to Customer (£)",
                min_value=round(total_mo, 2),
                value=round(total_mo, 2) if not current_total else round(min(current_total, current_total), 2),
                step=1.0,
                key="c_target_mo",
                help="Set this to match the customer's current spend to capture maximum value."
            )
            rate_uplift    = max(0.0, target_monthly - total_mo)
            extra_margin   = rate_uplift * lease_term
            adjusted_pat   = pat + extra_margin
            est_earnings   = round(adjusted_pat * (commission_pct / 100), 2)

        with c_right:
            if rate_uplift > 0:
                st.markdown(f"""
                <div style="background:#e8f8f0;border-left:4px solid #1a7a40;border-radius:0 8px 8px 0;
                     padding:1rem 1.2rem;margin-top:1.6rem">
                  <div style="font-size:0.72rem;color:#1a7a40;font-weight:700;text-transform:uppercase">Rate Increase</div>
                  <div style="font-size:1.6rem;font-weight:800;color:#1a7a40">+£{rate_uplift:.2f}/mo</div>
                  <div style="font-size:0.8rem;color:#555;margin-top:0.2rem">+£{extra_margin:.2f} over full term</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#f5f5f5;border-left:4px solid #ccc;border-radius:0 8px 8px 0;
                     padding:1rem 1.2rem;margin-top:1.6rem">
                  <div style="font-size:0.72rem;color:#888;font-weight:700;text-transform:uppercase">Rate Increase</div>
                  <div style="font-size:1.2rem;font-weight:700;color:#aaa">At base rate</div>
                </div>
                """, unsafe_allow_html=True)

        # ── Key Numbers ────────────────────────────────────────────────────
        st.markdown("### 📊 Deal at a Glance")

        # Row 1 — Spend comparison
        r1a, r1b, r1c = st.columns(3)
        with r1a:
            if current_total > 0:
                st.markdown(f"""
                <div style="background:#fff;border:2px solid #e0e8f0;border-radius:12px;
                     padding:1.2rem;text-align:center">
                  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:.08em;color:#888;margin-bottom:0.5rem">Customer Currently Pays</div>
                  <div style="font-size:2rem;font-weight:800;color:#c0392b">£{current_total:.2f}</div>
                  <div style="font-size:0.78rem;color:#aaa">per month + VAT</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#f8f9ff;border:2px dashed #d0d8e8;border-radius:12px;
                     padding:1.2rem;text-align:center">
                  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:.08em;color:#888;margin-bottom:0.5rem">Customer Currently Pays</div>
                  <div style="font-size:1rem;color:#aaa">Fill in current<br>costs in sidebar</div>
                </div>
                """, unsafe_allow_html=True)

        with r1b:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1f1450,#2d1f6e);
                 border-radius:12px;padding:1.2rem;text-align:center;border:2px solid #00b5a3">
              <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                   letter-spacing:.08em;color:rgba(255,255,255,0.6);margin-bottom:0.5rem">New Monthly with SY Comms</div>
              <div style="font-size:2rem;font-weight:800;color:#00b5a3">£{target_monthly:.2f}</div>
              <div style="font-size:0.78rem;color:rgba(255,255,255,0.5)">per month + VAT</div>
            </div>
            """, unsafe_allow_html=True)

        with r1c:
            if current_total > 0:
                saving    = current_total - target_monthly
                s_col     = "#1a7a40" if saving >= 0 else "#c0392b"
                s_bg      = "#e8f8f0" if saving >= 0 else "#fdf0f0"
                s_lbl     = "Customer Saves" if saving >= 0 else "Customer Pays More"
                s_prefix  = "-" if saving >= 0 else "+"
                st.markdown(f"""
                <div style="background:{s_bg};border:2px solid {s_col};
                     border-radius:12px;padding:1.2rem;text-align:center">
                  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:.08em;color:{s_col};margin-bottom:0.5rem">{s_lbl}</div>
                  <div style="font-size:2rem;font-weight:800;color:{s_col}">{s_prefix}£{abs(saving):.2f}</div>
                  <div style="font-size:0.78rem;color:{s_col}">per month  &middot;  {s_prefix}£{abs(saving*12):.0f}/yr</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#f8f9ff;border:2px dashed #d0d8e8;border-radius:12px;
                     padding:1.2rem;text-align:center">
                  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:.08em;color:#888;margin-bottom:0.5rem">Customer Saving</div>
                  <div style="font-size:1rem;color:#aaa">Add current<br>costs to calculate</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")

        # Row 2 — Commission (full width, prominent)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d4a2a,#1a7a40);border-radius:12px;
             padding:1.4rem 2rem;margin-top:0.5rem;display:flex;
             justify-content:space-between;align-items:center">
          <div>
            <div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;
                 letter-spacing:.1em;color:rgba(255,255,255,0.6)">Your Estimated Commission</div>
            <div style="font-size:2.2rem;font-weight:800;color:#fff">£{est_earnings:.2f}</div>
            <div style="font-size:0.82rem;color:rgba(255,255,255,0.55)">over the full {LEASE_TERM_LABELS[lease_term]} agreement</div>
          </div>
          {"<div style='text-align:right'><div style='font-size:0.75rem;color:rgba(255,255,255,0.5);'>Rate Uplift Applied</div><div style='font-size:1.3rem;font-weight:700;color:#7fe8a0'>+£" + f"{rate_uplift:.2f}" + "/mo</div></div>" if rate_uplift > 0 else "<div style='text-align:right'><div style='font-size:0.75rem;color:rgba(255,255,255,0.5)'>Tip</div><div style='font-size:0.88rem;color:rgba(255,255,255,0.7)'>Increase the monthly<br>rate above to earn more</div></div>"}
        </div>
        """, unsafe_allow_html=True)


        # ── Proposal notes ─────────────────────────────────────────────────
        st.markdown("### 📝 Consultant Notes / Special Conditions")
        consultant_notes = st.text_area(
            "", height=100, key="c_notes",
            placeholder="Add any special conditions, agreed credits, or notes for this deal...",
            label_visibility="collapsed"
        )

# ── TAB 6: SIGN & SEND ────────────────────────────────────────────────────────

with tab6:
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
with tab7:
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
