import { createStore } from 'redux';
import immer from "immer";

export const initial_state = get_initial_state();
export const store = createStore(
    reducer,
    initial_state,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__({
        name: 'admin_list_controls',
    }),
);

function reducer(current_state=initial_state, action) {
    return immer(current_state, state => {
        switch (action.type) {
            default:
                break;
        }
    });
}

function get_initial_state() {
    if (!window.admin_list_controls_initial_state) {
        throw new Error('Global `admin_list_controls_initial_state` has not been defined');
    }

    return window.admin_list_controls_initial_state;
}

