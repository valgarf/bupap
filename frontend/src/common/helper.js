export function groupBy(elements, keyFn) {
    const result = {}
    for (const el of elements) {
        const key = keyFn(el)
        result[key] = (result[key] || []).concat([el])
    }
    return result
}
