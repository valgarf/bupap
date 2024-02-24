import {Duration} from 'luxon'
import { ref, watchEffect } from 'vue'
import { colors } from 'quasar'

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
    return result
}

export function formatDatetimeMinutes(dt) {
    const s_date = dt.toISODate();
    const s_time = dt.diff(dt.startOf('day')).toFormat('hh:mm');
    return `${s_date} ${s_time}`
}

export function formatDatetimeDate(dt) {
    return dt.toISODate();
}

export function histogram(data) {
    // roughly https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule
    data.sort();
    const n = data.length;
    const iqr = data[Math.round(3 * n / 4)] - data[Math.round(n / 4)];
    var w = 1.5 * iqr / Math.pow(n, 1 / 3)
    w = parseFloat(w.toPrecision(2));
    var median = data[Math.round(n / 2)];
    median = parseFloat(median.toPrecision(2));
    
    var start = median - w / 2 - Math.ceil((median - w / 2 - data[0]) / w) * w
    
    const binsStart = [start]
    const binsCenter = [start +w/2]
    const binsEnd = [start + w]
    const binsFormatted = [`${start.toPrecision(3)} - ${(start+w).toPrecision(3)}`]
    const counts = []
    var count = 0
    function next_bin(final = false) {
        counts.push(count)
        start = start + w
        count = 0
        if (!final) {
            binsStart.push(start)
            binsCenter.push(start + w / 2)
            binsEnd.push(start + w)
            binsFormatted.push(`${start.toPrecision(3)} - ${(start+w).toPrecision(3)}`)
        }
    }
    for (const v of data) {
        if (v > start + w) {
            next_bin()
        } 
        count += 1
    }
    next_bin(true)
    return {binsStart, binsCenter, binsEnd, binsFormatted, counts}
}

export function lastNonNull(reference) {
    // var _lastValue = null
    // return computed(() => {
    //     if (reference.value != null) {
    //         _lastValue = reference.value;
    //         console.log(reference.value)
    //         return reference.value;
    //     }
    //     return _lastValue;
    // });
    const result = ref(null)
    watchEffect(() => {
        if (reference.value != null) {
            result.value = reference.value
        }
    })
    return result
}

export function textColorFromBackground(col) {
    return colors.luminosity(col) <= 0.4 ? 'white' : 'black'
}

export function qPageHeightForTabs(offset) {
    offset += 48 // height of tabs
    return offset ? `calc(100vh - ${offset}px)` : '100vh'
}
    
export function qPageStyleFnForTabs(offset) {
    return { minHeight: qPageHeightForTabs(offset) }
}

export function qPageStyleFnForTabsFixed(offset) {
    return {
        minHeight: qPageHeightForTabs(offset),
        height: qPageHeightForTabs(offset) + ' !important'
    }
}