// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function listToTree(data: any, idKey = 'dbId', parentIdKey = ['parent', 'dbId'], parentKey = 'parent', childrenKey = 'children') {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const data_by_id: {[k:string]: any} = {}
    for (const el of data) {
        data_by_id[el[idKey]] = el
        el[childrenKey] = []
    }
    const result = [];
    for (const el of data) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        let parentId: any = el
        for (const key of parentIdKey) {
            if (parentId == null) {
                break
            }
            parentId = parentId[key]
        }

        const parent = parentId == null? null :data_by_id[parentId]
        if (parent == null) {
            result.push(el)
        }
        else {
            parent[childrenKey].push(el)
            el[parentKey] = parent
        }
    }
    return result
}