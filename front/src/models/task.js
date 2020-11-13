class Task {
    constructor({
        serviceName: name,
        serviceId: id,
        maxStores: stores,
        firstBloods: firstBloods,
    }) {
        this.name = name;
        this.id = id;
        this.stores = stores;
        this.firstBloods = {};
        firstBloods.forEach(incoming_fb => {
            this.firstBloods[incoming_fb.storeIndex + 1] = incoming_fb;
        });
    }

    static comp(A, B) {
        return A.id - B.id;
    }
}

export default Task;
