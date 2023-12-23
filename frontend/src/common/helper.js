import {Duration} from 'luxon'

export function groupBy(elements, keyFn) {
    const result = {}
    for (const el of elements) {
        const key = keyFn(el)
        result[key] = (result[key] || []).concat([el])
    }
    return result
}

export function parseTimedelta(td) {
    if (td == null) {
        return null
    }
    var [h, m, s] = td.split(':').map((el) => parseFloat(el));
    const d = Duration.fromObject({ hours: h, minutes: m, seconds: s });
    const result = d.normalize().rescale();
    console.log(td, result)
    return result
}

export function formatDatetimeMinutes(dt) {
    const s_date = dt.toISODate();
    const s_time = dt.diff(dt.startOf('day')).toFormat('hh:mm');
    return `${s_date} ${s_time}`
}