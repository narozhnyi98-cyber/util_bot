import logging
from datetime import datetime

from services.currency import get_eur_rate

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# БАЗА АВТОМОБИЛЕЙ (ДВС + ЭЛЕКТРО + ГИБРИДЫ)
# engine_type: "ICE" — ДВС, "EV" — электро, "HEV" — гибрид
# ─────────────────────────────────────────────────────────────
CARS = [
    # ── TOYOTA (ICE) ──
    {"id":1,"make":"Toyota","model":"Corolla","country":"Япония","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":122,"price_foreign_rub":1250000,"engine_type":"ICE"},
    {"id":2,"make":"Toyota","model":"Camry","country":"Япония","body_type":"Седан","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":181,"price_foreign_rub":1850000,"engine_type":"ICE"},
    {"id":3,"make":"Toyota","model":"RAV4","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":149,"price_foreign_rub":1950000,"engine_type":"ICE"},
    {"id":4,"make":"Toyota","model":"Land Cruiser Prado","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2800,"engine_power_hp":177,"price_foreign_rub":3800000,"engine_type":"ICE"},
    {"id":5,"make":"Toyota","model":"Highlander","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":249,"price_foreign_rub":3500000,"engine_type":"ICE"},
    {"id":6,"make":"Toyota","model":"Yaris","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1500,"engine_power_hp":120,"price_foreign_rub":1100000,"engine_type":"ICE"},
    {"id":7,"make":"Toyota","model":"Alphard","country":"Япония","body_type":"Универсал","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":182,"price_foreign_rub":4000000,"engine_type":"ICE"},
    {"id":8,"make":"Toyota","model":"Vitz","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1000,"engine_power_hp":69,"price_foreign_rub":800000,"engine_type":"ICE"},
    {"id":9,"make":"Toyota","model":"Aqua","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1500,"engine_power_hp":74,"price_foreign_rub":900000,"engine_type":"ICE"},
    {"id":10,"make":"Toyota","model":"C-HR","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1200,"engine_power_hp":116,"price_foreign_rub":1800000,"engine_type":"ICE"},
    {"id":11,"make":"Toyota","model":"Prius","country":"Япония","body_type":"Хэтчбек","year_from":2020,"engine_volume_cc":1800,"engine_power_hp":98,"price_foreign_rub":1200000,"engine_type":"ICE"},

    # ── HONDA (ICE) ──
    {"id":12,"make":"Honda","model":"Vezel","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1500,"engine_power_hp":131,"price_foreign_rub":1300000,"engine_type":"ICE"},
    {"id":13,"make":"Honda","model":"CR-V","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1500,"engine_power_hp":193,"price_foreign_rub":2100000,"engine_type":"ICE"},
    {"id":14,"make":"Honda","model":"Fit","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1300,"engine_power_hp":98,"price_foreign_rub":950000,"engine_type":"ICE"},
    {"id":15,"make":"Honda","model":"Stepwgn","country":"Япония","body_type":"Универсал","year_from":2020,"engine_volume_cc":1500,"engine_power_hp":150,"price_foreign_rub":1800000,"engine_type":"ICE"},
    {"id":16,"make":"Honda","model":"Civic","country":"Япония","body_type":"Седан","year_from":2020,"engine_volume_cc":1500,"engine_power_hp":182,"price_foreign_rub":1700000,"engine_type":"ICE"},

    # ── NISSAN (ICE) ──
    {"id":17,"make":"Nissan","model":"X-Trail","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":149,"price_foreign_rub":1800000,"engine_type":"ICE"},
    {"id":18,"make":"Nissan","model":"Qashqai","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1300,"engine_power_hp":140,"price_foreign_rub":1450000,"engine_type":"ICE"},
    {"id":19,"make":"Nissan","model":"Note","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1200,"engine_power_hp":79,"price_foreign_rub":900000,"engine_type":"ICE"},
    {"id":20,"make":"Nissan","model":"Serena","country":"Япония","body_type":"Универсал","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1700000,"engine_type":"ICE"},
    {"id":21,"make":"Nissan","model":"Teana","country":"Япония","body_type":"Седан","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":173,"price_foreign_rub":1500000,"engine_type":"ICE"},
    {"id":22,"make":"Nissan","model":"Murano","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":170,"price_foreign_rub":2300000,"engine_type":"ICE"},

    # ── MAZDA (ICE) ──
    {"id":23,"make":"Mazda","model":"CX-5","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1750000,"engine_type":"ICE"},
    {"id":24,"make":"Mazda","model":"CX-9","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":231,"price_foreign_rub":2800000,"engine_type":"ICE"},
    {"id":25,"make":"Mazda","model":"CX-30","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1900000,"engine_type":"ICE"},
    {"id":26,"make":"Mazda","model":"3","country":"Япония","body_type":"Седан","year_from":2020,"engine_volume_cc":1500,"engine_power_hp":120,"price_foreign_rub":1400000,"engine_type":"ICE"},
    {"id":27,"make":"Mazda","model":"6","country":"Япония","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1600000,"engine_type":"ICE"},

    # ── HYUNDAI (ICE) ──
    {"id":28,"make":"Hyundai","model":"Elantra","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":128,"price_foreign_rub":1350000,"engine_type":"ICE"},
    {"id":29,"make":"Hyundai","model":"Tucson","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1850000,"engine_type":"ICE"},
    {"id":30,"make":"Hyundai","model":"Santa Fe","country":"Корея","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2200,"engine_power_hp":200,"price_foreign_rub":2300000,"engine_type":"ICE"},
    {"id":31,"make":"Hyundai","model":"Solaris","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":123,"price_foreign_rub":1150000,"engine_type":"ICE"},
    {"id":32,"make":"Hyundai","model":"i10","country":"Корея","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1200,"engine_power_hp":84,"price_foreign_rub":850000,"engine_type":"ICE"},
    {"id":33,"make":"Hyundai","model":"Palisade","country":"Корея","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2200,"engine_power_hp":200,"price_foreign_rub":3200000,"engine_type":"ICE"},
    {"id":34,"make":"Hyundai","model":"Creta","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":123,"price_foreign_rub":1400000,"engine_type":"ICE"},
    {"id":35,"make":"Hyundai","model":"Staria","country":"Корея","body_type":"Универсал","year_from":2021,"engine_volume_cc":2200,"engine_power_hp":177,"price_foreign_rub":2200000,"engine_type":"ICE"},

    # ── KIA (ICE) ──
    {"id":36,"make":"Kia","model":"K5","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1650000,"engine_type":"ICE"},
    {"id":37,"make":"Kia","model":"Sportage","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1750000,"engine_type":"ICE"},
    {"id":38,"make":"Kia","model":"Sorento","country":"Корея","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2200,"engine_power_hp":200,"price_foreign_rub":2200000,"engine_type":"ICE"},
    {"id":39,"make":"Kia","model":"Rio","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":123,"price_foreign_rub":1100000,"engine_type":"ICE"},
    {"id":40,"make":"Kia","model":"Picanto","country":"Корея","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1200,"engine_power_hp":84,"price_foreign_rub":800000,"engine_type":"ICE"},
    {"id":41,"make":"Kia","model":"K8","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":198,"price_foreign_rub":2100000,"engine_type":"ICE"},
    {"id":42,"make":"Kia","model":"Carnival","country":"Корея","body_type":"Универсал","year_from":2020,"engine_volume_cc":2200,"engine_power_hp":200,"price_foreign_rub":2400000,"engine_type":"ICE"},
    {"id":43,"make":"Kia","model":"Seltos","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":121,"price_foreign_rub":1500000,"engine_type":"ICE"},

    # ── BMW (ICE) ──
    {"id":44,"make":"BMW","model":"3 series","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":184,"price_foreign_rub":2500000,"engine_type":"ICE"},
    {"id":45,"make":"BMW","model":"X3","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":184,"price_foreign_rub":2800000,"engine_type":"ICE"},
    {"id":46,"make":"BMW","model":"X1","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":192,"price_foreign_rub":2500000,"engine_type":"ICE"},
    {"id":47,"make":"BMW","model":"5 series","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":249,"price_foreign_rub":3200000,"engine_type":"ICE"},
    {"id":48,"make":"BMW","model":"X5","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3000,"engine_power_hp":340,"price_foreign_rub":4500000,"engine_type":"ICE"},

    # ── MERCEDES (ICE) ──
    {"id":49,"make":"Mercedes","model":"C-class","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":184,"price_foreign_rub":2600000,"engine_type":"ICE"},
    {"id":50,"make":"Mercedes","model":"E-class","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":197,"price_foreign_rub":3000000,"engine_type":"ICE"},
    {"id":51,"make":"Mercedes","model":"GLE","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":245,"price_foreign_rub":3800000,"engine_type":"ICE"},
    {"id":52,"make":"Mercedes","model":"GLC","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":197,"price_foreign_rub":3200000,"engine_type":"ICE"},

    # ── AUDI (ICE) ──
    {"id":53,"make":"Audi","model":"Q5","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":190,"price_foreign_rub":2900000,"engine_type":"ICE"},
    {"id":54,"make":"Audi","model":"A4","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":190,"price_foreign_rub":2400000,"engine_type":"ICE"},
    {"id":55,"make":"Audi","model":"A6","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":249,"price_foreign_rub":3000000,"engine_type":"ICE"},
    {"id":56,"make":"Audi","model":"Q7","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3000,"engine_power_hp":340,"price_foreign_rub":4500000,"engine_type":"ICE"},

    # ── VOLKSWAGEN (ICE) ──
    {"id":57,"make":"Volkswagen","model":"Tiguan","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":150,"price_foreign_rub":1850000,"engine_type":"ICE"},
    {"id":58,"make":"Volkswagen","model":"Passat","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":1800,"engine_power_hp":180,"price_foreign_rub":1700000,"engine_type":"ICE"},
    {"id":59,"make":"Volkswagen","model":"Polo","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":125,"price_foreign_rub":1200000,"engine_type":"ICE"},
    {"id":60,"make":"Volkswagen","model":"Golf","country":"Европа","body_type":"Хэтчбек","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":150,"price_foreign_rub":1600000,"engine_type":"ICE"},
    {"id":61,"make":"Volkswagen","model":"Touareg","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3000,"engine_power_hp":249,"price_foreign_rub":4000000,"engine_type":"ICE"},

    # ── SKODA (ICE) ──
    {"id":62,"make":"Skoda","model":"Octavia","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":150,"price_foreign_rub":1500000,"engine_type":"ICE"},
    {"id":63,"make":"Skoda","model":"Superb","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":190,"price_foreign_rub":1800000,"engine_type":"ICE"},
    {"id":64,"make":"Skoda","model":"Fabia","country":"Европа","body_type":"Хэтчбек","year_from":2020,"engine_volume_cc":1200,"engine_power_hp":110,"price_foreign_rub":1100000,"engine_type":"ICE"},
    {"id":65,"make":"Skoda","model":"Kodiaq","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1400,"engine_power_hp":150,"price_foreign_rub":2000000,"engine_type":"ICE"},

    # ── CHERY (ICE) ──
    {"id":66,"make":"Chery","model":"Tiggo 2","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":113,"price_foreign_rub":900000,"engine_type":"ICE"},
    {"id":67,"make":"Chery","model":"Tiggo 4","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1150000,"engine_type":"ICE"},
    {"id":68,"make":"Chery","model":"Tiggo 7 Pro","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1550000,"engine_type":"ICE"},
    {"id":69,"make":"Chery","model":"Tiggo 8 Pro","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1600,"engine_power_hp":186,"price_foreign_rub":1800000,"engine_type":"ICE"},
    {"id":70,"make":"Chery","model":"Arrizo 8","country":"Китай","body_type":"Седан","year_from":2022,"engine_volume_cc":1600,"engine_power_hp":186,"price_foreign_rub":1600000,"engine_type":"ICE"},
    {"id":71,"make":"Chery","model":"Tiggo 8","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1600000,"engine_type":"ICE"},

    # ── HAVAL (ICE) ──
    {"id":72,"make":"Haval","model":"Jolion","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":143,"price_foreign_rub":1350000,"engine_type":"ICE"},
    {"id":73,"make":"Haval","model":"F7","country":"Китай","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":190,"price_foreign_rub":1600000,"engine_type":"ICE"},
    {"id":74,"make":"Haval","model":"Dargo","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":190,"price_foreign_rub":1800000,"engine_type":"ICE"},
    {"id":75,"make":"Haval","model":"H9","country":"Китай","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":218,"price_foreign_rub":2500000,"engine_type":"ICE"},
    {"id":76,"make":"Haval","model":"H6","country":"Китай","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2000,"engine_power_hp":190,"price_foreign_rub":1700000,"engine_type":"ICE"},

    # ── GEELY (ICE) ──
    {"id":77,"make":"Geely","model":"Coolray","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":177,"price_foreign_rub":1450000,"engine_type":"ICE"},
    {"id":78,"make":"Geely","model":"Monjaro","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":238,"price_foreign_rub":2300000,"engine_type":"ICE"},
    {"id":79,"make":"Geely","model":"Tugella","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":238,"price_foreign_rub":2100000,"engine_type":"ICE"},
    {"id":80,"make":"Geely","model":"Atlas","country":"Китай","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2400,"engine_power_hp":148,"price_foreign_rub":1500000,"engine_type":"ICE"},
    {"id":81,"make":"Geely","model":"Emgrand","country":"Китай","body_type":"Седан","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":122,"price_foreign_rub":1100000,"engine_type":"ICE"},

    # ── EXEED (ICE) ──
    {"id":82,"make":"Exeed","model":"TXL","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":197,"price_foreign_rub":2050000,"engine_type":"ICE"},
    {"id":83,"make":"Exeed","model":"LX","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1600,"engine_power_hp":186,"price_foreign_rub":1900000,"engine_type":"ICE"},
    {"id":84,"make":"Exeed","model":"VX","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":249,"price_foreign_rub":2500000,"engine_type":"ICE"},
    {"id":85,"make":"Exeed","model":"RX","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":249,"price_foreign_rub":2300000,"engine_type":"ICE"},

    # ── CHANGAN (ICE) ──
    {"id":86,"make":"Changan","model":"UNI-K","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":2000,"engine_power_hp":226,"price_foreign_rub":2000000,"engine_type":"ICE"},
    {"id":87,"make":"Changan","model":"UNI-T","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":180,"price_foreign_rub":1400000,"engine_type":"ICE"},
    {"id":88,"make":"Changan","model":"CS35 Plus","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1400,"engine_power_hp":149,"price_foreign_rub":1100000,"engine_type":"ICE"},
    {"id":89,"make":"Changan","model":"CS55 Plus","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":181,"price_foreign_rub":1500000,"engine_type":"ICE"},

    # ── GENESIS (ICE) ──
    {"id":90,"make":"Genesis","model":"GV70","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":249,"price_foreign_rub":3200000,"engine_type":"ICE"},
    {"id":91,"make":"Genesis","model":"G80","country":"Корея","body_type":"Седан","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":249,"price_foreign_rub":3300000,"engine_type":"ICE"},
    {"id":92,"make":"Genesis","model":"GV80","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":249,"price_foreign_rub":3800000,"engine_type":"ICE"},

    # ── LEXUS (ICE) ──
    {"id":93,"make":"Lexus","model":"RX","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3500,"engine_power_hp":300,"price_foreign_rub":4200000,"engine_type":"ICE"},
    {"id":94,"make":"Lexus","model":"NX","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":2500,"engine_power_hp":239,"price_foreign_rub":3800000,"engine_type":"ICE"},
    {"id":95,"make":"Lexus","model":"ES","country":"Япония","body_type":"Седан","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":200,"price_foreign_rub":3200000,"engine_type":"ICE"},
    {"id":96,"make":"Lexus","model":"GX","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":4000,"engine_power_hp":249,"price_foreign_rub":5000000,"engine_type":"ICE"},
    {"id":97,"make":"Lexus","model":"LX","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3500,"engine_power_hp":415,"price_foreign_rub":8000000,"engine_type":"ICE"},

    # ── SUBARU (ICE) ──
    {"id":98,"make":"Subaru","model":"Forester","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":185,"price_foreign_rub":2100000,"engine_type":"ICE"},
    {"id":99,"make":"Subaru","model":"Outback","country":"Япония","body_type":"Универсал","year_from":2020,"engine_volume_cc":2500,"engine_power_hp":175,"price_foreign_rub":2400000,"engine_type":"ICE"},
    {"id":100,"make":"Subaru","model":"XV","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1800000,"engine_type":"ICE"},

    # ── SUZUKI (ICE) ──
    {"id":101,"make":"Suzuki","model":"Swift","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":1200,"engine_power_hp":83,"price_foreign_rub":1000000,"engine_type":"ICE"},
    {"id":102,"make":"Suzuki","model":"Alto","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":660,"engine_power_hp":64,"price_foreign_rub":620000,"engine_type":"ICE"},
    {"id":103,"make":"Suzuki","model":"Vitara","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1600,"engine_power_hp":117,"price_foreign_rub":1500000,"engine_type":"ICE"},
    {"id":104,"make":"Suzuki","model":"Jimny","country":"Япония","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1500,"engine_power_hp":102,"price_foreign_rub":1700000,"engine_type":"ICE"},

    # ── DAIHATSU (ICE) ──
    {"id":105,"make":"Daihatsu","model":"Mira","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":660,"engine_power_hp":64,"price_foreign_rub":600000,"engine_type":"ICE"},
    {"id":106,"make":"Daihatsu","model":"Tanto","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":660,"engine_power_hp":64,"price_foreign_rub":700000,"engine_type":"ICE"},
    {"id":107,"make":"Daihatsu","model":"Move","country":"Япония","body_type":"Хэтчбек","year_from":2021,"engine_volume_cc":660,"engine_power_hp":64,"price_foreign_rub":650000,"engine_type":"ICE"},

    # ── LAND ROVER (ICE) ──
    {"id":108,"make":"Land Rover","model":"Range Rover","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3000,"engine_power_hp":400,"price_foreign_rub":5500000,"engine_type":"ICE"},
    {"id":109,"make":"Land Rover","model":"Discovery","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3000,"engine_power_hp":249,"price_foreign_rub":4500000,"engine_type":"ICE"},
    {"id":110,"make":"Land Rover","model":"Defender","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3000,"engine_power_hp":400,"price_foreign_rub":5500000,"engine_type":"ICE"},

    # ── VOLVO (ICE) ──
    {"id":111,"make":"Volvo","model":"XC60","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":250,"price_foreign_rub":2900000,"engine_type":"ICE"},
    {"id":112,"make":"Volvo","model":"XC90","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":250,"price_foreign_rub":4200000,"engine_type":"ICE"},
    {"id":113,"make":"Volvo","model":"S60","country":"Европа","body_type":"Седан","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":250,"price_foreign_rub":2600000,"engine_type":"ICE"},

    # ── JETOUR (ICE) ──
    {"id":114,"make":"Jetour","model":"X70","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1500000,"engine_type":"ICE"},
    {"id":115,"make":"Jetour","model":"X90","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1600,"engine_power_hp":190,"price_foreign_rub":1800000,"engine_type":"ICE"},
    {"id":116,"make":"Jetour","model":"Dashing","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1600000,"engine_type":"ICE"},

    # ── OMODA (ICE) ──
    {"id":117,"make":"Omoda","model":"C5","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1500000,"engine_type":"ICE"},
    {"id":118,"make":"Omoda","model":"S5","country":"Китай","body_type":"Седан","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":147,"price_foreign_rub":1400000,"engine_type":"ICE"},

    # ── INFINITI (ICE) ──
    {"id":119,"make":"Infiniti","model":"QX50","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":249,"price_foreign_rub":3200000,"engine_type":"ICE"},
    {"id":120,"make":"Infiniti","model":"QX60","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3500,"engine_power_hp":295,"price_foreign_rub":4000000,"engine_type":"ICE"},
    {"id":121,"make":"Infiniti","model":"QX80","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":5600,"engine_power_hp":405,"price_foreign_rub":6500000,"engine_type":"ICE"},

    # ── RENAULT (ICE) ──
    {"id":122,"make":"Renault","model":"Arkana","country":"Корея","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":1600,"engine_power_hp":150,"price_foreign_rub":1600000,"engine_type":"ICE"},
    {"id":123,"make":"Renault","model":"Duster","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1300,"engine_power_hp":150,"price_foreign_rub":1400000,"engine_type":"ICE"},
    {"id":124,"make":"Renault","model":"Kaptur","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1300,"engine_power_hp":150,"price_foreign_rub":1500000,"engine_type":"ICE"},

    # ── MITSUBISHI (ICE) ──
    {"id":125,"make":"Mitsubishi","model":"Outlander","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":2000,"engine_power_hp":150,"price_foreign_rub":1800000,"engine_type":"ICE"},
    {"id":126,"make":"Mitsubishi","model":"Pajero","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3000,"engine_power_hp":174,"price_foreign_rub":2500000,"engine_type":"ICE"},
    {"id":127,"make":"Mitsubishi","model":"ASX","country":"Япония","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":1600,"engine_power_hp":117,"price_foreign_rub":1400000,"engine_type":"ICE"},
    {"id":128,"make":"Mitsubishi","model":"L200","country":"Япония","body_type":"Универсал","year_from":2020,"engine_volume_cc":2400,"engine_power_hp":181,"price_foreign_rub":2400000,"engine_type":"ICE"},

    # ── JEEP (ICE) ──
    {"id":129,"make":"Jeep","model":"Grand Cherokee","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3600,"engine_power_hp":286,"price_foreign_rub":4000000,"engine_type":"ICE"},
    {"id":130,"make":"Jeep","model":"Wrangler","country":"Европа","body_type":"Кроссовер","year_from":2020,"engine_volume_cc":3600,"engine_power_hp":284,"price_foreign_rub":4500000,"engine_type":"ICE"},

    # ── ⚡ ЭЛЕКТРОМОБИЛИ (EV) ──
    {"id":200,"make":"Nissan","model":"Leaf","country":"Япония","body_type":"Хэтчбек","year_from":2020,"engine_volume_cc":0,"engine_power_hp":150,"price_foreign_rub":1100000,"engine_type":"EV"},
    {"id":201,"make":"Zeekr","model":"001","country":"Китай","body_type":"Седан","year_from":2022,"engine_volume_cc":0,"engine_power_hp":544,"price_foreign_rub":4200000,"engine_type":"EV"},
    {"id":202,"make":"Tesla","model":"Model 3","country":"Европа","body_type":"Седан","year_from":2021,"engine_volume_cc":0,"engine_power_hp":283,"price_foreign_rub":3500000,"engine_type":"EV"},
    {"id":203,"make":"Tesla","model":"Model Y","country":"Европа","body_type":"Кроссовер","year_from":2021,"engine_volume_cc":0,"engine_power_hp":331,"price_foreign_rub":4200000,"engine_type":"EV"},
    {"id":204,"make":"Hongqi","model":"E-HS9","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":0,"engine_power_hp":551,"price_foreign_rub":5500000,"engine_type":"EV"},
    {"id":205,"make":"Avatr","model":"11","country":"Китай","body_type":"Кроссовер","year_from":2023,"engine_volume_cc":0,"engine_power_hp":578,"price_foreign_rub":5800000,"engine_type":"EV"},
    {"id":206,"make":"Avatr","model":"12","country":"Китай","body_type":"Седан","year_from":2023,"engine_volume_cc":0,"engine_power_hp":578,"price_foreign_rub":6000000,"engine_type":"EV"},
    {"id":207,"make":"Geely","model":"EX5","country":"Китай","body_type":"Кроссовер","year_from":2023,"engine_volume_cc":0,"engine_power_hp":218,"price_foreign_rub":3500000,"engine_type":"EV"},
    {"id":208,"make":"Evolute","model":"i-Joy","country":"Китай","body_type":"Кроссовер","year_from":2023,"engine_volume_cc":0,"engine_power_hp":163,"price_foreign_rub":2500000,"engine_type":"EV"},

    # ── 🔌 ГИБРИДЫ (HEV) ──
    {"id":220,"make":"Voyah","model":"Free","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1500,"engine_power_hp":694,"price_foreign_rub":4000000,"engine_type":"HEV"},
    {"id":221,"make":"Li Auto","model":"L7","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1496,"engine_power_hp":449,"price_foreign_rub":4500000,"engine_type":"HEV"},
    {"id":222,"make":"Li Auto","model":"L9","country":"Китай","body_type":"Кроссовер","year_from":2022,"engine_volume_cc":1496,"engine_power_hp":449,"price_foreign_rub":5500000,"engine_type":"HEV"},
    {"id":223,"make":"Li Auto","model":"L6","country":"Китай","body_type":"Кроссовер","year_from":2023,"engine_volume_cc":1496,"engine_power_hp":408,"price_foreign_rub":3800000,"engine_type":"HEV"},
    {"id":224,"make":"Zeekr","model":"9X","country":"Китай","body_type":"Кроссовер","year_from":2024,"engine_volume_cc":1974,"engine_power_hp":789,"price_foreign_rub":9500000,"engine_type":"HEV"},
    {"id":225,"make":"Lynk & Co","model":"900","country":"Китай","body_type":"Кроссовер","year_from":2023,"engine_volume_cc":1974,"engine_power_hp":544,"price_foreign_rub":6500000,"engine_type":"HEV"},
    {"id":226,"make":"Geely","model":"EX5 EM-i","country":"Китай","body_type":"Кроссовер","year_from":2023,"engine_volume_cc":1498,"engine_power_hp":218,"price_foreign_rub":3200000,"engine_type":"HEV"},
]


# ─────────────────────────────────────────────────────────────
# ЦЕНЫ В РФ
# ─────────────────────────────────────────────────────────────
RF_PRICES = {
    # Toyota
    "Toyota|Corolla": 1850000, "Toyota|Camry": 3800000, "Toyota|RAV4": 2750000,
    "Toyota|Land Cruiser Prado": 4500000, "Toyota|Highlander": 4500000,
    "Toyota|Yaris": 1500000, "Toyota|Alphard": 6000000, "Toyota|Vitz": 1100000,
    "Toyota|Aqua": 1300000, "Toyota|C-HR": 2300000, "Toyota|Prius": 1700000,
    # Honda
    "Honda|Vezel": 1900000, "Honda|CR-V": 2600000, "Honda|Fit": 1350000,
    "Honda|Stepwgn": 2400000, "Honda|Civic": 2200000,
    # Nissan
    "Nissan|X-Trail": 2500000, "Nissan|Qashqai": 2200000, "Nissan|Note": 1250000,
    "Nissan|Serena": 2300000, "Nissan|Teana": 2000000, "Nissan|Murano": 2900000,
    # Mazda
    "Mazda|CX-5": 2800000, "Mazda|CX-9": 3500000, "Mazda|CX-30": 2500000,
    "Mazda|3": 1800000, "Mazda|6": 2100000,
    # Hyundai
    "Hyundai|Elantra": 1950000, "Hyundai|Tucson": 2850000, "Hyundai|Santa Fe": 2850000,
    "Hyundai|Solaris": 1600000, "Hyundai|i10": 1200000, "Hyundai|Palisade": 4200000,
    "Hyundai|Creta": 1900000, "Hyundai|Staria": 3000000,
    # Kia
    "Kia|K5": 2300000, "Kia|Sportage": 2700000, "Kia|Sorento": 3400000,
    "Kia|Rio": 1550000, "Kia|Picanto": 1150000, "Kia|K8": 2800000,
    "Kia|Carnival": 3400000, "Kia|Seltos": 2100000,
    # BMW
    "BMW|3 series": 3900000, "BMW|X3": 4500000, "BMW|X1": 3800000,
    "BMW|5 series": 4500000, "BMW|X5": 6500000,
    # Mercedes
    "Mercedes|C-class": 4100000, "Mercedes|E-class": 4500000,
    "Mercedes|GLE": 6500000, "Mercedes|GLC": 4800000,
    # Audi
    "Audi|Q5": 4200000, "Audi|A4": 3500000, "Audi|A6": 4200000, "Audi|Q7": 6800000,
    # VW
    "Volkswagen|Tiguan": 2700000, "Volkswagen|Passat": 2200000,
    "Volkswagen|Polo": 1550000, "Volkswagen|Golf": 2558000, "Volkswagen|Touareg": 5500000,
    # Skoda
    "Skoda|Octavia": 2200000, "Skoda|Superb": 2400000,
    "Skoda|Fabia": 1500000, "Skoda|Kodiaq": 2800000,
    # Chery
    "Chery|Tiggo 2": 1300000, "Chery|Tiggo 4": 1700000, "Chery|Tiggo 7 Pro": 2200000,
    "Chery|Tiggo 8 Pro": 2400000, "Chery|Arrizo 8": 2200000, "Chery|Tiggo 8": 2100000,
    # Haval
    "Haval|Jolion": 1900000, "Haval|F7": 2100000, "Haval|Dargo": 2400000,
    "Haval|H9": 3200000, "Haval|H6": 2200000,
    # Geely
    "Geely|Coolray": 2100000, "Geely|Monjaro": 3500000, "Geely|Tugella": 2800000,
    "Geely|Atlas": 2000000, "Geely|Emgrand": 1500000,
    # Exeed
    "Exeed|TXL": 3300000, "Exeed|LX": 2700000, "Exeed|VX": 3500000, "Exeed|RX": 3200000,
    # Changan
    "Changan|UNI-K": 2700000, "Changan|UNI-T": 1900000,
    "Changan|CS35 Plus": 1600000, "Changan|CS55 Plus": 2000000,
    # Genesis
    "Genesis|GV70": 4100000, "Genesis|G80": 4200000, "Genesis|GV80": 4800000,
    # Lexus
    "Lexus|RX": 4500000, "Lexus|NX": 4200000, "Lexus|ES": 3800000,
    "Lexus|GX": 5800000, "Lexus|LX": 10000000,
    # Subaru
    "Subaru|Forester": 2400000, "Subaru|Outback": 2800000, "Subaru|XV": 2200000,
    # Suzuki
    "Suzuki|Swift": 1450000, "Suzuki|Alto": 900000,
    "Suzuki|Vitara": 2000000, "Suzuki|Jimny": 2300000,
    # Daihatsu
    "Daihatsu|Mira": 850000, "Daihatsu|Tanto": 1000000, "Daihatsu|Move": 950000,
    # Land Rover
    "Land Rover|Range Rover": 8000000, "Land Rover|Discovery": 6000000,
    "Land Rover|Defender": 7500000,
    # Volvo
    "Volvo|XC60": 3800000, "Volvo|XC90": 5500000, "Volvo|S60": 3400000,
    # Jetour
    "Jetour|X70": 2000000, "Jetour|X90": 2400000, "Jetour|Dashing": 2100000,
    # Omoda
    "Omoda|C5": 2000000, "Omoda|S5": 1900000,
    # Infiniti
    "Infiniti|QX50": 4000000, "Infiniti|QX60": 5000000, "Infiniti|QX80": 8500000,
    # Renault
    "Renault|Arkana": 2200000, "Renault|Duster": 1900000, "Renault|Kaptur": 2000000,
    # Mitsubishi
    "Mitsubishi|Outlander": 2400000, "Mitsubishi|Pajero": 3200000,
    "Mitsubishi|ASX": 1900000, "Mitsubishi|L200": 3000000,
    # Jeep
    "Jeep|Grand Cherokee": 5500000, "Jeep|Wrangler": 6000000,
    # ⚡ Электромобили
    "Nissan|Leaf": 868000, "Zeekr|001": 5780000, "Tesla|Model 3": 3180000,
    "Tesla|Model Y": 4600000, "Hongqi|E-HS9": 4950000, "Avatr|11": 7450000,
    "Avatr|12": 7680000, "Geely|EX5": 4430000, "Evolute|i-Joy": 3070000,
    # 🔌 Гибриды
    "Voyah|Free": 6210000, "Li Auto|L7": 5780000, "Li Auto|L9": 6400000,
    "Li Auto|L6": 4800000, "Zeekr|9X": 12300000, "Lynk & Co|900": 8300000,
    "Geely|EX5 EM-i": 3950000,
}


# ─────────────────────────────────────────────────────────────
# РАСХОДЫ НА ОФОРМЛЕНИЕ И ЛОГИСТИКУ
# ─────────────────────────────────────────────────────────────
EXPENSES = {
    "СБКТС": 25000,
    "ЭПТС": 5000,
    "ГЛОНАСС": 15000,
    "Логистика Япония": 100000,
    "Логистика Корея": 100000,
    "Логистика Китай": 120000,
    "Логистика Европа": 200000,
    "Брокер": 35000,
}


# ─────────────────────────────────────────────────────────────
# ОФИЦИАЛЬНЫЕ ТАБЛИЦЫ (ПП РФ № 1637, № 1713)
# ─────────────────────────────────────────────────────────────

CUSTOMS_FEE_TIERS = [
    (200_000, 1_231),
    (450_000, 2_462),
    (1_200_000, 4_924),
    (2_700_000, 13_541),
    (4_200_000, 18_465),
    (5_500_000, 21_344),
    (10_000_000, 49_240),
    (float('inf'), 73_860),
]

DUTY_NEW = [
    (325_000, 0.54, 2.5),
    (650_000, 0.48, 3.5),
    (1_625_000, 0.48, 5.5),
    (3_250_000, 0.48, 7.5),
    (6_500_000, 0.48, 15.0),
    (float('inf'), 0.48, 20.0),
]

DUTY_3_5 = [
    (1_000, 1.5), (1_500, 1.7), (1_800, 2.5),
    (2_300, 2.7), (3_000, 3.0), (float('inf'), 3.6),
]

DUTY_5_PLUS = [
    (1_000, 3.0), (1_500, 3.2), (1_800, 3.5),
    (2_300, 4.8), (3_000, 5.0), (float('inf'), 5.7),
]

# Коэффициенты для ДВС
UTIL_COEF_ICE_NEW = [
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_ICE_OLD = [
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]

# Коэффициенты для электромобилей (льгота до 80 л.с.)
UTIL_COEF_EV_NEW = [
    (80, 0.17),
    (9999, 15.73),
]
UTIL_COEF_EV_OLD = [
    (80, 0.26),
    (9999, 15.73),
]

# Коэффициенты для гибридов (порог 160 л.с.)
UTIL_COEF_HEV_NEW = [
    (160, 0.17), (190, 92.40), (220, 109.68),
    (250, 129.96), (280, 153.96), (9999, 182.40),
]
UTIL_COEF_HEV_OLD = [
    (160, 0.26), (190, 129.72), (220, 151.20),
    (250, 176.16), (280, 205.20), (9999, 239.04),
]

UTIL_BASE_RATE = 20000


# ─────────────────────────────────────────────────────────────
# ФУНКЦИИ ДОСТУПА К БАЗЕ
# ─────────────────────────────────────────────────────────────

def load_cars() -> list:
    return CARS


def get_rf_price(make: str, model: str) -> int | None:
    return RF_PRICES.get(f"{make}|{model}")


# ─────────────────────────────────────────────────────────────
# РАСЧЁТНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────────────────────

def calculate_customs_fee(price_rub: int) -> int:
    for limit, fee in CUSTOMS_FEE_TIERS:
        if price_rub <= limit:
            return fee
    return CUSTOMS_FEE_TIERS[-1][1]


def calculate_duty(price_rub: int, volume_cc: int, age_years: int, eur_rub: float) -> float:
    # Для электромобилей пошлина считается по стоимости (нет объёма)
    if volume_cc == 0:
        # Для электро — 15% от стоимости
        return price_rub * 0.15

    if age_years < 3:
        for limit, percent, min_eur in DUTY_NEW:
            if price_rub <= limit:
                return max(price_rub * percent, min_eur * volume_cc * eur_rub)
        return price_rub * 0.48

    if age_years <= 5:
        for limit, rate in DUTY_3_5:
            if volume_cc <= limit:
                return rate * volume_cc * eur_rub
        return DUTY_3_5[-1][1] * volume_cc * eur_rub

    for limit, rate in DUTY_5_PLUS:
        if volume_cc <= limit:
            return rate * volume_cc * eur_rub
    return DUTY_5_PLUS[-1][1] * volume_cc * eur_rub


def calculate_util(engine_power_hp: int, age_years: int, engine_type: str = "ICE") -> float:
    """Утильсбор для физлица с учётом типа двигателя."""
    if engine_type == "EV":
        table = UTIL_COEF_EV_NEW if age_years < 3 else UTIL_COEF_EV_OLD
    elif engine_type == "HEV":
        table = UTIL_COEF_HEV_NEW if age_years < 3 else UTIL_COEF_HEV_OLD
    else:
        table = UTIL_COEF_ICE_NEW if age_years < 3 else UTIL_COEF_ICE_OLD

    for max_power, coef in table:
        if engine_power_hp <= max_power:
            return UTIL_BASE_RATE * coef
    return UTIL_BASE_RATE * table[-1][1]


def calculate_total_expenses(country: str) -> int:
    logistics_key = f"Логистика {country}"
    logistics = EXPENSES.get(logistics_key, 120_000)
    return (
        EXPENSES["СБКТС"]
        + EXPENSES["ЭПТС"]
        + EXPENSES["ГЛОНАСС"]
        + logistics
        + EXPENSES["Брокер"]
    )


# ─────────────────────────────────────────────────────────────
# ГЛАВНАЯ ФУНКЦИЯ ПОДБОРА
# ─────────────────────────────────────────────────────────────

async def select_cars(budget: int, body_type: str, country: str) -> list:
    cars = load_cars()
    current_year = datetime.now().year
    results = []

    eur_rub = await get_eur_rate()
    logger.info(f"Курс EUR для расчёта: {eur_rub:.2f} ₽")

    for car in cars:
        if body_type != "Любой" and car["body_type"] != body_type:
            continue
        if country != "Любая" and car["country"] != country:
            continue

        age_years = current_year - car["year_from"]
        engine_type = car.get("engine_type", "ICE")
        volume_cc = car.get("engine_volume_cc", 0)

        util = calculate_util(car["engine_power_hp"], age_years, engine_type)
        duty = calculate_duty(
            car["price_foreign_rub"],
            volume_cc,
            age_years,
            eur_rub,
        )
        customs_fee = calculate_customs_fee(car["price_foreign_rub"])
        expenses = calculate_total_expenses(car["country"])

        total = car["price_foreign_rub"] + duty + util + customs_fee + expenses

        rf_price = get_rf_price(car["make"], car["model"])
        if rf_price is not None:
            difference = rf_price - total
            is_profitable = difference > 0
        else:
            difference = None
            is_profitable = None

        if total <= budget * 1.5:
            results.append({
                "car": car,
                "total": total,
                "util": util,
                "duty": duty,
                "customs_fee": customs_fee,
                "expenses": expenses,
                "age_years": age_years,
                "eur_rub": eur_rub,
                "rf_price": rf_price,
                "difference": difference,
                "is_profitable": is_profitable,
                "over_budget": total > budget,
                "over_amount": max(0, total - budget),
            })

    def sort_key(x):
        bucket = 1 if x["over_budget"] else 0
        if x["difference"] is None:
            return (bucket, 2, x["total"])
        if x["difference"] > 0:
            return (bucket, 0, -x["difference"])
        return (bucket, 1, x["total"])

    results.sort(key=sort_key)
    return results[:7]
