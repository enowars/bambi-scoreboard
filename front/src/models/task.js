class Task {
    constructor({ ServiceName: name, ServiceId: id, MaxStores: stores, FirstBloods: firstBloods }) {
        this.name = name;
        this.id = id;
        this.stores = stores;
        this.firstBloods = firstBloods;
    }

    static comp(A, B) {
        return A.id - B.id;
    }
}

export default Task;
