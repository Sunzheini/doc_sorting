# -*- coding: utf-8 -*-


default_status_text = (
        'I. Правилно име на фолдър в Ready:\n' +
        '`20230928 - MC077-021-001-Leak proof joint design and drawing for hull`\n' +
        'или:\n'
        '`20230928 - MC077-021-001-Leak proof joint design and drawing for hull - 1`\n' +
        '\n' +
        'II. Правилно име на фолдър във Finished:\n' +
        '`MC077-021-001-Leak proof joint design and drawing for hull`\n' +
        '\n' +
        'III. Правилно име на файл:\n' +
        '`MC077-022-001_30092023.dwg`\n' +
        '\n' +
        'IV. Правилен формат на Excel-ския файл: .xlsx\n' +
        '\n' +
        'V. Принцип на работа:\n' +
        'а. Програмата сканира Ready и при наличие на такива с еднакви номер и име избира този с по-нова дата. '
        'При еднакви дати, избира този с по-голяма ревизия.' +
        '\n' +
        'б. След това програмата сканира `020 CLASSIFICATION DRAWINGS` и сравнява резултата с предходното сканиране. '
        '\n' +
        'в. Събира цялата информация от Excel-ския файл (Първият Sheet на Excel-ския файл!) и създава папките от тип '
        '`C ESD SYSTEM DESIGN` в `020 CLASSIFICATION DRAWINGS`' +
        '\n' +
        'г. Ключова стъпка: Сравнява Ready с `020 CLASSIFICATION DRAWINGS` и набелязва списък с разликите. '
        '\n' +
        'д. След това сравнява разликите с Excel-ския файл. Ако номер + име не съвпадат ги премахва'
        ' от списъка с разликите. Сканира .pdf файловете отново за сравнение с Excel-ския файл (само информативно без да ги маха от списъка'
        'с разликите). '
        '\n' +
        'е. След това програмата премества файловете от Ready във Finished и архивира съответния фолдър във Finished.'
)