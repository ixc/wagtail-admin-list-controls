import {createStore} from 'redux';
import immer from "immer";
import _ from 'lodash';
import * as constants from './constants';
import {clear_search_input, submit_form} from "./index";

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
            case constants.TOGGLE_PANEL:
                if (!(action.ref in state.collapsed_panels_by_ref)) {
                    const control = state.controls_by_ref[action.ref];
                    state.collapsed_panels_by_ref[action.ref] = !control.collapsed;
                } else {
                    state.collapsed_panels_by_ref[action.ref] = !state.collapsed_panels_by_ref[action.ref];
                }
                return;
            case constants.COLLAPSE_PANEL:
                state.collapsed_panels_by_ref[action.ref] = true;
                return;
            case constants.SET_VALUE:
                if (_.isArray(action.value)) {
                    state.values[action.name] = action.value;
                } else {
                    state.values[action.name] = [action.value];
                }
                return;
            case constants.REMOVE_VALUE:
                if (action.name in state.values) {
                    state.values[action.name] = _.pull(state.values[action.name], action.value);
                }
                return;
            case constants.REMOVE_ALL_VALUES:
                state.values = Object.create(null);
                clear_search_input();
                return;
            case constants.SUBMIT_FORM:
                submit_form();
                return;
            case constants.CLEAR_SEARCH_INPUT:
                clear_search_input();
                return;
            case constants.LINK:
                window.location = action.url;
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
        if (control.name) {
            if (!(control.name in values)) {
                values[control.name] = [];
            }
            if (_.isArray(control.value)) {
                control.value.forEach(value => {
                    if (value) {
                        values[control.name].push(value);
                    }
                })
            } else if ('is_selected' in control) {
                if (control.is_selected && !control.is_default) {
                    values[control.name].push(control.value);
                }
            } else if (control.value) {
                values[control.name].push(control.value);
            }
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

