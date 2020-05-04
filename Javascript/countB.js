function countBs(strings) {
    if (typeof strings === 'string') {
        var count = 0
        for (let i = 0; i < strings.len; i++) {
            if (strings[i] === "B") {
                count++;
            }
        }
        return count;
    }
}

function countAny(strings, alpha) {
    if (typeof strings === 'string' && typeof alpha === 'string') {
        var count = 0
        for (let i = 0; i < strings.len; i++) {
            if (strings[i] === alpha) {
                count++;
            }
        }
        return count;
    }
}

