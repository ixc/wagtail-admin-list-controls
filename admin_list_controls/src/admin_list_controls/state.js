import { createStore } from 'redux';
import immer from "immer";
import _ from 'lodash';
import * as c from './constants';
import {submit_form} from "./index";

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
            case c.TOGGLE_PANEL:
                if (!(action.ref in state.collapsed_panels_by_ref)) {
                    const control = state.controls_by_ref[action.ref];
                    state.collapsed_panels_by_ref[action.ref] = !control.collapsed;
                } else {
                    state.collapsed_panels_by_ref[action.ref] = !state.collapsed_panels_by_ref[action.ref];
                }
                return;
            case c.SET_VALUE:
                state.values[action.name] = [action.value];
                return;
            case c.REMOVE_VALUE:
                if (action.name in state.values) {
                    state.values[action.name] = _.pull(state.values[action.name], action.value);
                }
                return;
            case c.SUBMIT_FORM:
                submit_form();
                return;
            default:
                break;
        }
    });
}

function get_initial_state() {
    if (!window.admin_list_controls_initial_state) {
        throw new Error('Global `admin_list_controls_initial_state` has not been defined');
    }
    const initial_state = window.admin_list_controls_initial_state;
    const controls = initial_state.admin_list_controls;

    const controls_by_ref = Object.create(null);
    const values = Object.create(null);
    const collapsed_panels_by_ref = Object.create(null);

    traverse_controls(controls, control => {
        if (control.ref) {
            controls_by_ref[control.ref] = control;
        }
    });

    return _.assign(initial_state, {
        controls_by_ref,
        collapsed_panels_by_ref,
        values,
    });
}

function traverse_controls(control, cb) {
    cb(control);
    if (control.children) {
        control.children.forEach(control => traverse_controls(control, cb));
    }
}

