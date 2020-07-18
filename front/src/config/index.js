let url = '';

if (process.env.NODE_ENV === 'development') {
    url = 'http://127.0.0.1:8080';
} else {
    url = window.location.origin;
}

const serverUrl = url;

const statuses = [101, 102, 103, 104, 110, 111];

const statusesNames = {
    101: 'UP',
    102: 'RECOVERING',
    103: 'MUMBLE',
    104: 'DOWN',
    110: 'CHECK FAILED',
    111: 'INACTIVE',
    '-1': 'OFFLINE',
};

export { serverUrl, statusesNames, statuses };
