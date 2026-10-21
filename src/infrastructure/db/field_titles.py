"""Словарь title'ов из XML/форм. Используется для сопоставления field_dictionary."""

CHARGE_ENTRY_TITLES: dict[str, str] = {
    "ctn": "Номер телефона",
    "ban": "Договор",
    "ben": "Группа счетов",
    "offer_description": "Тарифный план",
    "usag_intl_actv_amt": "Международные звонки",
    "usag_national_actv_amt": "Междугородние звонки",
    "usag_air_actv_amt": "Местные звонки",
    "usag_sms_actv_amt": "SMS/MMS",
    "usag_gprs_actv_amt": "GPRS",
    "irom_local_actv_amt": "Международный роуминг Эфирное время (начисления партнера)",
    "irom_sms_actv_amt": "Международный роуминг SMS (начисления партнера)",
    "irom_gprs_actv_amt": "Международный роуминг GPRS (начисления партнера)",
    "irom_server_actv_amt": "Начисления за международный роуминг",
    "nrom_local_actv_amt": "В поездках по России Эфирное время",
    "nrom_sms_actv_amt": "В поездках по России SMS",
    "nrom_gprs_actv_amt": "В поездках по России Мобильный интернет",
    "nrom_server_actv_amt": "Начисления за трафик в поездках по России",
    "rc_pp_actv_amt": "Абонентская плата по тарифному плану",
    "rc_soc_actv_amt": "Абонентская плата за доп. услуги",
    "disc_actv_amt": "Скидки",
    "oc_ot_price": "Разовые начисления (Операции)",
    "latepym": "Пени",
    "subtotal_amount": "Итого по строке",
    "trs_lo_rc_uc_amt": "Перенесенные начисления по абон. плате и звонкам",
    "trs_lo_oc_amt": "Перенесенные значения за операции",
    "vat": "НДС",
    "total_amount": "Всего по строке",
}

CHARGES_SUMMARY_TITLES: dict[str, str] = {
    "ben": "Группа счетов",
    **{k: v for k, v in CHARGE_ENTRY_TITLES.items()
       if k in {
           "usag_intl_actv_amt", "usag_national_actv_amt", "usag_air_actv_amt",
           "usag_sms_actv_amt", "usag_gprs_actv_amt",
           "irom_local_actv_amt", "irom_sms_actv_amt",
           "irom_gprs_actv_amt", "irom_server_actv_amt",
           "nrom_local_actv_amt", "nrom_sms_actv_amt",
           "nrom_gprs_actv_amt", "nrom_server_actv_amt",
           "rc_pp_actv_amt", "rc_soc_actv_amt", "disc_actv_amt",
           "oc_ot_price", "latepym", "subtotal_amount",
           "trs_lo_rc_uc_amt", "trs_lo_oc_amt", "vat", "total_amount",
       }},
}

CHARGES_REPORT_TITLES: dict[str, str] = {
    "ban": "Договор",
    "period_start": "Дата начала периода",
    "period_end": "Дата окончания периода",
    "source_type": "Тип источника",
    "source_file": "Имя файла",
    "created_at": "Дата создания записи",
}

TITLE_DICTIONARY: dict[str, dict[str, str]] = {
    "charge_entry": CHARGE_ENTRY_TITLES,
    "charges_summary": CHARGES_SUMMARY_TITLES,
    "charges_report": CHARGES_REPORT_TITLES,
}
