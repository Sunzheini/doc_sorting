# -*- coding: utf-8 -*-


default_status_text = (
        'Правилно име на фолдър:\n' +
        '`20230928 - MC077-021-001-Leak proof joint design and drawing for hull`\n' +
        'или:\n'
        '`20230928 - MC077-021-001-Leak proof joint design and drawing for hull - 1`\n' +
        '\n' +
        'Правилно име на файл:\n' +
        '`MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg`\n' +
        'или:\n' +
        '`MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf`\n' +
        '\n' +
        'Към момента фолдърите в `020 CLASSIFICATION DRAWINGS` са с имена от този тип: `MC077-021-001!`\n' +
        '\n' +
        'Правилен формат на Excel-ския файл: .xlsx\n' +
        '\n' +
        'Програмата сканира Ready и при наличие на 2 с еднакви номер и име избира този с по-нова дата. '
        'При еднакви дати, избира с по-голяма ревизия.\n' +
        '\n' +
        'След това програмата сканира `020 CLASSIFICATION DRAWINGS` и сравнява резултата с предходното сканиране. '
        '\n' +
        'Събира цялата информация от Excel-ския файл и създава папките от тип `C ESD SYSTEM DESIGN` '
        'в `020 CLASSIFICATION DRAWINGS`' +
        '\n' +
        'Ключова стъпка: Сравнява Ready с `020 CLASSIFICATION DRAWINGS` и набелязва списък с разликите. '
        '\n' +
        'След това сравнява разликите с Excel-ския файл. Ако номер + име съвпадат не съвпадат ги премахва'
        ' от списъка с разликите. Сканира .pdf файловете отново за сравнение с Excel-ския файл (само информативно без да ги маха от списъка'
        'с разликите). '
        '\n' +
        'След това програмата премества файловете от Ready в Finished и архивира Finished.'
        '\n' +
        'Програмата чете от първия Sheet на Excel-ския файл!'
)
